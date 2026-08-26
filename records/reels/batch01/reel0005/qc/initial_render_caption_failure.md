# Reel 0005 Initial Render — Caption QC Failure

**Reviewed artifacts:** `qc/contact_sheet.png` and `qc/final_boundary_frame.png`
**Technical render:** Valid 1080×1920 MP4 with 54.00-second audio/video duration.
**Editorial QC decision:** **FAIL — do not upload or claim completion.**

## Finding

The first subtitle-rendering pass used the SRT input directly through FFmpeg/libass. Visual inspection found that captions were rendered at an oversized scale and were cropped at the frame boundaries. The closing **Mixed Evidence** label was not fully visible or legible.

## Required correction

Create an ASS subtitle track with an explicit 1080×1920 PlayRes canvas and a restrained Devanagari font style, then rerender and repeat technical and visual QC. The original narration, source records, and scene assets remain valid; only the subtitle-rendering configuration is rejected.
