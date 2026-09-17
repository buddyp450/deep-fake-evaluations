from pathlib import Path
import os, json, time
ROOT=Path(__file__).resolve().parents[1]
os.environ['HF_HOME']=str(ROOT/'models/huggingface')
os.environ['HF_HUB_DISABLE_XET']='1'
import truststore
truststore.inject_into_ssl()
import torch
import soundfile as sf
from chatterbox.tts import ChatterboxTTS
torch.set_num_threads(4)
torch.manual_seed(20260916)
text='This is a generated recording for a controlled detection test. The meeting begins at nine, and the agenda contains three items.'
start=time.time()
print('Loading Chatterbox on CUDA',flush=True)
model=ChatterboxTTS.from_pretrained(device='cuda')
print('Generating cloned speech',flush=True)
wav=model.generate(text,audio_prompt_path=str(ROOT/'assets/sources/gautam_voice_reference.wav'))
dest=ROOT/'assets/pilots/clone_indian_male.wav'
dest.parent.mkdir(exist_ok=True,parents=True)
sf.write(dest,wav.squeeze().detach().cpu().numpy(),model.sr)
dest.with_suffix('.json').write_text(json.dumps({'ground_truth':'cloned voice','source':'gautam_voice_reference.wav','model':'ResembleAI/chatterbox','script':text,'seed':20260916,'seconds':len(wav.squeeze())/model.sr,'elapsed_seconds':time.time()-start,'watermark':'Chatterbox built-in Perth watermark retained'},indent=2))
print(f'Saved {dest}',flush=True)
