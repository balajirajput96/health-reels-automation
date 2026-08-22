# Reel 0004 reconciliation blocker

**Run date:** 2026-08-22
**Authoritative queue target:** `reel_0004_cognitive_biases_what_studies_measure`
**Canonical path:** `3000_HINDI_RESEARCH_REELS/Batch_001/Reel_0004`

## Result

Local evidence research, Hindi script, AI narration, original procedural 9:16 visuals, assembly, and deterministic QC completed successfully for the queued cognitive-bias topic. The local package is in `work/reel_0004` and passed `automation/qc_reel0004.py` with a 72.142-second 720×1280 H.264/AAC portrait video, six ordered Devanagari caption cues, Hindi narration, source identifiers, safety wording, AI disclosure, and `publication_allowed: false`.

Drive listing verification found that the canonical `Reel_0004` folder already exists at folder ID `1dL1yz1Lx3tnT9ali6nujGLHvmAbJLwIa` under Batch_001. It contains a previously verified package whose remote QC record reports `state: verified`, but its identity and topic do not match the authoritative queue target. The remote script identifies `REEL-0004`, tuple `MND-L01-Q04`, and title **“मन भटकते क्यों है? Default Mode Network की कहानी”**, with neuroscience sources. The queue target is **“संज्ञानात्मक पूर्वाग्रह: अध्ययन वास्तव में क्या मापते हैं”**, with psychology measurement sources.

The existing remote folder and files were not overwritten, and no duplicate folder or file was created. The local cognitive-bias package was not uploaded because doing so would create an ambiguous canonical identity or require overwriting an existing verified package, neither of which is permitted by the playbook.

## Authenticated remote evidence

The folder was listed through the authenticated Google Workspace Drive API. The folder inventory contained `REEL-0004_reel.mp4`, `REEL-0004_voice.wav`, `REEL-0004_captions.srt`, `REEL-0004_script_hi.md`, `REEL-0004_research.md`, `REEL-0004_claims.json`, `REEL-0004_production_blueprint.md`, `REEL-0004_qc.json`, and four reference PNGs. Remote QC reported the folder and video IDs, a 64.533333-second 720×1280 H.264/AAC video, eight caption cues, and `videoMd5VerifiedAgainstDriveListing: true`.

## Safe retry state

The queue remains pointed at reel 0004 with `production_stage: planned`, `research_stage: verified`, and `qc.drive_verified: false`. The checkpoint records one bounded `canonical_path_topic_conflict` failure and retains `next_reel: reel_0004_cognitive_biases_what_studies_measure`. A future run must re-check the folder identity and must not upload, overwrite, or create a duplicate until the conflict is resolved through an authoritative workflow.
