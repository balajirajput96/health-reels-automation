from pathlib import Path
import re

p = Path('assets/reel_0040_environmental_friction_what_studies_measure_captions_hi.srt')
blocks = [b.strip().splitlines() for b in re.split(r'\n\s*\n', p.read_text(encoding='utf-8')) if b.strip()]
pat = re.compile(r'^(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})$')

def sec(values):
    return int(values[0]) * 3600 + int(values[1]) * 60 + int(values[2]) + int(values[3]) / 1000

assert len(blocks) == 19, len(blocks)
previous_end = 0.0
for block in blocks:
    assert len(block) >= 3 and block[0].isdigit(), block
    match = pat.match(block[1])
    assert match, block[1]
    start = sec(tuple(map(int, match.groups()[:4])))
    end = sec(tuple(map(int, match.groups()[4:])))
    assert start >= previous_end and end > start and end <= 69.0, (start, end, previous_end)
    previous_end = end
assert 'diagnosis' in blocks[-1][-1].lower()
assert 'treatment' in blocks[-1][-1].lower()
print('SRT_OK', len(blocks), 'last_end', previous_end)
