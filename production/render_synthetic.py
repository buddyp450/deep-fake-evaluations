from pathlib import Path
import json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
for row in json.loads((ROOT/'production/base_assets.json').read_text()):
 code=f"SYN_{row['gender']}_{row['accent']}"
 master=ROOT/'assets/masters'/f'{code}.mp4'
 if not master.exists():
  subprocess.run([sys.executable,str(ROOT/'production/lipsync_pilot.py'),'--source',str(ROOT/'assets/synthetic'/f'{code}.png'),'--audio',str(ROOT/'assets/synthetic/voices'/f'{code}.wav'),'--output',str(master)],check=True)
 subprocess.run([sys.executable,str(ROOT/'production/render_variants.py'),str(master),'--start-id',str(row['test_start']+60),'--label',f"Synthetic_{row['gender']}_{row['accent']}"],check=True)
 print(f'Completed {code}',flush=True)
