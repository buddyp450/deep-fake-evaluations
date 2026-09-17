"""Deterministic baked connection-video effects; audio continues unchanged in time."""
from pathlib import Path
import subprocess, json, argparse, hashlib
ROOT=Path(__file__).resolve().parents[1]
PROFILES={
 'Good':{'width':1280,'height':720,'fps':30,'kbps':2500,'freezes':[]},
 'Patchy':{'width':854,'height':480,'fps':15,'kbps':600,'freezes':[[10,10.5],[20,20.5]]},
 'Degraded':{'width':640,'height':360,'fps':10,'kbps':200,'freezes':[[8,10],[16,18],[24,26]]},
}
def run(cmd):
 subprocess.run(cmd,check=True)
def probe(path):
 return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
def render(master,start_id,label,outdir):
 outdir.mkdir(parents=True,exist_ok=True)
 info=probe(master);duration=float(info['format']['duration'])
 for idx,(name,p) in enumerate(PROFILES.items()):
  dest=outdir/f'T{start_id+idx:02d}_{label}_{name}.mp4'
  filters=[f"scale={p['width']}:{p['height']}:force_original_aspect_ratio=decrease",f"pad={p['width']}:{p['height']}:(ow-iw)/2:(oh-ih)/2",'setsar=1']
  # Drop video samples inside freeze windows, retaining timestamps.
  # fps then fills the missing timestamps with the previous selected frame.
  for a,b in p['freezes']:
   filters.append(f"select='not(gte(t,{a})*lt(t,{b}))'")
  filters.append(f"fps={p['fps']}:round=up")
  run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(master),'-map','0:v:0','-map','0:a:0','-vf',','.join(filters),'-c:v','libx264','-preset','medium','-b:v',f"{p['kbps']}k",'-maxrate',f"{p['kbps']}k",'-bufsize',f"{p['kbps']*2}k",'-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-ar','48000','-movflags','+faststart','-t',str(duration),str(dest)])
  actual=probe(dest)
  actual['format']['filename']=dest.relative_to(ROOT).as_posix()
  meta={'test_id':f'T{start_id+idx:02d}','master':str(master.relative_to(ROOT)),'profile':name,'settings':p,'audio':'Continuous original timeline; AAC 128 kbps, 48 kHz','method':'Baked simulated connection effects; no live network shaping','sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'probe':actual,'qa_status':'technical checks only; playback and detector run pending'}
  dest.with_suffix('.json').write_text(json.dumps(meta,indent=2))
  assert abs(float(actual['format']['duration'])-duration)<0.15
  print(f'Created {dest.name}',flush=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('master',type=Path);ap.add_argument('--start-id',type=int,required=True);ap.add_argument('--label',required=True)
 args=ap.parse_args();render(args.master.resolve(),args.start_id,args.label,ROOT/'output/videos')
