from __future__ import annotations
import argparse,json
from pathlib import Path
EXPECTED={'reel_0064_mind_wandering_what_studies_measure_hi.mp4','reel_0064_mind_wandering_what_studies_measure_narration_hi.wav','reel_0064_mind_wandering_what_studies_measure_captions_hi.srt','reel_0064_metadata.json','reel_0064_qc_report.json','reel_0064_mind_wandering_what_studies_measure_sources.md','reel_0064_mind_wandering_what_studies_measure_script.md','reel_0064_scene_01.png','reel_0064_scene_02.png','reel_0064_scene_03.png','reel_0064_scene_04.png'}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--listing',type=Path,required=True); ap.add_argument('--folder-id',required=True); ap.add_argument('--manifest-id',required=True); ap.add_argument('--output',type=Path); a=ap.parse_args()
 files=json.loads(a.listing.read_text(encoding='utf-8')).get('files',[]); current={f.get('name'):f for f in files if f.get('name') in EXPECTED}; manifests=[f for f in files if f.get('id')==a.manifest_id]
 missing=sorted(EXPECTED-set(current)); zero=sorted(n for n,f in current.items() if int(f.get('size',0) or 0)<=0); wrong=sorted(n for n,f in current.items() if a.folder_id not in (f.get('parents') or []))
 duplicate_names=sorted(n for n in EXPECTED if sum(1 for f in files if f.get('name')==n)>1)
 r={'folder_id':a.folder_id,'manifest_id':a.manifest_id,'expected_count':len(EXPECTED),'found_expected_count':len(current),'missing':missing,'zero_size':zero,'wrong_parent':wrong,'duplicate_expected_names':duplicate_names,'manifest_found_once':len(manifests)==1,'manifest_parent_ok':len(manifests)==1 and a.folder_id in (manifests[0].get('parents') or []),'manifest_nonzero':len(manifests)==1 and int(manifests[0].get('size',0) or 0)>0,'unrelated_remote_object_count':max(0,len(files)-len(current)-len(manifests)),'unrelated_remote_objects':sorted(f.get('name') for f in files if f.get('name') not in EXPECTED and f.get('id')!=a.manifest_id),'expected_objects':[{'name':n,'id':current[n].get('id'),'size':int(current[n].get('size',0) or 0),'mimeType':current[n].get('mimeType')} for n in sorted(current)]}
 r['valid']=not(missing or zero or wrong or duplicate_names or len(manifests)!=1 or not r['manifest_parent_ok'] or not r['manifest_nonzero'] or r['unrelated_remote_object_count']!=0); text=json.dumps(r,ensure_ascii=False,indent=2)+'\n'
 if a.output:a.output.write_text(text,encoding='utf-8')
 print(text,end=''); return 0 if r['valid'] else 1
if __name__=='__main__': raise SystemExit(main())
