from playwright.sync_api import sync_playwright
from subprocess import Popen
from pathlib import Path
import urllib.request,time
server=Popen(['python3','-m','http.server','8767','--directory','public'])
try:
 for _ in range(50):
  try:
   urllib.request.urlopen('http://127.0.0.1:8767/').close();break
  except OSError: time.sleep(.1)
 Path('visual-review').mkdir(exist_ok=True)
 with sync_playwright() as p:
  browser=p.chromium.launch()
  for width,height in ((1440,1000),(390,844)):
   for theme in ('light','dark'):
    page=browser.new_page(viewport={'width':width,'height':height},color_scheme=theme)
    for lang in ('es','en','de','fr','it'):
     page.goto('http://127.0.0.1:8767/'+lang+'/')
     page.wait_for_selector('main[data-ready=true]')
     assert page.locator('#count-players').inner_text()=='930'
     assert page.locator('#leaders .rank-row').count()==5
     assert page.locator('#decades progress').count()>0
     assert page.locator('#recent .score-row').count()==5
     for item in page.locator('#recent time').all():
      y,m,d=item.get_attribute('datetime').split('-')
      assert item.inner_text()==(f'{m}/{d}/{y}' if lang=='en' else f'{d}.{m}.{y}' if lang=='de' else f'{d}/{m}/{y}')
     assert page.locator('.team').count()==6
     before=page.locator('#leaders').inner_text()
     page.locator('#metric').select_option('pitching.W')
     assert page.locator('#leaders').inner_text()!=before
     assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
     page.locator('#metric').select_option('batting.HR')
     if lang in ('es','de'): page.screenshot(path=f'visual-review/{lang}-{width}-{theme}-home.png',full_page=True)
     page.locator('#player-query').fill('Fernando Abad')
     page.locator('.search-panel button').click()
     page.locator('tbody button',has_text='Fernando Abad').wait_for()
     assert page.locator('tbody tr').count()==1
     page.locator('tbody button').click()
     assert page.locator('h2').inner_text()=='Fernando Abad'
     assert page.locator('.profile-metrics strong').all_inner_texts()==['11','406','9','292']
     assert page.locator('.scroll-hint').count()==2
     if lang=='es': page.screenshot(path=f'visual-review/{lang}-{width}-{theme}-profile.png',full_page=True)
     page.goto('http://127.0.0.1:8767/'+lang+'/mlb/')
     page.locator('input[type=search]').fill('20250318')
     page.locator('tbody tr').first.wait_for()
     assert page.locator('tbody tr').count()>0
     assert page.locator('tbody tr').first.locator('td').nth(1).inner_text() in ('Los Angeles Dodgers','Chicago Cubs')
     if width==390:
      assert page.locator('tbody tr').first.locator('td').last.evaluate('(e)=>{const r=e.getBoundingClientRect();return r.left>=0 && r.right<=innerWidth}')
      assert page.locator('.stats-scroll').evaluate('(e)=>e.scrollWidth<=e.clientWidth')
     if lang=='es': page.screenshot(path=f'visual-review/{lang}-{width}-{theme}-mlb.png',full_page=True)
     print('Dashboard visual checks OK',lang,width,theme)
    page.close()
  browser.close()
finally: server.terminate();server.wait()
