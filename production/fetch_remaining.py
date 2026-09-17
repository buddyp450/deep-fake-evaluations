from pathlib import Path
import json,subprocess,hashlib
ROOT=Path(__file__).resolve().parents[1]
names={'File:Katherine Maher Access Interview Cropped.webm':'katherine_maher_original.webm','File:McGuinness, Mairead (en).webm':'mairead_mcguinness_original.webm','File:Jimmy Wales interview for WikipediaDay 2019.webm':'jimmy_wales_original.webm'}
records={}
for name in ['source_candidates.json','source_candidates_2.json']:
 for r in json.loads((ROOT/'production'/name).read_text(encoding='utf-8-sig'))['query']['pages'].values():records[r['title']]=r
for title,name in names.items():
 r=records[title];info=r['imageinfo'][0];dest=ROOT/'assets/sources'/name
 if not dest.exists() or dest.stat().st_size!=info['size']:
  print('Fetching '+name,flush=True)
  result=subprocess.run(['curl.exe','-L','--fail','--max-time','180',info['url'],'-o',str(dest),'--silent','--show-error'])
  if result.returncode:print('Stopped after failed request; no immediate retries',flush=True);break
 assert hashlib.sha1(dest.read_bytes()).hexdigest()==info['sha1']
 dest.with_suffix(dest.suffix+'.source.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
 print('Verified '+name,flush=True)
