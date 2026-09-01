from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'assets/reel_0075_self_determination_what_studies_measure_captions_hi.srt'
text=p.read_text(encoding='utf-8')
blocks=[b for b in re.split(r'\n\s*\n',text.strip()) if b.strip()]
assert len(blocks)==15, len(blocks)
prev=0.0; last=0.0; body=[]
for i,b in enumerate(blocks,1):
 lines=b.splitlines(); assert lines[0].strip()==str(i), (i,lines[:1])
 m=re.match(r'(\d\d):(\d\d):(\d\d),(\d\d\d) --> (\d\d):(\d\d):(\d\d),(\d\d\d)$',lines[1]); assert m, lines[1]
 vals=list(map(int,m.groups())); start=vals[0]*3600+vals[1]*60+vals[2]+vals[3]/1000; end=vals[4]*3600+vals[5]*60+vals[6]+vals[7]/1000
 assert start>=prev and end>start, (i,start,end,prev); prev=end; last=end; body.append(' '.join(lines[2:]))
assert abs(last-69.48)<0.01, last
joined=' '.join(body).lower()
for term in ('autonomy','competence','relatedness','questionnaires','domain-specific','engagement','persistence','diagnose','personal assessment'):
 assert term in joined, term
assert 'सीधे नहीं पढ़तीं' in joined and 'अलग evidence' in joined
print(f'R0075_CAPTIONS_OK cues={len(blocks)} end={last:.3f}')
