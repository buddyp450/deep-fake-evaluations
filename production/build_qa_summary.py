from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output'
reference=json.loads((ROOT/'assets/synthetic/voices/SYN_Male_Indian.json').read_text())['script']
def words(s):return re.findall(r'[a-z]+',s.lower())
def distance(a,b):
 d=list(range(len(b)+1))
 for i,x in enumerate(a,1):
  new=[i]
  for j,y in enumerate(b,1):new.append(min(new[-1]+1,d[j]+1,d[j-1]+(x!=y)))
  d=new
 return d[-1]
records={}
for name in ['synthetic_speech_qa.jsonl','cloned_speech_qa.jsonl','scottish_voice_repair_qa.jsonl']:
 for line in (ROOT/'production'/name).read_text(encoding='utf-8-sig',errors='replace').splitlines():
  if not line.startswith('{'):continue
  r=json.loads(line);stem=Path(r['file']).stem
  r['file']=stem+'.wav';r['word_edit_distance_vs_script']=distance(words(reference),words(r['transcript']));r['reference_word_count']=len(words(reference));records[stem]=r
assert len(records)==20,len(records)
(OUT/'speech_qa.json').write_text(json.dumps({'method':'Whisper tiny automatic transcription of generated 30-second speech','limitation':'Transcription differences may be recognition errors or generation errors. This does not verify accent, voice likeness, naturalness or audiovisual synchronization.','script':reference,'files':list(records.values())},indent=2),encoding='utf-8')
qa=json.loads((OUT/'media_qa.json').read_text());assert all(r['full_decode_ok'] for r in qa['files'])
for r in qa['files']:
 profile=r['file'].rsplit('_',1)[1].split('.')[0];a,b=map(int,r['fps'].split('/'))
 assert a/b=={'Good':30,'Patchy':15,'Degraded':10}[profile]
summary=['# Production QA','',f"- {qa['checked']} exported videos checked: duration, dimensions, H.264/AAC formats, frame rates, matching hashes and full-file decoding.",'- Twenty generated speech files automatically transcribed. The Scottish female cloned speech was regenerated after an incomplete first attempt; the repaired file is the delivered version.',f"- Automatic transcript word differences range from {min(r['word_edit_distance_vs_script'] for r in records.values())} to {max(r['word_edit_distance_vs_script'] for r in records.values())} against the {len(words(reference))}-word script. These differences do not establish which words were actually spoken incorrectly.",'- All ten genuine and ten fully synthetic masters visually inspected at 5 and 20 seconds. Cloned master visual review status is recorded separately in visual_qa.json.','- Reference freeze checks on the genuine Indian male variants found approximately 0.53-second Patchy holds at 10 and 20 seconds and 2-second Degraded holds at 8, 16 and 24 seconds. All variants use the same rendering recipe.','- Review-page JavaScript syntax, 90 unique case IDs and outcome-classification logic checked. Browser UI validation was blocked by the browser tool local-file policy.','', '## Not verified','- Human listening: intended accents, voice resemblance, naturalness and audio quality.','- Continuous audiovisual synchronization and every frame of facial animation.','- Actual OBS audio routing, Teams reception, detector bot readiness or detector outputs.','- Statistical confidence or real-network response; these are outside the agreed production scope.','', 'No detector results are invented or pre-filled. Technical checks apply to media files, not detection accuracy.']
(OUT/'QA_REPORT.md').write_text('\n'.join(summary)+'\n',encoding='utf-8')
print(f'Speech QA: {len(records)} files; max word differences {max(r["word_edit_distance_vs_script"] for r in records.values())}')
