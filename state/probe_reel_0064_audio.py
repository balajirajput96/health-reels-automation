from __future__ import annotations
import shutil, subprocess, sys
from pathlib import Path

def duration(path: Path) -> float:
    out=subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(path)],text=True).strip()
    return float(out)

if len(sys.argv)!=4: raise SystemExit('usage: probe AUDIO PROBE_FILE ATTEMPT')
audio=Path(sys.argv[1]); probe=Path(sys.argv[2]); attempt=sys.argv[3]
d=duration(audio); print(f'DURATION {d:.2f}')
if not 45.0 <= d <= 75.0:
    dest=audio.with_name(f'{audio.stem}_{attempt}_{d:.2f}s.wav')
    shutil.copy2(audio,dest)
    with (audio.parent.parent/'state'/'reel_0064_audio_attempts.txt').open('a',encoding='utf-8') as f:
        f.write(f'{attempt}\t{d:.2f}\tfailed_duration\t{dest.relative_to(audio.parent.parent)}\n')
    print('duration outside 45-75 seconds; preserved attempt',dest)
    raise SystemExit(1)
with (audio.parent.parent/'state'/'reel_0064_audio_attempts.txt').open('a',encoding='utf-8') as f:
    f.write(f'{attempt}\t{d:.2f}\taccepted_canonical\t{audio.relative_to(audio.parent.parent)}\n')
print('accepted canonical narration',audio)
