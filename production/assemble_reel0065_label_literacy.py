"""Assemble REEL-0065 from topic-specific label-literacy references and Hindi narration.

The assembler is deterministic after the AI reference images and TTS spans exist. It
keeps all generated media out of Git and writes a provenance record beside the draft.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "production" / "assets"
AUDIO = ROOT / "production" / "audio"
CAPTIONS_DIR = ROOT / "production" / "captions"
RENDERED = ROOT / "production" / "rendered"
WORK = ROOT / "production" / "assembly_work" / "reel0065"
OUT = RENDERED / "REEL-0065_label_literacy_draft.mp4"
AUDIO_OUT = AUDIO / "REEL-0065_narration_hi-IN.wav"
CAPTIONS = CAPTIONS_DIR / "REEL-0065_hi-IN.srt"

SPAN_TEXT = [
    "Label पढ़ते समय पहले Serving Size देखिए।\nCalories और nutrients,\nइसी एक serving के हिसाब से लिखे होते हैं।",
    "Serving Size यह नहीं बताता\nकि आपको कितना खाना चाहिए।\nयह label comparison के लिए एक reference amount है।",
    "Servings per container भी देखिए।\nअगर पैकेट में दो servings हैं\nऔर आप पूरा पैकेट खाते हैं,\nतो एक serving से अलग total amount मिलेगा।",
    "Total Sugars में फल या दूध की\nnaturally मौजूद sugar और added sugar,\nदोनों शामिल हो सकती हैं।",
    "Added Sugars processing में जोड़ी गई sugar होती है,\nजैसे कुछ syrups या sweeteners।\nIncludes Added Sugars लाइन पढ़िए।",
    "%DV बताता है कि एक serving पूरे दिन के\nreference value में कितना योगदान देती है।\nGeneral guide में 5% या कम low, और 20% या अधिक high माना जाता है।\nProducts compare करते समय serving size समान रखें।",
    "FDA के 2,000-calorie reference में added sugars का Daily Value 50 grams है—\nयह personal prescription नहीं है।\nआपकी needs अलग हो सकती हैं; specific diet या health advice के लिए qualified professional से पूछें।",
]
AUDIO_SPANS = [AUDIO / f"REEL-0065_span{index:02d}_hi-IN.wav" for index in range(1, 8)]
IMAGE_PATHS = [
    ASSETS / "reel0065_primary_label_literacy_20260823.png",
    ASSETS / "reel0065_ref02_serving_size_20260823.png",
    ASSETS / "reel0065_ref03_total_vs_added_sugars_20260823.png",
    ASSETS / "reel0065_ref04_added_sugars_line_20260823.png",
    ASSETS / "reel0065_ref05_percent_dv_20260823.png",
    ASSETS / "reel0065_ref06_checklist_takeaway_20260823.png",
    ASSETS / "reel0065_primary_label_literacy_20260823.png",
]
ATEMPO = 1.18


def run(args: list[str]) -> None:
    subprocess.run(args, check=True)


def duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def srt_time(value: float) -> str:
    millis = int(round(value * 1000))
    hours, millis = divmod(millis, 3_600_000)
    minutes, millis = divmod(millis, 60_000)
    seconds, millis = divmod(millis, 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"


def write_srt(durations: list[float]) -> None:
    cursor = 0.0
    blocks = []
    for index, (text, span_duration) in enumerate(zip(SPAN_TEXT, durations), start=1):
        end = cursor + span_duration
        blocks.append(f"{index}\n{srt_time(cursor)} --> {srt_time(end)}\n{text}\n")
        cursor = end
    CAPTIONS.write_text("\n".join(block.rstrip() for block in blocks) + "\n", encoding="utf-8")


def make_still_segment(image: Path, span_duration: float, output: Path, zoom_direction: str) -> None:
    zoom = "min(zoom+0.0007,1.035)" if zoom_direction == "in" else "max(zoom-0.0005,1.0)"
    vf = (
        "scale=720:1280:force_original_aspect_ratio=increase,"
        "crop=720:1280,"
        f"zoompan=z='{zoom}':d=1:s=720x1280:fps=30,format=yuv420p"
    )
    run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(image), "-t", f"{span_duration:.3f}",
        "-vf", vf, "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-r", "30", "-pix_fmt", "yuv420p", str(output),
    ])


def main() -> int:
    required = [*AUDIO_SPANS, *IMAGE_PATHS]
    for path in required:
        if not path.is_file():
            raise SystemExit(f"missing required input: {path}")
    WORK.mkdir(parents=True, exist_ok=True)
    AUDIO_OUT.parent.mkdir(parents=True, exist_ok=True)
    CAPTIONS_DIR.mkdir(parents=True, exist_ok=True)
    RENDERED.mkdir(parents=True, exist_ok=True)

    sped_paths = []
    for index, source in enumerate(AUDIO_SPANS, start=1):
        sped = WORK / f"span{index:02d}_sped.wav"
        run(["ffmpeg", "-y", "-i", str(source), "-filter:a", f"atempo={ATEMPO}", "-ar", "48000", "-ac", "2", str(sped)])
        sped_paths.append(sped)

    audio_list = WORK / "audio_concat.txt"
    audio_list.write_text("".join(f"file '{path.as_posix()}'\n" for path in sped_paths), encoding="utf-8")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(audio_list), "-c", "copy", str(AUDIO_OUT)])
    durations = [duration(path) for path in sped_paths]
    write_srt(durations)

    segments = []
    for index, (image, span_duration) in enumerate(zip(IMAGE_PATHS, durations), start=1):
        segment = WORK / f"segment_{index:02d}.mp4"
        make_still_segment(image, span_duration, segment, "in" if index % 2 else "out")
        segments.append(segment)
    video_list = WORK / "video_concat.txt"
    video_list.write_text("".join(f"file '{path.as_posix()}'\n" for path in segments), encoding="utf-8")
    concat_video = WORK / "concat_video.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(video_list), "-c", "copy", str(concat_video)])

    subtitle_filter = (
        f"subtitles={CAPTIONS.as_posix()}:"
        "force_style='FontName=Noto Sans Devanagari,FontSize=18,Outline=1,Shadow=0,MarginV=78,Alignment=2'"
    )
    total_duration = duration(AUDIO_OUT)
    run([
        "ffmpeg", "-y", "-i", str(concat_video), "-i", str(AUDIO_OUT),
        "-map", "0:v:0", "-map", "1:a:0", "-vf", subtitle_filter,
        "-t", f"{total_duration:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-r", "30", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
        "-ar", "48000", "-ac", "2", "-movflags", "+faststart", str(OUT),
    ])

    metadata = {
        "reel_id": "REEL-0065",
        "source_id": "reel_0065_reading_food_labels_added_sugars_decision_awareness",
        "output": str(OUT.relative_to(ROOT)),
        "production_mode": "topic_specific_ai_reference_montage",
        "visual_provenance": {
            "ai_reference_images": [str(path.relative_to(ROOT)) for path in IMAGE_PATHS],
            "deterministic_motion": "Ken Burns-style zoom and crop animation applied to topic-specific AI references",
        },
        "audio": str(AUDIO_OUT.relative_to(ROOT)),
        "captions": str(CAPTIONS.relative_to(ROOT)),
        "span_durations_seconds": durations,
        "target_duration_seconds": total_duration,
        "speed_adjustment": ATEMPO,
        "publication_allowed": False,
        "drive_verified": False,
        "full_qc_required": True,
        "note": "Topic-specific AI references were generated after research. This draft is not publication-ready until technical/editorial QC and Drive upload/re-list verification pass.",
    }
    (RENDERED / "REEL-0065_assembly_metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metadata, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
