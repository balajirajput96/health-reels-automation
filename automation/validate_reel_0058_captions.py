from pathlib import Path
import re
p=Path('assets/reel_0058_episodic_memory_what_studies_measure_captions_hi.srt')
blocks=[b.strip().splitlines() for b in re.split(r'\n\s*\n',p.read_text(encoding='utf-8')) if b.strip()]
pat=re.compile(r'^(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})$')
def sec(v): return int(v[0])*3600+int(v[1])*60+int(v[2])+int(v[3])/1000
assert len(blocks)==21,len(blocks)
prev=0.0
for b in blocks:
 assert len(b)>=3 and b[0].isdigit(),b
 m=pat.match(b[1]); assert m,b[1]
 start=sec(tuple(map(int,m.groups()[:4]))); end=sec(tuple(map(int,m.groups()[4:])))
 assert start>=prev and end>start and end<=70.44,(start,end,prev)
 prev=end
safety=' '.join(' '.join(b[2:]) for b in blocks).lower()
assert 'diagnosis' in safety and 'advice' in safety and 'personal' in safety
print('SRT_OK',len(blocks),'last_end',prev)
