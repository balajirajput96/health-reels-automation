#!/usr/bin/env bash
set -euo pipefail
FOLDER_ID="${1:?folder id required}"
ROOT="/home/ubuntu/repos/health-reels-automation"

upload_one(){
  local path="$1" name mime listing
  name="$(basename "$path")"
  case "$name" in
    *.mp4) mime="video/mp4";; *.wav) mime="audio/wav";; *.png) mime="image/png";;
    *.json) mime="application/json";; *.srt) mime="application/x-subrip";;
    *.md) mime="text/markdown";; *) mime="application/octet-stream";;
  esac
  listing="$(gws drive files list --params "{\"q\":\"name = '$name' and '$FOLDER_ID' in parents and trashed = false\",\"spaces\":\"drive\",\"pageSize\":100,\"fields\":\"files(id,name,size,mimeType,parents,modifiedTime)\"}")"
  if printf '%s' "$listing" | grep -Fq "\"name\": \"$name\""; then
    printf 'SKIP existing %s\n' "$name"
    return 0
  fi
  gws drive files create --upload "$path" --json "{\"name\":\"$name\",\"parents\":[\"$FOLDER_ID\"]}" --upload-content-type "$mime"
  printf 'UPLOADED %s\n' "$name"
}

upload_one "$ROOT/assets/reel_0055_uncertainty_what_studies_measure_hi.mp4"
upload_one "$ROOT/assets/reel_0055_uncertainty_what_studies_measure_narration_hi.wav"
upload_one "$ROOT/assets/reel_0055_uncertainty_what_studies_measure_captions_hi.srt"
upload_one "$ROOT/assets/reel_0055_metadata.json"
upload_one "$ROOT/assets/reel_0055_qc_report.json"
upload_one "$ROOT/research/reel_0055_uncertainty_what_studies_measure_sources.md"
upload_one "$ROOT/research/reel_0055_uncertainty_what_studies_measure_script.md"
upload_one "$ROOT/assets/reel_0055_scene_01.png"
upload_one "$ROOT/assets/reel_0055_scene_02.png"
upload_one "$ROOT/assets/reel_0055_scene_03.png"
upload_one "$ROOT/assets/reel_0055_scene_04.png"
