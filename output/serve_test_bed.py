"""Loopback-only, allowlisted test-pack server with MP4 byte-range support."""
from pathlib import Path
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from urllib.parse import urlsplit,unquote
import argparse,json,mimetypes,re,urllib.request,webbrowser
ROOT=Path(__file__).resolve().parent
APP='synthetic-identity-test-bed-v2'
PORT=8769
DOCS={'Review_Test_Pack.html','asset_manifest.json','SOURCE_CREDITS.md','PROVENANCE_AND_GENERATION.md','provenance.json','production_versions.json','QA_REPORT.md','media_qa.json','visual_qa.json','speech_qa.json','START_HERE.md','results_template.json','TEST_PROTOCOL.md'}
manifest=json.loads((ROOT/'asset_manifest.json').read_text(encoding='utf-8'))
ALLOW=DOCS|{c['file'] for c in manifest['cases']}|{c['file'].replace('.mp4','.json') for c in manifest['cases']}|{'previews/'+n for n in ['Genuine.jpg','Cloned.jpg','Fully_Synthetic.jpg']}
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_HEAD(self):self.serve(False)
 def do_GET(self):self.serve(True)
 def serve(self,body):
  valid_hosts={f'127.0.0.1:{PORT}',f'localhost:{PORT}'}
  if self.headers.get('Host') not in valid_hosts or self.headers.get('Sec-Fetch-Site')=='cross-site':self.send_error(403);return
  origin=self.headers.get('Origin')
  if origin and origin not in {'http://'+h for h in valid_hosts}:self.send_error(403);return
  key=unquote(urlsplit(self.path).path).lstrip('/') or 'Review_Test_Pack.html'
  if key=='health':
   data=json.dumps({'application':APP,'cases':len(manifest['cases'])}).encode()
   self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(data)));self.end_headers()
   if body:self.wfile.write(data)
   return
  if key not in ALLOW:self.send_error(404,'File is not part of the test pack');return
  path=(ROOT/key).resolve()
  if not path.is_relative_to(ROOT) or not path.is_file():self.send_error(404,'Test-pack file missing');return
  size=path.stat().st_size;start=0;end=size-1;status=200
  requested=self.headers.get('Range')
  if requested:
   m=re.fullmatch(r'bytes=(\d*)-(\d*)',requested)
   try:
    if not m or not any(m.groups()):raise ValueError()
    if m[1]:start=int(m[1]);end=min(int(m[2]),size-1) if m[2] else size-1
    else:
     suffix=int(m[2])
     if suffix<=0:raise ValueError()
     start=max(0,size-suffix)
    if start>end or start>=size:raise ValueError()
    status=206
   except ValueError:
    self.send_response(416);self.send_header('Content-Range',f'bytes */{size}');self.send_header('Content-Length','0');self.end_headers();return
  mime=mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
  if path.suffix=='.md':mime='text/plain; charset=utf-8'
  if path.suffix=='.html':mime='text/html; charset=utf-8'
  self.send_response(status);self.send_header('Content-Type',mime);self.send_header('Content-Length',str(end-start+1));self.send_header('Accept-Ranges','bytes');self.send_header('Cache-Control','no-cache');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Referrer-Policy','no-referrer')
  if status==206:self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
  self.end_headers()
  if not body:return
  try:
   with path.open('rb') as f:
    f.seek(start);remaining=end-start+1
    while remaining:
     block=f.read(min(256*1024,remaining))
     if not block:break
     self.wfile.write(block);remaining-=len(block)
  except (BrokenPipeError,ConnectionResetError,ConnectionAbortedError):pass
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--open',action='store_true');args=ap.parse_args();url=f'http://127.0.0.1:{PORT}/'
 try:server=ThreadingHTTPServer(('127.0.0.1',PORT),Handler)
 except OSError:
  try:
   with urllib.request.urlopen(url+'health',timeout=2) as r:existing=json.load(r)
   if existing.get('application')==APP:
    if args.open:webbrowser.open(url)
    return
  except Exception:pass
  raise RuntimeError(f'Port {PORT} is already in use by another application')
 if args.open:webbrowser.open(url)
 try:server.serve_forever()
 except KeyboardInterrupt:pass
 finally:server.server_close()
if __name__=='__main__':main()
