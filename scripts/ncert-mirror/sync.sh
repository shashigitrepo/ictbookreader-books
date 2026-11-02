#!/usr/bin/env bash
# Keeps a copy of every NCERT PDF the app links to in this repository's GitHub Releases, so the
# app can download a chapter from here when ncert.nic.in fails (bad certificate, site down…).
#
#   sync.sh fill   upload files that are not in the mirror yet (at most $MAX_UPLOADS per run)
#   sync.sh check  also re-download files whose size on NCERT changed (weekly)
#
# Files go to release "ncert-<first letter>" (e.g. fepr101.pdf -> ncert-f), at most ~730 per
# release (GitHub allows 1000). The app builds the same URL:
#   https://github.com/<repo>/releases/download/ncert-f/fepr101.pdf
# Every run first checks that ncert.nic.in works the way the app reaches it (system certificates +
# Let's Encrypt Gen Y, le-gen-y.pem); if it doesn't, the run fails and GitHub emails the owner.
set -uo pipefail
MODE=${1:-fill}
DIR=$(cd "$(dirname "$0")" && pwd)
WORK=${RUNNER_TEMP:-/tmp}/ncert-mirror
MAX_UPLOADS=${MAX_UPLOADS:-300}
mkdir -p "$WORK"
CA="$WORK/ca.pem"
cat "${SYSTEM_CA:-/etc/ssl/certs/ca-certificates.crt}" "$DIR/le-gen-y.pem" > "$CA"
CURL=(curl -sS --cacert "$CA" -A "Padhaku-mirror" --retry 3 --retry-delay 5)

# 1. Health check. GitHub's servers (USA) usually cannot connect to ncert.nic.in, so files are fetched
# through the "ncertFile" Firebase function in Mumbai (NCERT_RELAY + NCERT_RELAY_TOKEN). The relay
# checks NCERT's certificate like the app does, so a failure here means phones are likely affected.
RELAY=${NCERT_RELAY:-}
RELAY_TOKEN=${NCERT_RELAY_TOKEN:-}
probe=https://ncert.nic.in/textbook/pdf/fepr101.pdf
VIA=direct
if code=$("${CURL[@]}" -o /dev/null -w '%{http_code}' -I -m 30 "$probe" 2>/dev/null) && [ "$code" = 200 ]; then
  echo "ncert.nic.in health check OK (direct)"
elif [ -n "$RELAY" ] && [ -n "$RELAY_TOKEN" ] &&
     code=$(curl -sS -o /dev/null -w '%{http_code}' -m 90 --retry 4 --retry-delay 5 --retry-all-errors \
       -H "x-mirror-token: $RELAY_TOKEN" -H "Range: bytes=0-99" "$RELAY?f=textbook/pdf/fepr101.pdf") &&
     [ "$code" = 206 ]; then
  VIA=relay
  echo "ncert.nic.in health check OK (through the Mumbai relay; GitHub cannot reach NCERT directly)"
else
  echo "::error::ncert.nic.in health check failed (direct and relay, HTTP ${code:-none}). Phones may not be able to download NCERT books; the app will use this mirror."
  if [ -n "$RELAY" ] && [ -n "$RELAY_TOKEN" ]; then
    # The relay's answer says what went wrong between Mumbai and NCERT (e.g. "NCERT: certificate…").
    reason=$(curl -sS -m 90 -H "x-mirror-token: $RELAY_TOKEN" -H "Range: bytes=0-99" "$RELAY?f=textbook/pdf/fepr101.pdf" 2>&1 | head -c 300 | tr -cd '[:print:] ')
    echo "::error::Relay says: ${reason:-no answer}"
  fi
  [ -n "$RELAY" ] || echo "::error::NCERT_RELAY_TOKEN secret is missing: see scripts/ncert-mirror/README in the app repo notes."
  exit 1
fi

# Size of an NCERT file, or empty if NCERT doesn't have it. Through the relay, a 1-byte Range request
# (Google's front end rejects HEAD answers from the function): "Content-Range: bytes 0-0/<size>".
ncert_size() {
  if [ "$VIA" = direct ]; then
    "${CURL[@]}" -I -m 60 "$1" | tr -d '\r' |
      awk '$1 ~ /^HTTP/ {st=$2} tolower($1)=="content-length:" {v=$2} END {if (st == 200) print v}'
  else
    curl -sS -o /dev/null -D - -m 90 --retry 4 --retry-delay 3 --retry-all-errors -H "x-mirror-token: $RELAY_TOKEN" -H "Range: bytes=0-0" \
      "$RELAY?f=${1#https://ncert.nic.in/}" | tr -d '\r' |
      awk '$1 ~ /^HTTP/ {st=$2} tolower($1)=="content-range:" {n=split($2 $3, a, "/"); v=a[n]} END {if (st == 206) print v}'
  fi
}

