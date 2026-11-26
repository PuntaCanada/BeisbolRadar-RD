import unittest,json,pathlib
P=pathlib.Path('public')
class Sponsorship(unittest.TestCase):
 def test_disabled(self):
  d=json.loads((P/'data/status.json').read_text())['sponsorship']
  self.assertIs(d['enabled'],False)
  self.assertEqual(d['placements'],[])
  for l in ('es','en','de','fr','it'):
   h=(P/l/'sponsorship/index.html').read_text()
   self.assertIn('class="hero"',h)
   self.assertIn('930',h)
   self.assertNotIn('mailto:',h)
   self.assertNotIn('wa.me',h)
 def test_csp(self):
  h=(P/'_headers').read_text()
  self.assertIn("script-src 'self' https://static.cloudflareinsights.com/beacon.min.js;",h)
  self.assertIn("connect-src 'self' https://cloudflareinsights.com;",h)
  self.assertNotIn("'unsafe-inline'",h)
