#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
RENDERED = ROOT / "rendered"
WORK = ROOT / "work"
AUDIO = ROOT / "narration_hi-IN.wav"
OUTPUT = RENDERED / "REEL-0004_habit_automaticity_QC_pending.mp4"
ASS = WORK / "captions_hi-IN.ass"
SRT = WORK / "captions_hi-IN.srt"
MANIFEST = RENDERED / "REEL-0004_local_manifest.json"
WIDTH, HEIGHT, FPS = 720, 1280, 30

SPANS = [
    "कोई काम बार-बार करना और उसे automatic habit कहना—दोनों एक ही बात नहीं हैं।",
    "Habit research के अनुसार, habit अक्सर recurring context में repeat हुए response और cue के link से जुड़ी होती है। यानी वही जगह, समय या situation response शुरू करने का संकेत बन सकती है।",
    "लेकिन frequency सिर्फ़ बताती है कि behaviour कितनी बार हुआ। Automaticity पूछती है: क्या cue आते ही response कम सोच-विचार के शुरू होता है?",
    "Gardner और colleagues ने दिखाया कि popular Self-Report Habit Index में automaticity के साथ frequency और identity भी mix हो सकते हैं। इसलिए researchers ने automaticity-focused चार-item measure भी test किया।",
    "यह measurement research tool है, किसी व्यक्ति का diagnosis या brain-scan proof नहीं। Context बदलने पर वही behaviour कम automatic महसूस हो सकता है, और deliberate goals फिर भी मायने रखते हैं।",
    "इसलिए “मैं यह रोज़ करता हूँ” को “यह हर जगह अपने-आप होता है” मत समझिए। Habit context-dependent pattern है—moral label नहीं। यह general education है, personal medical या mental-health advice नहीं।",
]
WEIGHTS = [0.12, 0.19, 0.18, 0.20, 0.18, 0.13]
IMAGES = [
    ASSETS / "scene_01_frequency_not_automatic.png",
    ASSETS / "scene_02_context_cue.png",
    ASSETS / "scene_03_measurement_split.png",
    ASSETS / "scene_04_context_change.png",
    ASSETS / "scene_05_deliberate_choice.png",
    ASSETS / "scene_06_takeaway.png",
]


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)


def duration(path: Path) -> float:
    return float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path)
    ], text=True).strip())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ass_time(seconds: float) -> str:
    return f"{int(seconds // 3600)}:{int(seconds % 3600 // 60):02d}:{seconds % 60:05.2f}"


