from pathlib import Path
import sys,json,urllib.request,subprocess
import truststore
truststore.inject_into_ssl()
from range_download import download
repo,folder,*wanted=sys.argv[1:]
items=json.load(urllib.request.urlopen(f'https://huggingface.co/api/models/{repo}/tree/main?recursive=true'))
for item in items:
 name=item['path']
 if item['type']!='file' or (wanted and name not in wanted) or name=='.gitattributes':continue
 dest=Path(folder)/name;dest.parent.mkdir(parents=True,exist_ok=True)
 if dest.exists() and dest.stat().st_size==item['size']:continue
 url=f'https://huggingface.co/{repo}/resolve/main/{name}?download=true'
 if item['size']>32*1024*1024:download(url,dest,item['size'],item.get('lfs',{}).get('oid'))
 else:subprocess.run(['curl.exe','-L','--fail','--retry','3','--max-time','120',url,'-o',str(dest),'--silent','--show-error'],check=True)
 print(f'Ready {dest}',flush=True)
