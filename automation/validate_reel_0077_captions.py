from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRT = ROOT / 'assets/reel_0077_stress_appraisal_what_studies_measure_captions_hi.srt'
text = SRT.read_text(encoding='utf-8-sig').strip()
blocks = re.split(r'\n\s*\n', text)
assert len(blocks) == 15, len(blocks)
previous_end = -1.0
for index, block in enumerate(blocks, 1):
    lines = block.splitlines()
    assert lines[0].strip() == str(index), (index, lines[:1])
    match = re.match(r'(\d\d):(\d\d):(\d\d),(\d{3}) --> (\d\d):(\d\d):(\d\d),(\d{3})', lines[1])
    assert match, (index, lines[1])
    vals = [int(value) for value in match.groups()]
    start = vals[0]*3600 + vals[1]*60 + vals[2] + vals[3]/1000
    end = vals[4]*3600 + vals[5]*60 + vals[6] + vals[7]/1000
    assert end > start and start >= previous_end, (index, start, end, previous_end)
    previous_end = end
    assert len(' '.join(lines[2:]).strip()) > 0
assert abs(previous_end - 74.760) < 0.01, previous_end
joined = text.lower()
for term in ('exposure', 'perceived stress', 'appraisal', 'physiology', 'association', 'diagnosis'):
    assert term in joined, term
print('R0077_CAPTIONS_OK')
print('cues', len(blocks), 'last_end', f'{previous_end:.3f}')
