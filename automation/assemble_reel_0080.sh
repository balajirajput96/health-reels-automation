#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

ffmpeg -y -hide_banner -loglevel warning \
  -loop 1 -t 17.790 -i assets/reel_0080_scene_01.png \
  -loop 1 -t 17.790 -i assets/reel_0080_scene_02.png \
  -loop 1 -t 17.790 -i assets/reel_0080_scene_03.png \
  -loop 1 -t 17.790 -i assets/reel_0080_scene_04.png \
  -i assets/reel_0080_social_buffering_what_studies_measure_narration_hi.wav \
  -filter_complex "[0:v]zoompan=z='min(zoom+0.0012,1.08)':d=534:s=1080x1920:fps=30,setsar=1[v0];[1:v]zoompan=z='min(zoom+0.0014,1.08)':d=534:s=1080x1920:fps=30,setsar=1[v1];[2:v]zoompan=z='min(zoom+0.0016,1.08)':d=534:s=1080x1920:fps=30,setsar=1[v2];[3:v]zoompan=z='min(zoom+0.0012,1.08)':d=534:s=1080x1920:fps=30,setsar=1[v3];[v0][v1][v2][v3]concat=n=4:v=1:a=0,subtitles='assets/reel_0080_social_buffering_what_studies_measure_captions_hi.srt':fontsdir='/usr/share/fonts/truetype/noto':force_style='FontName=Noto Sans Devanagari,FontSize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H80000000,BorderStyle=1,Outline=2,Shadow=1,Alignment=2,MarginV=130'[v]" \
  -map "[v]" -map 4:a -t 71.160 \
  -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 160k -ar 48000 -ac 1 \
  -metadata "title=सामाजिक बफ़रिंग: अध्ययन वास्तव में क्या मापते हैं" \
  -metadata "comment=Evidence-bounded public education. AI-generated Hindi narration and deterministic conceptual visuals. Not personal, medical, or financial advice." \
  assets/reel_0080_social_buffering_what_studies_measure_hi.mp4 \
  2> state/reel_0080_ffmpeg_stderr.txt
