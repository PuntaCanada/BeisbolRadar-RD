from playwright.sync_api import sync_playwright
from subprocess import Popen
import time
server=Popen(['python3','-m','http.server','8765','--directory','public'])
try:
 with sync_playwright() as p:
  browser=p.chromium.launch()
  for width,height in [(1280,800),(390,844)]:
   page=browser.new_page(viewport={'width':width,'height':height})
   for lang in ('es','en','de','fr','it'):
    for section in ('','lidom/','mlb/','players/','news/','sponsorship/','sources/'):
     response=page.goto('http://127.0.0.1:8765/'+lang+'/'+section)
     assert response.status==200
     assert page.locator('html').get_attribute('lang')==lang
     assert page.locator('h1').count()==1
     assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
     page.locator('#theme').click()
     theme=page.locator('html').get_attribute('data-theme')
     page.reload()
     assert theme==page.locator('html').get_attribute('data-theme')
     print(width,lang,section,'OK')
   page.close()
  browser.close()
finally: server.terminate();server.wait()
