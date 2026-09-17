"""Download large public model files in bounded ranges and verify SHA256."""
from pathlib import Path
import argparse,subprocess,concurrent.futures,hashlib,threading,time
def download(url,dest,size,sha256=None):
 dest=Path(dest);dest.parent.mkdir(parents=True,exist_ok=True)
 if dest.exists() and dest.stat().st_size==size:
  if not sha256 or file_hash(dest)==sha256:return
 staging=dest.with_suffix(dest.suffix+'.partial')
 with staging.open('wb') as f:f.truncate(size)
 lock=threading.Lock();done=0;chunk=32*1024*1024;started=time.time()
 def part(start):
  nonlocal done
  end=min(start+chunk,size)-1
  temp=dest.with_suffix(dest.suffix+f'.part-{start}')
  try:
   subprocess.run(['curl.exe','-L','--fail','--retry','3','--max-time','120','--range',f'{start}-{end}',url,'-o',str(temp),'--silent','--show-error'],check=True)
   if temp.stat().st_size!=end-start+1:raise ValueError('Unexpected range response size')
   with lock:
    with staging.open('r+b') as f:f.seek(start);f.write(temp.read_bytes())
    done+=end-start+1
    print(f'{dest.name}: {done/size:.0%}, {done/1024**2:.0f} MiB, {time.time()-started:.0f}s',flush=True)
  finally:
   if temp.exists():temp.unlink()
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(part,range(0,size,chunk)))
 if sha256 and file_hash(staging)!=sha256:raise ValueError('SHA256 mismatch')
 staging.replace(dest)
 print(f'Complete: {dest}',flush=True)
def file_hash(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  while data:=f.read(8*1024*1024):h.update(data)
 return h.hexdigest()
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('url');p.add_argument('dest');p.add_argument('size',type=int);p.add_argument('--sha256');a=p.parse_args();download(a.url,a.dest,a.size,a.sha256)
