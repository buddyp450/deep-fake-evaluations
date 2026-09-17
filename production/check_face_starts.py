from pathlib import Path
import cv2,json
ROOT=Path(__file__).resolve().parents[1];haar=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
rows=[]
for p in sorted((ROOT/'assets/masters').glob('GEN_*.mp4')):
 cap=cv2.VideoCapture(str(p));ok,frame=cap.read();cap.release()
 factor=min(1,640/frame.shape[1]);small=cv2.resize(frame,None,fx=factor,fy=factor)
 det=haar.detectMultiScale(cv2.cvtColor(small,cv2.COLOR_BGR2GRAY),scaleFactor=1.1,minNeighbors=5,minSize=(int(70*factor),int(70*factor)))
 boxes=[(b/factor).astype(int).tolist() for b in det]
 rows.append({'file':p.name,'boxes_xywh':boxes})
 print(p.name,boxes)
 if not boxes:cv2.imwrite(str(ROOT/'tmp/pdfs'/f'{p.stem}-first.jpg'),frame)
(ROOT/'production/face_start_checks.json').write_text(json.dumps(rows,indent=2))
