from pathlib import Path
import json,subprocess,hashlib,time
ROOT=Path(__file__).resolve().parents[1]
names={
 'File:Interview Netha Hussain.ogv':'netha_hussain_original.ogv',
 'File:Interview with a Tom McConn of Hollygrove, County Galway, Ireland in 2018.webm':'tom_mcconn_original.webm',
 'File:WIKITONGUES- Christine speaking Shetlandic.webm':'christine_deluca_original.webm',
 'File:WIKITONGUES- David speaking Doric Scots and English.webm':'david_campbell_original.webm',
 'File:WIKITONGUES- Simon speaking Cumbrian.webm':'simon_original.webm',
 'File:Jimmy Wales interview for WikipediaDay 2019.webm':'jimmy_wales_original.webm',
 'File:Katherine Maher Access Interview Cropped.webm':'katherine_maher_original.webm',
 'File:McGuinness, Mairead (en).webm':'mairead_mcguinness_original.webm',
 'File:Conference Welcome Shannon Eichelberger Wikimedia Community Ireland Lucy Crompton-Reid Wikimedia UK 25.09.2024 Celtic Knot Conference.mpg':'celtic_knot_welcome_original.mpg',
}
records=[]
for filename in ['source_candidates.json','source_candidates_2.json']:
 data=json.loads((ROOT/'production'/filename).read_text(encoding='utf-8-sig'))
 records.extend(data['query']['pages'].values())
def fetch(record):
 info=record['imageinfo'][0];dest=ROOT/'assets/sources'/names[record['title']]
 if not dest.exists() or dest.stat().st_size!=info['size']:
  subprocess.run(['curl.exe','-L','--fail','--retry','2','--retry-delay','30','--max-time','180',info['url'],'-o',str(dest),'--silent','--show-error'],check=True)
 h=hashlib.sha1()
 with dest.open('rb') as f:
  while block:=f.read(8*1024*1024):h.update(block)
 assert h.hexdigest()==info['sha1'],dest
 dest.with_suffix(dest.suffix+'.source.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
 print(f'Fetched and verified {dest.name}',flush=True)
for record in records:
 try:fetch(record)
 except Exception as e:print(f'NOT FETCHED: {record["title"]}: {e}',flush=True)
