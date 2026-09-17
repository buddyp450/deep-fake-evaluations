from pathlib import Path
import json,zipfile,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output'
manifest=json.loads((OUT/'asset_manifest.json').read_text());qa=json.loads((OUT/'media_qa.json').read_text())
assert len(manifest['cases'])==90 and all(c['available'] for c in manifest['cases'])
assert qa['checked']==90 and all(c['full_decode_ok'] for c in qa['files'])
assert json.loads((OUT/'visual_qa.json').read_text())['cloned']['masters_reviewed']==10
archive=ROOT/'Synthetic_Identity_Assets.zip'
repo=ROOT if (ROOT/'.git').is_dir() else ROOT/'github-transfer'
tracked=set(subprocess.check_output(['git','-C',str(repo),'ls-files'],text=True).splitlines())
files=[]
for c in manifest['cases']:
 video=OUT/c['file']
 assert video.is_file() and video.with_suffix('.json').is_file()
 assert hashlib.sha256(video.read_bytes()).hexdigest()==c['sha256']
 files.extend([video,video.with_suffix('.json')])
assert len(set(files))==180
assert not any('output/'+p.relative_to(OUT).as_posix() in tracked for p in files), 'Asset ZIP would overwrite a tracked file'
with zipfile.ZipFile(archive,'w',allowZip64=True) as z:
 for p in sorted(files):
  z.write(p,p.relative_to(OUT).as_posix(),compress_type=zipfile.ZIP_STORED if p.suffix=='.mp4' else zipfile.ZIP_DEFLATED)
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 assert len([n for n in z.namelist() if n.startswith('videos/') and n.endswith('.mp4')])==90
 assert len(z.namelist())==180 and all(n.startswith('videos/') for n in z.namelist())
sha=hashlib.sha256(archive.read_bytes()).hexdigest()
archive.with_suffix('.zip.sha256.txt').write_text(sha+'  '+archive.name+'\n')
print(f'Archive verified: {archive}; {archive.stat().st_size/1024/1024:.1f} MiB; SHA256 {sha}')
