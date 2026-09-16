"""Derive displayed query timing statistics, not model-server or servo latency."""
from pathlib import Path
import re,json,statistics,hashlib
ROOT=Path(__file__).resolve().parent
source=ROOT/'asim_index.html'
SOURCE_SHA256='50af836616bef6dfaed22e142702d37da7e5884c85954e9cb9ae3e7d685d4851'
SOURCE_COMMIT='1e7952c26e0a8783e4eca48514b3a1cc03e2c5df'
assert hashlib.sha256(source.read_bytes()).hexdigest()==SOURCE_SHA256,'unreviewed source bytes'
assert source.read_bytes()==(ROOT/'asim_index_pinned.html').read_bytes(),'live/pinned source mismatch'
text=source.read_text()
# Every episode has one video and ends with one details element. Do not include
# the 3 example queries in section 2 or historical runs from September 7.
episodes=[]
for match in re.finditer(r'<div class="ep"><video[^>]+src="media/([^/]+)/([^\"]+)".*?</details></div>',text,re.S):
 run,ep=match.group(1,2)
 if '__20260908T' not in run:continue
 task,interface,state,model,seed,stamp=run.split('__')
 if state!='proprio' or model!='codex-gpt-6-astra':continue
 body=match.group()
 declared=int(re.search(r'模型的推理轨迹（(\d+) 次查询）',body).group(1))
 times=[float(s) for s in re.findall(r'<b>查询 \d+</b>（第 \d+ 步，([\d.]+) s，',body)]
 assert len(times)==declared,(run,ep,declared,len(times))
 episodes.append({'run':run,'episode':ep,'task':task,'interface':interface,'state':state,'query_seconds':times})
assert len(episodes)==180,len(episodes)
expected_runs={
 'Can__code__proprio__codex-gpt-6-astra__s0__20260908T152543Z',
 'Can__delta__proprio__codex-gpt-6-astra__s0__20260908T135533Z',
 'Can__waypoint__proprio__codex-gpt-6-astra__s0__20260908T122925Z',
 'Lift__code__proprio__codex-gpt-6-astra__s0__20260908T134254Z',
 'Lift__delta__proprio__codex-gpt-6-astra__s0__20260908T125956Z',
 'Lift__waypoint__proprio__codex-gpt-6-astra__s0__20260908T122854Z',
 'Square__code__proprio__codex-gpt-6-astra__s0__20260908T142029Z',
 'Square__delta__proprio__codex-gpt-6-astra__s0__20260908T131857Z',
 'Square__waypoint__proprio__codex-gpt-6-astra__s0__20260908T132052Z',
}
expected_grid={(run,f'ep{i:02d}.mp4') for run in expected_runs for i in range(20)}
assert {(row['run'],row['episode']) for row in episodes}==expected_grid,'episode identity mismatch'
summary=[]
for interface in ['delta','waypoint','code']:
 for task in ['Lift','Can','Square','ALL']:
  rows=[x for x in episodes if x['interface']==interface and (task=='ALL' or x['task']==task)]
  times=[v for row in rows for v in row['query_seconds']]
  assert len(rows)==(60 if task=='ALL' else 20)
  summary.append({'interface':interface,'task':task,'episodes':len(rows),'queries':len(times),'mean_s':statistics.mean(times),'median_s':statistics.median(times),'min_s':min(times),'max_s':max(times),'sum_s':sum(times),'inverse_mean_s':1/statistics.mean(times)})
result={'source_url':'https://asimfish.github.io/astra-control-dashboard/#sec4','source_sha256':SOURCE_SHA256,'source_commit':SOURCE_COMMIT,'description':'Derived from per-query displayed seconds; not an independently timed experiment, not end-to-end feedback Hz. prompt v3, proprio, Lift/Can/Square, 20 episodes per task/interface; excludes historical runs, none and privileged.','summary':summary,'episodes':episodes}
(ROOT/'asim_query_times_derived.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
for row in summary:print(row)
