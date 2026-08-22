#!/usr/bin/env python3
"""Deterministic technical and safety preflight for one Hindi research reel.

The checker does not judge the truth of research claims. It verifies that the
required source record exists and that the asset package contains explicit
caveats, captions, audio, and AI disclosure before Drive upload.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

DANGEROUS_CLAIM_PATTERNS = [
    re.compile(r"\b100\s*%\b"),
    re.compile(r"\bguarantee(?:d|s)?\b", re.I),
    re.compile(r"\bguaranteed\b", re.I),
    re.compile(r"\bmiracle\b", re.I),
    re.compile(r"\bmagic(?:al)?\s+(?:button|cure|fix)\b", re.I),
    re.compile(r"\b(?:cure|treat|diagnos(?:e|is)|medication|prescription)\b", re.I),
    re.compile(r"(?:इलाज|गारंटी|जादुई|निदान|दवा)"),
]
NEGATION_MARKERS = ("not", "no", "without", "not a", "not an", "do not", "don't", "rather than", "instead of", "नहीं", "नही", "बिना", "न करें", "दावा नहीं", "न समझें", "न मानें", "न समझना", "न कि", "बजाय")


def probe(path: Path) -> dict[str, Any]:
    cmd = ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def parse_srt(path: Path) -> tuple[list[tuple[float, float]], list[str]]:
    text = path.read_text(encoding="utf-8-sig")
    blocks = re.split(r"\n\s*\n", text.strip()) if text.strip() else []
    cues: list[tuple[float, float]] = []
    problems: list[str] = []

    def seconds(value: str) -> float:
        h, m, rest = value.split(":")
        s, ms = rest.split(",")
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

    for index, block in enumerate(blocks, 1):
        lines = block.splitlines()
        if len(lines) < 3:
            problems.append(f"caption block {index} is incomplete")
            continue
        match = re.match(r"^(\d{2}:\d{2}:\d{2},\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2},\d{3})", lines[1].strip())
        if not match:
            problems.append(f"caption block {index} has invalid timing")
            continue
        start, end = seconds(match.group(1)), seconds(match.group(2))
        if end <= start:
            problems.append(f"caption block {index} ends before it starts")
        cues.append((start, end))
    for previous, current in zip(cues, cues[1:]):
        if current[0] < previous[0]:
            problems.append("caption cues are not chronological")
    return cues, problems


def claim_scan(text: str) -> list[str]:
    problems: list[str] = []
    for line_number, line in enumerate(text.splitlines(), 1):
        lowered = line.lower()
        for pattern in DANGEROUS_CLAIM_PATTERNS:
            if pattern.search(line) and not any(marker in lowered or marker in line for marker in NEGATION_MARKERS):
                problems.append(f"possible unsupported treatment/guarantee wording at line {line_number}")
                break
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="QC a single Hindi research reel package")
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--audio", type=Path, required=True)
    parser.add_argument("--captions", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--sources", type=Path, required=True)
    parser.add_argument("--script", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    problems: list[str] = []
    required = [args.video, args.audio, args.captions, args.metadata, args.sources, args.script]
    for path in required:
        if not path.exists() or path.stat().st_size == 0:
            problems.append(f"missing or empty: {path}")

    metadata: dict[str, Any] = {}
    report: dict[str, Any] = {"video": str(args.video), "checks": {}, "problems": problems}
    if not problems:
        try:
            metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            problems.append(f"metadata is not valid JSON: {exc}")
        try:
            info = probe(args.video)
            streams = info.get("streams", [])
            video = next((s for s in streams if s.get("codec_type") == "video"), None)
            audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
            if not video:
                problems.append("video stream missing")
            else:
                width, height = int(video.get("width", 0)), int(video.get("height", 0))
                duration = float(video.get("duration") or info.get("format", {}).get("duration") or 0)
                ratio_ok = width * 16 == height * 9
                duration_ok = 45.0 <= duration <= 75.0
                report["checks"].update({"width": width, "height": height, "duration_seconds": round(duration, 3), "aspect_ratio_9_16": ratio_ok, "duration_45_to_75": duration_ok})
                if not ratio_ok:
                    problems.append(f"video is not 9:16: {width}x{height}")
                if not duration_ok:
                    problems.append(f"video duration outside 45–75 seconds: {duration:.3f}")
            if not audio:
                problems.append("audio stream missing")
            else:
                report["checks"]["audio_stream"] = {"codec": audio.get("codec_name"), "sample_rate": audio.get("sample_rate"), "channels": audio.get("channels")}
        except (subprocess.CalledProcessError, json.JSONDecodeError, ValueError) as exc:
            problems.append(f"ffprobe failed: {exc}")

        cues, caption_problems = parse_srt(args.captions)
        problems.extend(caption_problems)
        duration = float(report["checks"].get("duration_seconds", 0))
        if not cues:
            problems.append("captions contain no valid cues")
        if duration and cues and max(end for _, end in cues) > duration + 0.5:
            problems.append("caption timing extends beyond video duration")
        report["checks"]["caption_cues"] = len(cues)
        report["checks"]["caption_timing_ok"] = not caption_problems and bool(cues)

        source_text = args.sources.read_text(encoding="utf-8", errors="replace")
        script_text = args.script.read_text(encoding="utf-8", errors="replace")
        source_ids = metadata.get("source_ids") or metadata.get("sources") or []
        disclosure = metadata.get("ai_content_disclosure")
        if not source_ids:
            problems.append("metadata has no source IDs/records")
        if not disclosure or not str(disclosure).strip():
            problems.append("AI-content disclosure missing")
        if not re.search(r"(?:doi\.org|PMID|pubmed|https?://)", source_text, re.I):
            problems.append("sources file has no recognizable citation URL/identifier")
        problems.extend(claim_scan(script_text))
        report["checks"].update({"source_records": len(source_ids) if isinstance(source_ids, list) else 1, "source_identifier_present": bool(re.search(r"(?:doi\.org|PMID|pubmed|https?://)", source_text, re.I)), "ai_disclosure_present": bool(disclosure), "safety_wording_ok": not any("unsupported treatment/guarantee" in p for p in problems)})

    report["valid"] = not problems
    report["problems"] = problems
    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    print(output, end="")
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
