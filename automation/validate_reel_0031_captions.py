from pathlib import Path
import re
p=Path('assets/reel_0031_behavior_change_what_studies_measure_captions_hi.srt')
blocks=[b.strip().splitlines() for b in re.split(r'\n\s*\n',p.read_text(encoding='utf-8')) if b.strip()]
pat=re.compile(r'^(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})$')
def sec(parts):
    return int(parts[0])*3600+int(parts[1])*60+int(parts[2])+int(parts[3])/1000
prev=0.0
assert len(blocks)==21
for b in blocks:
    assert len(b)>=3 and b[0].isdigit()
    m=pat.match(b[1]); assert m, b[1]
    s=sec(tuple(map(int,m.groups()[:4]))); e=sec(tuple(map(int,m.groups()[4:])))
    assert s>=prev and e>s and e<=74.6, (s,e,prev)
    prev=e
print('SRT_OK',len(blocks),'last_end',prev)
