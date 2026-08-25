from __future__ import annotations
import argparse
import json
from pathlib import Path

EXPECTED={
 'reel_0049_interleaving_what_studies_measure_hi.mp4',
 'reel_0049_interleaving_what_studies_measure_narration_hi.wav',
 'reel_0049_interleaving_what_studies_measure_captions_hi.srt',
 'reel_0049_metadata.json','reel_0049_qc_report.json',
 'reel_0049_interleaving_what_studies_measure_sources.md',
 'reel_0049_interleaving_what_studies_measure_script.md',
 'reel_0049_scene_01.png','reel_0049_scene_02.png','reel_0049_scene_03.png','reel_0049_scene_04.png'}

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--listing',type=Path,required=True); ap.add_argument('--folder-id',required=True); ap.add_argument('--manifest-id',required=True); ap.add_argument('--output',type=Path); args=ap.parse_args()
 files=json.loads(args.listing.read_text(encoding='utf-8')).get('files',[])
 current={f.get('name'):f for f in files if f.get('name') in EXPECTED}; manifests=[f for f in files if f.get('id')==args.manifest_id]
 missing=sorted(EXPECTED-set(current)); zero=sorted(n for n,f in current.items() if int(f.get('size',0) or 0)<=0); wrong=sorted(n for n,f in current.items() if args.folder_id not in (f.get('parents') or []))
 result={'folder_id':args.folder_id,'manifest_id':args.manifest_id,'expected_count':len(EXPECTED),'found_expected_count':len(current),'missing':missing,'zero_size':zero,'wrong_parent':wrong,'manifest_found_once':len(manifests)==1,'manifest_parent_ok':len(manifests)==1 and args.folder_id in (manifests[0].get('parents') or []),'manifest_nonzero':len(manifests)==1 and int(manifests[0].get('size',0) or 0)>0,'unrelated_remote_object_count':max(0,len(files)-len(current)-len(manifests)),'unrelated_remote_objects':sorted(f.get('name') for f in files if f.get('name') not in EXPECTED and f.get('id')!=args.manifest_id),'expected_objects':[{'name':n,'id':current[n].get('id'),'size':int(current[n].get('size',0) or 0),'mimeType':current[n].get('mimeType')} for n in sorted(current)]}
 result['valid']=not(missing or zero or wrong or len(manifests)!=1 or not result['manifest_parent_ok'] or not result['manifest_nonzero'])
 text=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
 if args.output: args.output.write_text(text,encoding='utf-8')
 print(text,end=''); return 0 if result['valid'] else 1
if __name__=='__main__': raise SystemExit(main())
