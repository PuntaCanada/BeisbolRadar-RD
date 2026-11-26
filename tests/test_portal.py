import unittest,json,pathlib,xml.etree.ElementTree as E
P=pathlib.Path('public')
class Portal(unittest.TestCase):
 def test_pages(self):
  for l in ('es','en','de','fr','it'):
   for s in ('','lidom','mlb','players','news','sponsorship','sources'):
    h=(P/l/s/'index.html').read_text(); self.assertIn('lang="'+l+'"',h); self.assertEqual(h.count('hreflang='),5)
 def test_sitemap(self):
  self.assertEqual(len(E.parse(P/'sitemap.xml').getroot()),35)
 def test_fail_closed(self):
  d=json.loads((P/'data/status.json').read_text()); self.assertFalse(d['sponsorship']['enabled']); self.assertEqual(d['games']+d['players']+d['news'],[])
