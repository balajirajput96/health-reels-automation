#!/usr/bin/env python3
"""Build the controlled Batch 50 Reel backlog from validated research artifacts."""
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

ROOT = Path("/home/ubuntu/reels_ops")
CANDIDATE = ROOT / "research/2026-08-19__batch50__candidate-reel-briefs.csv"
REVIEWED = ROOT / "research/2026-08-19__batch50__safety-reviewed-production-briefs.csv"
OUTPUT = ROOT / "drafts/2026-08-19__batch50__controlled-production-backlog.md"


def clean(value: str | None) -> str:
    return (value or "").replace("\n", " ").replace("|", "/").strip()


def main() -> None:
    with CANDIDATE.open(encoding="utf-8", newline="") as handle:
        candidates = list(csv.DictReader(handle))
    with REVIEWED.open(encoding="utf-8", newline="") as handle:
        reviewed = list(csv.DictReader(handle))

    rows = []
    for index, reviewed_row in enumerate(reviewed):
        candidate = candidates[index] if index < len(candidates) else {}
        subject = candidate.get("Subject", reviewed_row["Subject"])
        priority = candidate.get("Production Priority", "")
        rows.append((int(priority) if str(priority).isdigit() else 999, subject, candidate, reviewed_row))
    rows.sort(key=lambda item: (item[0], item[1]))

    safe_as_is = sum(row[3]["Quality Status"] == "SAFE_AS_IS" for row in rows)
    safe_with_edits = sum(row[3]["Quality Status"] == "SAFE_WITH_EDITS" for row in rows)
    holds = sum(row[3]["Quality Status"] == "HOLD" for row in rows)

    lines = [
        "# Batch 50 — Controlled Health-Education Reel Backlog",
        "",
        f"**Created:** {date.today().isoformat()}  ",
        "**Target account:** `@balajirajput96` only.  ",
        "**Release rule:** Produce and validate one complete 60-second Reel at a time; never upload isolated clips or mass-release content.  ",
        "**Publication rule:** Use only the official Instagram workflow, confirm the active target account, enable AI-content disclosure, and record the verified post ID and URL after publication.",
        "",
        "## Safety gate summary",
        "",
        "| Status | Count | Operational treatment |",
        "|---|---:|---|",
        f"| SAFE_AS_IS | {safe_as_is} | Eligible for individual final source check and production planning. |",
        f"| SAFE_WITH_EDITS | {safe_with_edits} | Eligible only with the reviewed, narrowed claim and safety boundary. |",
        f"| HOLD | {holds} | Excluded from production until independently resolved. |",
        "",
        "## Backlog ledger",
        "",
        "| Queue | Topic | Pillar | Safety status | Required production treatment |",
        "|---:|---|---|---|---|",
    ]

    for sequence, (priority, subject, candidate, review) in enumerate(rows, start=1):
        treatment = "Use reviewed script as-is after final source check." if review["Quality Status"] == "SAFE_AS_IS" else "Use only the reviewed narrowed script and disclaimer."
        if review["Quality Status"] == "HOLD":
            treatment = "Do not produce or publish; revisit only with stronger source validation."
        title = clean(review["Final Title"])
        pillar = clean(candidate.get("Content Pillar", "Unclassified"))
        lines.append(
            f"| {sequence} | {title} | {pillar} | {clean(review['Quality Status'])} | {treatment} |"
        )

    lines += [
        "",
        "## Shared production boundaries",
        "",
        "All scripts must remain general public education in Hinglish. They must avoid diagnoses, treatment claims, outcome guarantees, fixed personal targets, and personalized advice. Every finished Reel requires actual narration, source-derived visuals and cover, audio-faithful subtitles if subtitles are used, technical validation, a neutral caption, an AI-content label, duplicate checks, and an individual official share confirmation before public publication.",
        "",
        "## Source artifacts",
        "",
        "The supporting candidate research, independently validated scripts, and safety-review data are stored in the companion CSV and JSON files under `reels_ops/research/`.",
        "",
    ]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT} with {len(rows)} backlog entries")


if __name__ == "__main__":
    main()