# Downloads an NCERT file to $2 ($3 = its size). Through the relay it comes in pieces of $CHUNK bytes.
CHUNK=${MIRROR_CHUNK:-$((20 * 1024 * 1024))}
ncert_get() {
  if [ "$VIA" = direct ]; then
    "${CURL[@]}" -f -m 1200 -o "$2" "$1"
    return
  fi
  : > "$2"
  local start=0 end
  while [ "$start" -lt "$3" ]; do
    end=$((start + CHUNK - 1)); [ "$end" -lt "$3" ] || end=$(($3 - 1))
    curl -sS -f -m 300 --retry 4 --retry-delay 5 --retry-all-errors -H "x-mirror-token: $RELAY_TOKEN" -H "Range: bytes=$start-$end" \
      "$RELAY?f=${1#https://ncert.nic.in/}" >> "$2" || return 1
    start=$((end + 1))
  done
}

# 2. Releases and what they already hold.
have="$WORK/have.txt"; : > "$have"
for letter in $(sed -E 's#.*/##; s#^(.).*#\1#' "$DIR/files.txt" | sort -u); do
  tag="ncert-$letter"
  if ! gh release view "$tag" >/dev/null 2>&1; then
    gh release create "$tag" --title "NCERT books ($letter…)" --latest=false \
      --notes "Copies of NCERT textbook PDFs (© NCERT, https://ncert.nic.in/textbook.php), used by the Padhaku app only when ncert.nic.in cannot be reached. Updated automatically." || exit 1
  fi
  gh release view "$tag" --json assets --jq '.assets[] | "\(.name) \(.size)"' >> "$have" || exit 1
done
echo "Mirror holds $(wc -l < "$have") of $(grep -c . "$DIR/files.txt") files"

# 3. Upload missing (and, in check mode, changed) files.
uploads=0; failed=0; checked=0
while read -r url; do
  [ -n "$url" ] || continue
  name=${url##*/}; tag="ncert-${name:0:1}"
  size=$(awk -v n="$name" '$1==n {print $2}' "$have")
  if [ -n "$size" ] && [ "$MODE" != check ]; then continue; fi
  len=$(ncert_size "$url")
  if [ -z "$len" ]; then echo "::warning::$name: NCERT did not answer"; failed=$((failed + 1)); continue; fi
  if [ -n "$size" ]; then
    checked=$((checked + 1))
    [ "$len" = "$size" ] && continue
    echo "$name changed on NCERT ($size -> $len bytes)"
  fi
  [ "$uploads" -lt "$MAX_UPLOADS" ] || continue
  tmp="$WORK/$name"
  if ! ncert_get "$url" "$tmp" "$len" || [ "$(stat -c %s "$tmp")" != "$len" ]; then
    echo "::warning::$name: download from NCERT failed"; failed=$((failed + 1)); rm -f "$tmp"; continue
  fi
  if [ "$(head -c 4 "$tmp")" != "%PDF" ]; then
    echo "::warning::$name: NCERT did not send a PDF"; failed=$((failed + 1)); rm -f "$tmp"; continue
  fi
  if gh release upload "$tag" "$tmp" --clobber >/dev/null; then
    uploads=$((uploads + 1)); echo "uploaded $name ($(stat -c %s "$tmp") bytes)"
  else
    echo "::warning::$name: upload to GitHub failed"; failed=$((failed + 1))
  fi
  rm -f "$tmp"
  sleep 2   # stay well under GitHub's limits for creating content
done < "$DIR/files.txt"

total=$(grep -c . "$DIR/files.txt")
echo "Uploaded $uploads, checked $checked, failed $failed (of $total files)"
{
  echo "### NCERT mirror ($MODE)"
  echo "- uploaded: $uploads, checked: $checked, failed: $failed, files listed: $total"
} >> "${GITHUB_STEP_SUMMARY:-/dev/null}"
# A few dead links on NCERT are normal; many failures mean NCERT (or GitHub) is having problems.
if [ "$failed" -gt $((total / 20)) ]; then
  echo "::error::$failed files failed: NCERT may be down or blocking downloads."
  exit 1
fi
