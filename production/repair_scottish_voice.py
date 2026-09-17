from pathlib import Path
import os,json,subprocess,time
ROOT=Path(__file__).resolve().parents[1]
os.environ['HF_HOME']=str(ROOT/'models/huggingface')
import truststore
truststore.inject_into_ssl()
import torch,soundfile as sf,numpy as np
from chatterbox.tts import ChatterboxTTS
torch.set_num_threads(4)
code='CLN_Female_UK-Scottish';folder=ROOT/'assets/cloned/voices';dest=folder/f'{code}.wav'
meta=json.loads(dest.with_suffix('.json').read_text());text=meta['script']
sentences=text.split('. ');chunks=['. '.join(sentences[:3])+'.','. '.join(sentences[3:4])+'.','. '.join(sentences[4:])]
model=ChatterboxTTS.from_pretrained(device='cuda');parts=[];start=time.time()
for i,chunk in enumerate(chunks):
 torch.manual_seed(20263007+i)
 print('Generating repair section '+str(i+1),flush=True)
 wav=model.generate(chunk,audio_prompt_path=str(ROOT/meta['reference']),temperature=.6,exaggeration=.3)
 parts.extend([wav.squeeze().detach().cpu().numpy(),np.zeros(int(model.sr*.15))])
audio=np.concatenate(parts);raw=folder/f'{code}_raw.wav';sf.write(raw,audio,model.sr)
length=len(audio)/model.sr;speed=length/30
assert .5<=speed<=2,length
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(raw),'-af',f'atempo={speed},apad','-t','30','-ar','24000',str(dest)],check=True)
meta.update({'seed':[20263007+i for i in range(len(chunks))],'raw_duration':length,'atempo':speed,'elapsed_seconds':time.time()-start,'repair':'Original generation omitted script sections; regenerated in three chunks','generation_settings':{'temperature':.6,'exaggeration':.3,'pause_seconds':.15}})
dest.with_suffix('.json').write_text(json.dumps(meta,indent=2));print('Repair saved',flush=True)
