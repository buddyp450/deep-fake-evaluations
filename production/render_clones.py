from pathlib import Path
import json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
for row in json.loads((ROOT/'production/base_assets.json').read_text()):
 code=f"CLN_{row['gender']}_{row['accent']}"
 master=ROOT/'assets/masters'/f'{code}.mp4'
 if not master.exists():
  subprocess.run([sys.executable,str(ROOT/'production/lipsync_pilot.py'),'--source',str(ROOT/'assets/masters'/f"GEN_{row['gender'][0]}_{row['accent']}.mp4"),'--audio',str(ROOT/'assets/cloned/voices'/f'{code}.wav'),'--output',str(master)],check=True)
 outputs=[ROOT/'output/videos'/f"T{row['test_start']+30+i:02d}_Cloned_{row['gender']}_{row['accent']}_{profile}.json" for i,profile in enumerate(['Good','Patchy','Degraded'])]
 if not all(p.exists() for p in outputs):subprocess.run([sys.executable,str(ROOT/'production/render_variants.py'),str(master),'--start-id',str(row['test_start']+30),'--label',f"Cloned_{row['gender']}_{row['accent']}"],check=True)
 print('Completed '+code,flush=True)
