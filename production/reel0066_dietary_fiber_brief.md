# REEL-0066 production brief

## Concept

A roughly one-minute Hindi research reel explaining why dietary fiber belongs in a varied eating pattern, using recognizable plant-food visuals and a careful distinction between established public-health guidance and ongoing gut-microbiome research.

## Audience and goal

The audience is Hindi-speaking adults seeking practical, general nutrition education. The goal is to replace the narrow “fiber equals constipation” frame with a balanced behavior cue: include a variety of fiber-containing plant foods gradually, without turning the reel into a personal diet plan.

## Format

| Field | Specification |
|---|---|
| Aspect ratio | 9:16 portrait |
| Working resolution | 720×1280 final render |
| Duration | Approximately 60–65 seconds |
| Language | Hindi narration and Hindi captions with familiar English nutrition terms where natural |
| Voice | Calm, clear, informative documentary voice; one consistent voice across seven spans |
| Visual route | Topic-specific AI reference images with deterministic Ken Burns motion; no invented product labels or numerical charts |
| Audio | Hindi narration only; no music required |
| Publication | Blocked until final editorial review; Drive verification is mandatory |

## Seven-span visual arc

| Span | Narrative purpose | Visual direction | Evidence label |
|---|---|---|---|
| 01 | Hook | Overhead still life of colorful plant foods and a bowl of lentils; gentle push-in | General education |
| 02 | Public-health framing | Whole grains, pulses, vegetables and fruit arranged as a varied plate | WHO guidance |
| 03 | Practical sources | Close-ups of dal, chickpeas, beans, oats, brown rice, vegetables and nuts | Established nutrition explanation |
| 04 | Gut mechanism | Conceptual, non-literal gut-microbe visual with plant fibers moving toward a calm intestinal pathway | Harvard educational synthesis |
| 05 | Uncertainty boundary | Split conceptual visual showing different fiber types and varied microbial responses; no numeric claims | Peer-reviewed review; effects vary |
| 06 | Behavior cue | Gradual-addition checklist and a small portion added to a meal; no prescriptive quantities beyond attributed WHO context | Practical guidance |
| 07 | Safety boundary | Calm closing kitchen scene with open space for captions and clinician/dietitian disclaimer | General education; not personal advice |

## Visual constraints

All generated images must be upright 9:16, topic-specific, consistent in lighting and palette, free of logos, watermarks, fabricated readable labels, medical imagery that implies diagnosis, and unsupported numbers. The visual layer must not imply that fiber alone prevents or treats disease. Captions are added deterministically in the video assembly because the exact Hindi wording must remain synchronized and legible.

## Caption policy

Use real multiline SRT line breaks, a readable Devanagari font, controlled line lengths, high contrast, outline, and a lower-third safe area. Captions must reflect the spoken narration exactly enough for comprehension. Check for literal escape sequences, extra blank lines, overflow, and timing gaps before Drive upload.

## QC gates

The reel cannot advance to Drive verification unless: research and citations are present; the script separates WHO guidance, university synthesis, and peer-reviewed uncertainty; seven Hindi narration spans are generated; captions contain seven correctly timed blocks; final video is 720×1280 at 30 fps with H.264/AAC; FFmpeg decode and FFprobe pass; visual spot-check shows no fatal crop or caption defect; SHA-256 is recorded; no secret patterns are present; and the complete package is uploaded to the exact identity folder and re-listed.

## Package contents

Final video, combined narration WAV, Hindi SRT, Hindi script, this brief, evidence register, assembly metadata, QC JSON, pending/final manifest, and topic-specific reference images. Generated media remains ignored by Git; reproducible source and metadata are tracked.

## Disclosure and safety

The brief and manifest must disclose the use of AI-generated reference visuals with deterministic motion. The reel is general education and not a diagnosis, treatment, or individualized nutrition prescription. Publication is prohibited until separate editorial review and publishing verification.
