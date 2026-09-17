"""MuseTalk 1.5 inference using supplied face boxes (pilot) or OpenCV tracking.
Uses the upstream pretrained generator and blending; avoids the separate pose-estimation stack.
"""
from pathlib import Path
import sys, os, argparse, json, time, subprocess
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools/MuseTalk'))
import torch, cv2, numpy as np
from transformers import WhisperModel
from musetalk.models.vae import VAE
from musetalk.models.unet import UNet, PositionalEncoding
from musetalk.utils.audio_processor import AudioProcessor
from musetalk.utils.face_parsing import FaceParsing
from musetalk.utils.blending import get_image

class LocalFaceParsing(FaceParsing):
 def model_init(self):
  return super().model_init(str(ROOT/'models/face-parse/resnet18-5c106cde.pth'),str(ROOT/'models/face-parse/79999_iter.pth'))

@torch.inference_mode()
def main(args):
 torch.set_num_threads(4);torch.manual_seed(20260916)
 box_file=ROOT/'production/face_boxes.json'
 if not args.box and box_file.exists():args.box=json.loads(box_file.read_text()).get(args.source.name)
 device='cuda';dtype=torch.float16;start=time.time()
 print('Loading MuseTalk, VAE and speech features',flush=True)
 vae=VAE(str(ROOT/'models/sd-vae'),use_float16=True)
 unet=UNet(str(ROOT/'models/musetalk/musetalkV15/musetalk.json'),str(ROOT/'models/musetalk/musetalkV15/unet.pth'),use_float16=True,device=device)
 unet.model.eval();vae.vae.eval()
 pe=PositionalEncoding().to(device=device,dtype=dtype)
 whisper=WhisperModel.from_pretrained(str(ROOT/'models/whisper')).to(device=device,dtype=dtype).eval()
 processor=AudioProcessor(str(ROOT/'models/whisper'))
 features,length=processor.get_audio_feature(str(args.audio))
 chunks=processor.get_whisper_chunk(features,device,dtype,whisper,length,fps=args.fps)
 del whisper;torch.cuda.empty_cache()
 fp=LocalFaceParsing()
 n=len(chunks)
 still=args.source.suffix.lower() in ['.png','.jpg','.jpeg']
 cap=None if still else cv2.VideoCapture(str(args.source))
 source_fps=0 if still else cap.get(cv2.CAP_PROP_FPS)
 source_count=0 if still else int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
 source_index=-1
 if not still and source_fps<=0:raise RuntimeError('Cannot determine source frame rate')
 image=cv2.imread(str(args.source)) if still else None
 if still:
  original_fp=fp
  cached_mask=[]
  def cached_fp(image,mode='raw'):
   if not cached_mask:cached_mask.append(original_fp(image,mode=mode))
   return cached_mask[0].copy()
  fp=cached_fp
 frames=[];boxes=[];latents=[]
 haar=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
 last=None
 print(f'Preparing {n} frames',flush=True)
 for i in range(n if not still else 1):
  if still: frame=image.copy()
  else:
   target_index=round(i*source_fps/args.fps)
   if target_index>=source_count:
    if target_index-source_count>1:raise RuntimeError('Source video is shorter than generated speech')
    target_index=source_count-1
   while source_index<target_index:
    ok,frame=cap.read();source_index+=1
    if not ok: raise RuntimeError('Source video is shorter than generated speech')
  if args.box: box=tuple(args.box)
  else:
   factor=min(1,640/frame.shape[1])
   gray=cv2.cvtColor(cv2.resize(frame,None,fx=factor,fy=factor),cv2.COLOR_BGR2GRAY)
   detections=haar.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(int(70*factor),int(70*factor)))
   if last is not None:
    cx,cy=(last[0]+last[2])/2,(last[1]+last[3])/2
    old_w,old_h=last[2]-last[0],last[3]-last[1]
    detections=[d for d in detections if abs((d[0]+d[2]/2)/factor-cx)<old_w*.7 and abs((d[1]+d[3]/2)/factor-cy)<old_h*.7 and .6<d[2]/factor/old_w<1.6]
   if len(detections):
    x,y,w,h=np.array(max(detections,key=lambda q:q[2]*q[3]))/factor;box=np.array([x,y,x+w,min(frame.shape[0],y+h+10)],dtype=float)
    if last is not None:box=.6*last+.4*box
    last=box;box=tuple(box.astype(int))
   elif last is not None:box=tuple(last.astype(int))
   else:raise RuntimeError('No face detected; provide reviewed --box x1 y1 x2 y2')
  x1,y1,x2,y2=box
  crop=cv2.resize(frame[y1:y2,x1:x2],(256,256),interpolation=cv2.INTER_LANCZOS4)
  latents.append(vae.get_latents_for_unet(crop));frames.append(frame);boxes.append(box)
  if i%50==0:print(f'Prepared {i+1}/{n}',flush=True)
 if cap:cap.release()
 h,w=frames[0].shape[:2]
 args.output.parent.mkdir(parents=True,exist_ok=True)
 silent=args.output.with_name(args.output.stem+'_silent.mp4')
 writer=cv2.VideoWriter(str(silent),cv2.VideoWriter_fourcc(*'mp4v'),args.fps,(w,h))
 ts=torch.tensor([0],device=device)
 print('Generating synchronized mouth motion',flush=True)
 for first in range(0,n,args.batch):
  ids=list(range(first,min(n,first+args.batch)))
  latent=torch.cat([latents[0 if still else i] for i in ids]).to(dtype=dtype)
  pred=unet.model(latent,ts,encoder_hidden_states=pe(chunks[ids].to(device=device,dtype=dtype))).sample
  images=vae.decode_latents(pred)
  for i,result in zip(ids,images):
   j=0 if still else i;box=boxes[j];x1,y1,x2,y2=box
   face=cv2.resize(result,(x2-x1,y2-y1))
   output=get_image(frames[j],face,box,mode='jaw',fp=fp)
   writer.write(output)
  if first%40==0:print(f'Rendered {first}/{n}',flush=True)
 writer.release()
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(silent),'-i',str(args.audio),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-shortest','-movflags','+faststart',str(args.output)],check=True)
 args.output.with_suffix('.json').write_text(json.dumps({'source':str(args.source),'audio':str(args.audio),'generator':'TMElyralab/MuseTalk 1.5','face_localization':'reviewed fixed box' if args.box else 'OpenCV Haar detector with smoothed boxes','frames':n,'fps':args.fps,'elapsed_seconds':time.time()-start,'status':'generated; visual/playback QA required','still_source':still,'face_mask_cache':still},indent=2))
 print(f'Saved {args.output}',flush=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--audio',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--box',nargs=4,type=int);ap.add_argument('--fps',type=int,default=25);ap.add_argument('--batch',type=int,default=8)
 main(ap.parse_args())
