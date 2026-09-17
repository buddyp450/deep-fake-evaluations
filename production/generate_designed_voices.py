from pathlib import Path
import os,json,time,subprocess
ROOT=Path(__file__).resolve().parents[1]
os.environ['HF_HOME']=str(ROOT/'models/huggingface')
import torch,soundfile as sf
from qwen_tts import Qwen3TTSModel
torch.set_num_threads(4)
text='Thank you for making time for this meeting. I would like to begin with a short update on the project. We have finished the initial review and collected the information needed for the next stage. Today, we can discuss the outstanding questions, agree on the order of the remaining activities, and confirm who will take responsibility for each item. After the meeting, I will prepare a brief summary so that everyone has the same understanding of the next steps and the expected schedule.'
accents={'UK-Irish':'Irish English','UK-British':'standard southern English, England','UK-Scottish':'Scottish English','American':'general American English','Indian':'Indian English'}
model=Qwen3TTSModel.from_pretrained(str(ROOT/'models/qwen-voice-design'),device_map='cuda:0',dtype=torch.bfloat16,attn_implementation='sdpa')
folder=ROOT/'assets/synthetic/voices';folder.mkdir(parents=True,exist_ok=True)
for gender in ['Male','Female']:
 for i,(accent,description) in enumerate(accents.items()):
  code=f'SYN_{gender}_{accent}';dest=folder/f'{code}.wav'
  if dest.exists():continue
  seed=20261000+i+(10 if gender=='Female' else 0);torch.manual_seed(seed)
  instruction=f'An adult {gender.lower()} speaking English with a clearly recognizable {description} accent. Calm natural conversational delivery, medium pitch, clear pronunciation, moderate pace. Clean recording.'
  print(f'Generating {code}',flush=True);start=time.time()
  wavs,sr=model.generate_voice_design(text=text,language='English',instruct=instruction,max_new_tokens=1200)
  raw=folder/f'{code}_raw.wav';sf.write(raw,wavs[0],sr)
  length=len(wavs[0])/sr;speed=length/30
  if not .5<=speed<=2:raise RuntimeError(f'Unexpected generated duration {length}')
  subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(raw),'-af',f'atempo={speed},apad','-t','30','-ar','24000',str(dest)],check=True)
  dest.with_suffix('.json').write_text(json.dumps({'identity_type':'Fully synthetic','gender':gender,'accent_target':accent,'accent_verified':False,'model':'Qwen3-TTS-12Hz-1.7B-VoiceDesign','reference_person':None,'instruction':instruction,'script':text,'seed':seed,'raw_duration':length,'atempo':speed,'duration':30,'elapsed_seconds':time.time()-start},indent=2))
  print(f'Saved {code}',flush=True)
