from playwright.sync_api import sync_playwright
from subprocess import Popen
import urllib.request,time
server=Popen(['python3','-m','http.server','8766','--directory','public'])
try:
 for _ in range(50):
  try:
   urllib.request.urlopen('http://127.0.0.1:8766/').close();break
  except OSError: time.sleep(.1)
 with sync_playwright() as p:
  browser=p.chromium.launch()
  for width in (390,1280):
   page=browser.new_page(viewport={'width':width,'height':844})
   for lang in ('es','en','de','fr','it'):
    page.goto('http://127.0.0.1:8766/'+lang+'/players/')
    search=page.locator('input[type=search]')
    search.fill('Fernando Abad')
    page.locator('tbody button',has_text='Fernando Abad').click()
    assert page.locator('h2').inner_text()=='Fernando Abad'
    assert page.locator('table').count()==2
    page.locator('table').first.locator('th button').first.click()
    assert page.locator('table').first.locator('tbody tr').count()>1
    page.goto('http://127.0.0.1:8766/'+lang+'/mlb/')
    page.locator('input[type=search]').fill('20250318')
    page.locator('tbody tr').first.wait_for()
    expected={'es':'18/03/2025','en':'03/18/2025','de':'18.03.2025','fr':'18/03/2025','it':'18/03/2025'}[lang]
    date=page.locator('tbody tr').first.locator('time')
    assert date.inner_text()==expected
    assert date.get_attribute('datetime')=='2025-03-18'
    for query in (expected,'2025-03-18'):
     page.locator('input[type=search]').fill(query)
     assert page.locator('tbody tr').count()==1
     assert date.inner_text()==expected
    page.locator('input[type=search]').fill('2025')
    page.locator('thead th button').first.click()
    dates=page.locator('tbody time').evaluate_all('(nodes)=>nodes.map(n=>n.dateTime)')
    assert len(dates)==2430 and dates==sorted(dates)
    page.locator('thead th button').first.click()
    dates=page.locator('tbody time').evaluate_all('(nodes)=>nodes.map(n=>n.dateTime)')
    assert dates==sorted(dates,reverse=True)
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    print('Stats interactions OK',lang,width)
  browser.close()
finally: server.terminate();server.wait()
