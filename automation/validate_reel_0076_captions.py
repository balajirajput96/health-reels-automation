from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / 'assets/reel_0076_procrastination_what_studies_measure_captions_hi.srt'
text = p.read_text(encoding='utf-8')
blocks = [b for b in re.split(r'\n\s*\n', text.strip()) if b.strip()]
assert len(blocks) == 15, len(blocks)
prev = 0.0
last = 0.0
body = []
for i, block in enumerate(blocks, 1):
    lines = block.splitlines()
    assert lines[0].strip() == str(i), (i, lines[:1])
    match = re.match(r'(\d\d):(\d\d):(\d\d),(\d\d\d) --> (\d\d):(\d\d):(\d\d),(\d\d\d)$', lines[1])
    assert match, lines[1]
    values = list(map(int, match.groups()))
    start = values[0] * 3600 + values[1] * 60 + values[2] + values[3] / 1000
    end = values[4] * 3600 + values[5] * 60 + values[6] + values[7] / 1000
    assert start >= prev and end > start, (i, start, end, prev)
    prev = end
    last = end
    body.append(' '.join(lines[2:]))
assert abs(last - 61.0) < 0.01, last
joined = ' '.join(body).lower()
for term in ('self-report', 'behavior', 'planned', 'actual', 'completion days', 'deadline pacing', 'moderate', 'outcomes', 'association', 'diagnosis'):
    assert term in joined, term
print(f'R0076_CAPTIONS_OK cues={len(blocks)} end={last:.3f}')
