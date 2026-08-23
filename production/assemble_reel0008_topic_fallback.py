#!/usr/bin/env python3
"""Assemble Reel 0008 from quota-permitted topic-specific visuals.

This is a resumable, clearly labeled fallback: one native AI clip plus five
AI-generated meal-timing/circadian reference images animated deterministically.
The output remains non-publishable until Drive verification and editorial review.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "production" / "assets"
VIDEO = ROOT / "production" / "video"
AUDIO = ROOT / "production" / "audio"
CAPTIONS = ROOT / "production" / "captions" / "REEL-0008_hi-IN.srt"
RENDERED = ROOT / "production" / "rendered"
WORK = ROOT / "production" / "assembly_work" / "reel0008"
OUT = RENDERED / "REEL-0008_quota_limited_topic_fallback.mp4"
AUDIO_OUT = AUDIO / "REEL-0008_narration_hi-IN.wav"

SPAN_DURATIONS = [9.0, 8.4, 8.72, 7.0, 9.2, 10.88, 11.68]
NATIVE_CLIP = VIDEO / "reel0008_clip01_morning_meal_timing.mp4"
IMAGE_PATHS = [
    ASSETS / "reel0008_meal_timing_primary_reference_20260823.png",
    ASSETS / "reel0008_ref02_circadian_dial_20260823.png",
    ASSETS / "reel0008_ref03_controlled_study_20260823.png",
    ASSETS / "reel0008_ref04_no_perfect_time_20260823.png",
    ASSETS / "reel0008_ref05_review_uncertainty_20260823.png",
    ASSETS / "reel0008_ref06_practical_cues_20260823.png",
]


def run(args: list[str]) -> None:
    subprocess.run(args, check=True)


def make_still_segment(image: Path, duration: float, output: Path, zoom_direction: str) -> None:
    zoom = "min(zoom+0.0007,1.035)" if zoom_direction == "in" else "max(zoom-0.0005,1.0)"
    vf = (
        "scale=720:1280:force_original_aspect_ratio=increase,"
        "crop=720:1280,"
        f"zoompan=z='{zoom}':d=1:s=720x1280:fps=30,format=yuv420p"
    )
    run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(image), "-t", f"{duration:.3f}",
        "-vf", vf, "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-r", "30", "-pix_fmt", "yuv420p", str(output),
    ])


def main() -> int:
    for path in [NATIVE_CLIP, *IMAGE_PATHS, CAPTIONS, AUDIO / "REEL-0007_narration_hi-IN.wav"]:
        if not path.is_file():
            raise SystemExit(f"missing required input: {path}")
    WORK.mkdir(parents=True, exist_ok=True)
    RENDERED.mkdir(parents=True, exist_ok=True)
    AUDIO_OUT.parent.mkdir(parents=True, exist_ok=True)
    if not AUDIO_OUT.exists():
        shutil.copy2(AUDIO / "REEL-0007_narration_hi-IN.wav", AUDIO_OUT)

    native = WORK / "segment_01_native.mp4"
    run([
        "ffmpeg", "-y", "-i", str(NATIVE_CLIP), "-t", f"{SPAN_DURATIONS[0]:.3f}",
        "-vf", "fps=30,tpad=stop_mode=clone:stop_duration=1,format=yuv420p",
        "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-r", "30",
        "-pix_fmt", "yuv420p", str(native),
    ])

    segments = [native]
    for index, (image, duration) in enumerate(zip(IMAGE_PATHS[1:], SPAN_DURATIONS[1:]), start=2):
        segment = WORK / f"segment_{index:02d}_still.mp4"
        make_still_segment(image, duration, segment, "in" if index % 2 == 0 else "out")
        segments.append(segment)

    concat_list = WORK / "concat.txt"
    concat_list.write_text("".join(f"file '{segment.as_posix()}'\n" for segment in segments), encoding="utf-8")
    concat_video = WORK / "concat_video.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list), "-c", "copy", str(concat_video)])

    subtitle_filter = (
        f"subtitles={CAPTIONS.as_posix()}:"
        "force_style='FontName=Noto Sans Devanagari,FontSize=24,Outline=2,Shadow=0,MarginV=72,Alignment=2'"
    )
    total_duration = sum(SPAN_DURATIONS)
    run([
        "ffmpeg", "-y", "-i", str(concat_video), "-i", str(AUDIO_OUT),
        "-map", "0:v:0", "-map", "1:a:0", "-vf", subtitle_filter,
        "-t", f"{total_duration:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-r", "30", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
        "-ar", "48000", "-ac", "2", "-movflags", "+faststart", str(OUT),
    ])

    metadata = {
        "reel_id": "REEL-0008",
        "output": str(OUT.relative_to(ROOT)),
        "production_mode": "quota_limited_topic_specific_fallback",
        "visual_provenance": {
            "native_ai_clip": str(NATIVE_CLIP.relative_to(ROOT)),
            "ai_reference_images": [str(path.relative_to(ROOT)) for path in IMAGE_PATHS],
            "deterministic_motion": "Ken Burns-style zoom/pan animation applied only to topic-specific AI reference images",
        },
        "audio": str(AUDIO_OUT.relative_to(ROOT)),
        "captions": str(CAPTIONS.relative_to(ROOT)),
        "target_duration_seconds": total_duration,
        "publication_allowed": False,
        "drive_verified": False,
        "full_qc_required": True,
        "note": "Topic-specific AI visuals were available after quota reset, but only one native video clip was permitted by the daily video quota. Requires explicit editorial re-review before any Drive completion or publication.",
    }
    (RENDERED / "REEL-0008_quota_limited_fallback_assembly.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(metadata, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
