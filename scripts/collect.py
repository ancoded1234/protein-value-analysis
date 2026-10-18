"""Public web evidence collection. Existing parent .env is read only."""
from pathlib import Path
import os,json,time,datetime,requests,argparse
from dotenv import load_dotenv
R=Path(__file__).resolve().parents[1]
for parent in [R,*R.parents]:
    if (parent/'.env').is_file():
        load_dotenv(parent/'.env',override=False);break
def scrape(url,slug):
    dest=R/'data/firecrawl';dest.mkdir(parents=True,exist_ok=True)
    cached=dest/f'{slug}.json'
    if cached.exists():return json.loads(cached.read_text(encoding='utf-8'))
    key=os.getenv('FIRECRAWL_API_KEY')
    if not key:raise RuntimeError('FIRECRAWL_API_KEY is not configured')
    for attempt in range(4):
        response=requests.post('https://api.firecrawl.dev/v2/scrape',headers={'Authorization':'Bearer '+key},json={'url':url,'formats':['markdown','links'],'onlyMainContent':True},timeout=110)
        payload=response.json()
        if response.status_code!=429:break
        time.sleep(min(55,max(8,payload.get('retry_after_seconds',20))))
    data=payload.get('data',{}); meta=data.get('metadata',{})
    record={'url':url,'collected_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Firecrawl v2 scrape','api_status':response.status_code,'page_status':meta.get('statusCode'),'success':bool(payload.get('success')) and meta.get('statusCode')==200,'data':data,'error':payload.get('error')}
    cached.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    (dest/f'{slug}.md').write_text(data.get('markdown',''),encoding='utf-8')
    print(slug,record['success'],'page',record['page_status'],'characters',len(data.get('markdown','')),flush=True)
    time.sleep(7)
    return record
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('url');p.add_argument('slug');a=p.parse_args();scrape(a.url,a.slug)
