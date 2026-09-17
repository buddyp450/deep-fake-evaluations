from pathlib import Path
import subprocess,sys,time,json
ROOT=Path(__file__).resolve().parents[1]
deadline=time.time()+3600
while not (ROOT/'output/videos/T60_Cloned_Female_Indian_Degraded.json').exists():
 if time.time()>deadline:raise TimeoutError('Clone batch has not completed; inspect render_clones.log')
 time.sleep(5)
for script in ['check_media.py','build_delivery.py','build_qa_summary.py','contact_sheets.py']:
 subprocess.run([sys.executable,str(ROOT/'production'/script)],check=True)
manifest=json.loads((ROOT/'output/asset_manifest.json').read_text())
assert len(manifest['cases'])==90 and all(c['available'] for c in manifest['cases'])
print('All 90 exports ready for final visual review',flush=True)
