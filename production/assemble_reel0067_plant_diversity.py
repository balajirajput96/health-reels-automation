#!/usr/bin/env python3
"""Assemble REEL-0067 from Hindi narration spans and two topic-specific references.

This is a deterministic, quota-aware fallback. The official image-generation limit
prevented additional companion references, so the assembly reuses the two successful
plant-diversity images with gentle Ken Burns motion. It does not claim native video
or six unique visual assets.
"""
from __future__ import annotations

import hashlib
import json
import math
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIO_DIR = ROOT / "production" / "audio"
ASSET_DIR = ROOT / "production" / "assets"
CAPTION_DIR = ROOT / "production" / "captions"
RENDER_DIR = ROOT / "production" / "rendered"
TMP_DIR = RENDER_DIR / "reel0067_tmp"

IMAGE_NAMES = [
    "reel0067_primary_plant_diversity.png",
    "reel0067_ref02_plant_food_groups.png",
]
# Keep the sequence topic-specific while reusing only the two successful references.
IMAGE_SEQUENCE = [0, 1, 0, 1, 0, 1, 1]

CAPTIONS = [
    "क्या healthy eating का मतलब सिर्फ एक perfect food है?\nनहीं—थाली की variety भी मायने रख सकती है।",
    "Plant-rich eating का मतलब vegan बनना जरूरी नहीं।\nFruits, vegetables, grains, pulses, nuts और seeds की variety शामिल की जा सकती है।",
    "अलग foods अलग nutrients देते हैं। Reviews के मुताबिक\ndietary diversity nutrient intake को support कर सकती है,\nपर यह personal prescription नहीं।",
    "Plant-rich patterns बेहतर health से associated पाए गए हैं।\nलेकिन association causation नहीं; पूरी diet, lifestyle और context\nभी मायने रखते हैं।",
    "Gut microbiome पर कुछ promising findings हैं,\nपर results contradictory भी हैं। हर व्यक्ति में एक जैसा effect साबित नहीं।",
    "अगली meal में अपनी पसंद और budget के अनुसार\nएक अलग plant food जोड़ें। कोई fixed weekly number जरूरी नहीं।",
    "यह general education है, personal diet plan नहीं।\nAllergy या medical condition हो तो qualified clinician या dietitian से सलाह लें।",
]


def run(args: list[str]) -> None:
    print("$", " ".join(args))
    subprocess.run(args, check=True)


def probe_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def hms(seconds: float) -> str:
    millis = int(round((seconds - math.floor(seconds)) * 1000))
    whole = int(math.floor(seconds))
    if millis == 1000:
        whole += 1
        millis = 0
    hours, rem = divmod(whole, 3600)
    minutes, secs = divmod(rem, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def write_srt(durations: list[float], output: Path) -> None:
    start = 0.0
    blocks: list[str] = []
    for index, (duration, text) in enumerate(zip(durations, CAPTIONS), start=1):
        end = start + duration
        blocks.append(f"{index}\n{hms(start)} --> {hms(end)}\n{{\\an2}}{text}\n")
        start = end
    output.write_text("\n".join(blocks), encoding="utf-8")


def main() -> None:
    for directory in (CAPTION_DIR, RENDER_DIR, TMP_DIR):
        directory.mkdir(parents=True, exist_ok=True)

    spans = [AUDIO_DIR / f"REEL-0067_span{index:02d}_hi-IN.wav" for index in range(1, 8)]
    images = [ASSET_DIR / name for name in IMAGE_NAMES]
    missing = [str(path) for path in spans + images if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing required local inputs:\n" + "\n".join(missing))

    durations = [probe_duration(path) for path in spans]
    total_audio = sum(durations)
    if not 55.0 <= total_audio <= 75.0:
        raise RuntimeError(f"Narration duration {total_audio:.3f}s is outside the 55–75s assembly target")

    concat_list = TMP_DIR / "audio_concat.txt"
    concat_list.write_text("\n".join(f"file '{path.as_posix()}'" for path in spans) + "\n", encoding="utf-8")
    narration = AUDIO_DIR / "REEL-0067_narration_hi-IN.wav"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list), "-c", "copy", str(narration)])

    captions = CAPTION_DIR / "REEL-0067_hi-IN.srt"
    write_srt(durations, captions)

    clip_list = TMP_DIR / "video_concat.txt"
    clip_paths: list[Path] = []
    for index, (duration, image_index) in enumerate(zip(durations, IMAGE_SEQUENCE), start=1):
        frames = max(1, int(round(duration * 30)))
        clip = TMP_DIR / f"clip_{index:02d}.mp4"
        image = images[image_index]
        zoom = "min(zoom+0.0007,1.06)" if index % 2 else "max(1.0,zoom-0.0005)"
        vf = f"scale=720:1280,zoompan=z='{zoom}':d={frames}:s=720x1280:fps=30,format=yuv420p"
        run([
            "ffmpeg", "-y", "-loop", "1", "-i", str(image),
            "-vf", vf, "-frames:v", str(frames), "-an", "-c:v", "libx264",
            "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", str(clip),
        ])
        clip_paths.append(clip)
    clip_list.write_text("\n".join(f"file '{path.as_posix()}'" for path in clip_paths) + "\n", encoding="utf-8")

    silent = TMP_DIR / "silent_video.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(clip_list), "-c", "copy", str(silent)])

    with_audio = TMP_DIR / "with_audio.mp4"
    run([
        "ffmpeg", "-y", "-i", str(silent), "-i", str(narration), "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(with_audio),
    ])

    final_video = RENDER_DIR / "REEL-0067_plant-diversity-balanced-meal-variety.mp4"
    caption_path = str(captions).replace("\\", "/").replace(":", "\\:")
    style = "FontName=Noto Sans Devanagari,FontSize=15,PrimaryColour=&H00FFFFFF,OutlineColour=&H001A1A1A,BorderStyle=1,Outline=2,Shadow=0,Alignment=2,MarginV=70"
    escaped_style = style.replace(",", "\\,")
    subtitle_filter = f"subtitles=filename='{caption_path}':force_style={escaped_style}"
    run([
        "ffmpeg", "-y", "-i", str(with_audio), "-vf", subtitle_filter,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "copy", "-movflags", "+faststart", str(final_video),
    ])

    metadata = {
        "reel_id": "REEL-0067",
        "source_id": "reel_0067_plant_diversity_balanced_meal_variety",
        "assembly_type": "quota_limited_topic_specific_still_motion_fallback",
        "disclosure": "Two AI-generated topic-specific reference images animated with deterministic Ken Burns motion after the official image-generation limit prevented additional companion references; no native multi-clip video generation claimed.",
        "quota_event": "image_generation_free_plan_limit_20_of_20",
        "narration_spans": len(spans),
        "span_durations_seconds": [round(value, 3) for value in durations],
        "narration_duration_seconds": round(probe_duration(narration), 3),
        "video_duration_seconds": round(probe_duration(final_video), 3),
        "images": [str(path) for path in images],
        "image_sequence": [IMAGE_NAMES[index] for index in IMAGE_SEQUENCE],
        "caption_file": str(captions),
        "narration_file": str(narration),
        "final_video": str(final_video),
        "sha256": hashlib.sha256(final_video.read_bytes()).hexdigest(),
        "evidence_register": str(ROOT / "research" / "2026-08-23__reel0067__plant-diversity-source-validation.md"),
        "publication_allowed": False,
        "publication_block_reason": "Requires editorial review; general education only and not a personalized diet prescription.",
    }
    (RENDER_DIR / "REEL-0067_plant_diversity_assembly.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
