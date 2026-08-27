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
OUTPUT = RENDERED / "REEL-0009_context_cues_QC_pending.mp4"
ASS = WORK / "captions_hi-IN.ass"
SRT = WORK / "captions_hi-IN.srt"
MANIFEST = RENDERED / "REEL-0009_local_manifest.json"
WIDTH, HEIGHT, FPS = 720, 1280, 30

SPANS = [
    "कभी कोई signal मिलते ही आप बिना ज़्यादा सोचे एक काम शुरू कर देते हैं? जैसे चाय के बाद किताब खोलना, या जूते पहनते ही walk के लिए निकलना।",
    "Psychology में habit को सिर्फ़ बार-बार किया गया काम नहीं माना जाता। Habit में context का cue किसी action को अपने-आप शुरू करने से जुड़ सकता है।",
    "Research में एक ही तरह के place और time पर behaviour दोहराने से automaticity को support मिलने की बात सामने आई है। एक study में stable context, automaticity और habit-repetition goal attainment से जुड़ा था।",
    "लेकिन cue कोई command नहीं है। Context बदलने पर वही action कम fluent लग सकता है, और एक study का result हर व्यक्ति या हर behaviour पर guarantee नहीं बनता।",
    "आज एक छोटा, self-chosen action चुनिए। उसे किसी पहले से मौजूद routine के बाद जोड़िए—जैसे breakfast के बाद पाँच मिनट पढ़ना। Signal को simple रखिए और कुछ repetitions observe कीजिए।",
    "याद रखिए: cue शुरुआत को support कर सकता है, लेकिन fit, repetition और context भी मायने रखते हैं। Reminder miss हो जाए तो खुद को दोष न दें। यह general education है, treatment या guaranteed habit formula नहीं।",
]
WEIGHTS = [0.13, 0.17, 0.18, 0.16, 0.16, 0.20]
IMAGES = [
    ASSETS / "scene_01_everyday_signal.png",
    ASSETS / "scene_02_cue_action_context.png",
    ASSETS / "scene_03_stable_repetition.png",
    ASSETS / "scene_04_context_change.png",
    ASSETS / "scene_05_small_action_plan.png",
    ASSETS / "scene_06_cue_not_command.png",
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


def wrap_caption(text: str, max_chars: int = 30) -> str:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else current + " " + word
        if current and len(candidate) > max_chars:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return r"\N".join(lines)


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
        caption = wrap_caption(span)
        ass_lines.append(f"Dialogue: 0,{ass_time(t)},{ass_time(end)},Reel,,0,0,0,,{caption}")
        srt_lines += [str(i), f"{srt_time(t)} --> {srt_time(end)}", caption.replace(r"\N", "\n"), ""]
        t = end
    ASS.write_text("\n".join(ass_lines) + "\n", encoding="utf-8")
    SRT.write_text("\n".join(srt_lines), encoding="utf-8")
    (WORK / "caption_font_path.txt").write_text(font_path + "\n" + font_dir + "\n", encoding="utf-8")
    return font_dir


def render() -> dict:
    required = [AUDIO, *IMAGES, ROOT / "production_brief.md", ROOT / "script_hi-IN.md", ROOT / "source_validation.md"]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise FileNotFoundError("Missing Reel 0009 inputs: " + ", ".join(missing))
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
        "reel_id": "0009",
        "display_id": "REEL-0009",
        "batch": "Batch_001",
        "working_title_hi": "आदतें और व्यवहार परिवर्तन: संकेत — शुरुआत (विज़ुअल मॉडल)",
        "status": "rendered_local_pending_qc_and_drive_upload",
        "canonical_drive_path": "3000_HINDI_RESEARCH_REELS/Batch_001/Reel_0009",
        "format": {"width": WIDTH, "height": HEIGHT, "aspect_ratio": "9:16", "fps": FPS, "duration_seconds": round(final_duration, 3)},
        "language": "hi-IN",
        "production_mode": "original AI-generated still scenes with deterministic pan-zoom motion, Hindi narration, and burned-in captions",
        "evidence_status": "verified_with_limits",
        "sources": [
            {"title": "Gardner, Lally, and Wardle (2012), Making health habitual: the psychology of habit-formation and general practice", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC3505409/"},
            {"title": "Stojanovic, Grund, and Fries (2022), Context Stability in Habit Building Increases Automaticity and Goal Attainment", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9226889/"},
            {"title": "Stojanovic, Grund, and Fries (2022), publisher page", "url": "https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2022.883795/full"},
            {"title": "Singh et al. (2024), Time to Form a Habit: A Systematic Review and Meta-Analysis", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11641623/"},
        ],
        "claims_boundary": "Contextual cues and stable contexts may support habit initiation and automaticity, but cues are not commands and do not guarantee completion or durable habit formation. Effects vary by person, behaviour, meaning, and context. This is general education, not treatment, diagnosis, or a guarantee.",
        "ai_content_disclosure": "Hindi narration and visual scenes were AI-assisted; motion assembly and captions were deterministic.",
        "files": {
            "video": OUTPUT.name,
            "narration": AUDIO.name,
            "captions_ass": ASS.name,
            "captions_srt": SRT.name,
            "script": "script_hi-IN.md",
            "production_brief": "production_brief.md",
            "source_validation": "../../../research/2026-08-27__reel0009__context-cues-source-validation.md",
        },
        "sha256": {name: sha256(path) for name, path in [(OUTPUT.name, OUTPUT), (AUDIO.name, AUDIO), (ASS.name, ASS), (SRT.name, SRT)]},
        "segment_durations_seconds": [round(x, 3) for x in durations],
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"output": str(OUTPUT), "manifest": str(MANIFEST), "duration_seconds": final_duration, "audio_duration_seconds": total}


if __name__ == "__main__":
    print(json.dumps(render(), ensure_ascii=False))
