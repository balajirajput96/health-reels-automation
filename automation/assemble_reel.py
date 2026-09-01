#!/usr/bin/env python3
"""Assemble a narrated vertical reel from still visuals and timed captions."""
from __future__ import annotations

import argparse
import shlex
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Assemble a 9:16 Hindi reel")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audio", type=Path, required=True)
    parser.add_argument("--captions", type=Path, required=True)
    parser.add_argument("--duration", type=float, required=True)
    parser.add_argument("--title", default="Hindi research reel")
    parser.add_argument("--comment", default="Evidence-bounded public education. AI-generated narration and visuals may be used.")
    parser.add_argument("--image", action="append", required=True, help="image path followed by seconds, e.g. --image scene.png:12")
    args = parser.parse_args()

    images: list[tuple[Path, float]] = []
    for item in args.image:
        try:
            raw_path, raw_duration = item.rsplit(":", 1)
            path, duration = Path(raw_path), float(raw_duration)
        except ValueError as exc:
            raise SystemExit(f"invalid --image value {item!r}; expected path:seconds") from exc
        if not path.exists():
            raise SystemExit(f"missing image: {path}")
        if duration <= 0:
            raise SystemExit(f"image duration must be positive: {item!r}")
        images.append((path, duration))
    for path in (args.audio, args.captions):
        if not path.exists():
            raise SystemExit(f"missing input: {path}")
    if abs(sum(d for _, d in images) - args.duration) > 0.25:
        raise SystemExit("image durations must sum to the requested output duration within 0.25 seconds")

    cmd: list[str] = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "warning"]
    for path, duration in images:
        cmd += ["-loop", "1", "-t", f"{duration:.3f}", "-i", str(path)]
    audio_index = len(images)
    cmd += ["-i", str(args.audio)]
    filters: list[str] = []
    for index, (_, duration) in enumerate(images):
        frames = max(1, round(duration * 30))
        zoom = 0.0012 + (index % 3) * 0.0002
        filters.append(f"[{index}:v]zoompan=z='min(zoom+{zoom:.4f},1.08)':d={frames}:s=1080x1920:fps=30,setsar=1[v{index}]")
    joined = "".join(f"[v{i}]" for i in range(len(images)))
    concat = f"{joined}concat=n={len(images)}:v=1:a=0"
    fontdir = "/usr/share/fonts/truetype/noto"
    subtitle_path = str(args.captions).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
    filter_complex = ";".join(filters) + ";" + concat + f",subtitles='{subtitle_path}':fontsdir='{fontdir}':force_style='FontName=Noto Sans Devanagari,FontSize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H80000000,BorderStyle=1,Outline=2,Shadow=1,Alignment=2,MarginV=130'[v]"
    cmd += ["-filter_complex", filter_complex, "-map", "[v]", "-map", f"{audio_index}:a", "-t", f"{args.duration:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-metadata", f"title={args.title}", "-metadata", f"comment={args.comment}", str(args.output)]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    print("Running:", " ".join(shlex.quote(part) for part in cmd))
    subprocess.run(cmd, check=True)
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
