#!/usr/bin/env python3
"""Assemble REEL-0066 from local narration spans and topic-specific still references.

This is a deterministic, quota-aware fallback assembly. It does not claim native
multi-clip AI video generation; it uses gentle Ken Burns motion over topic-specific
AI reference images, a concatenated Hindi narration track, and burned-in Hindi SRT
captions. All generated media remains ignored by Git.
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
TMP_DIR = RENDER_DIR / "reel0066_tmp"

SPAN_TEXT = [
    "क्या fiber सिर्फ कब्ज के लिए है? नहीं—यह varied diet का भी हिस्सा हो सकता है।",
    "WHO guidance में whole grains, fruits, vegetables और pulses जैसी विविध plant foods शामिल हैं।",
    "दाल, चना, beans, oats, brown rice, पूरे फल, सब्ज़ियाँ और nuts fiber के natural sources हो सकते हैं। Focus variety पर है, superfood पर नहीं।",
    "Harvard के मुताबिक fiber ordinary carbohydrate की तरह पूरी तरह digest नहीं होता; कुछ हिस्सा gut microbes ferment कर सकते हैं।",
    "Reviews बताती हैं कि fiber और gut microbiome का connection research-supported है, पर असर type, मात्रा, समय और व्यक्ति के context पर बदलता है। कोई एक food सबको एक जैसा असर नहीं देता।",
    "Fiber-rich foods धीरे-धीरे जोड़ें। WHO का 25-gram figure population guidance है, personal prescription नहीं।",
    "यह general education है, personal diet plan नहीं। Digestive disease या special needs हों, बदलाव से पहले clinician या registered dietitian से सलाह लें।",
]
IMAGE_NAMES = [
    "reel0066_primary_varied_fiber.png",
    "reel0066_ref02_plant_sources.png",
    "reel0066_ref03_gut_microbe_concept.png",
    "reel0066_ref04_varied_meal.png",
    "reel0066_ref05_gradual_addition.png",
    "reel0066_ref06_closing_safety.png",
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
    # Controlled breaks keep Devanagari and mixed English terms within the lower-third safe area.
    captions = [
        "क्या fiber सिर्फ कब्ज के लिए है?\nनहीं—यह varied diet का भी हिस्सा हो सकता है।",
        "WHO guidance में whole grains, fruits, vegetables\nऔर pulses जैसी विविध plant foods शामिल हैं।",
        "दाल, चना, beans, oats, brown rice, पूरे फल,\nसब्ज़ियाँ और nuts fiber के natural sources हो सकते हैं।\nFocus variety पर है, superfood पर नहीं।",
        "Harvard के मुताबिक fiber ordinary carbohydrate की तरह\nपूरी तरह digest नहीं होता; कुछ हिस्सा gut microbes\nferment कर सकते हैं।",
        "Reviews बताती हैं कि fiber और gut microbiome का connection\nresearch-supported है, पर असर type, मात्रा, समय और व्यक्ति\nके context पर बदलता है। कोई एक food सबको एक जैसा असर नहीं देता।",
        "Fiber-rich foods धीरे-धीरे जोड़ें।\nWHO का 25-gram figure population guidance है,\npersonal prescription नहीं।",
        "यह general education है, personal diet plan नहीं।\nDigestive disease या special needs हों, बदलाव से पहले\nclinician या registered dietitian से सलाह लें।",
    ]
    start = 0.0
    blocks = []
    for idx, (duration, text) in enumerate(zip(durations, captions), start=1):
        end = start + duration
        blocks.append(f"{idx}\n{hms(start)} --> {hms(end)}\n{{\\an2}}{text}\n")
        start = end
    output.write_text("\n".join(blocks), encoding="utf-8")


def main() -> None:
    for directory in (CAPTION_DIR, RENDER_DIR, TMP_DIR):
        directory.mkdir(parents=True, exist_ok=True)

    spans = [AUDIO_DIR / f"REEL-0066_span{idx:02d}_hi-IN.wav" for idx in range(1, 8)]
    missing = [str(path) for path in spans + [ASSET_DIR / name for name in IMAGE_NAMES] if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing required local inputs:\n" + "\n".join(missing))

    durations = [probe_duration(path) for path in spans]
    total_audio = sum(durations)
    if not 55.0 <= total_audio <= 75.0:
        raise RuntimeError(f"Narration duration {total_audio:.3f}s is outside the 55–75s assembly target")

    concat_list = TMP_DIR / "audio_concat.txt"
    concat_list.write_text("\n".join(f"file '{path.as_posix()}'" for path in spans) + "\n", encoding="utf-8")
    narration = AUDIO_DIR / "REEL-0066_narration_hi-IN.wav"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list), "-c", "copy", str(narration)])

    captions = CAPTION_DIR / "REEL-0066_hi-IN.srt"
    write_srt(durations, captions)

    # Reuse the six generated references across seven spans; each span is rendered with
    # a small, deterministic push-in so the result is animated while staying topic-specific.
    clip_list = TMP_DIR / "video_concat.txt"
    clip_paths = []
    for idx, (duration, image_name) in enumerate(zip(durations, IMAGE_NAMES + [IMAGE_NAMES[-1]]), start=1):
        frames = max(1, int(round(duration * 30)))
        clip = TMP_DIR / f"clip_{idx:02d}.mp4"
        zoom = "min(zoom+0.0007,1.06)" if idx % 2 else "max(1.0,zoom-0.0005)"
        vf = f"scale=720:1280,zoompan=z='{zoom}':d={frames}:s=720x1280:fps=30,format=yuv420p"
        run([
            "ffmpeg", "-y", "-loop", "1", "-i", str(ASSET_DIR / image_name),
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

    final_video = RENDER_DIR / "REEL-0066_dietary_fiber_varied_eating.mp4"
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
        "reel_id": "REEL-0066",
        "source_id": "reel_0066_dietary_fiber_varied_eating_patterns",
        "assembly_type": "quota_aware_topic_specific_still_motion_fallback",
        "disclosure": "AI-generated topic-specific reference images animated with deterministic Ken Burns motion; no native multi-clip video generation claimed.",
        "narration_spans": len(spans),
        "span_durations_seconds": [round(value, 3) for value in durations],
        "narration_duration_seconds": round(probe_duration(narration), 3),
        "video_duration_seconds": round(probe_duration(final_video), 3),
        "images": [str(ASSET_DIR / name) for name in IMAGE_NAMES],
        "caption_file": str(captions),
        "narration_file": str(narration),
        "final_video": str(final_video),
        "sha256": hashlib.sha256(final_video.read_bytes()).hexdigest(),
        "evidence_register": str(ROOT / "research" / "2026-08-23__reel0066__dietary-fiber-source-validation.md"),
        "publication_allowed": False,
        "publication_block_reason": "Requires editorial review; general education only and not a personalized diet prescription.",
    }
    (RENDER_DIR / "REEL-0066_dietary_fiber_assembly.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
