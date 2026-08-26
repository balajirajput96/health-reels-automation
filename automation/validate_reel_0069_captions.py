from pathlib import Path
import re,sys
p=Path('assets/reel_0069_empathy_what_studies_measure_captions_hi.srt')
t=p.read_text(encoding='utf-8-sig').strip(); blocks=re.split(r'\n\s*\n',t)
assert len(blocks)==15, len(blocks)
def sec(x):
 h,m,s=x.split(':'); ss,ms=s.split(','); return int(h)*3600+int(m)*60+int(ss)+int(ms)/1000
last=-1; ends=[]; full=[]
for i,b in enumerate(blocks,1):
 lines=b.splitlines(); assert lines[0].strip()==str(i), i
 m=re.match(r'^(\d\d:\d\d:\d\d,\d{3}) --> (\d\d:\d\d:\d\d,\d{3})$',lines[1]); assert m, i
 a,z=sec(m.group(1)),sec(m.group(2)); assert a>=last and z>a and z<=62.0, (i,a,z)
 last=a; ends.append(z); full.append(' '.join(lines[2:]))
joined=' '.join(full)
for term in ('self-report','empathic accuracy','affective response','universal empathy','diagnosis','AI-generated educational visuals'):
 assert term in joined, term
assert 'नहीं' in joined
print(f'SRT_OK {len(blocks)} last_end {max(ends):.2f}')
