import urllib.request,xml.etree.ElementTree as ET
for url in ('https://lidom.com/feed/','https://www.mlb.com/feeds/news/rss.xml'):
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'BeisbolRadar-RD source check'}),timeout=15) as r:
   data=r.read(2000001)
   if len(data)>2000000: raise ValueError('oversize')
   root=ET.fromstring(data)
   tag=root.tag.split('}')[-1]
   if tag not in ('rss','feed','RDF'): raise ValueError('not a feed')
   count=sum(e.tag.split('}')[-1] in ('item','entry') for e in root.iter())
   print(url,r.status,tag,count,'items; redistribution disabled')
 except Exception as e: print(url,'UNVERIFIED',type(e).__name__,str(e))
