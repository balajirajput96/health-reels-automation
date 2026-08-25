# Google Drive account and canonical-root reconciliation — 2026-08-23

## Findings

The activated Google Workspace connector is the previously authorized unnamed account UID `b083f8c4-a617-5bbe-9ea5-0ecd6e4fc4f7`, selected from the preserved Drive reconciliation history. The connector now responds successfully through `gws drive`.

A read-only Drive search returned two non-trashed folders named `3000_HINDI_RESEARCH_REELS`:

| Root ID | Observed contents | Interpretation |
|---|---|---|
| `1s8HhWxw2k1n57lhMyLmIT30Ln6y8rnc4` | Many `Batch_001` through at least `Batch_036` folders; Batch_001 contains a large generated package set | Legacy or bulk archive candidate; requires package-level identity reconciliation before use |
| `1vYLRarvedtfaYzNcINGKpKAeeFaz0OnD` | `Batch_001`, `checkpoint.json`, `canonical_production_state.json`, and `reel_registry_3000_slots.json` | Newer state-management candidate; Batch_001 contains a Reel 0001 neuroplasticity package with duplicate MP4/QC variants |

The previously recorded root ID `1qBzjS18Pd4zNEmgNhZsDqKHrl17uCOyS` is not accessible under this active account and returned Drive API 404. Therefore it was not modified.

The local authoritative checkpoint remains `last_completed = reel_0003_self_concept_what_studies_measure`, `next_reel = reel_0004_cognitive_biases_what_studies_measure`, and `completed_drive_verified = 3`. It records a separate prior canonical-path conflict and metadata hash mismatch for Reel 0004. No upload, overwrite, duplicate folder, or destructive cleanup was performed during this reconciliation.

## Safe continuation rule

Completed local and Drive-verified reels must not be regenerated. Before Reel 0004 is uploaded or marked complete, the production runner must select one canonical root and one canonical package identity, verify the manifest hash against the exact remote metadata bytes, and refuse ambiguous or conflicting packages. If ambiguity remains, keep Reel 0004 in `RETRY_QUEUE` and continue only with a separately resolved, non-duplicate item after updating the authoritative checkpoint.
