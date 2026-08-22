#!/usr/bin/env python3
"""Select the next unused validated reel concept without mutating production state.

The selector is intentionally deterministic and non-secret. It compares canonical
backlog identities with the ledger's recorded titles, subjects, and reel IDs, then
writes one JSON selection plus an audit summary for a resumable workflow.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any

STOPWORDS = {
    "a", "an", "and", "as", "at", "by", "for", "from", "in", "into", "is", "of", "on", "or", "the", "to", "with",
    "your", "you", "की", "के", "का", "और", "में", "से", "पर", "को", "एक", "यह", "इस", "हो", "है",
}

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BACKLOG = ROOT / "research" / "batch50" / "validated-script-briefs.csv"
DEFAULT_LEDGER = ROOT / "state" / "reels_ledger.json"


def norm(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().casefold())


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_ledger(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
        raise ValueError("ledger must be an object containing an items list")
    return payload


def topic_tokens(value: Any) -> set[str]:
    return {
        token
        for token in re.findall(r"[\w\u0900-\u097f]+", norm(value))
        if len(token) >= 4 and token not in STOPWORDS
    }


def recorded_identities(items: list[dict[str, Any]]) -> tuple[set[str], set[str]]:
    phrases: set[str] = set()
    tokens: set[str] = set()
    for item in items:
        fields = [item.get(key, "") for key in ("id", "reel_id", "title", "subject", "canonical_title", "filename", "notes")]
        for value in fields:
            normalized = norm(value)
            if normalized:
                phrases.add(normalized)
                tokens.update(topic_tokens(value))
    return phrases, tokens


def choose(backlog: list[dict[str, str]], ledger: dict[str, Any]) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    phrases, identities = recorded_identities(ledger["items"])
    skipped: list[dict[str, Any]] = []
    for row_number, row in enumerate(backlog, start=2):
        title = row.get("Canonical Title", "").strip()
        subject = row.get("Subject", "").strip()
        keys = {norm(title), norm(subject)} - {""}
        title_tokens = topic_tokens(title)
        subject_tokens = topic_tokens(subject)
        phrase_match = any(key in phrase for phrase in phrases for key in keys if len(key) >= 12)
        token_match = len(title_tokens & identities) >= 2 or len(subject_tokens & identities) >= 2
        if phrase_match or token_match:
            skipped.append({"row": row_number, "title": title, "subject": subject, "reason": "ledger_identity_match"})
            continue
        selection = {
            "backlog_row": row_number,
            "title": title,
            "subject": subject,
            "primary_source": row.get("Primary Source", "").strip(),
            "secondary_source": row.get("Secondary Source", "").strip(),
            "evidence_summary": row.get("Evidence Summary", "").strip(),
            "narration_spans": row.get("Narration Spans", "").strip(),
            "caption": row.get("Caption", "").strip(),
            "hashtags": row.get("Hashtags", "").strip(),
            "cover_concept": row.get("Cover Concept", "").strip(),
            "safety_boundary": row.get("Safety Boundary", "").strip(),
            "status": "selected_for_research",
        }
        return selection, {"backlog_rows": len(backlog), "ledger_items": len(ledger["items"]), "skipped": skipped}
    return None, {"backlog_rows": len(backlog), "ledger_items": len(ledger["items"]), "skipped": skipped}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--backlog", type=Path, default=DEFAULT_BACKLOG)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    if not args.backlog.is_file():
        raise SystemExit(f"backlog not found: {args.backlog}")
    if not args.ledger.is_file():
        raise SystemExit(f"ledger not found: {args.ledger}")

    selection, audit = choose(load_rows(args.backlog), load_ledger(args.ledger))
    payload = {"selection": selection, "audit": audit}
    encoded = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0 if selection else 2


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["choose", "load_ledger", "load_rows"]
