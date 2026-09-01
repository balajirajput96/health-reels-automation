#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/ubuntu/repos/health-reels-automation"
ASSETS="$ROOT/assets"
OUT="$ASSETS/reel_0001_affect_labeling_hi.mp4"
FONTDIR="/usr/share/fonts/truetype/noto"

ffmpeg -y \
  -hide_banner -loglevel warning \
  -loop 1 -t 6.0 -i "$ASSETS/reel_0001_visual_reference.png" \
  -loop 1 -t 10.0 -i "$ASSETS/reel_0001_scene_01_emotion_pause.png" \
  -loop 1 -t 19.0 -i "$ASSETS/reel_0001_scene_02_amygdala_study.png" \
  -loop 1 -t 11.0 -i "$ASSETS/reel_0001_scene_03_label_and_context.png" \
  -loop 1 -t 9.2 -i "$ASSETS/reel_0001_scene_03_label_and_context.png" \
  -i "$ASSETS/reel_0001_narration_hi.wav" \
  -filter_complex "\
    [0:v]zoompan=z='min(zoom+0.0015,1.08)':d=180:s=1080x1920:fps=30,setsar=1[v0];\
    [1:v]zoompan=z='min(zoom+0.0012,1.07)':d=300:s=1080x1920:fps=30,setsar=1[v1];\
    [2:v]zoompan=z='min(zoom+0.0008,1.06)':d=570:s=1080x1920:fps=30,setsar=1[v2];\
    [3:v]zoompan=z='min(zoom+0.0010,1.07)':d=330:s=1080x1920:fps=30,setsar=1[v3];\
    [4:v]zoompan=z='min(zoom+0.0010,1.06)':d=276:s=1080x1920:fps=30,setsar=1[v4];\
    [v0][v1][v2][v3][v4]concat=n=5:v=1:a=0,\
    subtitles='$ASSETS/reel_0001_captions_hi.srt':fontsdir='$FONTDIR':force_style='FontName=Noto Sans Devanagari,FontSize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H80000000,BorderStyle=1,Outline=2,Shadow=1,Alignment=2,MarginV=130'[v]" \
  -map "[v]" -map 5:a \
  -t 55.2 -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 160k -ar 48000 \
  -metadata title="भावना को नाम देना" \
  -metadata comment="Evidence-bounded public education; not diagnosis or treatment. Sources: PMID 17576282; Front Psychol 2014; PLOS ONE 2022; BMC Psychol 2024. AI-generated narration and visuals may be used." \
  "$OUT"

printf 'Wrote %s\n' "$OUT"
