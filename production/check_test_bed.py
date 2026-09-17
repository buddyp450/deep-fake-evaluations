from pathlib import Path
import json,urllib.request,urllib.error
root=Path(__file__).resolve().parents[1];out=root/'output';base='http://127.0.0.1:8769/'
cases=json.loads((out/'asset_manifest.json').read_text())['cases']
for c in cases:
 p=out/c['file']
 with urllib.request.urlopen(urllib.request.Request(base+c['file'],method='HEAD')) as r:
  assert int(r.headers['Content-Length'])==p.stat().st_size
  assert r.headers['Content-Type']=='video/mp4'
 with urllib.request.urlopen(urllib.request.Request(base+c['file'],headers={'Range':'bytes=100-199'})) as r:
  assert r.status==206 and r.read()==p.read_bytes()[100:200]
for path,status,headers in [('PROJECT_STATE.md',404,{}),(cases[0]['file'],416,{'Range':'bytes=999999999-'}),('health',403,{'Origin':'https://example.com'})]:
 try:urllib.request.urlopen(urllib.request.Request(base+path,headers=headers));raise AssertionError(path)
 except urllib.error.HTTPError as e:assert e.code==status
print('90 video paths, MIME types, lengths and byte-range bodies passed; missing path, invalid range and foreign-origin checks passed.')
