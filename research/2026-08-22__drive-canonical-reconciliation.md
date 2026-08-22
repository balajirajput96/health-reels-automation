# Google Drive canonical reel reconciliation — 2026-08-22

**Purpose:** Preserve the authoritative Drive inventory before resuming content production and prevent duplicate Reel IDs or destructive overwrites.

## Verified inventory boundary

The required Drive root and Batch_001 folder were queried read-only through the authorized Google Workspace CLI. The root is `3000_HINDI_RESEARCH_REELS` (`1qBzjS18Pd4zNEmgNhZsDqKHrl17uCOyS`) and Batch_001 is `19uErd4g0xD0geAUi6SJbdPV3Ih4K3mHC`.

The canonical folders named `REEL-0001` through `REEL-0006` were found under Batch_001. Each canonical folder contains a manifest and a rendered video; the Drive manifests identify the packages as `complete_drive_verified`. Their detailed IDs, hashes, and verification observations are preserved in `checkpoints/drive_canonical_reconciliation_20260822T0942Z.json` outside the repository.

| Drive reel | Canonical folder | Observed topic | Observed status | Reconciliation note |
|---|---|---|---|---|
| REEL-0001 | `1-TVdwDN2HIf2OWfPb6Jv-FmCgFJ7LT4u` | Affect labeling and emotional regulation | `complete_drive_verified` | Matches the local `drive_verified` record and is not published by this mission state. |
| REEL-0002 | `1JzyQOs5SYvvrk12rPOXD9kf1OtP1FVHP` | Homeostatic sleep pressure and the circadian clock | `complete_drive_verified` | Preserve alongside the local fallback record; the two manifests contain different video hashes and must not be overwritten. |
| REEL-0003 | `1RAfj9uOe67srsRiGlhLx1LJNO8bioLx-` | Predictive processing and whether the predictive brain ignores reality | `complete_drive_verified` | This existing Drive package owns the `REEL-0003` identity. |
| REEL-0004 | `1uYBw--o8pSZi_7ni8tlaVJTaZk6X0JXW` | Predictive processing and reality framing | `complete_drive_verified` | Existing Drive package; retain its original identity and metadata. |
| REEL-0005 | `1W3X_PyL-fYb3FJ27E-iy3NfxGpk60MoN` | Observing expectations through a predictive-processing lens | `complete_drive_verified` | Existing Drive package; retain its original identity and metadata. |
| REEL-0006 | `14Ud3qCRv27UWcli5x01JR9zoQaXRf6zU` | Context-dependent effects of expectation | `complete_drive_verified` | Existing Drive package with additional reconciliation artifacts; retain all files. |

## Identity collision and safe reindex

The local review branch had a research-ready meal-timing draft named `REEL-0003`, but the authoritative Drive inventory already contains a different verified `REEL-0003` about predictive processing. The meal-timing draft therefore cannot be uploaded or registered under `REEL-0003`. It has been reindexed to **`REEL-0007`** on the review branch, with its brief, script, research record, and pending manifest renamed and internally corrected.

Reindexing does not make the meal-timing item complete. Its lifecycle remains `research_ready`; it has no video, narration, captions, QC record, Drive folder, ledger entry, or publication authorization. Topic-specific visual generation remains subject to the provider quota and must be attempted only through the authorized path.

## Duplicate and legacy preservation

Several older or alternate folders were also visible, including `Reel_0001`, `Reel_0002`, `Reel_0003`, `Reel_0004`, `REEL-0002` duplicate folder `18xQxeiMfdTlMCDf09VQnzYMXkfSKAbzD`, and `R0001`–`R0006` experiment folders. None was deleted, trashed, overwritten, or promoted to canonical status by this reconciliation.

## Safety boundary

This record reports observed Drive metadata only. It does not claim publication, social-post verification, or authorization beyond the Drive package statuses. No credentials were copied, no access-control or quota control was bypassed, and no Drive write operation was performed during reconciliation.
