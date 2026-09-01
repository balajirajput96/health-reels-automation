import argparse,json
from pathlib import Path
EXPECTED={'reel_0073_goal_gradients_what_studies_measure_hi.mp4','reel_0073_goal_gradients_what_studies_measure_narration_hi.wav','reel_0073_goal_gradients_what_studies_measure_captions_hi.srt','reel_0073_metadata.json','reel_0073_qc_report.json','reel_0073_goal_gradients_what_studies_measure_sources.md','reel_0073_goal_gradients_what_studies_measure_script.md','reel_0073_scene_01.png','reel_0073_scene_02.png','reel_0073_scene_03.png','reel_0073_scene_04.png'}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--listing',type=Path,required=True); ap.add_argument('--folder-id',required=True); ap.add_argument('--manifest-id',required=True); ap.add_argument('--output',type=Path); a=ap.parse_args()
 files=json.loads(a.listing.read_text()).get('files',[]); current=[f for f in files if f.get('name') in EXPECTED]; by={f.get('name'):f for f in current}; manifests=[f for f in files if f.get('id')==a.manifest_id]
 missing=sorted(EXPECTED-set(by)); zero=sorted(n for n,f in by.items() if int(f.get('size',0) or 0)<=0); wrong=sorted(n for n,f in by.items() if a.folder_id not in (f.get('parents') or [])); dups=sorted(n for n in EXPECTED if sum(1 for f in files if f.get('name')==n)>1); unrelated=[f for f in files if f.get('name') not in EXPECTED and f.get('id')!=a.manifest_id]
 r={'folder_id':a.folder_id,'manifest_id':a.manifest_id,'expected_count':11,'found_expected_count':len(by),'missing':missing,'zero_size':zero,'wrong_parent':wrong,'duplicate_expected_names':dups,'manifest_found_once':len(manifests)==1,'manifest_parent_ok':len(manifests)==1 and a.folder_id in (manifests[0].get('parents') or []),'manifest_nonzero':len(manifests)==1 and int(manifests[0].get('size',0) or 0)>0,'unrelated_remote_object_count':len(unrelated),'unrelated_remote_objects':sorted(f.get('name') for f in unrelated),'expected_objects':[{'name':n,'id':by[n].get('id'),'size':int(by[n].get('size',0) or 0),'mimeType':by[n].get('mimeType')} for n in sorted(by)]}
 r['valid']=not(missing or zero or wrong or dups or len(manifests)!=1 or not r['manifest_parent_ok'] or not r['manifest_nonzero'] or unrelated); out=json.dumps(r,ensure_ascii=False,indent=2)+'\n'
 if a.output:a.output.write_text(out)
 print(out,end=''); return 0 if r['valid'] else 1
if __name__=='__main__': raise SystemExit(main())
