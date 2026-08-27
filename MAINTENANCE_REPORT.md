# Daily Repository Maintenance Report

**Date:** 2026-08-27

This report identifies configuration drift, stale references, and safety constraints checked across the private health-reels automation repository.

## Findings

1. **Duplicated State:**
   - Duplicated content found.
   - **Affected files:**
     - `records/reels/batch01/reel0004/remote/REEL-0004_script_hi.md` and `records/reels/batch01/reel0004/remote_reverification_20260822T0937Z/remote_script_hi.md`
     - `records/reels/batch01/reel0004/remote/REEL-0004_script_hi.md` and `records/reels/batch01/reel0004/remote_reverification_20260822T1041Z/remote_script_hi.md`
     - `production/active_drive_batch001/REEL-0008_fresh_start/source_validation.md` and `research/2026-08-27__reel0008__fresh-start-source-validation.md`
     - `production/active_drive_batch001/REEL-0009_context_cues/source_validation.md` and `research/2026-08-27__reel0009__context-cues-source-validation.md`
     - `production/active_drive_batch001/REEL-0010_study_reading/source_validation.md` and `research/2026-08-27__reel0010__reading-a-habit-study-source-validation.md`

2. **Unsafe Health-Language Patterns:**
   - Unsafe patterns detected.
     - `content/batches/batch04_evening_screens/production-plan.md` contains '\bmedical advice\b'
     - `docs/AUTONOMOUS_SOCIAL_VIDEO_AUTOMATION_BLUEPRINT.md` contains '\bdiagnosis\b'
     - `docs/cross_platform_integration_audit.md` contains '\bmedical advice\b'
     - `drafts/2026-08-16_sleep_stress_health_reel_brief.md` contains '\bdiagnosis\b'
     - `drafts/2026-08-16_sleep_stress_health_reel_brief.md` contains '\bmedical advice\b'
     - `drafts/2026-08-17__batch03__morning-light__production-plan.md` contains '\bdiagnosis\b'
     - `drafts/2026-08-17__batch03__morning-light__production-plan.md` contains '\bmedical advice\b'
     - `policy/ZERO_TOUCH_REELS_OPERATING_POLICY.md` contains '\btreat\b'
     - `policy/ZERO_TOUCH_REELS_OPERATING_POLICY.md` contains '\bmedical advice\b'
     - `production/reel0007_script_hi-IN.md` contains '\bmedical advice\b'
     - `production/rendered/REEL-0001_script_hi-IN.md` contains '\bguarantee\b'
     - `production/rendered/REEL-0001_script_hi-IN.md` contains '\bdiagnosis\b'
     - `production/rendered/REEL-0003_script_hi-IN.md` contains '\bdiagnosis\b'
     - `production/rendered/REEL-0003_script_hi-IN.md` contains '\bmedical advice\b'
     - `production/rendered/REEL-0004_script_hi-IN.md` contains '\bguarantee\b'
     - `production/rendered/REEL-0004_script_hi-IN.md` contains '\bdiagnosis\b'
     - `production/rendered/REEL-0004_script_hi-IN.md` contains '\bmedical advice\b'
     - `production/legacy/reel0001_affect_labeling_brief.md` contains '\bguarantee\b'
     - `production/legacy/reel0002_sleep_environment_brief.md` contains '\bguarantee\b'
     - `production/legacy/reel0003_self_concept_brief.md` contains '\bdiagnosis\b'
     - `production/legacy/reel0003_self_concept_brief.md` contains '\bmedical advice\b'
     - `production/legacy/reel0004_cognitive_biases_brief.md` contains '\bdiagnosis\b'
     - `production/legacy/reel0004_cognitive_biases_brief.md` contains '\bmedical advice\b'
     - `production/legacy/reel0007_meal_timing_brief.md` contains '\bmedical advice\b'
     - `production/legacy/reel0008_meal_timing_brief.md` contains '\bmedical advice\b'
     - `production/legacy/reel0008_script_hi-IN.md` contains '\bmedical advice\b'
     - `production/legacy/reel0031_meal_timing_brief.md` contains '\bmedical advice\b'
     - `production/legacy/reel0031_script_hi-IN.md` contains '\bmedical advice\b'
     - `production/legacy/reel0066_dietary_fiber_brief.md` contains '\bdiagnosis\b'
     - `production/legacy/reel0068_script_hi-IN.md` contains '\bmedical advice\b'
     - `production/legacy/reel0068_walking_meetings_brief.md` contains '\bguarantee\b'
     - `production/legacy/reel0069_script_hi-IN.md` contains '\bdiagnosis\b'
     - `production/legacy/reel0069_strength_activities_brief.md` contains '\bguarantee\b'
     - `production/legacy/reel0070_postural_variability_brief.md` contains '\bcure\b'
     - `production/legacy/reel0070_postural_variability_brief.md` contains '\bguarantee\b'
     - `production/legacy/reel0070_postural_variability_brief.md` contains '\btreat\b'
     - `production/legacy/reel0072_mindfulness_present_moment_brief.md` contains '\bguarantee\b'
     - `production/legacy/reel0072_script_hi-IN.md` contains '\bcure\b'
     - `production/legacy/reel0074_journaling_self_observation_brief.md` contains '\bcure\b'
     - `production/legacy/reel0074_script_hi-IN.md` contains '\bdiagnosis\b'
     - `production/legacy/reel0075_meaningful_hobbies_recovery_brief.md` contains '\bcure\b'
     - `production/legacy/reel0075_script_hi-IN.md` contains '\bcure\b'
     - `production/legacy/reel0076_notification_attention_brief.md` contains '\bdiagnosis\b'
     - `production/legacy/reel0077_script_hi-IN.md` contains '\bguarantee\b'
     - `production/legacy/reel0078_script_hi-IN.md` contains '\bguarantee\b'
     - `production/legacy/reel0078_script_hi-IN.md` contains '\bmedical advice\b'
     - `production/legacy/reel0079_script_hi-IN.md` contains '\bguarantee\b'
     - `production/legacy/reel0079_script_hi-IN.md` contains '\bdiagnosis\b'
     - `production/legacy/reel0079_script_hi-IN.md` contains '\bmedical advice\b'
     - `production/legacy/reel0079_tracking_habits_without_perfectionism_brief.md` contains '\bguarantee\b'
     - `records/publications/2026-08-25__batch06__movement-breaks__publication-record.md` contains '\bmedical advice\b'
     - `records/reels-ops/batch07/2026-08-20__batch07__physical-activity-stress__metadata.md` contains '\bmedical advice\b'
     - `records/reels-ops/batch08/2026-08-20__batch08__social-connection__metadata.md` contains '\bmedical advice\b'
     - `records/reels-ops/batch08/2026-08-20__batch08__social-connection__source-validation.md` contains '\bguarantee\b'
     - `records/reels-ops/batch08/2026-08-21__batch08__social-connection__final-staging.md` contains '\bcure\b'
     - `records/reels/batch01/reel0002/reconciliation.md` contains '\bdiagnosis\b'
     - `records/reels/batch01/reel0003/reconciliation.md` contains '\bdiagnosis\b'
     - `records/reels/batch01/reel0003/source_validation.md` contains '\bguarantee\b'
     - `records/reels/batch01/reel0003/source_validation.md` contains '\bdiagnosis\b'
     - `records/reels/batch01/reel0003/source_validation.md` contains '\bmedical advice\b'
     - `records/reels/batch01/reel0004/remote/REEL-0004_script_hi.md` contains '\bdiagnosis\b'
     - `records/reels/batch01/reel0004/remote_reverification_20260822T0937Z/remote_script_hi.md` contains '\bdiagnosis\b'
     - `records/reels/batch01/reel0004/remote_reverification_20260822T1041Z/remote_script_hi.md` contains '\bdiagnosis\b'
     - `records/reels/batch01/reel0004/remote_reverification_20260822T124055Z/remote_script_hi.md` contains '\bdiagnosis\b'
     - `records/reels/batch01/reel0004/remote_reverification_20260822T124055Z/remote_sources.md` contains '\bguarantee\b'
     - `records/reels/batch01/reel0004/remote_reverification_20260822T124055Z/remote_sources.md` contains '\bdiagnosis\b'
     - `records/reels/batch01/reel0005/script/script_hi-IN.md` contains '\bdiagnosis\b'
     - `records/reels/batch05/2026-08-20__batch05__caffeine-timing__production-plan.md` contains '\bdiagnosis\b'
     - `records/reels/batch05/2026-08-20__batch05__caffeine-timing__source-validation.md` contains '\bmedical advice\b'
     - `records/reels/batch06/2026-08-20__batch06__movement-breaks__metadata.md` contains '\bmedical advice\b'
     - `records/reels/batch06/2026-08-20__batch06__movement-breaks__production-plan.md` contains '\bguarantee\b'
     - `research/2026-08-22__drive-identity-reconciliation-0007-0009.md` contains '\btreat\b'
     - `research/2026-08-25__reel0007__behavior-change-limits-source-validation.md` contains '\btreat\b'
     - `research/2026-08-25__reel0079__tracking-habits-without-perfectionism-source-validation.md` contains '\btreat\b'

## Proposed Patch

Please review the proposed patch to ensure constraints and standards are maintained.
