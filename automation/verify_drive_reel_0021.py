from __future__ import annotations
import argparse, json
from pathlib import Path
EXPECTED={
'reel_0021_sensory_integration_what_studies_measure_hi.mp4',
'reel_0021_sensory_integration_what_studies_measure_narration_hi.wav',
'reel_0021_sensory_integration_what_studies_measure_captions_hi.srt',
'reel_0021_metadata.json','reel_0021_qc_report.json',
'reel_0021_sensory_integration_what_studies_measure_sources.md',
'reel_0021_sensory_integration_what_studies_measure_script.md',
'reel_0021_scene_01.png','reel_0021_scene_02.png','reel_0021_scene_03.png','reel_0021_scene_04.png'}
def main():
    p=argparse.ArgumentParser(); p.add_argument('--listing',type=Path,required=True); p.add_argument('--folder-id',required=True); p.add_argument('--manifest-id',required=True); p.add_argument('--output',type=Path); a=p.parse_args()
    files=json.loads(a.listing.read_text(encoding='utf-8')).get('files',[])
    current={x.get('name'):x for x in files if x.get('name') in EXPECTED}
    manifests=[x for x in files if x.get('id')==a.manifest_id]
    missing=sorted(EXPECTED-set(current)); zero=sorted(n for n,x in current.items() if int(x.get('size',0) or 0)<=0); wrong=sorted(n for n,x in current.items() if a.folder_id not in (x.get('parents') or []))
    result={'folder_id':a.folder_id,'manifest_id':a.manifest_id,'expected_count':len(EXPECTED),'found_expected_count':len(current),'missing':missing,'zero_size':zero,'wrong_parent':wrong,'manifest_found_once':len(manifests)==1,'manifest_parent_ok':len(manifests)==1 and a.folder_id in (manifests[0].get('parents') or []),'manifest_nonzero':len(manifests)==1 and int(manifests[0].get('size',0) or 0)>0,'unrelated_remote_object_count':max(0,len(files)-len(current)-len(manifests)),'expected_objects':[{'name':n,'id':current[n].get('id'),'size':int(current[n].get('size',0) or 0),'mimeType':current[n].get('mimeType')} for n in sorted(current)]}
    result['valid']=not (missing or zero or wrong or len(manifests)!=1 or not result['manifest_parent_ok'] or not result['manifest_nonzero'])
    text=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if a.output: a.output.write_text(text,encoding='utf-8')
    print(text,end=''); return 0 if result['valid'] else 1
if __name__=='__main__': raise SystemExit(main())
