from __future__ import annotations

import json
import shutil
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state"
QUEUE = STATE / "reels_3000_queue.jsonl"
CHECKPOINT = STATE / "reels_3000_checkpoint.json"
LEDGER = STATE / "reels_ledger.json"
RECORD = ROOT / "records" / "reels" / "batch01" / "reel0004"
TARGET = "reel_0004_cognitive_biases_what_studies_measure"
EVIDENCE_REF = "remote_reverification_20260822T0937Z"
FOLDER_ID = "1dL1yz1Lx3tnT9ali6nujGLHvmAbJLwIa"
REMOTE_QC_ID = "1s7pb4eDrEXozxDct22V7bSDHYQWOrhy7"


def now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def atomic_write(path: Path, text: str) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def main() -> None:
    evidence_dir = RECORD / EVIDENCE_REF
    required_evidence = [
        evidence_dir / "folder_metadata.json",
        evidence_dir / "child_listing.json",
        evidence_dir / "remote_qc.json",
    ]
    if not all(path.exists() for path in required_evidence):
        raise RuntimeError("Missing authenticated remote evidence; refusing to mutate state")

    queue_entries = [json.loads(line) for line in QUEUE.read_text(encoding="utf-8").splitlines() if line.strip()]
    matches = [entry for entry in queue_entries if entry.get("reel_id") == TARGET]
    if len(matches) != 1:
        raise RuntimeError(f"Expected exactly one queue entry for {TARGET}, found {len(matches)}")
    checkpoint = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
    if checkpoint.get("next_reel") != TARGET or checkpoint.get("next_sequence") != 4:
        raise RuntimeError("Checkpoint no longer points to reel 0004; refusing to mutate state")
    if any(item.get("stage") == "canonical_path_topic_conflict_reverified" and item.get("evidence_ref") == EVIDENCE_REF for item in checkpoint.get("failure_log", [])):
        print(json.dumps({"decision": "already_recorded", "next_reel": checkpoint["next_reel"], "evidence_ref": EVIDENCE_REF}, ensure_ascii=False, indent=2))
        return

    for path in (QUEUE, CHECKPOINT, LEDGER):
        backup = RECORD / f"pre_reverification_{path.name}"
        if not backup.exists():
            shutil.copy2(path, backup)

    target = matches[0]
    target["failure_count"] = int(target.get("failure_count", 0)) + 1
    target["retries"] = int(target.get("retries", 0)) + 1
    target["notes"] = (
        "Local evidence, Hindi script, narration, procedural 9:16 visuals, assembly, and deterministic QC passed. "
        "Authenticated Drive re-verification confirms the canonical Reel_0004 folder is still occupied by a verified but different topic "
        "(MND-L01-Q04, Default Mode Network). A first files.download attempt returned HTTP 500 backendError; alternate authenticated "
        "files.get alt=media retrieved the script and QC content. No upload, overwrite, duplicate folder, or public posting performed."
    )
    if target.get("qc", {}).get("decode_ok") is not True or target.get("qc", {}).get("aspect_ratio_9_16") is not True:
        raise RuntimeError("Authoritative queue does not record a passed local media QC; refusing to record this state")
    target["qc"]["drive_verified"] = False
    atomic_write(QUEUE, "".join(json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n" for entry in queue_entries))

    failure = {
        "reel_id": TARGET,
        "stage": "canonical_path_topic_conflict_reverified",
        "status": "blocked_retryable",
        "exact_error": (
            f"Authenticated Drive re-verification found canonical path 3000_HINDI_RESEARCH_REELS/Batch_001/Reel_0004 at folder ID {FOLDER_ID}; "
            "remote QC file " + REMOTE_QC_ID + " reports state=verified, title=\"मन भटकता क्यों है? Default Mode Network की कहानी\", "
            "tuple=MND-L01-Q04, and all remote artifacts listed non-trashed. This conflicts with queued topic "
            "\"संज्ञानात्मक पूर्वाग्रह: अध्ययन वास्तव में क्या मापते हैं\". The initial files.download request returned HTTP 500 "
            "backendError, but alternate authenticated files.get alt=media retrieved the remote script and QC records. Upload, overwrite, "
            "and duplicate-folder creation remain refused to prevent ambiguous canonical identity."
        ),
        "retry_state": "keep next_reel at reel_0004; do not upload or overwrite; retry only after authoritative path/identity resolution",
        "local_qc": "passed",
        "remote_identity": {
            "folder_id": FOLDER_ID,
            "remote_qc_file_id": REMOTE_QC_ID,
            "remote_title": "मन भटकता क्यों है? Default Mode Network की कहानी",
            "remote_tuple": "MND-L01-Q04",
            "remote_state": "verified",
            "evidence_ref": EVIDENCE_REF,
        },
        "evidence_ref": EVIDENCE_REF,
        "recorded_at": now(),
    }
    checkpoint.setdefault("failure_log", []).append(failure)
    checkpoint["next_reel"] = TARGET
    checkpoint["next_sequence"] = 4
    checkpoint["last_completed"] = "reel_0003_self_concept_what_studies_measure"
    checkpoint["completed_drive_verified"] = 3
    checkpoint["production_counts"] = {"final": 3, "planned": 2997}
    checkpoint["updated_at"] = now()
    atomic_write(CHECKPOINT, json.dumps(checkpoint, ensure_ascii=False, indent=2) + "\n")

    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    ledger_matches = [item for item in ledger.get("items", []) if item.get("filename") == "reel_0004_cognitive_biases_what_studies_measure.mp4"]
    if len(ledger_matches) != 1:
        raise RuntimeError(f"Expected one existing reel0004 ledger identity, found {len(ledger_matches)}")
    ledger_item = ledger_matches[0]
    ledger_item["notes"] = (
        "Local QC passed, but authenticated canonical Drive path Reel_0004 remains occupied by a verified different topic "
        "(MND-L01-Q04 / Default Mode Network); upload and overwrite refused. Re-verification evidence is stored under "
        f"records/reels/batch01/reel0004/{EVIDENCE_REF}/. Initial files.download returned HTTP 500 backendError; alternate files.get "
        "retrieved the remote script and QC. No publication."
    )
    atomic_write(LEDGER, json.dumps(ledger, ensure_ascii=False, indent=2) + "\n")

    blocker_record = RECORD / f"{EVIDENCE_REF}_blocker.md"
    blocker_record.write_text(
        "# Reel 0004 re-verification blocker\n\n"
        f"- Recorded at: {failure['recorded_at']}\n"
        f"- Canonical path: `3000_HINDI_RESEARCH_REELS/Batch_001/Reel_0004`\n"
        f"- Remote folder ID: `{FOLDER_ID}`\n"
        "- Remote verified identity: `MND-L01-Q04`, `मन भटकता क्यों है? Default Mode Network की कहानी`\n"
        "- Queue identity: `reel_0004_cognitive_biases_what_studies_measure`, `संज्ञानात्मक पूर्वाग्रह: अध्ययन वास्तव में क्या मापते हैं`\n"
        "- Result: retryable blocker. The verified remote package was preserved; no upload, overwrite, duplicate, or publication occurred.\n"
        "- Retrieval note: the first authenticated `files.download` attempt returned HTTP 500 `backendError`; alternate authenticated `files.get` with `alt=media` retrieved the remote script and QC records.\n"
        "- Safe retry: retain `next_reel` at reel0004 and wait for authoritative canonical identity resolution.\n",
        encoding="utf-8",
    )
    print(json.dumps({"decision": "recorded", "next_reel": checkpoint["next_reel"], "failure": failure, "ledger_identity_reused": True}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
