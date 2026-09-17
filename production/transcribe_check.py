from pathlib import Path
import argparse,subprocess,json
ROOT=Path(__file__).resolve().parents[1]
import torch,librosa
from transformers import WhisperProcessor,WhisperForConditionalGeneration
ap=argparse.ArgumentParser();ap.add_argument('files',nargs='+',type=Path);ap.add_argument('--start',type=float,default=0);a=ap.parse_args()
torch.set_num_threads(4)
processor=WhisperProcessor.from_pretrained(str(ROOT/'models/whisper'))
model=WhisperForConditionalGeneration.from_pretrained(str(ROOT/'models/whisper')).eval()
for file in a.files:
 temp=ROOT/'tmp'/f'{file.stem}-qa.wav'
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(a.start),'-i',str(file),'-t','30','-vn','-ac','1','-ar','16000',str(temp)],check=True)
 wav,_=librosa.load(temp,sr=16000)
 inputs=processor(wav,sampling_rate=16000,return_tensors='pt').input_features
 with torch.inference_mode():ids=model.generate(inputs,language='en',task='transcribe',max_new_tokens=200)
 text=processor.batch_decode(ids,skip_special_tokens=True)[0]
 result={'file':str(file),'start_seconds':a.start,'transcript':text,'method':'Whisper tiny automatic transcript; not a listening or accent verification'}
 print(json.dumps(result),flush=True)
