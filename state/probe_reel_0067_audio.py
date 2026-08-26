from __future__ import annotations
import shutil, subprocess, sys
from pathlib import Path
if len(sys.argv) != 3:
    raise SystemExit('usage: probe AUDIO ATTEMPT')
root = Path(__file__).resolve().parents[1]
audio = Path(sys.argv[1]).resolve(); attempt = sys.argv[2]
duration = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(audio)], text=True).strip())
print(f'DURATION {duration:.2f}')
audit = root / 'state' / 'reel_0067_audio_attempts.txt'
if not 45.0 <= duration <= 75.0:
    dest = audio.with_name(f'{audio.stem}_{attempt}_{duration:.2f}s.wav')
    shutil.copy2(audio, dest)
    with audit.open('a', encoding='utf-8') as f:
        f.write(f'{attempt}\t{duration:.2f}\tfailed_duration\t{dest.relative_to(root)}\n')
    raise SystemExit(f'duration outside 45-75 seconds; preserved {dest}')
with audit.open('a', encoding='utf-8') as f:
    f.write(f'{attempt}\t{duration:.2f}\taccepted_canonical\t{audio.relative_to(root)}\n')
print(f'accepted canonical narration {audio}')
