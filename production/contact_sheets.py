from pathlib import Path
import subprocess
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];tmp=ROOT/'tmp/pdfs';tmp.mkdir(exist_ok=True,parents=True)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
for prefix in ['GEN','CLN','SYN']:
 files=sorted(p for p in (ROOT/'assets/masters').glob(prefix+'_*.mp4') if not p.stem.endswith('_silent'))
 if not files:continue
 canvas=Image.new('RGB',(1280,240*((len(files)+1)//2)),'white');draw=ImageDraw.Draw(canvas)
 for i,path in enumerate(files):
  x=(i%2)*640;y=(i//2)*240
  draw.text((x+6,y+5),path.stem,font=font,fill='black')
  for j,t in enumerate([5,20]):
   thumb=tmp/f'{path.stem}-{t}.jpg'
   subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(path),'-frames:v','1','-vf','scale=320:180:force_original_aspect_ratio=decrease,pad=320:180:(ow-iw)/2:(oh-ih)/2',str(thumb)],check=True)
   canvas.paste(Image.open(thumb),(x+j*320,y+32));draw.text((x+j*320+5,y+215),f'{t}s',font=font,fill='black')
 dest=tmp/f'{prefix}-contact-sheet.jpg';canvas.save(dest,quality=92);print(dest)
