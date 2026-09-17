from pathlib import Path
import os
ROOT=Path(__file__).resolve().parents[1]
os.environ['HF_HUB_DISABLE_XET']='1'
import truststore
truststore.inject_into_ssl()
from huggingface_hub import hf_hub_download
tasks={
 'TMElyralab/MuseTalk':('musetalk',['musetalkV15/musetalk.json','musetalkV15/unet.pth']),
 'stabilityai/sd-vae-ft-mse':('sd-vae',['config.json','diffusion_pytorch_model.bin']),
 'openai/whisper-tiny':('whisper',['config.json','pytorch_model.bin','preprocessor_config.json']),
 'ManyOtherFunctions/face-parse-bisent':('face-parse',['79999_iter.pth','resnet18-5c106cde.pth']),
}
for repo,(folder,files) in tasks.items():
 for name in files:
  print(f'Downloading {repo}/{name}',flush=True)
  hf_hub_download(repo_id=repo,filename=name,local_dir=ROOT/'models'/folder)
print('Video models ready',flush=True)