def srt_time(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_captions(durations: list[float]) -> str:
    font_path = subprocess.check_output(["fc-match", "-f", "%{file}", "Noto Sans Devanagari"], text=True).strip()
    font_dir = str(Path(font_path).parent)
    ass_lines = [
        "[Script Info]", "ScriptType: v4.00+", "PlayResX: 720", "PlayResY: 1280",
        "WrapStyle: 2", "ScaledBorderAndShadow: yes", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: Reel,Noto Sans Devanagari,31,&H00FFFFFF,&H00FFFFFF,&H00000000,&HCC06101D,0,0,3,2,0,2,38,38,118,1",
        "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    srt_lines: list[str] = []
    t = 0.0
    for i, (span, segment_duration) in enumerate(zip(SPANS, durations), 1):
        end = t + segment_duration
        ass_lines.append(f"Dialogue: 0,{ass_time(t)},{ass_time(end)},Reel,,0,0,0,,{span}")
        srt_lines += [str(i), f"{srt_time(t)} --> {srt_time(end)}", span, ""]
        t = end
    ASS.write_text("\n".join(ass_lines) + "\n", encoding="utf-8")
    SRT.write_text("\n".join(srt_lines), encoding="utf-8")
    (WORK / "caption_font_path.txt").write_text(font_path + "\n" + font_dir + "\n", encoding="utf-8")
    return font_dir


def render() -> dict:
    required = [AUDIO, *IMAGES, ROOT / "production_brief.md", ROOT / "script_hi-IN.md"]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise FileNotFoundError("Missing Reel 0004 inputs: " + ", ".join(missing))
    WORK.mkdir(parents=True, exist_ok=True)
    RENDERED.mkdir(parents=True, exist_ok=True)
    total = duration(AUDIO)
    durations = [total * weight for weight in WEIGHTS]
    durations[-1] += total - sum(durations)
    clips: list[Path] = []
    for i, (image, segment_duration) in enumerate(zip(IMAGES, durations), 1):
        clip = WORK / f"scene_{i:02d}.mp4"
        vf = (
            f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,"
            f"crop={WIDTH}:{HEIGHT},"
            "zoompan=z='min(zoom+0.00025,1.045)':x='iw/2-(iw/zoom/2)':"
            f"y='ih/2-(ih/zoom/2)':d=1:s={WIDTH}x{HEIGHT}:fps={FPS},format=yuv420p"
        )
        run(["ffmpeg", "-y", "-loop", "1", "-framerate", str(FPS), "-i", str(image), "-t", f"{segment_duration:.3f}", "-vf", vf, "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", str(clip)])
        clips.append(clip)
    concat = WORK / "concat.txt"
    concat.write_text("".join(f"file '{clip.as_posix()}'\n" for clip in clips), encoding="utf-8")
    silent = WORK / "silent.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(silent)])
    font_dir = write_captions(durations)
    subtitle_filter = f"subtitles={ASS.as_posix()}:fontsdir={font_dir}"
    run(["ffmpeg", "-y", "-i", str(silent), "-i", str(AUDIO), "-vf", subtitle_filter, "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest", str(OUTPUT)])
    final_duration = duration(OUTPUT)
    manifest = {
        "reel_id": "0004",
        "display_id": "REEL-0004",
        "batch": "Batch_001",
        "working_title_hi": "Frequent काम और automatic habit एक ही चीज़ नहीं",
        "status": "rendered_local_pending_qc_and_drive_upload",
        "canonical_drive_path": "3000_HINDI_RESEARCH_REELS/Batch_001/Reel_0004",
        "format": {"width": WIDTH, "height": HEIGHT, "aspect_ratio": "9:16", "fps": FPS, "duration_seconds": round(final_duration, 3)},
        "language": "hi-IN",
        "production_mode": "original AI-generated still scenes with deterministic pan-zoom motion, Hindi narration, and burned-in captions",
        "evidence_status": "verified_with_limits",
        "sources": [
            {"title": "Wood & Rünger (2016), Psychology of Habit", "url": "https://doi.org/10.1146/annurev-psych-122414-033417"},
            {"title": "Gardner et al. (2012), Towards parsimony in habit measurement", "url": "https://doi.org/10.1186/1479-5868-9-102"},
            {"title": "PubMed record for Wood & Rünger (2016)", "url": "https://pubmed.ncbi.nlm.nih.gov/26361052/"},
        ],
        "claims_boundary": "Habit research distinguishes recurring-context automaticity from mere frequency. The SRBAI is a research measure, not a diagnosis or brain-scan proof. Habits do not eliminate deliberate goals, and this is general education only.",
        "ai_content_disclosure": "Hindi narration and visual scenes were AI-assisted; motion assembly and captions were deterministic.",
        "files": {
            "video": OUTPUT.name,
            "narration": AUDIO.name,
            "captions_ass": ASS.name,
            "captions_srt": SRT.name,
            "script": "script_hi-IN.md",
            "production_brief": "production_brief.md",
            "source_validation": "../../../research/2026-08-25__reel0004__habit-automaticity-source-validation.md",
        },
        "sha256": {name: sha256(path) for name, path in [(OUTPUT.name, OUTPUT), (AUDIO.name, AUDIO), (ASS.name, ASS), (SRT.name, SRT)]},
        "segment_durations_seconds": [round(x, 3) for x in durations],
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"output": str(OUTPUT), "manifest": str(MANIFEST), "duration_seconds": final_duration, "audio_duration_seconds": total}


if __name__ == "__main__":
    print(json.dumps(render(), ensure_ascii=False))
