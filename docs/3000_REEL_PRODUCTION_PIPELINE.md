# 3,000 Hindi Research-Reel Production Pipeline

## Purpose

This repository now contains a resumable planning and validation layer for 3,000 unique Hindi research reels. The queue is planning metadata, not evidence that future reels have been researched or produced. A reel becomes complete only after research, script safety review, Hindi narration, Hindi captions, 9:16 assembly, deterministic QC, Drive upload, and independent Drive listing verification.

## Durable state

| File | Role |
|---|---|
| `state/reels_3000_queue.jsonl` | One JSON record for each sequence from 0001 through 3000. |
| `state/reels_3000_checkpoint.json` | Aggregate counts, next unfinished sequence, last completed reel, and failure log. |
| `state/reels_ledger.json` | Shared idempotency ledger for final/staged/published artifacts. |
| `automation/checkpoint.py` | Atomic selection, forward-only stage updates, failure recording, and checkpoint refresh. |
| `automation/scaffold_3000_queue.py` | Deterministic queue creation and integrity validation. |
| `automation/reel_qc.py` | Technical and safety preflight for a complete asset package. |
| `automation/assemble_reel.py` | Parameterized 9:16 ffmpeg assembly from still visuals, audio, and SRT captions. |

The queue is arranged as `Batch_001` through `Batch_100`, with 30 records per batch. Every record has a stable sequence, a generated unique angle key, a topic key, a pillar, a Drive path, required asset names, source-ID slots, safety status, retries, and QC flags. Future entries remain `planned`, `research_pending`, and `REVIEW_REQUIRED` until an actual production run advances them.

## Stage discipline

The worker must process the first non-terminal item and must not rebuild a `final` or `rejected` item. A failure is recorded explicitly, increments the retry counter, and remains visible in the checkpoint rather than being silently skipped. The valid forward stages are:

`planned → research_pending → research_verified → script_ready → audio_ready → visuals_ready → assembled → qc_passed → uploaded → final`

A `final` transition is rejected unless the item has non-empty source IDs and QC flags for decode success, captions, Hindi audio, AI disclosure, and verified Drive upload. Public social publication is a separate operation and is not part of this queue’s completion condition.

## QC boundary

`automation/reel_qc.py` verifies that the required files exist, the MP4 has a 9:16 pixel ratio and a 45–75 second duration, an audio stream is present, captions are parseable and remain within the media duration, sources contain recognizable identifiers or URLs, metadata contains source records and AI-content disclosure, and the script does not contain unsupported positive treatment, diagnosis, guarantee, or miracle wording. It does not replace human or scholarly verification of whether a claim is true; every research record must still distinguish established findings, hypotheses, expert interpretations, philosophy, and spiritual belief.

The safety scanner is designed to permit explicit caveats such as “not a guaranteed method” and “इलाज का दावा नहीं” while rejecting uncaveated promise language. Scripts must remain general public education: no diagnosis, individualized treatment, fixed outcome promises, or crisis/medical instructions.

## Drive and continuation

Each completed reel is uploaded under `3000_HINDI_RESEARCH_REELS/Batch_NNN/Reel_NNNN/` together with its MP4, WAV, SRT, metadata, research sources, script, and visual provenance. The upload is not considered complete until a fresh listing confirms the files and sizes. If Drive, media generation, browser authentication, or another required capability is unavailable, the continuation must record the blocker and leave the item pending.

The existing recurring engineering continuation remains active and now includes a bounded queue/checkpoint maintenance instruction. It has the GitHub connector only; it must not claim that media generation or Drive access is available in that run, and it must never use that schedule to publish or bypass authentication.
