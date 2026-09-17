from pathlib import Path
import json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
for kind,folder in [('cloned','cloned'),('synthetic','synthetic')]:
 dest=ROOT/'production'/f'{kind}_speech_qa.jsonl';done=set()
 if dest.exists():
  for line in dest.read_text(encoding='utf-8-sig',errors='replace').splitlines():
   if line.startswith('{'):
    done.add(Path(json.loads(line)['file']).name)
 missing=[str(p) for p in (ROOT/'assets'/folder/'voices').glob('*.wav') if not p.stem.endswith('_raw') and p.name not in done]
 if missing:
  with dest.open('a',encoding='utf-8') as f:subprocess.run([sys.executable,str(ROOT/'production/transcribe_check.py'),*missing],stdout=f,stderr=subprocess.STDOUT,check=True)
 print(kind+': missing transcripts added: '+str(len(missing)))
