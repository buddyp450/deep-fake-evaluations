from pathlib import Path
import json,subprocess
from render_variants import render
ROOT=Path(__file__).resolve().parents[1]
for a in json.loads((ROOT/'production/base_assets.json').read_text()):
 source=ROOT/'assets/sources'/a['source']
 if not source.exists():print('MISSING SOURCE',a['source'],flush=True);continue
 master=ROOT/'assets/masters'/f"GEN_{a['gender'][0]}_{a['accent']}.mp4"
 if not master.exists():subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(a['start']),'-i',str(source),'-t','30','-vf','scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30:start_time=0','-c:v','libx264','-crf','18','-c:a','aac','-b:a','128k',str(master)],check=True)
 reference=ROOT/'assets/sources'/f"REF_{a['gender']}_{a['accent']}.wav"
 reference_input=source if 'voice_reference_start' in a else master
 reference_start=a.get('voice_reference_start',5);reference_duration=a.get('voice_reference_duration',12)
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(reference_start),'-i',str(reference_input),'-t',str(reference_duration),'-vn','-ac','1','-ar','24000',str(reference)],check=True)
 master.with_suffix('.json').write_text(json.dumps({**a,'identity_type':'Genuine','changes':'30-second trim, resize/pad, fps conversion and re-encoding; original face and voice retained','accent_review':'candidate assignment; listening review pending'},indent=2))
 render(master,a['test_start'],f"Genuine_{a['gender']}_{a['accent']}",ROOT/'output/videos')
