import hashlib,json,sys
from pathlib import Path
p=Path(sys.argv[1])
expected={'players.json':'1a927d37e411bb5dc56b35f0c62a08e9043c2eb6440f24677dfe21f9696df4c7','history.json':'b63376b99635ce66651fe57baf6ecb2d90feac036d9e52b4e5e023596cd28a7e','lahman-readme.txt':'b5e8251deebce363d583cd94bddd6fd134c6589ecfc64e13f11f8ba0dcd09e3a','provenance.json':'b8d3e5f99ddc0f34e8d985705bca8b1f3433d01463ba0c3a27b65ae9befe85b3'}
for n,digest in expected.items():
 assert hashlib.sha256((p/n).read_bytes()).hexdigest()==digest,n
players=json.loads((p/'players.json').read_text())['players']
games=json.loads((p/'history.json').read_text())['games']
assert len(players)==len({x['id'] for x in players})==930
assert sum(len(x['seasons']) for x in players)==4961
assert len(games)==len({(g['date'],g['number'],g['away'],g['home']) for g in games})==2430
for x in players:
 for kind,career in x['career'].items():
  for k,v in career.items():
   vals=[s[kind][k] for s in x['seasons'].values() if kind in s]
   assert v==(None if None in vals else sum(vals))
assert 'Attribution-ShareAlike 3.0' in (p/'lahman-readme.txt').read_text(encoding='utf-8-sig')
assert json.loads((p/'provenance.json').read_text())['revision']=='1a94791aa697cc817c8dbbde007a2b490507652b'
print('Verified 930 players, 4961 player seasons, 2430 games and four SHA-256 digests')
