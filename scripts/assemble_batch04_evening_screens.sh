#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/ubuntu/reels_ops"
RENDER="$ROOT/renders"
AUDIO="$ROOT/audio"
WORK="$ROOT/work/batch04_evening_screens"
FINAL="$ROOT/final"
OUT="$FINAL/2026-08-19__batch04__evening-screens__draft.mp4"
COVER="$FINAL/2026-08-19__batch04__evening-screens__cover.jpg"

mkdir -p "$WORK" "$FINAL"
cat > "$WORK/videos.txt" <<LIST
file '$RENDER/batch04_evening_screens_segment01.mp4'
file '$RENDER/batch04_evening_screens_segment02.mp4'
file '$RENDER/batch04_evening_screens_segment03.mp4'
file '$RENDER/batch04_evening_screens_segment04.mp4'
file '$RENDER/batch04_evening_screens_segment05.mp4'
file '$RENDER/batch04_evening_screens_segment06.mp4'
file '$RENDER/batch04_evening_screens_segment07.mp4'
file '$RENDER/batch04_evening_screens_segment08_close.mp4'
LIST

ffmpeg -hide_banner -loglevel error -y \
  -f concat -safe 0 -i "$WORK/videos.txt" \
  -i "$AUDIO/batch04_evening_screens_narration_01.wav" \
  -i "$AUDIO/batch04_evening_screens_narration_02.wav" \
  -i "$AUDIO/batch04_evening_screens_narration_03.wav" \
  -i "$AUDIO/batch04_evening_screens_narration_04.wav" \
  -i "$AUDIO/batch04_evening_screens_narration_05.wav" \
  -i "$AUDIO/batch04_evening_screens_narration_06.wav" \
  -i "$AUDIO/batch04_evening_screens_narration_07.wav" \
  -filter_complex "[1:a]apad=pad_dur=2.04,atrim=duration=8[a1];[2:a]apad=pad_dur=1.40,atrim=duration=8[a2];[3:a]apad=pad_dur=0.52,atrim=duration=8[a3];[4:a]apad=pad_dur=1.12,atrim=duration=8[a4];[5:a]apad=pad_dur=2.04,atrim=duration=8[a5];[6:a]apad=pad_dur=0.52,atrim=duration=8[a6];[7:a]apad=pad_dur=2.36,atrim=duration=12[a7];[a1][a2][a3][a4][a5][a6][a7]concat=n=7:v=0:a=1[nar]" \
  -map 0:v:0 -map "[nar]" -t 60 \
  -r 24 -c:v libx264 -pix_fmt yuv420p -movflags +faststart \
  -c:a aac -b:a 192k "$OUT"

ffmpeg -hide_banner -loglevel error -y -ss 0.7 -i "$OUT" -frames:v 1 -q:v 2 "$COVER"
printf 'Created draft: %s\nCreated cover: %s\n' "$OUT" "$COVER"
