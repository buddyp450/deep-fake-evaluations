from pathlib import Path
import json,re,html,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output'
rows=json.loads((ROOT/'production/base_assets.json').read_text())
def plain(s):return html.unescape(re.sub('<[^>]+>','',s)).strip()
source_records={}
credits=['# Source credits and transformations','', 'These recordings are used as genuine baselines and as inputs to clearly identified cloned test media. Generated speech is not a statement made by the represented person. No endorsement by a speaker, author or source organization is implied. Retain these credits with copies of the test assets.','']
for row in rows:
 path=ROOT/'assets/sources'/row['source'];side=path.with_suffix(path.suffix+'.source.json')
 if side.exists():
  info=json.loads(side.read_text(encoding='utf-8-sig'))['imageinfo'][0];m=info['extmetadata']
  record={'title':plain(m.get('ObjectName',{}).get('value',row['source'])),'author':plain(m['Artist']['value']),'page':info['descriptionurl'],'license':m['LicenseShortName']['value'],'license_url':m['LicenseUrl']['value'],'original_sha1':info['sha1']}
 else:
  assert row['person']=='Gautam John'
  record={'title':'WikipediansSpeak-Gautam John','author':'Subhashish Panigrahi (Centre for Internet and Society / Access To Knowledge)','page':'https://commons.wikimedia.org/wiki/File:WikipediansSpeak-Gautam_John.webm','license':'CC BY-SA 3.0','license_url':'https://creativecommons.org/licenses/by-sa/3.0/','original_sha1':'979d9c1ce8a01ff62361e1c75ce6fda5e2225812'}
 assert hashlib.sha1(path.read_bytes()).hexdigest()==record['original_sha1']
 source_records[row['source']]=record
 credits += [f"## {row['person']} / {row['gender']} / {row['accent']}",f"- Work: {record['title']}",f"- Author: {record['author']}",f"- Source: {record['page']}",f"- License: {record['license']} - {record['license_url']}",f"- Original SHA1: {record['original_sha1']}",f"- Genuine excerpt: {row['start']}-{row['start']+30} seconds; trim, resize, frame-rate conversion and encoding.",'- Cloned derivatives: reference-conditioned Chatterbox speech and MuseTalk lip replacement of the real person; generated speech replaces the original audio. Derivatives are distributed under the same Creative Commons license listed above.','- Connection derivatives: re-encoding, resolution/frame-rate reduction, and timed frame holds for Patchy/Degraded.', '']
credits += ['## Fully synthetic people','- Invented portraits generated with the built-in image-generation tool; no real-person reference was supplied. Individual prompt records are beside the portrait files under assets/synthetic.','- Voices are generated from text descriptions using Qwen3-TTS VoiceDesign. No real-person audio reference is used for these voices.','- MuseTalk generates lip motion. The portrait outside the animated face region remains still.','- Gender/accent values are test labels and targets. Accent is not inferred from appearance and requires listening review.','', '## Generation software and model references','- Chatterbox: https://github.com/resemble-ai/chatterbox (repository license included under tools/chatterbox). Built-in watermark is retained at generation; detectability after encoding is unverified.','- Qwen3-TTS: https://github.com/QwenLM/Qwen3-TTS and https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign .','- MuseTalk: https://github.com/TMElyralab/MuseTalk and https://huggingface.co/TMElyralab/MuseTalk . Repository and model/component terms apply separately.','- Speech features: https://huggingface.co/openai/whisper-tiny . VAE: https://huggingface.co/stabilityai/sd-vae-ft-mse .','- The local tools directories retain upstream license files. Sources and model versions are independent of detector results.','']
(OUT/'SOURCE_CREDITS.md').write_text('\n'.join(credits),encoding='utf-8')
cases=[]
for group,offset,prefix,label in [('Genuine',0,'GEN','Genuine'),('Cloned',30,'CLN','Cloned'),('Fully synthetic',60,'SYN','Synthetic')]:
 for row in rows:
  for i,profile in enumerate(['Good','Patchy','Degraded']):
   tid=f"T{row['test_start']+offset+i:02d}";name=f"{tid}_{label}_{row['gender']}_{row['accent']}_{profile}.mp4";video=OUT/'videos'/name
   meta=json.loads(video.with_suffix('.json').read_text()) if video.with_suffix('.json').exists() else {}
   case={'test_id':tid,'identity_type':group,'source_identity_label':'Deepfake' if offset==60 else group,'gender':row['gender'],'accent_target':row['accent'],'accent_review':'Pending human listening review','profile':profile,'expected':['Not fake'] if not offset else ['Fake','Inconclusive'],'file':'videos/'+name,'available':video.exists() and bool(meta),'sha256':meta.get('sha256'),'duration_seconds':float(meta['probe']['format']['duration']) if meta else None,'source_person':row['person'] if offset<60 else None,'source_record':source_records[row['source']] if offset<60 else None,'detector_status':'Not run','notes':[]}
   if offset<60 and row['accent']=='UK-Irish' and row['gender']=='Male':case['notes'].append('Genuine excerpt contains interviewer interjections. Clone reference uses original 342-349 seconds; separate from genuine excerpt. Mixed-speaker audio is a known limitation of the genuine case.')
   if offset<60 and row['accent']=='UK-British' and row['gender']=='Male':case['notes'].append('Cumbrian regional English source includes discussion of dialect vocabulary; broad original UK-British label retained.')
   if offset<60 and row['accent']=='UK-Scottish' and row['gender']=='Male':case['notes'].append('Excerpt moved to English storytelling at 290 seconds; earlier Doric passage excluded.')
   if offset==60:case['notes'].append('Invented still portrait with generated mouth movement and designed voice; no natural head/body motion.')
   cases.append(case)
manifest={'version':1,'scope':'90-case working test set; no detector runs performed','cases':cases}
(OUT/'asset_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(OUT/'results_template.json').write_text(json.dumps({'schema_version':1,'environment':{'tester':'','teams_version':'','obs_version':'','detector_version_configuration':'','audio_route':'','meeting_reference':''},'runs':[],'case_ids':[c['test_id'] for c in cases]},indent=2),encoding='utf-8')
template=(ROOT/'production/review_template.html').read_text(encoding='utf-8')
(OUT/'Review_Test_Pack.html').write_text(template.replace('__CASES__',json.dumps(cases).replace('</','<\\/')),encoding='utf-8')
print(f"Manifest: {sum(c['available'] for c in cases)}/90 files available")
