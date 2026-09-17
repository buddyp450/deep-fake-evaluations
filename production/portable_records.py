"""Convert machine-specific project paths to portable relative record paths."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def portable(value):
 if isinstance(value,str):
  for prefix in [str(ROOT)+'\\',str(ROOT).replace('\\','/')+'/']:
   value=value.replace(prefix,'')
  return value
 if isinstance(value,list):return [portable(v) for v in value]
 if isinstance(value,dict):return {k:portable(v) for k,v in value.items()}
 return value
