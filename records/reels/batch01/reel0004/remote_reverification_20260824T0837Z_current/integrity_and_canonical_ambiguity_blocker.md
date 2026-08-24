# Reel 0004 — Fresh Drive Re-verification Blocker

- Re-verification time: `2026-08-24T08:38:57Z`
- Queued identity: `reel_0004_cognitive_biases_what_studies_measure`
- Canonical path: `3000_HINDI_RESEARCH_REELS/Batch_001/Reel_0004`
- Canonical folder ID: `1dL1yz1Lx3tnT9ali6nujGLHvmAbJLwIa`
- Authenticated listing source: `child_listing.json`, queried with `'<folder_id>' in parents and trashed = false`
- Fresh non-trashed child count: `24`

## Verified remote package

The fresh listing contains the queued-topic package, including video `1RFDW_qFKbNETKUZGNcEE3NGoDTI683AZ`, metadata `1MypkEiQmIcVdcddM6cx5oqoHlIzS-upw`, upload manifest `1MZiWUSiqjQuT3L_tkXWrNA-OhZVZ6af5`, and QC `1ZyRn1M-IIuxkcjpn6ORO28rbjKf9ObIb`. The queued-topic QC is authenticated from Drive and reports `valid: true`, `problems: []`, `ai_disclosure_present: true`, `aspect_ratio_9_16: true`, `safety_wording_ok: true`, `source_records: 3`, and a 63.467-second 1080x1920 portrait output.

The remote metadata identifies the queued topic and records `publication_status: not_published`, Hindi language `hi-IN`, the AI-assisted visual/narration disclosure, the research evidence class, and three peer-reviewed sources. These records support the content and safety checks but do not resolve the canonical ambiguity.

## Blocking findings

The same canonical folder also contains a prior verified package with QC file `1s7pb4eDrEXozxDct22V7bSDHYQWOrhy7`, title `मन भटकता क्यों है? Default Mode Network की कहानी`, tuple `MND-L01-Q04`, and state `verified`. The prior package is a different topic from the queued identity. Therefore the canonical folder is still identity-ambiguous.

The authenticated remote metadata bytes have SHA-256 `93e48f4ae055f392ed20d4af827c8f66b242227ac31ae3933968645a35fe32cc`, while the remote upload manifest records expected local SHA-256 `bcd191f2afbfffa8bd37b85c679a21d610c43e6901924d524272ef0bf335dc67` for `reel_0004_metadata.json`. The bytes therefore do not match the manifest integrity record.

## Safe disposition

Final Drive verification is withheld. No upload, overwrite, duplicate folder/file creation, deletion, publication, or queue advancement was performed. Retry state remains: resolve the canonical folder identity and produce a manifest-consistent metadata artifact before any final status transition.
