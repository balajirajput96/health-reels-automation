from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRT = ROOT / 'assets/reel_0079_recovery_what_studies_measure_captions_hi.srt'
text = SRT.read_text(encoding='utf-8')
blocks = [b for b in re.split(r'\n\s*\n', text.strip()) if b.strip()]
assert len(blocks) == 15, len(blocks)
last_end = 0
required = ['रिकवरी', 'baseline', 'HRV', 'self-report', 'daily diaries', 'biomarker', 'AI-सहायित', 'व्यक्तिगत सलाह नहीं']
full = ''
for index, block in enumerate(blocks, 1):
    lines = block.splitlines()
    assert lines[0].strip() == str(index)
    match = re.fullmatch(r'(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})', lines[1])
    assert match, lines[1]
    values = [int(value) for value in match.groups()]
    start = ((values[0] * 60 + values[1]) * 60 + values[2]) * 1000 + values[3]
    end = ((values[4] * 60 + values[5]) * 60 + values[6]) * 1000 + values[7]
    assert start == last_end, (index, start, last_end)
    assert end > start, index
    last_end = end
    full += '\n'.join(lines[2:]) + '\n'
assert last_end == 68_200, last_end
for phrase in required:
    assert phrase in full, phrase
print('R0079_CAPTIONS_OK')
print(f'cues={len(blocks)} duration_ms={last_end}')
