# Reel 0005 Quality-Control Report

**Canonical reel ID:** `reel_0005_psychological_flexibility_what_studies_measure`
**Final media file:** `assets/Reel_0005_psychological_flexibility_hi-IN.mp4`
**QC status:** **PASS for local render; Drive verification pending**

## Technical checks

| Check | Result |
|---|---|
| Video codec | H.264 |
| Audio codec | AAC, mono, 24 kHz |
| Frame size | 1080 × 1920 (9:16) |
| Frame rate | 30 fps |
| Measured duration | 54.00 seconds |
| File size | 5,417,706 bytes |
| Full decode | Passed with `ffmpeg -v error -i … -f null -` |
| Final MP4 SHA-256 | `ae8a29f9276bb24afab01f8868cbf51bc6c5e57237c470d18a34645d826230a7` |

## Editorial and evidence checks

The narration is evidence-bounded and labels the topic **Mixed Evidence**. It identifies the construct as research-based, includes the self-report measurement caveat from the 2020 review, does not diagnose viewers, does not promise a clinical outcome, and includes a qualified-support boundary for severe or functionally impairing distress.

The first caption-rendering pass failed editorial QC because direct SRT rendering produced oversized and cropped captions. That rejected configuration is recorded in `qc/initial_render_caption_failure.md`. The final render uses an explicit 1080×1920 ASS canvas, Noto Sans Devanagari, restrained 44-point text, safe margins, and a visible closing **Evidence label: Mixed Evidence** line. Visual review of `qc/final_boundary_frame_corrected.png` confirmed the closing Hindi safety text and evidence label are fully visible and legible.

## Completion boundary

This report does **not** certify Drive upload, canonical remote listing, remote checksum verification, ledger registration, or publication. Those gates remain required before `COMPLETED_VERIFIED` may be claimed.
