#!/usr/bin/env python3
"""Scaffold and validate the 3,000-reel Hindi research queue.

This file creates planning metadata only. It does not claim research, media,
QC, Drive upload, or publication for entries that have not passed those gates.
It is intentionally credential-free and safe to rerun: an existing queue is
never overwritten unless --force is supplied.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "state" / "reels_3000_queue.jsonl"
CHECKPOINT = ROOT / "state" / "reels_3000_checkpoint.json"

PILLARS = [
    ("psychology", "मनोविज्ञान"),
    ("neuroscience", "न्यूरोसाइंस"),
    ("mind", "मन"),
    ("brain", "मस्तिष्क"),
    ("consciousness", "चेतना"),
    ("behavior", "व्यवहार"),
    ("emotions", "भावनाएँ"),
    ("habits", "आदतें"),
    ("meditation", "ध्यान"),
    ("learning", "सीखना"),
    ("decision_making", "निर्णय"),
    ("memory", "स्मृति"),
    ("attention", "ध्यान और एकाग्रता"),
    ("social_cognition", "सामाजिक संज्ञान"),
    ("motivation", "प्रेरणा"),
    ("stress", "तनाव"),
    ("sleep", "नींद"),
    ("language", "भाषा"),
    ("philosophy", "दर्शन"),
    ("spirituality", "आध्यात्मिकता"),
]

# Five researchable anchor concepts per pillar = 100 anchors. These are
# prompts for future evidence review, not pre-approved claims.
ANCHORS = [
    ("emotion_prediction", "भावनाओं का अनुमान", 0), ("self_concept", "स्व-अवधारणा", 0), ("cognitive_biases", "संज्ञानात्मक पूर्वाग्रह", 0), ("psychological_flexibility", "मनोवैज्ञानिक लचीलापन", 0), ("context_effects", "संदर्भ का प्रभाव", 0),
    ("neural_plasticity", "न्यूरल प्लास्टिसिटी", 1), ("reward_learning", "रिवार्ड लर्निंग", 1), ("interoception", "इंटरोसेप्शन", 1), ("amygdala_context", "अमिग्डाला और संदर्भ", 1), ("prefrontal_control", "प्रीफ्रंटल नियंत्रण", 1),
    ("mental_models", "मानसिक मॉडल", 2), ("inner_speech", "आंतरिक संवाद", 2), ("metacognition", "मेटाकॉग्निशन", 2), ("rumination", "रूमिनेशन", 2), ("mental_time_travel", "मानसिक समय-यात्रा", 2),
    ("brain_networks", "मस्तिष्क नेटवर्क", 3), ("hemispheric_myths", "मस्तिष्क-गोलार्ध मिथक", 3), ("glial_cells", "ग्लियल कोशिकाएँ", 3), ("brain_energy", "मस्तिष्क ऊर्जा", 3), ("sensory_integration", "संवेदी एकीकरण", 3),
    ("conscious_access", "चेतन पहुँच", 4), ("global_workspace", "ग्लोबल वर्कस्पेस", 4), ("predictive_processing", "प्रेडिक्टिव प्रोसेसिंग", 4), ("self_awareness", "स्व-जागरूकता", 4), ("altered_states", "परिवर्तित अवस्थाएँ", 4),
    ("observational_learning", "अवलोकन से सीखना", 5), ("social_norms", "सामाजिक मानदंड", 5), ("choice_architecture", "चॉइस आर्किटेक्चर", 5), ("prosocial_behavior", "परोपकारी व्यवहार", 5), ("behavior_change", "व्यवहार परिवर्तन", 5),
    ("affect_labeling_context", "भावना-नामकरण का संदर्भ", 6), ("emotion_granularity", "भावना-ग्रैन्युलैरिटी", 6), ("reappraisal", "रीएप्रेज़ल", 6), ("mood_congruent_memory", "मूड-कॉन्ग्रुएंट स्मृति", 6), ("emotional_contagion", "भावनात्मक संक्रामकता", 6),
    ("implementation_intentions", "इम्प्लीमेंटेशन इंटेंशन्स", 7), ("cue_competition", "क्यू कॉम्पटीशन", 7), ("habit_automaticity", "हैबिट ऑटोमैटिसिटी", 7), ("environmental_friction", "पर्यावरणीय घर्षण", 7), ("identity_and_habits", "पहचान और आदतें", 7),
    ("mindfulness_attention", "माइंडफुलनेस और ध्यान", 8), ("meditation_training", "ध्यान-अभ्यास", 8), ("breath_awareness", "श्वास-जागरूकता", 8), ("compassion_practice", "करुणा-अभ्यास", 8), ("contemplative_traditions", "चिंतन परंपराएँ", 8),
    ("retrieval_practice", "रिट्रीवल प्रैक्टिस", 9), ("spacing_effect", "स्पेसिंग इफ़ेक्ट", 9), ("interleaving", "इंटरलीविंग", 9), ("desirable_difficulty", "वांछनीय कठिनाई", 9), ("feedback_learning", "फीडबैक से सीखना", 9),
    ("choice_overload", "चॉइस ओवरलोड", 10), ("framing_effect", "फ्रेमिंग इफ़ेक्ट", 10), ("base_rate_reasoning", "बेस-रेट तर्क", 10), ("uncertainty", "अनिश्चितता", 10), ("deliberation", "विचार-विमर्श", 10),
    ("working_memory", "वर्किंग मेमोरी", 11), ("episodic_memory", "एपिसोडिक स्मृति", 11), ("semantic_memory", "सिमेंटिक स्मृति", 11), ("false_memory", "झूठी स्मृति", 11), ("memory_reconsolidation", "मेमोरी रिकॉन्सॉलिडेशन", 11),
    ("selective_attention", "चयनात्मक ध्यान", 12), ("attentional_blink", "अटेंशनल ब्लिंक", 12), ("mind_wandering", "माइंड-वांडरिंग", 12), ("task_switching", "टास्क स्विचिंग", 12), ("deep_work_claims", "गहरे काम के दावे", 12),
    ("theory_of_mind", "थ्योरी ऑफ माइंड", 13), ("social_learning", "सामाजिक सीखना", 13), ("empathy", "सहानुभूति", 13), ("dehumanization", "अमानवीकरण", 13), ("belonging", "संबद्धता", 13),
    ("intrinsic_motivation", "आंतरिक प्रेरणा", 14), ("goal_gradients", "लक्ष्य-ग्रेडिएंट", 14), ("expectancy_value", "एक्सपेक्टेंसी-वैल्यू", 14), ("self_determination", "स्व-निर्धारण", 14), ("procrastination", "टालमटोल", 14),
    ("stress_appraisal", "तनाव-मूल्यांकन", 15), ("acute_stress", "तीव्र तनाव", 15), ("recovery", "रिकवरी", 15), ("social_buffering", "सामाजिक बफ़रिंग", 15), ("stress_and_attention", "तनाव और ध्यान", 15),
    ("circadian_timing", "सर्केडियन टाइमिंग", 16), ("sleep_pressure", "स्लीप प्रेशर", 16), ("memory_and_sleep", "नींद और स्मृति", 16), ("light_and_clock", "प्रकाश और जैविक घड़ी", 16), ("sleep_regularization", "नींद नियमितता", 16),
    ("language_prediction", "भाषा-पूर्वानुमान", 17), ("bilingual_control", "द्विभाषी नियंत्रण", 17), ("metaphor", "रूपक", 17), ("narrative_identity", "कथा और पहचान", 17), ("inner_speech_language", "आंतरिक भाषा", 17),
    ("stoic_practice", "स्टोइक अभ्यास", 18), ("meaning_and_wellbeing", "अर्थ और कल्याण", 18), ("free_will", "स्वतंत्र इच्छा", 18), ("virtue_ethics", "सद्गुण नैतिकता", 18), ("self_and_personhood", "स्व और व्यक्तित्व", 18),
    ("spiritual_experience", "आध्यात्मिक अनुभव", 19), ("ritual_and_attention", "अनुष्ठान और ध्यान", 19), ("non_attachment", "अनासक्ति", 19), ("compassion_and_service", "करुणा और सेवा", 19), ("science_and_belief", "विज्ञान और विश्वास", 19),
]

ANGLES = [
    ("what_studies_measure", "अध्ययन वास्तव में क्या मापते हैं"),
    ("common_misunderstanding", "लोकप्रिय गलतफहमी बनाम प्रमाण"),
    ("one_experiment", "एक प्रयोग को सरल भाषा में पढ़ना"),
    ("how_context_changes", "संदर्भ बदलने पर निष्कर्ष कैसे बदलता है"),
    ("correlation_vs_causation", "सहसंबंध और कारण में अंतर"),
    ("brain_and_behavior_link", "मस्तिष्क और व्यवहार का सावधान संबंध"),
    ("everyday_example", "रोज़मर्रा के उदाहरण से समझना"),
    ("limits_of_evidence", "प्रमाण की सीमाएँ"),
    ("replication_question", "दोहराव और विश्वसनीयता का सवाल"),
    ("measurement_problem", "मापन की चुनौती"),
    ("individual_differences", "व्यक्तिगत अंतर क्यों मायने रखते हैं"),
    ("developmental_view", "विकास के नज़रिए से समझना"),
    ("cross_cultural_view", "संस्कृतियों के बीच अंतर"),
    ("short_term_long_term", "कम और लंबी अवधि के प्रभाव अलग करना"),
    ("dose_timing_context", "समय और तीव्रता की भूमिका"),
    ("theory_vs_finding", "सिद्धांत और निष्कर्ष में फर्क"),
    ("expert_disagreement", "विशेषज्ञ असहमति को समझना"),
    ("philosophy_boundary", "दर्शन कहाँ शुरू होता है"),
    ("spiritual_claim_boundary", "आध्यात्मिक दावे की सीमा"),
    ("ethical_question", "नैतिक प्रश्न"),
    ("history_of_idea", "विचार का संक्षिप्त इतिहास"),
    ("replication_and_nulls", "नकारात्मक परिणाम भी क्यों ज़रूरी हैं"),
    ("language_and_translation", "भाषा में अनुवाद की सावधानी"),
    ("visual_metaphor", "एक वैज्ञानिक रूपक की जाँच"),
    ("how_to_read_headline", "वैज्ञानिक हेडलाइन कैसे पढ़ें"),
    ("study_design", "अध्ययन-डिज़ाइन का असर"),
    ("alternative_explanations", "वैकल्पिक व्याख्याएँ"),
    ("practical_observation", "बिना इलाज-दावे के आत्म-अवलोकन"),
    ("balanced_takeaway", "संतुलित निष्कर्ष"),
    ("open_question", "अभी कौन-सा सवाल खुला है"),
]


def now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def make_item(number: int) -> dict[str, Any]:
    if number == 1:
        return {
            "reel_id": "reel_0001_affect_labeling",
            "sequence": 1,
            "batch": "Batch_001",
            "topic": "भावना को नाम देने का असर संदर्भ और तीव्रता पर क्यों निर्भर हो सकता है",
            "topic_key": "affect_labeling_context_timing_intensity",
            "pillar": "emotions",
            "pillar_hi": "भावनाएँ",
            "unique_angle": "एक उपयोगी अभ्यास को सार्वभौमिक इलाज न समझना",
            "angle_key": "context_timing_not_guarantee",
            "evidence_class": "peer_reviewed_primary_plus_secondary",
            "safety_status": "SAFE_WITH_EDITS",
            "production_stage": "final",
            "research_stage": "verified",
            "source_ids": ["PMID:17576282", "DOI:10.3389/fpsyg.2014.00221", "DOI:10.1371/journal.pone.0279303", "DOI:10.1186/s40359-024-02103-y"],
            "drive_path": "3000_HINDI_RESEARCH_REELS/Batch_001/Reel_0001",
            "required_assets": ["mp4", "wav", "srt", "metadata.json", "sources.md", "script.md", "visual_reference.png"],
            "asset_checksums": {"mp4": "bef8f13e55c13cd14288584a1ed3d65833b7df033a62e96d65b94aeea7782dc4"},
            "qc": {"aspect_ratio_9_16": True, "duration_seconds": 55.2, "hindi_audio": True, "captions": True, "decode_ok": True, "ai_disclosure": True, "drive_verified": True},
            "retries": 0,
            "failure_count": 0,
            "notes": "Completed and Drive-upload verified; not published.",
        }
    anchor_key, anchor_hi, pillar_index = ANCHORS[(number - 2) % len(ANCHORS)]
    angle_index = ((number - 2) // len(ANCHORS)) % len(ANGLES)
    angle_key, angle_hi = ANGLES[angle_index]
    pillar_key, pillar_hi = PILLARS[pillar_index]
    batch = ((number - 1) // 30) + 1
    return {
        "reel_id": f"reel_{number:04d}_{anchor_key}_{angle_key}",
        "sequence": number,
        "batch": f"Batch_{batch:03d}",
        "topic": f"{anchor_hi}: {angle_hi}",
        "topic_key": anchor_key,
        "pillar": pillar_key,
        "pillar_hi": pillar_hi,
        "unique_angle": angle_hi,
        "angle_key": angle_key,
        "evidence_class": "research_pending",
        "safety_status": "REVIEW_REQUIRED",
        "production_stage": "planned",
        "research_stage": "pending",
        "source_ids": [],
        "drive_path": f"3000_HINDI_RESEARCH_REELS/Batch_{batch:03d}/Reel_{number:04d}",
        "required_assets": ["mp4", "wav", "srt", "metadata.json", "sources.md", "script.md", "visual_reference.png"],
        "asset_checksums": {},
        "qc": {"aspect_ratio_9_16": False, "duration_seconds": None, "hindi_audio": False, "captions": False, "decode_ok": False, "ai_disclosure": False, "drive_verified": False},
        "retries": 0,
        "failure_count": 0,
        "notes": "Planning record only. Research and safety review are mandatory before production.",
    }


def checkpoint(items: list[dict[str, Any]]) -> dict[str, Any]:
    counts: dict[str, int] = {}
    for item in items:
        stage = item["production_stage"]
        counts[stage] = counts.get(stage, 0) + 1
    complete = [i for i in items if i["production_stage"] == "final" and i["qc"].get("drive_verified")]
    next_item = next((i for i in items if i["production_stage"] not in {"final", "rejected"}), None)
    return {
        "schema_version": 1,
        "mission": "3000 unique Hindi research reels",
        "total_reels": len(items),
        "total_batches": 100,
        "reels_per_batch": 30,
        "generated_at": now(),
        "updated_at": now(),
        "production_counts": counts,
        "completed_drive_verified": len(complete),
        "next_reel": next_item["reel_id"] if next_item else None,
        "next_sequence": next_item["sequence"] if next_item else None,
        "last_completed": complete[-1]["reel_id"] if complete else None,
        "failure_log": [],
        "rules": {
            "one_complete_reel_at_a_time": True,
            "no_silent_skips": True,
            "research_before_script": True,
            "source_reuse_requires_new_angle": True,
            "publication_requires_separate_verification": True,
            "ai_disclosure_required": True,
        },
    }


def write_queue(force: bool) -> None:
    if (QUEUE.exists() or CHECKPOINT.exists()) and not force:
        raise SystemExit("Queue/checkpoint already exists; use --force only after reviewing the current state.")
    QUEUE.parent.mkdir(parents=True, exist_ok=True)
    items = [make_item(n) for n in range(1, 3001)]
    keys = [i["reel_id"] for i in items]
    if len(keys) != len(set(keys)):
        raise SystemExit("Duplicate reel_id generated")
    QUEUE.write_text("".join(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n" for item in items), encoding="utf-8")
    CHECKPOINT.write_text(json.dumps(checkpoint(items), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"queue": str(QUEUE), "checkpoint": str(CHECKPOINT), "items": len(items), "sha256": hashlib.sha256(QUEUE.read_bytes()).hexdigest()}, ensure_ascii=False, indent=2))


def validate() -> int:
    if not QUEUE.exists() or not CHECKPOINT.exists():
        print("missing queue or checkpoint")
        return 1
    items = [json.loads(line) for line in QUEUE.read_text(encoding="utf-8").splitlines() if line.strip()]
    problems: list[str] = []
    if len(items) != 3000:
        problems.append(f"expected 3000 items, got {len(items)}")
    ids = [i.get("reel_id") for i in items]
    if len(ids) != len(set(ids)):
        problems.append("duplicate reel_id")
    sequences = [i.get("sequence") for i in items]
    if sequences != list(range(1, 3001)):
        problems.append("sequence is not exactly 1..3000")
    for i, item in enumerate(items, 1):
        expected_batch = f"Batch_{((i - 1) // 30) + 1:03d}"
        if item.get("batch") != expected_batch:
            problems.append(f"sequence {i} has wrong batch")
        if i > 1 and item.get("production_stage") != "planned":
            problems.append(f"sequence {i} unexpectedly marked complete/non-planned")
    cp = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
    if cp.get("total_reels") != 3000 or cp.get("completed_drive_verified") != 1:
        problems.append("checkpoint totals do not preserve Reel 0001 completion")
    if problems:
        print(json.dumps({"valid": False, "problems": problems}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"valid": True, "items": len(items), "batches": 100, "completed_drive_verified": cp["completed_drive_verified"], "next_sequence": cp["next_sequence"]}, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["create", "validate"])
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if args.command == "create":
        write_queue(args.force)
        return validate()
    return validate()


if __name__ == "__main__":
    raise SystemExit(main())
