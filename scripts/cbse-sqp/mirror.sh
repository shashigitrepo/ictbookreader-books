#!/usr/bin/env bash
# Copies every PDF listed in cbse-sample-papers.json into the GitHub Release "cbse-sqp-<session>" of this
# repository (the app downloads the copy first, CBSE as fallback). Files already copied are skipped.
# Needs GH_TOKEN (contents: write). Exits non-zero if CBSE can't be reached at all (GitHub then emails).
set -euo pipefail
cd "$(dirname "$0")/../.."
session=$(python3 -c "import json;print(json.load(open('cbse-sample-papers.json'))['session'])")
tag="cbse-sqp-$session"
gh release view "$tag" >/dev/null 2>&1 || gh release create "$tag" --title "CBSE sample papers $session" \
  --notes "Copies of CBSE's sample question papers and marking schemes ($session) for the Padhaku app. Source: cbseacademic.nic.in"
have=$(gh release view "$tag" --json assets -q '.assets[].name' | sort)
bundle=$(mktemp); cat /etc/ssl/certs/ca-certificates.crt scripts/cbse-sqp/emsign-root-g1.pem > "$bundle"
tmp=$(mktemp -d); copied=0; failed=0
python3 -c "
import json
for p in json.load(open('cbse-sample-papers.json'))['papers']:
    for k in ('sqp', 'ms'):
        if p.get(k): print(p[k + 'File'], p[k])
" | while read -r name url; do
  if grep -qxF "$name" <<<"$have"; then continue; fi
  if curl -fsSL --retry 3 --cacert "$bundle" -A "Mozilla/5.0" -o "$tmp/$name" "$url" && head -c 4 "$tmp/$name" | grep -q '%PDF'; then
    gh release upload "$tag" "$tmp/$name" --clobber >/dev/null && copied=$((copied+1)) && echo "copied $name"
  else
    echo "could not copy $name from $url"; failed=$((failed+1))
  fi
  rm -f "$tmp/$name"
done
echo "done"
