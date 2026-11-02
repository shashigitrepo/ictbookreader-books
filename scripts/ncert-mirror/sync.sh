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

# 1. Health check: NCERT reachable with the app's certificate rules?
probe=https://ncert.nic.in/textbook/pdf/fepr101.pdf
if ! code=$("${CURL[@]}" -o /dev/null -w '%{http_code}' -I -m 60 "$probe") || [ "$code" != 200 ]; then
  echo "::error::ncert.nic.in health check failed (HTTP ${code:-none}). The app's direct downloads are probably broken; it will use this mirror."
  "${CURL[@]}" -v -I -m 60 "$probe" 2>&1 | tail -20
  exit 1
fi
echo "ncert.nic.in health check OK"

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
  if [ -n "$size" ]; then
    checked=$((checked + 1))
    len=$("${CURL[@]}" -I -m 60 "$url" | tr -d '\r' | awk 'tolower($1)=="content-length:" {v=$2} END {print v}')
    if [ -z "$len" ]; then echo "::warning::$name: NCERT did not answer"; failed=$((failed + 1)); continue; fi
    [ "$len" = "$size" ] && continue
    echo "$name changed on NCERT ($size -> $len bytes)"
  fi
  [ "$uploads" -lt "$MAX_UPLOADS" ] || continue
  tmp="$WORK/$name"
  if ! "${CURL[@]}" -f -m 1200 -o "$tmp" "$url"; then
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
