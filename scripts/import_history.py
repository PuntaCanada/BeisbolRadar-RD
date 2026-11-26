"""Import reviewed local Lahman CSV and Retrosheet regular-season game logs; never fetch at runtime."""
import csv,json,hashlib,sys
from pathlib import Path
from collections import defaultdict
def rows(p):
 with p.open(encoding='utf-8-sig',newline='') as f: yield from csv.DictReader(f)
def write(p,d):
 p.write_text(json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n',encoding='utf-8')
def build(lahman,retro,out):
 files=[lahman/x for x in ['People.csv','Batting.csv','Pitching.csv','readme2025.txt']]
 if 'Attribution-ShareAlike 3.0' not in files[-1].read_text(encoding='utf-8-sig',errors='replace'): raise ValueError('license not found')
 people={p['playerID']:dict(id=p['playerID'],name=(p['nameFirst']+' '+p['nameLast']).strip(),city=p['birthCity'],seasons={}) for p in rows(files[0]) if p['birthCountry'].strip() in ('D.R.','Dominican Republic')}
 for path,kind,fields in [(files[1],'batting',['G','AB','H','HR','RBI','BB','SO']),(files[2],'pitching',['G','W','L','IPouts','ER','SO','BB'])]:
  seen=set()
  for a in rows(path):
   if a['playerID'] not in people or a['lgID'] not in ('AL','NL'): continue
   key=tuple(a[k] for k in ('playerID','yearID','stint','teamID','lgID'))
   if key in seen: raise ValueError('duplicate stint')
   seen.add(key)
   y=int(a['yearID'])
   if not 1871<=y<=2025: raise ValueError('year')
   d=people[a['playerID']]['seasons'].setdefault(str(y),{}).setdefault(kind,{})
   for k in fields:
    v=int(a[k]) if a[k].strip() else None
    if v is not None and v<0: raise ValueError('negative statistic')
    d[k]=None if v is None or (k in d and d[k] is None) else d.get(k,0)+v
 players=[]
 for p in people.values():
  if not p['seasons']: continue
  career={}
  for season in p['seasons'].values():
   for kind,vals in season.items():
    d=career.setdefault(kind,{})
    for k,v in vals.items(): d[k]=None if v is None or (k in d and d[k] is None) else d.get(k,0)+v
  p['career']=career;players.append(p)
 if not players: raise ValueError('no Dominican players')
 games=[];seen=set()
 with retro.open(encoding='utf-8-sig',newline='') as f:
  for a in csv.reader(f):
   if len(a)<11 or len(a[0])!=8 or not a[0].isdigit(): raise ValueError('game log schema')
   key=(a[0],a[1],a[3],a[6])
   if key in seen: raise ValueError('duplicate game')
   seen.add(key)
   if a[9].isdigit() and a[10].isdigit(): games.append(dict(date=a[0],number=a[1],away=a[3],home=a[6],awayRuns=int(a[9]),homeRuns=int(a[10])))
 if not games: raise ValueError('no games')
 out.mkdir(parents=True,exist_ok=True)
 write(out/'players.json',dict(source='SABR Lahman 2025',license='CC BY-SA 3.0',scope='Dominican Republic birthplace; AL/NL regular season',players=sorted(players,key=lambda x:x['id']),sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}))
 write(out/'history.json',dict(source='Retrosheet',sha256=hashlib.sha256(retro.read_bytes()).hexdigest(),games=games))
 print('Imported',len(players),'players;',len(games),'games')
if __name__=='__main__': build(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]))
