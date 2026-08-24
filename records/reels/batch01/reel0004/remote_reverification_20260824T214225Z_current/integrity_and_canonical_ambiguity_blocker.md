# Reel_0004 remote integrity and canonical-identity blocker

- Evidence ref: `remote_reverification_20260824T214225Z_current`
- Verification time: `2026-08-24T21:42:25Z`
- Canonical path: `3000_HINDI_RESEARCH_REELS/Batch_001/Reel_0004`
- Folder ID: `1dL1yz1Lx3tnT9ali6nujGLHvmAbJLwIa`
- Queued identity: `reel_0004_cognitive_biases_what_studies_measure`
- Queued title: `Cognitive Bias का Score: Studies क्या Measure करती हैं?`

## Fresh authenticated listing

The authenticated Drive listing contains 24 non-trashed children in the canonical folder. It contains both a prior package using the names `REEL-0004_qc.json`, `REEL-0004_reel.mp4`, `REEL-0004_script_hi.md`, and related artifacts, and the queued-topic package using `reel_0004_cognitive_biases_what_studies_measure_*` names. The prior package is an identity conflict because its remote QC record is for a different topic and tuple (`MND-L01-Q04`, “मन भटकता क्यों है? Default Mode Network की कहानी”), while the queued package identifies the cognitive-bias topic.

The queued-topic remote records are present and readable through authenticated Drive:

| Record | Drive file ID | Result |
|---|---|---|
| Queued-topic video | `1RFDW_qFKbNETKUZGNcEE3NGoDTI683AZ` | Present, non-trashed |
| Queued-topic metadata | `1MypkEiQmIcVdcddM6cx5oqoHlIzS-upw` | Present, non-trashed; `reel_id` matches queue |
| Queued-topic QC | `1ZyRn1M-IIuxkcjpn6ORO28rbjKf9ObIb` | `valid: true`, no listed problems |
| Upload manifest | `1MZiWUSiqjQuT3L_tkXWrNA-OhZVZ6af5` | Present, non-trashed |

The queued-topic QC reports that the media is 1080×1920, 63.467 seconds, has Hindi-audio-compatible audio metadata, ten caption cues, AI disclosure, safety wording, and source identifiers. These checks do not resolve the canonical identity conflict or manifest-integrity mismatch.

## Manifest-integrity mismatch

The authenticated remote metadata bytes were captured as `remote_metadata_stdout.json` and hash to:

`93e48f4ae055f392ed20d4af827c8f66b242227ac31ae3933968645a35fe32cc`

The authenticated upload manifest records the expected local SHA-256 for `reel_0004_metadata.json` as:

`bcd191f2afbfffa8bd37b85c679a21d610c43e6901924d524272ef0bf335dc67`

These hashes differ. The manifest itself also identifies the queued reel and the same canonical folder, but the authoritative remote bytes do not match its recorded local metadata hash.

## Safe decision

Final Drive verification is **refused**. No upload, overwrite, duplicate-folder creation, deletion, renaming, publication, or queue advancement was performed. The checkpoint cursor remains on `reel_0004_cognitive_biases_what_studies_measure`; retry only after an authoritative canonical-folder identity resolution and a manifest-consistent metadata artifact are supplied. The queued reel remains retryable but blocked, and later IDs must not be processed.
