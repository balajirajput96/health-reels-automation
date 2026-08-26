from pathlib import Path
import re,sys
p=Path(__file__).resolve().parents[1]/'assets/reel_0074_expectancy_value_what_studies_measure_captions_hi.srt'
text=p.read_text(encoding='utf-8').strip(); blocks=[b for b in text.split('\n\n') if b.strip()]
assert len(blocks)==15, len(blocks)
prev=0.0
for i,b in enumerate(blocks,1):
 lines=b.splitlines(); assert lines[0]==str(i), (i,lines[0]); m=re.match(r'(\d\d):(\d\d):(\d\d),(\d\d\d) --> (\d\d):(\d\d):(\d\d),(\d\d\d)$',lines[1]); assert m, lines[1]
 vals=[int(x) for x in m.groups()]; start=vals[0]*3600+vals[1]*60+vals[2]+vals[3]/1000; end=vals[4]*3600+vals[5]*60+vals[6]+vals[7]/1000
 assert start>=prev and end>start and end<=63.68+1e-6, (i,start,end); prev=end
body=' '.join(line for b in blocks for line in b.splitlines()[2:])
for term in ('Expectancy','Value','Cost','questionnaires','self-report','Relationship','diagnosis','personal assessment'):
 assert term.lower() in body.lower(), term
assert not any(x in body.lower() for x in ('guaranteed','guarantee है','हर व्यक्ति','सदा'))
print('R0074_CAPTIONS_OK cues=15 end=63.680')
