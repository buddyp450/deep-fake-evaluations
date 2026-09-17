from pathlib import Path
import json,subprocess,hashlib,concurrent.futures
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'output/media_qa.json'
old=json.loads(dest.read_text()).get('files',[]) if dest.exists() else []
cache={r['file']:r for r in old}
def check(path):
 name=path.name;sha=hashlib.sha256(path.read_bytes()).hexdigest()
 if name in cache and cache[name].get('sha256')==sha:return cache[name]
 info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
 video=next(s for s in info['streams'] if s['codec_type']=='video');audio=next(s for s in info['streams'] if s['codec_type']=='audio')
 meta=json.loads(path.with_suffix('.json').read_text());profile=meta['settings'];issues=[]
 if abs(float(info['format']['duration'])-30)>.16:issues.append('Unexpected duration')
 if (video['width'],video['height'])!=(profile['width'],profile['height']):issues.append('Resolution mismatch')
 if video['codec_name']!='h264' or audio['codec_name']!='aac':issues.append('Unexpected codec')
 a,b=map(int,video['avg_frame_rate'].split('/'))
 if abs(a/b-profile['fps'])>.01:issues.append('Frame rate mismatch')
 if meta['sha256']!=sha:issues.append('Manifest checksum mismatch')
 result=subprocess.run(['ffmpeg','-hide_banner','-v','error','-threads','2','-i',str(path),'-f','null','-'],capture_output=True,text=True)
 if result.returncode or result.stderr.strip():issues.append('Decode issue: '+result.stderr[:1000])
 print(name+(': OK' if not issues else ': '+str(issues)),flush=True)
 return {'file':name,'sha256':sha,'duration_seconds':float(info['format']['duration']),'width':video['width'],'height':video['height'],'fps':video['avg_frame_rate'],'full_decode_ok':not issues,'issues':issues}
files=sorted((ROOT/'output/videos').glob('T*.mp4'))
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(check,files))
dest.write_text(json.dumps({'scope':'Technical validation only; no listening review or detector execution','checked':len(results),'files':results},indent=2))
assert not [r for r in results if r['issues']]
print(f'Checked {len(results)} files',flush=True)
