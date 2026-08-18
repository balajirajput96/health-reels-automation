#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/ubuntu/reels_ops"
AUDIO="$ROOT/audio"
RENDERS="$ROOT/renders"
FINAL="$ROOT/final"
WORK="$ROOT/work/batch03_morning_light"

mkdir -p "$WORK" "$FINAL"

for i in 01 02 03 04 05 06 07; do
  ffmpeg -hide_banner -loglevel error -y \
    -i "$AUDIO/batch03_morning_light_narration_${i}.wav" \
    -af "apad=pad_dur=8" -t 8 -ar 48000 -ac 1 \
    "$WORK/narration_${i}.wav"
done

ffmpeg -hide_banner -loglevel error -y \
  -f lavfi -t 4 -i anullsrc=r=48000:cl=mono \
  "$WORK/narration_08.wav"

cat > "$WORK/video_concat.txt" <<EOF
file '$RENDERS/batch03_morning_light_segment01.mp4'
file '$RENDERS/batch03_morning_light_segment02.mp4'
file '$RENDERS/batch03_morning_light_segment03.mp4'
file '$RENDERS/batch03_morning_light_segment04.mp4'
file '$RENDERS/batch03_morning_light_segment05.mp4'
file '$RENDERS/batch03_morning_light_segment06.mp4'
file '$RENDERS/batch03_morning_light_segment07.mp4'
file '$RENDERS/batch03_morning_light_segment08_close.mp4'
EOF

cat > "$WORK/audio_concat.txt" <<EOF
file '$WORK/narration_01.wav'
file '$WORK/narration_02.wav'
file '$WORK/narration_03.wav'
file '$WORK/narration_04.wav'
file '$WORK/narration_05.wav'
file '$WORK/narration_06.wav'
file '$WORK/narration_07.wav'
file '$WORK/narration_08.wav'
EOF

ffmpeg -hide_banner -loglevel error -y \
  -f concat -safe 0 -i "$WORK/video_concat.txt" \
  -c:v libx264 -preset medium -crf 19 -r 24 -pix_fmt yuv420p \
  "$WORK/video_only.mp4"

ffmpeg -hide_banner -loglevel error -y \
  -f concat -safe 0 -i "$WORK/audio_concat.txt" \
  -c:a pcm_s16le -ar 48000 -ac 1 \
  "$WORK/batch03_morning_light_full_narration.wav"

ffmpeg -hide_banner -loglevel error -y \
  -i "$WORK/video_only.mp4" -i "$WORK/batch03_morning_light_full_narration.wav" \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 160k -shortest \
  -movflags +faststart \
  "$FINAL/2026-08-17__batch03__morning-light__draft.mp4"

ffmpeg -hide_banner -loglevel error -y \
  -ss 1 -i "$FINAL/2026-08-17__batch03__morning-light__draft.mp4" \
  -frames:v 1 -q:v 2 \
  "$FINAL/2026-08-17__batch03__morning-light__cover.jpg"

cp "$WORK/batch03_morning_light_full_narration.wav" \
  "$AUDIO/batch03_morning_light_full_narration.wav"

echo "Batch 03 assembly complete."
