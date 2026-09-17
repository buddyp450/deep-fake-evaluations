from pathlib import Path
import os,json,time,subprocess
ROOT=Path(__file__).resolve().parents[1]
os.environ['HF_HOME']=str(ROOT/'models/huggingface')
os.environ['HF_HUB_DISABLE_XET']='1'
import truststore
truststore.inject_into_ssl()
import torch,soundfile as sf
from chatterbox.tts import ChatterboxTTS
torch.set_num_threads(4)
text=json.loads((ROOT/'assets/synthetic/voices/SYN_Male_Indian.json').read_text())['script']
device=os.environ.get('CLONE_DEVICE','cuda')
print('Loading cloned speech model on '+device,flush=True)
model=ChatterboxTTS.from_pretrained(device=device)
folder=ROOT/'assets/cloned/voices';folder.mkdir(parents=True,exist_ok=True)
for i,row in enumerate(json.loads((ROOT/'production/base_assets.json').read_text())):
 code=f"CLN_{row['gender']}_{row['accent']}";dest=folder/f'{code}.wav'
 if dest.exists():continue
 ref=ROOT/'assets/sources'/f"REF_{row['gender']}_{row['accent']}.wav"
 seed=20262000+i;torch.manual_seed(seed)
 print('Generating '+code,flush=True);start=time.time()
 wav=model.generate(text,audio_prompt_path=str(ref))
 raw=folder/f'{code}_raw.wav';sf.write(raw,wav.squeeze().detach().cpu().numpy(),model.sr)
 length=wav.shape[-1]/model.sr;speed=length/30
 if not .5<=speed<=2:raise RuntimeError(f'Unexpected generated duration {length}')
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(raw),'-af',f'atempo={speed},apad','-t','30','-ar','24000',str(dest)],check=True)
 dest.with_suffix('.json').write_text(json.dumps({'identity_type':'Cloned','person':row['person'],'reference':str(ref.relative_to(ROOT)),'gender':row['gender'],'accent_target':row['accent'],'accent_verified':False,'model':'ResembleAI/chatterbox','script':text,'seed':seed,'raw_duration':length,'atempo':speed,'duration':30,'elapsed_seconds':time.time()-start,'watermark':'Built-in Perth watermark retained in generated audio; survival after processing not verified'},indent=2))
 print('Saved '+code,flush=True)
