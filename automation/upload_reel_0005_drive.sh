#!/usr/bin/env bash
set -euo pipefail

FOLDER_ID="1mXqypA4kHfYpmF5hAgbald15ouaFRJ-f"
ROOT="/home/ubuntu/repos/health-reels-automation"

upload_one() {
  local path="$1"
  local name
  local mime
  name="$(basename "$path")"
  mime="$(file --mime-type -b "$path")"
  local existing
  existing="$(gws drive files list --params "{\"q\":\"name = '${name}' and '${FOLDER_ID}' in parents and trashed = false\",\"fields\":\"files(id,name,size,md5Checksum)\",\"pageSize\":10}" --format json)"
  if grep -Fq "\"name\": \"$name\"" <<<"$existing"; then
    printf 'SKIP existing %s\n' "$name"
    return 0
  fi
  printf 'UPLOAD %s (%s)\n' "$name" "$mime"
  gws drive files create \
    --upload "$path" \
    --json "{\"name\":\"$name\",\"parents\":[\"$FOLDER_ID\"],\"mimeType\":\"$mime\"}" \
    --upload-content-type "$mime" \
    --format json
}

files=(
  "$ROOT/assets/reel_0005_psychological_flexibility_measurement_hi.mp4"
  "$ROOT/assets/reel_0005_psychological_flexibility_measurement_narration_hi.wav"
  "$ROOT/assets/reel_0005_psychological_flexibility_measurement_captions_hi.srt"
  "$ROOT/assets/reel_0005_metadata.json"
  "$ROOT/research/reel_0005_psychological_flexibility_measurement_sources.md"
  "$ROOT/research/reel_0005_psychological_flexibility_measurement_script.md"
  "$ROOT/state/reel_0005_qc_report.json"
  "$ROOT/assets/reel_0005_scene_01.png"
  "$ROOT/assets/reel_0005_scene_02.png"
  "$ROOT/assets/reel_0005_scene_03.png"
  "$ROOT/assets/reel_0005_scene_04.png"
)

for path in "${files[@]}"; do
  [[ -s "$path" ]] || { echo "missing or empty: $path" >&2; exit 2; }
  upload_one "$path"
done
