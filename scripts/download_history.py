import urllib.request,zipfile,io,hashlib,re,json,tempfile
from pathlib import Path
from import_history import build
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 BeisbolRadar RD research'}),timeout=60) as r:
  data=r.read(80000001)
  if len(data)>80000000: raise ValueError('download too large')
  print(r.status,r.geturl(),len(data),hashlib.sha256(data).hexdigest(),flush=True)
  return data
def unpack(data,dest,names):
 with zipfile.ZipFile(io.BytesIO(data)) as z:
  for name in names:
   matches=[i for i in z.infolist() if Path(i.filename).name.lower()==name.lower()]
   if len(matches)!=1: raise ValueError('missing or ambiguous '+name+'; archive: '+str(z.namelist()[:80]))
   (dest/name).write_bytes(z.read(matches[0]))
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)
 # Public Box shared link from official SABR release; direct download endpoint.
 share='y1prhc795jk8zvmelfd3jq7tl389y6cd'
 lahman=get('https://sabr.app.box.com/shared/static/'+share+'.zip')
 unpack(lahman,p,['People.csv','Batting.csv','Pitching.csv','readme2025.txt'])
 retro=get('https://www.retrosheet.org/gamelogs/gl2025.zip')
 unpack(retro,p,['GL2025.TXT'])
 out=Path('review-history')
 build(p,p/'GL2025.TXT',out)
 for file in sorted(out.glob('*.json')):
  print(file,len(file.read_bytes()),hashlib.sha256(file.read_bytes()).hexdigest())
