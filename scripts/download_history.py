import urllib.request,zipfile,io,hashlib,tempfile,json
from pathlib import Path
from import_history import build
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'BeisbolRadar RD research'}),timeout=60) as r:
  data=r.read(80000001)
  if len(data)>80000000: raise ValueError('download too large')
  print(r.status,r.geturl(),len(data),hashlib.sha256(data).hexdigest(),flush=True)
  return data
def unpack(data,dest,names):
 with zipfile.ZipFile(io.BytesIO(data)) as z:
  for name in names:
   matches=[i for i in z.infolist() if Path(i.filename).name.lower()==name.lower()]
   if len(matches)!=1: raise ValueError('missing or ambiguous '+name)
   (dest/name).write_bytes(z.read(matches[0]))
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)
 names=['People.csv','Batting.csv','Pitching.csv','readme2025.txt']
 # Pin mirror revision via public GitHub API; mirror provenance is not original verification.
 repo='myceliumdata/lahman-seed'
 sha=json.loads(get('https://api.github.com/repos/'+repo+'/commits/main'))['sha']
 base='https://raw.githubusercontent.com/'+repo+'/'+sha+'/lahman_1871-2025_csv/'
 for name in names: (p/name).write_bytes(get(base+name))
 retro=get('https://www.retrosheet.org/gamelogs/gl2025.zip')
 unpack(retro,p,['GL2025.TXT'])
 out=Path('review-history')
 build(p,p/'GL2025.TXT',out)
 (out/'provenance.json').write_text(json.dumps({'mirror':repo,'revision':sha,'original_verified':False,'retrosheet':'https://www.retrosheet.org/gamelogs/gl2025.zip'},indent=2))
 (out/'lahman-readme.txt').write_bytes((p/'readme2025.txt').read_bytes())
 for file in sorted(out.iterdir()): print(file,len(file.read_bytes()),hashlib.sha256(file.read_bytes()).hexdigest())
