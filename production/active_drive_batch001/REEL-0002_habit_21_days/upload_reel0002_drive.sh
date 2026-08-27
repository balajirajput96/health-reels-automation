#!/usr/bin/env bash
set -euo pipefail

FOLDER_ID="12EwnZQ9RN6BUYmefbzHAmDhQ77F-Fduo"
ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="$ROOT/drive_upload_results"
mkdir -p "$OUT"

upload() {
  local name="$1"
  local path="$2"
  local mime="$3"
  local key="$4"
  local existing
  existing="$(gws drive files list --params "{\"q\":\"'$FOLDER_ID' in parents and name = '$name' and trashed = false\",\"pageSize\":20,\"fields\":\"files(id,name,mimeType,size,md5Checksum,modifiedTime,parents)\"}" --format json)"
  if printf '%s' "$existing" | grep -q '"files": \[\]'; then
    gws drive files create \
      --json "{\"name\":\"$name\",\"parents\":[\"$FOLDER_ID\"]}" \
      --upload "$path" \
      --upload-content-type "$mime" \
      --format json > "$OUT/$key.json"
    printf 'uploaded %s\n' "$name"
  else
    printf '%s' "$existing" > "$OUT/$key.json"
    printf 'reused_existing %s\n' "$name"
  fi
}

upload "REEL-0002_habit_21_days_QC_pending.mp4" "$ROOT/rendered/REEL-0002_habit_21_days_QC_pending.mp4" "video/mp4" "video"
upload "REEL-0002_narration_hi-IN.wav" "$ROOT/narration_hi-IN.wav" "audio/wav" "narration"
upload "REEL-0002_captions_hi-IN.srt" "$ROOT/work/captions_hi-IN.srt" "application/x-subrip" "captions_srt"
upload "REEL-0002_captions_hi-IN.ass" "$ROOT/work/captions_hi-IN.ass" "text/plain" "captions_ass"
upload "REEL-0002_local_manifest.json" "$ROOT/rendered/REEL-0002_local_manifest.json" "application/json" "manifest"
upload "REEL-0002_script_hi-IN.md" "$ROOT/script_hi-IN.md" "text/markdown" "script"
upload "REEL-0002_production_brief.md" "$ROOT/production_brief.md" "text/markdown" "brief"
upload "REEL-0002_source_validation.md" "$ROOT/source_validation.md" "text/markdown" "sources"
upload "REEL-0002_ffprobe.json" "$ROOT/rendered/ffprobe.json" "application/json" "ffprobe"

for image in "$ROOT"/assets/*.png; do
  base="$(basename "$image")"
  upload "REEL-0002_$base" "$image" "image/png" "asset_${base%.png}"
done

printf 'upload_complete\n'
