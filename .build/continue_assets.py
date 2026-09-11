import concurrent.futures, hashlib, json, urllib.request
from pathlib import Path
root=Path('/home/limx/Desktop/agent_for_robotics/.build')
jobs={
'enpire_scaling.png':'https://arxiv.org/html/2606.19980v1/auto_env_bench.png',
'enpire_utilization.svg':'https://arxiv.org/html/2606.19980v1/agent_resource_utilization.svg',
}
for key in ['painting','astra_real2sim','astra_microphone']:
 d=json.loads((root/(key+'_metadata.json')).read_text())
 f=d['tweet']['media']['videos'][0]['formats']
 q=[x for x in f if x.get('container')=='mp4' and '720' in x['url']]
 jobs[key+'_source.mp4']=q[0]['url'] if q else d['tweet']['media']['videos'][0]['url']
def fetch(k,u):
 target=root/'assets'/k
 if target.exists():return {'name':k,'url':u,'status':'existing','sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
 temp=target.with_suffix(target.suffix+'.partial')
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=80) as response,temp.open('wb') as out:
   while chunk:=response.read(1024*1024):out.write(chunk)
  temp.replace(target)
  return {'name':k,'url':u,'accessed':'2026-09-10','status':'downloaded','bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
 except Exception as e:return {'name':k,'url':u,'status':'failed','error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:records=list(pool.map(lambda kv:fetch(*kv),jobs.items()))
(root/'continuation_downloads.json').write_text(json.dumps(records,indent=2));print(json.dumps(records,indent=2))
