from pathlib import Path
import re
p=Path('assets/reel_0067_theory_of_mind_what_studies_measure_captions_hi.srt')
blocks=[b.strip().splitlines() for b in re.split(r'\n\s*\n',p.read_text(encoding='utf-8-sig')) if b.strip()]
pat=re.compile(r'^(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})$')
def sec(vals): return int(vals[0])*3600+int(vals[1])*60+int(vals[2])+int(vals[3])/1000
assert len(blocks)==15, len(blocks)
prev=0.0
for i,b in enumerate(blocks,1):
    assert len(b)>=3 and b[0]==str(i), b
    m=pat.match(b[1]); assert m, b[1]
    start=sec(tuple(map(int,m.groups()[:4]))); end=sec(tuple(map(int,m.groups()[4:])))
    assert start>=prev and end>start and end<=69.12,(start,end,prev)
    prev=end
text=' '.join(' '.join(b[2:]) for b in blocks).lower()
for term in ('सीधे मन नहीं पढ़तीं','diagnosis','personal assessment','ai-generated educational visuals'):
    assert term in text, term
print('SRT_OK',len(blocks),'last_end',prev)
