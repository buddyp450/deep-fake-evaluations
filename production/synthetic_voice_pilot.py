from pathlib import Path
import os,json,time
ROOT=Path(__file__).resolve().parents[1]
os.environ['HF_HOME']=str(ROOT/'models/huggingface')
os.environ['HF_HUB_DISABLE_XET']='1'
import truststore
truststore.inject_into_ssl()
import torch,soundfile as sf
from qwen_tts import Qwen3TTSModel
torch.set_num_threads(4);torch.manual_seed(20260916)
text='This is a generated recording for a controlled detection test. The meeting begins at nine, and the agenda contains three items.'
instruct='An adult male voice with a clear general American English accent, medium pitch, calm conversational delivery, natural speaking pace. Clean studio audio.'
print('Loading Qwen VoiceDesign',flush=True);start=time.time()
tts=Qwen3TTSModel.from_pretrained(str(ROOT/'models/qwen-voice-design'),device_map='cuda:0',dtype=torch.bfloat16,attn_implementation='sdpa')
print('Designing a voice without a real-person reference',flush=True)
wavs,sr=tts.generate_voice_design(text=text,language='English',instruct=instruct,max_new_tokens=600)
dest=ROOT/'assets/pilots/synthetic_american_male.wav';dest.parent.mkdir(parents=True,exist_ok=True)
sf.write(dest,wavs[0],sr)
dest.with_suffix('.json').write_text(json.dumps({'ground_truth':'designed synthetic voice','model':'Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign','script':text,'voice_description':instruct,'reference_person':None,'seed':20260916,'elapsed_seconds':time.time()-start,'seconds':len(wavs[0])/sr,'accent_qa':'pending listening review'},indent=2))
print(f'Saved {dest}',flush=True)
