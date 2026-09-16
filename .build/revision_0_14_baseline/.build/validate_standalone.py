"""Static and browser-bound checks for the self-contained deck.

Usage: python3 validate_standalone.py            # static checks + browser audits bound to the current hash
       python3 validate_standalone.py --static   # static checks only; records that browser audits are pending
"""
from pathlib import Path
from html.parser import HTMLParser
import base64, hashlib, html, json, re, sys
ROOT=Path('/home/limx/Desktop/agent_for_robotics');B=ROOT/'.build';out=ROOT/'output';f=out/'Agents_for_Robotics_Self_Contained.html'
STATIC_ONLY='--static' in sys.argv
class Audit(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.external=[];self.scripts={};self.active=None;self.charset=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='meta' and a.get('charset','').lower()=='utf-8':self.charset=True
  for k in ('src','poster'):
   if k in a and not a[k].startswith(('data:','blob:')):self.external.append((tag,k,a[k]))
  if tag=='link' and a.get('href'):self.external.append((tag,'href',a['href']))
  if tag=='script':self.active=a.get('id');self.scripts.setdefault(self.active,'')
 def handle_data(self,data):
  if self.active:self.scripts[self.active]+=data
 def handle_endtag(self,tag):
  if tag=='script':self.active=None
p=Audit();text=f.read_text();p.feed(text)
assert text.startswith('<!DOCTYPE html>') and p.charset
assert len(p.ids)==len(set(p.ids))
assert not p.external,p.external
deck=json.loads(p.scripts['deck-data']);N=35;V=18
assert len(deck['slides'])==N and len(deck['media'])==V
assert [r['number'] for r in deck['slides']]==list(range(1,N+1))
expected_keys=[1, 2, 'questions', 'control', 'hierarchy', 'responsibility_shift', 'astra_direct', 'control_demos', 'interfaces', 'interface_results', 'hybrid', 'robodojo_results', 'robolab_results', 'report_heatmap', 'interface_timing', 'control_summary', 'world', 10, 11, 12, 'real2sim_results', 'simulation_demos', 19, 'world_summary', 'improve', 15, 16, 'idea_tree', 17, 'enpire_results', 'enpire_robocasa', 'improvement_demos', 18, 'end', 'thanks']
assert [(r['old_slide'] if r['old_slide'] is not None else r['new_slide_key']) for r in deck['slides']]==expected_keys
opening_slides=[r['number'] for r in deck['slides'] if r['chapter_opening']]
assert opening_slides==[4,17,25]
assert [r['diagram_key'] for r in deck['slides'] if r['diagram_key']]==['control','world','improve']
for number in opening_slides:
 chapter=deck['slides'][number-1]
 assert next(r['number'] for r in deck['slides'] if r['group']==chapter['group'])==number
 assert 'Chapter overview' in chapter['html']
assert [r['group'] for r in deck['slides']]==['Introduction']*3+['1 · Agent Controls Robot']*13+['2 · Agent Creates Data']*8+['3 · Agent Improves Policy']*9+['Closing']*2
expected_titles=['Agents for Robotics', 'Demo: Painting with Feedback', 'Three Roles for Robotics Agents', 'Agent Controls Robot', 'Hierarchical Robot Control', 'Where Does Generalization Live?', 'Astra: Stronger Real-Robot Performance', 'Astra: More Real-Robot Demos', 'Same Astra, Different Action Outputs', 'Astra Interfaces: Three Tasks', 'Astra: Direct or Hybrid?', 'RoboDojo: Overall Results', 'RoboLab: Overall Results', 'RoboDojo: Task-Level Patterns', 'Astra Interfaces and Query Time', 'Control: Strengths and Open Gaps', 'Agent Creates Data', 'Real Episode and Its Twin', 'Agentic Real2Sim: Method', 'DROID-100: Protocol and Results', 'Real2Sim: All Backend Results', 'Data: Replay and Scene Assets', 'Data: Mechanism and CAD Assets', 'Data: Physics and Training Value', 'Agent Improves Policy', 'ENPIRE: Environment and Improvement', 'ENPIRE: Reset and Verification', 'ENPIRE: What Did the Agent Change?', 'ENPIRE: Pin Insertion Curve', 'ENPIRE: Two Physical Tasks', 'ENPIRE: Autoresearch in RoboCasa', 'Astra: Training and Context', 'ENPIRE: Cost and Chapter Summary', 'Takeaways', 'Thank You']
assert [r['title'] for r in deck['slides']]==expected_titles
assert all(len(t)<=40 for t in expected_titles)
def slide(n):return deck['slides'][n-1]
# Each promised source remains scoped to its role: architecture, evidence, or community demo.
assert slide(5)['ids']==['HIROBOT','HELIX','HELIX02']
assert len(re.findall(r'class="art original"',slide(5)['html']))==3
assert slide(11)['ids']==['ANON']
for n in [18, 19, 20]:assert slide(n)['ids']==['S13']
for n in [25, 26, 27, 28, 29]:assert slide(n)['ids']==['S15']
assert slide(33)['ids']==['S15','ENPIRE_SITE']
assert all(t in slide(4)['html'] for t in ['q / EEF Pose','Agent Tools','IK / motion planner','VLA / WAM / Learned policy','servo / controller'])
assert all(t in slide(7)['html'] for t in ['19 / 20','2 / 20','Astra: Stronger Real-Robot Performance'])
assert '20 calls/run;' not in slide(7)['html'] and 'No independent VLA.' not in slide(7)['html']
assert 'Astra: More Real-Robot Demos' in slide(8)['html']
assert 'Selected demonstrations, not success-rate estimates.' not in slide(8)['html']
assert slide(8)['html'].count('Control interface: not disclosed')==2
assert '不能仅从Franka外观' in slide(8)['script']
assert all(t in slide(9)['html'] for t in ['1 / 20','18 / 20','16 / 20','200 steps','500 steps','unequal control'])
assert all(t in slide(9)['script'] for t in ['256.6','不是 joint q','proprio','没有重跑'])
assert all(t in slide(11)['script'] for t in ['50×14','1–15','1–5','25 Hz','14D','OR','FK trajectory','内部网络'])
assert all(t in slide(11)['html'] for t in ['13 / 50','24 / 50'])
assert 'simulation' in slide(11)['html'] and 'omit LLM waiting' in slide(11)['footer']
assert 'control-time playback' in slide(11)['script'] and '不能用来比较端到端 latency' in slide(11)['script']
assert all(t in slide(20)['html'] for t in ['48 accepted','8 partial','44 failed','3 VLM judges','8/10'])
assert all(t in slide(28)['script'] for t in ['I37','10.8','I66','I76','不是三项独立'])
assert 'one-shot' in slide(29)['script'] and 'tokens' in slide(33)['script']
assert all(t in slide(32)['footer'] for t in ['4 experts','FULL EVAL NOT MET','8×'])
assert 'Not a validated' in slide(23)['html']
# v0.10: shared-start interface layout, capability diagnosis and sparse closing.
assert all(t in slide(16)['html'] for t in ['Semantic understanding','Spatial generalization','High-frequency control','Physical generalization','Not yet reliable / established'])
assert all(t in slide(16)['script'] for t in ['不是三种独立','is not fundamental','因果对照仍未披露'])
assert slide(16)['ids'][0]=='HIROBOT_DISCUSSION'
assert len(re.sub('<[^>]+>',' ',slide(34)['html']).split())<65
assert all(t in slide(34)['html'] for t in ['Takeaways','Reliable execution','Physics + training value','Held-out gain + cost'])
assert '不是一条已打通' in slide(34)['script']
assert 'Thank you' in slide(35)['html'] and 'Questions &amp; discussion' in slide(35)['html']
assert len(re.sub('<[^>]+>',' ',slide(35)['html']).split())<25
# v0.12: Hi Robot results are replaced, not the original architecture figures.
assert slide(6)['new_slide_key']=='responsibility_shift'
assert 'data-table-cell' not in slide(6)['html']
assert slide(6)['html'].count('System 0')==2 and 'Servo' not in slide(6)['html']
assert re.sub('<[^>]+>',' ',slide(6)['html']).split().count('Controller')==2
assert len(re.sub('<[^>]+>',' ',slide(6)['html']).split())<80
assert all(t in slide(6)['html'] for t in ['Earlier','Generalist VLA / WAM','π(a | o, l)','π(a | o, c)','c = (k, g)','a: controller target','Emerging','Action primitives','Controller','Partial shift'])
assert all(t in slide(6)['script'] for t in ['设计目标','不是某个已有模型的能力保证','部分职责迁移','因果对照尚未披露'])
assert 'functional synthesis' in slide(6)['footer']
assert '不是整层搬走' in slide(6)['script'] and '简称' in slide(6)['script']
assert all(t in slide(16)['script'] for t in ['第6页','generalist VLA / WAM','motor competence'])

# v0.11: distinguish inference time, local control and candidate-data validity.
from evidence_v011 import load_evidence
new_evidence=load_evidence(ROOT)
assert slide(15)['ids']==['ASIM','DOG','ROBOCURVE','ANON','G1_SONIC']
for term in ['12-joint chunks','simulator pauses','EEF pose targets','OSC · 20 Hz','Prior review / correction','Joint tracking / IK','30.75 s','26.08 s','41.98 s','414 queries','241 queries','76 queries','Controller Hz ≠ Agent inference Hz']:
 assert term in slide(15)['html'],term
assert all(term in slide(15)['script'] for term in ['q_nominal + 0.5a','0.024–0.038','180回合','不是完整闭环','不能统一称为atomic skills'])
assert slide(17)['ids']==['AWESOME','S13','DEXGPT']
assert all(term in slide(17)['html'] for term in ['Assets / scenes','Real-to-sim Replay','Data Rollout','Validate physics'])
assert 'Not a validated' in slide(23)['html'] and '190个STEP' in slide(23)['script']
assert slide(24)['ids']==['S13','DEXGPT']
assert all(term in slide(24)['html'] for term in ['Physical validation: NOT MET','Replay match ≠ physical validity'])
assert all(term in slide(24)['script'] for term in ['5.623 mm','203个','不是203次','downstream training'])
assert 'Beyond' not in ' '.join(r['title'] for r in deck['slides'])
# No media payload was altered during reclassification.
baseline=json.loads((B/'revision_0_13_baseline/.build/standalone_build_audit.json').read_text())
assert {r['name']:r['sha256'] for r in baseline['media']}=={r['name']:r['sha256'] for r in deck['media']}
removed_alts={
 'Original Direct LIBERO-40 success-rate panel; uncertainty and all model labels retained',
 'Original supervised LIBERO-40 panel; VLA-alone baseline and uncertainty retained',
 'RPent original framework',
}
removed_figures={r['sha256'] for r in baseline['images'] if r.get('alt') in removed_alts}
assert len(removed_figures)==3
from report_figures_v013 import load_report_figures
captures=load_report_figures(ROOT)
new_image_keys={name:hashlib.sha256(file.read_bytes()).hexdigest() for name,file in captures.items()}
assert set(deck['assets'])==({r['sha256'] for r in baseline['images']}-removed_figures)|set(new_image_keys.values())
for n,names in {12:['panel-score-ranking.png','panel-sr-ranking.png'],13:['robolab-success-ranking.png'],14:['task-score-table-complete.png']}.items():
 assert 'data-table-cell' not in slide(n)['html']
 assert slide(n)['ids']==['ANON']
 for name in names:assert new_image_keys[name] in slide(n)['html']
assert all(t in slide(12)['html'] for t in ['24/50','13/50','not paired reruns'])
assert all(t in slide(12)['script'] for t in ['48个scored episodes','分母都保持50','执行段长'])
assert all(t in slide(13)['script'] for t in ['authorized retries','180提高到500','June cohort','49/50','46/50'])
assert all(t in slide(14)['script'] for t in ['不是success rate','64与12','十个任务','七种方法'])
assert slide(7)['new_slide_key']=='astra_direct'
for r in deck['slides'][:16]:
 assert 'S09' not in r['ids'] and 'RPENT' not in r['ids']
 assert 'Claude' not in r['script'] and 'RPent' not in r['script']

# v0.9: a result table is complete only when its cells and qualifying protocol travel together.
results=json.loads((ROOT/'research/results_v0_9.json').read_text())
assert results['sources']==json.loads((ROOT/'research/results_v0_9_sources.json').read_text())['sources']
for relative,expected in results['sources'].items():
 assert hashlib.sha256((ROOT/relative).read_bytes()).hexdigest()==expected,relative
def table_cells(number,headers,rows):
 values=[html.unescape(t) for t in re.findall(r'<div class="text"[^>]*>(.*?)</div>',slide(number)['html'],re.S)]
 expected=headers+[str(cell) for row in rows for cell in row]
 start=values.index(headers[0])
 assert values[start:start+len(expected)]==expected,(number,values[start:],expected)
table_cells(7,['Completions','Fable 5','Fable 5.1','GPT-6 Astra'],
 [[t]+[f"{r['successes']} / {r['n']}" for r in results['robocurve'] if r['task']==t] for t in ['Block into bowl','Puzzle into groove']])
table_cells(10,['Task','Script\nupper','Random\nlower','ΔEEF\nproprio','Waypoint\nnone','Waypoint\nproprio','Code\nproprio','Code\nprivileged'],results['asim'])
table_cells(21,['Backend','Accepted','Partial','Failed','Model-call bill'],
 [[r[0],r[1],r[2],r[3],f'${r[4]:.2f}'] for r in results['real2sim']])
table_cells(30,['Coding agent','Push-T @ 8 h\nNormalized score','Pin @ 4 h\nSuccess rate'],
 [['Codex','0.938','95.5%'],['Claude','0.750','97.5%'],['Kimi','0.625','79.0%']])
table_cells(31,['Method','What changes','Reported evidence'],
 [['GR00T N1.5','End-to-end VLA','Baseline'],['CaP-X*','Zero-shot agentic tool use','No autoresearch'],['ENPIRE','Tool / VLA code + feedback','Highest aggregate bar']])
table_cells(33,['Agent–robot pairs','Mean robot utilization','Mean GPU utilization','Mean tokens / minute'],
 [[str(r['agentCount']),f"{r['robotMean']:.1f} ± {r['robotStd']:.1f}%",f"{r['gpuMean']:.1f} ± {r['gpuStd']:.1f}%",f"{t['mean']/1000:.1f} ± {t['std']/1000:.1f}k"] for r,t in zip(results['enpire_resources']['utilization'],results['enpire_resources']['tokenRate'])])
# Independent expected coordinates: body rows/columns are zero-based. All ties retained.
expected_bold={7: {(1, 2), (1, 3), (0, 3)}, 10: {(0, 7), (0, 4), (2, 7), (0, 3), (0, 6), (1, 7), (0, 5)}, 21: {(0, 1), (0, 3), (1, 3), (0, 4)}, 30: {(0, 1), (1, 2)}, 31: {(2, 2)}, 33: {(0, 1), (0, 3), (2, 2)}}
for number,wanted in expected_bold.items():
 observed=set();all_coordinates=set()
 for tag in re.findall(r'<div class="text"[^>]+>',slide(number)['html']):
  match=re.search(r'data-table-cell="(\d+),(\d+)"',tag)
  if not match:continue
  coord=tuple(map(int,match.groups()))
  assert coord not in all_coordinates,(number,coord)
  all_coordinates.add(coord)
  marked='data-result-best="true"' in tag
  assert marked==('font-weight:700;' in tag),(number,coord,tag)
  if marked:observed.add(coord)
 assert observed==wanted,(number,observed,wanted)
 assert 'Bold:' in slide(number)['footer']
assert {s['number'] for s in deck['slides'] if 'data-table-cell=' in s['html']}==set(expected_bold)
for number,terms in {10: ['Unequal budgets', '200', '500'], 21: ['100 episodes', 'excluded'], 30: ['4 plotted traces', 'conditional retries', 'not pooled pass@1'], 31: ['40-episode', 'No reset/retry', 'not published']}.items():
 assert all(term in slide(number)['html'] for term in terms),(number,terms)
assert all(term in slide(33)['script'] for term in ['4.5/3.2/2.0','不是同一组数','整队 token rate'])
assert all(len(slide(n)['title'])<=40 for n in range(1,N+1))
# Demo slides stay sparse and labels retain medium/speed boundaries.
for n in [8, 22, 32]:
 assert len(re.sub('<[^>]+>',' ',slide(n)['html']).split())<100
assert '20×' in slide(8)['html'] and '12×' in slide(8)['html']
assert sum(r['minutes'] for r in deck['slides'])==55
assert deck['scriptMarkdown']==(out/'Speaker_Script_Revised.md').read_text()
assert all(re.search(r'[一-鿿]',r['script']) for r in deck['slides'])
headings=dict((int(n),t) for n,t in re.findall(r'^## (\d{2})\. (.+)$',deck['scriptMarkdown'],re.M))
assert all(headings[r['number']]==r['title'] for r in deck['slides'])
for key,a in deck['assets'].items():assert hashlib.sha256(base64.b64decode(a['data'],validate=True)).hexdigest()==key
build_audit=json.loads((B/'standalone_build_audit.json').read_text())
assert build_audit['sha256']==hashlib.sha256(f.read_bytes()).hexdigest()
assert {record['sha256'] for record in build_audit['images']}==set(deck['assets']),'Image audit must describe exactly the delivered assets.'
for m in deck['media']:
 raw=base64.b64decode(p.scripts[m['payloadId']],validate=True)
 assert hashlib.sha256(raw).hexdigest()==m['sha256']
 assert raw==(B/'clips'/f'{m["name"]}.mp4').read_bytes()
 assert m['speed_multiplier']==1 and m.get('posterKey') in deck['assets']
 slide=deck['slides'][m['slide']-1]
 assert 'VIDEO:'+m['name'] not in slide['html'],'Posters are player-only.'
old_media=json.loads((out/'offline_player/media_credits.json').read_text())
original_by_name={m['name']:m for m in old_media}
community=[]
for name in ['clip_manifest.json','clip_manifest_v2.json','clip_manifest_v3.json','clip_manifest_v4.json']:
 community+=json.loads((B/name).read_text())
community_by_name={c['name']:c for c in community}
expected_media={2: {'painting'}, 7: {'astra_bowl', 'astra_insertion'}, 8: {'keyboard', 'policy_plug'}, 9: {'asim_waypoint', 'asim_delta'}, 11: {'anon_hybrid_pack', 'anon_direct_sort'}, 18: {'ar2s_sim', 'ar2s_real'}, 22: {'astra_real2sim', 'office_newton'}, 27: {'enpire_verify', 'enpire_reset'}, 32: {'quad_rl', 'wenli_icl'}, 23: {'hand'}}
assert set(m['slide'] for m in deck['media'])==set(expected_media)
for number,names in expected_media.items():
 assert {m['name'] for m in deck['media'] if m['slide']==number}==names
for m in deck['media']:
 record=community_by_name.get(m['name'],original_by_name.get(m['name']))
 assert m['sha256']==record['sha256']
 source=record.get('source_url') or original_by_name.get(m['name'],{}).get('sourceUrl')
 assert m['sourceUrl']==source
# Every embedded clip must sit inside the 1280x720 stage and above the footer.
for m in deck['media']:assert m['x']>=0 and m['y']>=0 and m['x']+m['w']<=1280.5 and m['y']+m['h']<=660,m['name']
# All Chinese characters used by script, slide text and player UI must exist in the embedded CJK subset.
sys.path.insert(0,str(B/'font_deps'))
from fontTools.ttLib import TTFont
cmap=TTFont(B/'assets/noto_cjk_script.woff2').getBestCmap()
used={c for src in [deck['scriptMarkdown'],''.join(s['html'] for s in deck['slides']),(B/'standalone_player.js').read_text()] for c in src if ord(c)>0x2E7F}
missing=sorted(c for c in used if ord(c) not in cmap)
assert not missing,missing
js=(B/'standalone_player.js').read_text()
assert not re.search(r'\b(fetch|XMLHttpRequest|WebSocket|importScripts)\s*\(',js)
assert ' / 24 · ' not in js and '24 slides' not in js and 'show(24)' not in js and 'show(26)' not in js
assert 'show(deck.slides.length)' in js
assert "connect-src 'none'" in text and text.count('@font-face')==4
assert len(list((B/'standalone_isolation').iterdir()))==1
assert (B/'standalone_isolation/index.html').read_bytes()==f.read_bytes()
html_sha256=hashlib.sha256(f.read_bytes()).hexdigest()
report={'html_sha256':html_sha256,'chapter_opening_slides':opening_slides,'slide_count':len(deck['slides']),'embedded_video_count':V,'embedded_image_count':len(deck['assets']),'font_faces':4,'all_media_byte_identical':True,'media_slide_mapping_verified':True,'external_runtime_resources':0,'all_scripts_chinese':True,'script_file_equals_embedded_script':True,'isolated_directory_only_html':True,'cjk_glyphs_used':len(used),'html_bytes':f.stat().st_size}
if STATIC_ONLY:
 report.update(browser_audits='pending: layout, playback, UI and mobile audits are not bound to this hash',desktop_text_overflow=None,mobile_button_overflow=None)
 (B/'standalone_delivery_audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False));print(json.dumps(report,indent=2,ensure_ascii=False));sys.exit(0)
layout=json.loads((B/'standalone_layout_audit.json').read_text())
assert isinstance(layout,dict) and layout['html_sha256']==html_sha256,'Fresh layout audit required.'
assert len(layout['slides'])==N and all(not r['overflow'] and r['images'] and all(i['loaded'] for i in r['images']) for r in layout['slides'])
assert [r['number'] for r in layout['slides']]==list(range(1,N+1))
phone=json.loads((B/'standalone_mobile_audit.json').read_text());assert phone['html_sha256']==html_sha256
assert phone['documentWidth']==phone['viewport']
assert phone['script']['documentWidth']==phone['script']['viewport']
assert all(b['rect']['left']>=0 and b['rect']['right']<=phone['script']['viewport']+.5 for b in phone['script']['buttons'])
assert all(b['rect']['left']>=0 and b['rect']['right']<=phone['viewport']+.5 for b in phone['buttons'])
playback=json.loads((B/'standalone_playback_audit.json').read_text());assert playback['html_sha256']==html_sha256
observed_clips=[v['clip'] for row in playback['slides'] for v in row['playing']]
assert sorted(observed_clips)==sorted(m['name'] for m in deck['media'])
for row in playback['slides']:
 assert all(v['time']>0 and not v['paused'] and not v['error'] for v in row['playing'])
 assert all(v['paused'] for v in row['pause'])
 assert all(a['clip']==b['clip'] and b['paused'] and abs(a['time']-b['time'])<.05 for a,b in zip(row['pause'],row['pauseLater']))
 assert all(v['paused'] and v['time']<=.05 for v in row['restart'])
ui=json.loads((B/'standalone_ui_audit.json').read_text());assert ui['html_sha256']==html_sha256
assert ui['fullScriptHeadings']==[f'{r["number"]:02}. {r["title"]}' for r in deck['slides']]
assert all(r['back']==r['opening'] for r in ui['transitions'])
assert ui['focusView']['enabled'] and ui['keyboard']['focusExited']
assert ui['figureDialog']['open'] and ui['figureDialog']['loaded'] and ui['figureDialog']['closed']
assert ui['keyboard']['endSlide']==N
assert [r['slide'] for r in ui['addedFigures']]==[11,12,13,14,19,24,26,28] and all(r['open'] and r['loaded'] for r in ui['addedFigures'])
report.update(browser_audits='passed for this hash',desktop_text_overflow=0,mobile_button_overflow=0)
(B/'standalone_delivery_audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False));print(json.dumps(report,indent=2,ensure_ascii=False))
