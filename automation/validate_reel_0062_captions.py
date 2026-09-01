from pathlib import Path
import re
p=Path('assets/reel_0062_selective_attention_what_studies_measure_captions_hi.srt')
blocks=[b.strip().splitlines() for b in re.split(r'\n\s*\n',p.read_text(encoding='utf-8')) if b.strip()]
pat=re.compile(r'^(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})$')
def sec(v): return int(v[0])*3600+int(v[1])*60+int(v[2])+int(v[3])/1000
assert len(blocks)==20,len(blocks); prev=0.0
for i,b in enumerate(blocks,1):
 assert len(b)>=3 and b[0]==str(i),b
 m=pat.match(b[1]); assert m,b[1]
 start=sec(tuple(map(int,m.groups()[:4]))); end=sec(tuple(map(int,m.groups()[4:])))
 assert start>=prev and end>start and end<=73.36,(start,end,prev); prev=end
safety=' '.join(' '.join(b[2:]) for b in blocks).lower()
for term in ('diagnosis','advice','direct readout','guarantee'): assert term in safety,term
print('SRT_OK',len(blocks),'last_end',prev)
