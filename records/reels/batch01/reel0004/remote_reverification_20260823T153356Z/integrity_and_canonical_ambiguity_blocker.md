# Reel 0004 — Safe Retry Blocker

- Recorded at: 2026-08-23T15:33:56Z
- Evidence: `remote_reverification_20260823T153356Z`
- Canonical path: `3000_HINDI_RESEARCH_REELS/Batch_001/Reel_0004`
- Folder ID: `1dL1yz1Lx3tnT9ali6nujGLHvmAbJLwIa`
- Queued identity: `reel_0004_cognitive_biases_what_studies_measure`
- Fresh authenticated child listing: 24 non-trashed entries. It contains the queued-topic package (`reel_0004_cognitive_biases_what_studies_measure_*`) and a prior different-topic `REEL-0004_*` package in the same canonical folder.
- Queued-topic remote QC: valid; 1080×1920 portrait, 63.467 seconds, 10 caption cues, 3 source records, safety wording present, and AI disclosure present.
- Upload-manifest expected SHA-256 for `reel_0004_metadata.json`: `bcd191f2afbfffa8bd37b85c679a21d610c43e6901924d524272ef0bf335dc67`.
- Authenticated remote SHA-256 for `reel_0004_metadata.json`: `93e48f4ae055f392ed20d4af827c8f66b242227ac31ae3933968645a35fe32cc`.
- Exact blocker: the canonical folder is identity-ambiguous and the authenticated remote metadata bytes do not match the upload manifest’s recorded local bytes. Final Drive verification is therefore unsafe even though the queued-topic QC report is valid.
- Safe retry state: keep `next_reel` at reel-0004, preserve all remote and local records, and retry only after canonical-folder identity resolution and a manifest-consistent metadata artifact are established.
- Prohibited in this run: upload, overwrite, duplicate-folder/file creation, queue advancement, or social publication.

## Supporting authenticated IDs

| Artifact | Drive file ID |
|---|---|
| Queued-topic upload manifest | `1MZiWUSiqjQuT3L_tkXWrNA-OhZVZ6af5` |
| Queued-topic metadata | `1MypkEiQmIcVdcddM6cx5oqoHlIzS-upw` |
| Queued-topic QC | `1ZyRn1M-IIuxkcjpn6ORO28rbjKf9ObIb` |
| Queued-topic video | `1RFDW_qFKbNETKUZGNcEE3NGoDTI683AZ` |
| Prior conflicting QC | `1s7pb4eDrEXozxDct22V7bSDHYQWOrhy7` |

Repository validation before state update: deterministic unit tests passed, state-guard status completed without mutation, and the non-destructive repository health check passed.
