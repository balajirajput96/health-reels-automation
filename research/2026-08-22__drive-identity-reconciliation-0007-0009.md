# Drive identity reconciliation — Reel 0007, Reel 0008, and Reel 0009

**Recorded:** 2026-08-22
**Purpose:** Prevent local pending metadata from overwriting or duplicating canonical Google Drive packages.
**Drive source of truth:** `3000_HINDI_RESEARCH_REELS` (`1qBzjS18Pd4zNEmgNhZsDqKHrl17uCOyS`) → `Batch_001` (`19uErd4g0xD0geAUi6SJbdPV3Ih4K3mHC`).

## Authoritative findings

The refreshed non-trashed Batch_001 inventory contains canonical folders for REEL-0001 through REEL-0007, a missing REEL-0008 slot, and a canonical REEL-0009 folder. Two REEL-0002 folders remain; the established canonical folder is preserved and the duplicate is not deleted or overwritten.

| Identity | Drive folder | Topic/status | Decision |
|---|---|---|---|
| REEL-0007 | `1OD00swazBKl04aDJVkawUvUklP9jHIu3` | Predictive processing; `complete_drive_verified`; 720×1280; 62.233333 seconds | Treat as canonical. Do not overwrite. |
| REEL-0008 | No folder found | Reserved gap; local meal-timing item is `research_ready` only | Safe target for the local meal-timing draft after review. |
| REEL-0009 | `1pPOeS7gzF9_5KxNUmad7hswD-MZ7Ty9v` | Prediction / visual-perception myth-check; Drive record says upload verified; 720×1280; 58 seconds | Treat as canonical. Preserve read-back evidence. |

The canonical REEL-0007 Drive package has manifest `1M-XArZvBdOXkTKPEWJy3BJabjoain8Fo`, QC `1tDFKVbQrYriRGLl7DwV2s9n9xpSmxAPM`, video `1R3V50WRmRWjpXzP1ARCpUCUx2KXwWLrD`, and SHA-256 `863cc402829a7a7aa56d953043e16fc83feaa49b33101a6a6131fa6893de281c`. Its topic is predictive processing, not meal timing.

The canonical REEL-0009 Drive package has manifest `1NYXzyfB2ijhPH8UAHn1DinaXW4c0wce3`, Drive record `19EdzNaFwfOZtvAcFHXevbYREO_QvQ_Lt`, and video `1qbsu8vzKU7znOEWz7frgxUP9GzR2cFw6`. The Drive record was read back as `uploadStatus: verified`; the package is preserved without relying on the manifest’s older `qc_passed_pending_drive_upload` wording alone.

## Reindex decision

The local pending meal-timing research, script, brief, captions, and pending-QC metadata previously used REEL-0007. Because Drive already contains a different canonical REEL-0007 predictive-processing package, the meal-timing item is reindexed to **REEL-0008**. The reindex changes identity and local artifact paths only; it does not alter the approved scientific text, citations, uncertainty boundary, safety disclaimer, or lifecycle state.

REEL-0008 remains `research_ready`, `drive_verified: false`, and `publication_allowed: false`. The current package has no final video. Its topic-specific image generation was blocked at the authorized daily image limit of 20/20, and native video generation remains blocked by the inherited 1/1 limit. Its local narration and captions must not be treated as a completed reel until the visual, video, full-QC, and Drive re-list gates pass.

## Safety and resume rule

No Drive package is created or overwritten by this reconciliation. The next production action is to review this identity change through a GitHub pull request. Only after that boundary, and after provider quotas reset, may REEL-0008 proceed to topic-specific 9:16 visuals, final assembly, full QC, canonical Drive upload, and re-list verification. No ledger completion state or publication ID is created before those gates pass.

**Supporting checkpoint:** `/home/ubuntu/github-workspace/checkpoints/reels_mission_checkpoint_20260822T1129Z.json`.

**Integrity boundary:** No authentication, quota, billing, security, or Drive deletion control was bypassed.

## References

1. Canonical Drive inventory and package read-back: `/home/ubuntu/github-workspace/checkpoints/reels_mission_checkpoint_20260822T1129Z.json`.
2. REEL-0007 Drive content reconciliation: `/home/ubuntu/github-workspace/checkpoints/drive_reel0007_content_reconciliation_20260822T1126Z.md`.
3. Earlier canonical inventory: `/home/ubuntu/github-workspace/checkpoints/drive_canonical_reconciliation_20260822T0942Z.json`.
4. Local meal-timing source validation: `research/2026-08-22__reel0007__meal-timing-source-validation.md`.
5. Local meal-timing production brief: `production/reel0007_meal_timing_brief.md`.
6. Local meal-timing Hindi script: `production/reel0007_script_hi-IN.md`.
7. Local pending manifest/QC and narration checkpoint: `production/rendered/REEL-0007_pending_manifest.json`, `production/rendered/REEL-0007_pending_qc.json`, and PR #18 branch artifacts.

> This record is an identity reconciliation, not a claim that REEL-0008 is final, Drive-verified, or publishable.
