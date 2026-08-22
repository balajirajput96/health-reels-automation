from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state"
QUEUE = STATE / "reels_3000_queue.jsonl"
CHECKPOINT = STATE / "reels_3000_checkpoint.json"
LEDGER = STATE / "reels_ledger.json"
RECORD = ROOT / "records" / "reels" / "batch01" / "reel0004"
EVIDENCE_REF = os.environ.get("EVIDENCE_REF", "remote_reverification_20260822T1442Z")
EVIDENCE = RECORD / EVIDENCE_REF
TARGET = "reel_0004_cognitive_biases_what_studies_measure"
FOLDER_ID = "1dL1yz1Lx3tnT9ali6nujGLHvmAbJLwIa"
REMOTE_METADATA_ID = "1MypkEiQmIcVdcddM6cx5oqoHlIzS-upw"
REMOTE_MANIFEST_ID = "1MZiWUSiqjQuT3L_tkXWrNA-OhZVZ6af5"
REMOTE_QC_ID = "1ZyRn1M-IIuxkcjpn6ORO28rbjKf9ObIb"
REMOTE_VIDEO_ID = "1RFDW_qFKbNETKUZGNcEE3NGoDTI683AZ"
CANONICAL_PATH = "3000_HINDI_RESEARCH_REELS/Batch_001/Reel_0004"


