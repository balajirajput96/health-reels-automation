from __future__ import annotations
import shutil, subprocess, sys
from pathlib import Path

def duration(path: Path) -> float:
    return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(path)], text=True).strip())

if len(sys.argv) != 4:
    raise SystemExit('usage: probe AUDIO PROBE_FILE ATTEMPT')
audio=Path(sys.argv[1]); probe=Path(sys.argv[2]); attempt=sys.argv[3]
root=audio.parent.parent
d=duration(audio)
print(f'DURATION {d:.2f}')
if not 45.0 <= d <= 75.0:
    dest=audio.with_name(f'{audio.stem}_{attempt}_{d:.2f}s.wav')
    shutil.copy2(audio,dest)
    with (root/'state'/'reel_0065_audio_attempts.txt').open('a',encoding='utf-8') as f:
        f.write(f'{attempt}\t{d:.2f}\tfailed_duration\t{dest.relative_to(root)}\n')
    raise SystemExit(f'duration outside 45-75 seconds; preserved {dest}')
with (root/'state'/'reel_0065_audio_attempts.txt').open('a',encoding='utf-8') as f:
    f.write(f'{attempt}\t{d:.2f}\taccepted_canonical\t{audio.relative_to(root)}\n')
print(f'accepted canonical narration {audio}')
