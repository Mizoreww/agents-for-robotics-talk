from pathlib import Path
import urllib.request,json,datetime,hashlib,concurrent.futures,re,html
ROOT=Path(__file__).resolve().parent
text=(ROOT/'robocurve.html').read_text()
rows=[]
for row in re.findall(r'<tr.*?</tr>',text,re.S):
 cols=[html.unescape(re.sub('<[^>]+>','',c)).strip() for c in re.findall(r'<td[^>]*>(.*?)</td>',row,re.S)]
 if len(cols)!=8 or cols[1]!='GPT-6 Astra':continue
 match=re.search(r"href=['\"](runs/transcripts/[^'\"]+)['\"]",row)
 if match:rows.append({'task':cols[0],'model':cols[1],'stage':int(cols[2]),'url':'https://openai.robocurve.org/gpt-6-astra/'+match.group(1)})
assert len(rows)==40,len(rows)
(ROOT/'robocurve_transcripts').mkdir(exist_ok=True)
def fetch(row):
 url=row['url']; filename='robocurve_transcripts/'+url.rsplit('/',1)[-1]
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'research-source-check'}),timeout=50) as resp:data=resp.read()
 (ROOT/filename).write_bytes(data)
 return {**row,'file':filename,'fetched_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:manifest=list(ex.map(fetch,rows))
(ROOT/'robocurve_transcripts_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Saved',len(manifest),'Astra run transcripts',sum(x['bytes'] for x in manifest),'bytes')