def now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_write(path: Path, text: str) -> None:
    fd, temp_name = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def main() -> int:
    required = [
        EVIDENCE / "folder_metadata.json",
        EVIDENCE / "child_listing.json",
        EVIDENCE / "remote_metadata_stdout.json",
        EVIDENCE / "remote_qc_report_stdout.json",
        EVIDENCE / "remote_drive_upload_manifest_fresh.json",
    ]
    missing = [str(path) for path in required if not path.is_file() or path.stat().st_size == 0]
    if missing:
        raise RuntimeError("Missing fresh authenticated evidence; refusing state mutation: " + ", ".join(missing))

    queue_entries = [json.loads(line) for line in QUEUE.read_text(encoding="utf-8").splitlines() if line.strip()]
    matches = [entry for entry in queue_entries if entry.get("reel_id") == TARGET]
    if len(matches) != 1:
        raise RuntimeError(f"Expected exactly one queue entry for {TARGET}, found {len(matches)}")
    checkpoint = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
    if checkpoint.get("next_reel") != TARGET or checkpoint.get("next_sequence") != 4:
        raise RuntimeError("Checkpoint no longer points to Reel_0004; refusing state mutation")

    folder = json.loads((EVIDENCE / "folder_metadata.json").read_text(encoding="utf-8"))
    listing = json.loads((EVIDENCE / "child_listing.json").read_text(encoding="utf-8"))
    metadata = json.loads((EVIDENCE / "remote_metadata_stdout.json").read_text(encoding="utf-8"))
    remote_qc = json.loads((EVIDENCE / "remote_qc_report_stdout.json").read_text(encoding="utf-8"))
    manifest = json.loads((EVIDENCE / "remote_drive_upload_manifest_fresh.json").read_text(encoding="utf-8"))

    if folder.get("id") != FOLDER_ID or folder.get("name") != "Reel_0004" or folder.get("trashed") is not False:
        raise RuntimeError("Fresh folder identity is not the expected canonical Reel_0004 folder")
    if metadata.get("reel_id") != TARGET:
        raise RuntimeError("Fresh remote metadata is not for the queued Reel_0004 identity")
    if manifest.get("drive_path") != CANONICAL_PATH or manifest.get("drive_folder_id") != FOLDER_ID:
        raise RuntimeError("Fresh remote manifest does not match the canonical path")
    if remote_qc.get("valid") is not True:
        raise RuntimeError("Fresh remote QC is not valid; refusing to record a blocker")

    names = {item.get("name") for item in listing.get("files", []) if item.get("trashed") is False}
    queued_names = {
        "reel_0004_cognitive_biases_what_studies_measure_hi.mp4",
        "reel_0004_cognitive_biases_what_studies_measure_narration_hi.wav",
        "reel_0004_cognitive_biases_what_studies_measure_captions_hi.srt",
        "reel_0004_metadata.json",
        "reel_0004_qc_report.json",
        "reel_0004_drive_upload_manifest.json",
        "reel_0004_cognitive_biases_what_studies_measure_script.md",
        "reel_0004_cognitive_biases_what_studies_measure_sources.md",
    }
    if not queued_names.issubset(names):
        raise RuntimeError("Fresh authenticated child listing lacks required queued-topic artifacts")
    conflicting_names = {
        "REEL-0004_qc.json",
        "REEL-0004_reel.mp4",
        "REEL-0004_script_hi.md",
        "REEL-0004_research.md",
    }
    if not conflicting_names.issubset(names):
        raise RuntimeError("Fresh listing no longer proves the prior conflicting package is present")

    manifest_entry = next((item for item in manifest.get("files", []) if item.get("name") == "reel_0004_metadata.json"), None)
    if manifest_entry is None:
        raise RuntimeError("Fresh Drive manifest lacks reel_0004_metadata.json")
    observed_metadata_sha = sha256(EVIDENCE / "remote_metadata_stdout.json")
    expected_metadata_sha = manifest_entry.get("local_sha256")
    if observed_metadata_sha == expected_metadata_sha:
        raise RuntimeError("Metadata integrity mismatch disappeared; use a success reconciler instead")

    existing_failures = checkpoint.setdefault("failure_log", [])
    if any(item.get("evidence_ref") == EVIDENCE_REF and item.get("stage") == "remote_package_integrity_and_canonical_ambiguity" for item in existing_failures):
        print(json.dumps({"status": "already_recorded", "reel_id": TARGET, "evidence_ref": EVIDENCE_REF}, ensure_ascii=False))
        return 0

    for path in (QUEUE, CHECKPOINT, LEDGER):
        backup = EVIDENCE / f"pre_current_reverification_{path.name}"
        if not backup.exists():
            shutil.copy2(path, backup)

    target = matches[0]
    target["failure_count"] = int(target.get("failure_count", 0)) + 1
    target["retries"] = int(target.get("retries", 0)) + 1
    target.setdefault("qc", {})["drive_verified"] = False
    target["production_stage"] = "planned"
    target["research_stage"] = "verified"
    target["notes"] = (
        "Fresh authenticated Drive re-verification found the queued-topic package in the canonical folder, but the folder still retains a prior verified different-topic package. "
        "The queued package's remote QC is valid, yet the downloaded remote metadata SHA-256 does not match the Drive upload manifest's recorded local SHA-256 "
        f"(expected {expected_metadata_sha}, observed {observed_metadata_sha}). No upload, overwrite, duplicate folder/file, or publication performed."
    )

    recorded_at = now()
    failure = {
        "reel_id": TARGET,
        "stage": "remote_package_integrity_and_canonical_ambiguity",
        "status": "blocked_retryable",
        "exact_error": (
            f"Fresh authenticated Drive listing at {EVIDENCE_REF} shows canonical path {CANONICAL_PATH} in folder {FOLDER_ID} with both the prior verified package "
            f"(REEL-0004_qc.json, tuple MND-L01-Q04) and the queued-topic package ({REMOTE_VIDEO_ID}, {REMOTE_METADATA_ID}, {REMOTE_MANIFEST_ID}, {REMOTE_QC_ID}). "
            f"The queued-topic remote QC is valid and metadata reel_id is {TARGET}, but the downloaded remote metadata SHA-256 {observed_metadata_sha} differs from the manifest local_sha256 {expected_metadata_sha}. "
            "Because the canonical folder is identity-ambiguous and the manifest integrity record does not match the authenticated remote metadata bytes, final Drive verification was refused."
        ),
        "retry_state": "keep next_reel at reel_0004; re-verify after canonical-folder cleanup/identity resolution and a manifest-consistent metadata artifact; do not upload, overwrite, or publish",
        "local_qc": "remote_qc_valid_and_prior_independent_ffprobe_passed; manifest_metadata_hash_mismatch",
        "remote_identity": {
            "folder_id": FOLDER_ID,
            "queued_topic_manifest_id": REMOTE_MANIFEST_ID,
            "queued_topic_metadata_id": REMOTE_METADATA_ID,
            "queued_topic_qc_id": REMOTE_QC_ID,
            "queued_topic_video_id": REMOTE_VIDEO_ID,
            "queued_topic_reel_id": TARGET,
            "prior_conflicting_package_present": True,
            "fresh_child_count": len(listing.get("files", [])),
            "evidence_ref": EVIDENCE_REF,
        },
        "manifest_integrity": {
            "asset": "reel_0004_metadata.json",
            "expected_local_sha256": expected_metadata_sha,
            "observed_remote_sha256": observed_metadata_sha,
        },
        "evidence_ref": EVIDENCE_REF,
        "recorded_at": recorded_at,
    }
    existing_failures.append(failure)
    checkpoint.update({
        "next_reel": TARGET,
        "next_sequence": 4,
        "last_completed": "reel_0003_self_concept_what_studies_measure",
        "completed_drive_verified": 3,
        "production_counts": {"final": 3, "planned": 2997},
        "updated_at": recorded_at,
    })

    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    ledger_matches = [item for item in ledger.get("items", []) if item.get("filename") == "reel_0004_cognitive_biases_what_studies_measure.mp4"]
    if len(ledger_matches) != 1:
        raise RuntimeError(f"Expected one Reel_0004 ledger identity, found {len(ledger_matches)}")
    ledger_matches[0]["stage"] = "failed"
    ledger_matches[0]["notes"] = (
        "Fresh authenticated Drive listing confirms the queued-topic package remains in the canonical folder, but the folder retains a prior different-topic package and the authenticated remote metadata SHA-256 "
        f"({observed_metadata_sha}) differs from the upload manifest record ({expected_metadata_sha}). Final status withheld; no upload, overwrite, duplicate, or publication. Evidence: records/reels/batch01/reel0004/{EVIDENCE_REF}/."
    )

    atomic_write(QUEUE, "".join(json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n" for entry in queue_entries))
    atomic_write(CHECKPOINT, json.dumps(checkpoint, ensure_ascii=False, indent=2) + "\n")
    atomic_write(LEDGER, json.dumps(ledger, ensure_ascii=False, indent=2) + "\n")
    (EVIDENCE / "integrity_and_canonical_ambiguity_blocker.md").write_text(
        "# Reel_0004 remote integrity and canonical-identity blocker\n\n"
        f"- Recorded at: {recorded_at}\n"
        f"- Evidence: `{EVIDENCE_REF}`\n"
        f"- Canonical path: `{CANONICAL_PATH}`\n"
        f"- Folder ID: `{FOLDER_ID}`\n"
        f"- Queued identity: `{TARGET}`\n"
        f"- Fresh authenticated child listing count: `{len(listing.get('files', []))}` non-trashed package entries include the queued-topic package and the prior `REEL-0004_*` package.\n"
        f"- Manifest metadata SHA-256: `{expected_metadata_sha}`\n"
        f"- Authenticated remote metadata SHA-256: `{observed_metadata_sha}`\n"
        "- Remote QC is valid and prior independent media QC passed, but the integrity mismatch and canonical-folder ambiguity make final Drive verification unsafe.\n"
        "- Safe action: preserve all remote files, do not upload, overwrite, create a duplicate folder/file, advance the queue, or publish.\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": "blocked_retryable", "reel_id": TARGET, "evidence_ref": EVIDENCE_REF, "expected_metadata_sha": expected_metadata_sha, "observed_metadata_sha": observed_metadata_sha}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# end
