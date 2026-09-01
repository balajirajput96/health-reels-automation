from pathlib import Path
import re
p=Path('assets/reel_0070_dehumanization_what_studies_measure_captions_hi.srt')
blocks=re.split(r'\n\s*\n',p.read_text(encoding='utf-8-sig').strip()); assert len(blocks)==15
def sec(x):
 h,m,s=x.split(':'); ss,ms=s.split(','); return int(h)*3600+int(m)*60+int(ss)+int(ms)/1000
prev=-1; ends=[]; texts=[]
for i,b in enumerate(blocks,1):
 lines=b.splitlines(); assert lines[0].strip()==str(i); m=re.match(r'^(\d\d:\d\d:\d\d,\d{3}) --> (\d\d:\d\d:\d\d,\d{3})$',lines[1]); assert m
 a,z=sec(m.group(1)),sec(m.group(2)); assert a>=prev and z>a and z<=68.84,(i,a,z); prev=a; ends.append(z); texts.append(' '.join(lines[2:]))
joined=' '.join(texts)
for term in ('Dehumanization','Explicit rating','Relationship questionnaire','Implicit task','association-strength','private belief','direct mind-reading','AI-generated educational visuals','diagnosis'):
 assert term in joined,term
assert 'नहीं' in joined
print(f'SRT_OK {len(blocks)} last_end {max(ends):.2f}')
