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
deck=json.loads(p.scripts['deck-data']);N=38;V=18
assert len(deck['slides'])==N and len(deck['media'])==V
assert [r['number'] for r in deck['slides']]==list(range(1,N+1))
expected_keys=[1, 2, 'questions', 'control', 'hierarchy', 'hirobot_results', 'claude_method', 'claude_results', 'rpent', 'rpent_results', 'astra_direct', 'control_demos', 'interfaces', 'interface_results', 'hybrid', 'robodojo_results', 'robolab_results', 'interface_timing', 'control_summary', 'world', 10, 11, 12, 'real2sim_results', 'simulation_demos', 19, 'world_summary', 'improve', 15, 16, 'idea_tree', 17, 'enpire_results', 'enpire_robocasa', 'improvement_demos', 18, 'end', 'thanks']
assert [(r['old_slide'] if r['old_slide'] is not None else r['new_slide_key']) for r in deck['slides']]==expected_keys
opening_slides=[r['number'] for r in deck['slides'] if r['chapter_opening']]
assert opening_slides==[4,20,28]
assert [r['diagram_key'] for r in deck['slides'] if r['diagram_key']]==['control','world','improve']
for number in opening_slides:
 chapter=deck['slides'][number-1]
 assert next(r['number'] for r in deck['slides'] if r['group']==chapter['group'])==number
 assert 'Chapter overview' in chapter['html']
assert [r['group'] for r in deck['slides']]==['Introduction']*3+['1 · Agent Controls Robot']*16+['2 · Agent Creates Data']*8+['3 · Agent Improves Policy']*9+['Closing']*2
expected_titles=['Agents for Robotics', 'Demo: Painting with Feedback', 'Three Roles for Robotics Agents', 'Agent Controls Robot', 'Hierarchical Robot Control', 'Hi Robot: Instruction and Progress', 'Claude Plays Robotics: Interfaces', 'Claude: The Value of a Motor Prior', 'RPent: Organizing Robot Tools', 'RPent: Harness VLA Results', 'Astra: Direct Actions in Practice', 'Astra: Visual Feedback in Action', 'Same Astra, Different Action Outputs', 'Astra Interfaces: Three Tasks', 'Astra: Direct or Hybrid?', 'RoboDojo: Per-Task Results', 'RoboLab: Selected Final Slots', 'Astra Interfaces and Query Time', 'Control: Strengths and Open Gaps', 'Agent Creates Data', 'Real Episode and Its Twin', 'Agentic Real2Sim: Method', 'DROID-100: Protocol and Results', 'Real2Sim: All Backend Results', 'Data: Replay and Scene Assets', 'Data: Mechanism and CAD Assets', 'Data: Physics and Training Value', 'Agent Improves Policy', 'ENPIRE: Environment and Improvement', 'ENPIRE: Reset and Verification', 'ENPIRE: What Did the Agent Change?', 'ENPIRE: Pin Insertion Curve', 'ENPIRE: Two Physical Tasks', 'ENPIRE: Autoresearch in RoboCasa', 'Astra: Training and Context', 'ENPIRE: Cost and Chapter Summary', 'Takeaways', 'Thank You']
assert [r['title'] for r in deck['slides']]==expected_titles
assert all(len(t)<=40 for t in expected_titles)
def slide(n):return deck['slides'][n-1]
# Each promised source remains scoped to its role: architecture, evidence, or community demo.
assert slide(5)['ids']==['HIROBOT','HELIX','HELIX02']
assert len(re.findall(r'class="art original"',slide(5)['html']))==3
for n in [7,8]:assert slide(n)['ids']==['S09']
assert slide(9)['ids']==['RPENT'] and slide(15)['ids']==['ANON']
for n in [21,22,23]:assert slide(n)['ids']==['S13']
for n in [28,29,30,31,32]:assert slide(n)['ids']==['S15']
assert slide(36)['ids']==['S15','ENPIRE_SITE']
assert all(t in slide(4)['html'] for t in ['q / EEF Pose','Agent Tools','IK / motion planner','VLA / WAM / Learned policy','servo / controller'])
assert all(t in slide(7)['html'] for t in ['7D EEF','40 tasks × 5 seeds','Training supervision'])
assert all(t in slide(8)['html'] for t in ['3.5%','76%','86%'])
assert 'different y-axis scales' in slide(8)['footer']
assert all(t in slide(11)['html'] for t in ['19 / 20','2 / 20','No independent VLA'])
assert all(t in slide(13)['html'] for t in ['1 / 20','18 / 20','16 / 20','200 steps','500 steps','unequal control'])
assert all(t in slide(13)['script'] for t in ['256.6','不是 joint q','proprio','没有重跑'])
assert all(t in slide(15)['script'] for t in ['50×14','1–15','1–5','25 Hz','14D','OR','FK trajectory','内部网络'])
assert all(t in slide(15)['html'] for t in ['13 / 50','24 / 50'])
assert 'simulation' in slide(15)['html'] and 'omit LLM waiting' in slide(15)['footer']
assert 'control-time playback' in slide(15)['script'] and '不能用来比较端到端 latency' in slide(15)['script']
assert all(t in slide(23)['html'] for t in ['48 accepted','8 partial','44 failed','3 VLM judges','8/10'])
assert all(t in slide(31)['script'] for t in ['I37','10.8','I66','I76','不是三项独立'])
assert 'one-shot' in slide(32)['script'] and 'tokens' in slide(36)['script']
assert all(t in slide(35)['footer'] for t in ['4 experts','FULL EVAL NOT MET','8×'])
assert 'Not a validated' in slide(26)['html']
# v0.10: shared-start interface layout, capability diagnosis and sparse closing.
assert re.findall(r'<div class="text"[^>]*>(LLM)</div>',slide(7)['html'])==['LLM']
assert all(t in slide(7)['html'] for t in ['Controller','Learned policy','MolmoAct proposal'])
assert all(t in slide(19)['html'] for t in ['Semantic understanding','Spatial generalization','High-frequency control','Physical generalization','Not yet reliable / established'])
assert all(t in slide(19)['script'] for t in ['不是三种独立','is not fundamental','6%到32%','因果对照仍未披露'])
assert slide(19)['ids'][0]=='HIROBOT_DISCUSSION'
assert len(re.sub('<[^>]+>',' ',slide(37)['html']).split())<65
assert all(t in slide(37)['html'] for t in ['Takeaways','Reliable execution','Physics + training value','Held-out gain + cost'])
assert '不是一条已打通' in slide(37)['script']
assert 'Thank you' in slide(38)['html'] and 'Questions &amp; discussion' in slide(38)['html']
assert len(re.sub('<[^>]+>',' ',slide(38)['html']).split())<25
# v0.11: distinguish inference time, local control and candidate-data validity.
from evidence_v011 import load_evidence
new_evidence=load_evidence(ROOT)
assert slide(18)['ids']==['ASIM','DOG','ROBOCURVE','ANON','G1_SONIC']
for term in ['12-joint chunks','simulator pauses','EEF pose targets','OSC · 20 Hz','Prior review / correction','Joint tracking / IK','30.75 s','26.08 s','41.98 s','414 queries','241 queries','76 queries','Controller Hz ≠ Agent inference Hz']:
 assert term in slide(18)['html'],term
assert all(term in slide(18)['script'] for term in ['q_nominal + 0.5a','0.024–0.038','180回合','不是完整闭环','不能统一称为atomic skills'])
assert slide(20)['ids']==['AWESOME','S13','DEXGPT']
assert all(term in slide(20)['html'] for term in ['Assets / scenes','Real-to-sim Replay','Data Rollout','Validate physics'])
assert 'Not a validated' in slide(26)['html'] and '190个STEP' in slide(26)['script']
assert slide(27)['ids']==['S13','DEXGPT']
assert all(term in slide(27)['html'] for term in ['Physical validation: NOT MET','Replay match ≠ physical validity'])
assert all(term in slide(27)['script'] for term in ['5.623 mm','203个','不是203次','downstream training'])
assert 'Beyond' not in ' '.join(r['title'] for r in deck['slides'])
# No media payload was altered during reclassification.
baseline=json.loads((B/'revision_0_11_baseline/.build/standalone_build_audit.json').read_text())
assert {r['name']:r['sha256'] for r in baseline['media']}=={r['name']:r['sha256'] for r in deck['media']}

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
average=results['hirobot']['values']['Average']
table_cells(6,['Author-displayed average','Instruction Accuracy (%)','Task Progress (%)'],
 [[m if m!='Expert Human' else 'Expert human high-level (oracle)',average['Instruction Accuracy'][m],average['Task Progress'][m]] for m in average['Instruction Accuracy']])
table_cells(8,['LIBERO-40','Opus 4.6 Direct','Opus 4.6 + MolmoAct','MolmoAct alone'],
 [['Success rate','3.5%','76%','86%'],['Trials / condition','200','200','200']])
table_cells(10,['Method','Instruction redirect','Position swap','Overall'],
 [[r['method'].replace('πRLinf','Direct frozen π0.5-SFT'),f"{r['redirect']} / 400",f"{r['swap']} / 400",f"{r['successes']} / 800"] for r in results['rpent']])
table_cells(11,['Completions','Fable 5','Fable 5.1','GPT-6 Astra'],
 [[t]+[f"{r['successes']} / {r['n']}" for r in results['robocurve'] if r['task']==t] for t in ['Block into bowl','Puzzle into groove']])
table_cells(14,['Task','Script\nupper','Random\nlower','ΔEEF\nproprio','Waypoint\nnone','Waypoint\nproprio','Code\nproprio','Code\nprivileged'],results['asim'])
dojo_names=['Organize table','Sort by language','Imitate sorting sequence','Arrange largest number','Pack objects into box','Classify objects','Build tower','Make kong','Fold clothes','Bottles into dustbin']
table_cells(16,['Task','Astra Direct','Astra + π0.5 Hybrid'],
 [[name,f"{r['gpt']} / 5",f"{r['mix']} / 5"] for name,r in zip(dojo_names,results['robodojo']['rows'])]+[['Total success','13 / 50 (26%)','24 / 50 (48%)']])
lab_methods=['pi05_only','astra_pi05','pure_astra','cosmos_nano_policy','dreamzero']
table_cells(17,['Task','π0.5¹','Astra\nHybrid','Astra\nDirect','Cosmos3¹','DreamZero¹'],
 [[r['label']]+[f"{r['successes'][m]} / 5" for m in lab_methods] for r in results['robolab']['tasks']]+[['Total / 50',18,46,49,18,17]])
table_cells(24,['Backend','Accepted','Partial','Failed','Model-call bill'],
 [[r[0],r[1],r[2],r[3],f'${r[4]:.2f}'] for r in results['real2sim']])
table_cells(33,['Coding agent','Push-T @ 8 h\nNormalized score','Pin @ 4 h\nSuccess rate'],
 [['Codex','0.938','95.5%'],['Claude','0.750','97.5%'],['Kimi','0.625','79.0%']])
table_cells(34,['Method','What changes','Reported evidence'],
 [['GR00T N1.5','End-to-end VLA','Baseline'],['CaP-X*','Zero-shot agentic tool use','No autoresearch'],['ENPIRE','Tool / VLA code + feedback','Highest aggregate bar']])
table_cells(36,['Agent–robot pairs','Mean robot utilization','Mean GPU utilization','Mean tokens / minute'],
 [[str(r['agentCount']),f"{r['robotMean']:.1f} ± {r['robotStd']:.1f}%",f"{r['gpuMean']:.1f} ± {r['gpuStd']:.1f}%",f"{t['mean']/1000:.1f} ± {t['std']/1000:.1f}k"] for r,t in zip(results['enpire_resources']['utilization'],results['enpire_resources']['tokenRate'])])
# Independent expected coordinates: body rows/columns are zero-based. All ties retained.
expected_bold={6: {(2, 1), (2, 2)}, 8: {(0, 3)}, 10: {(2, 3), (2, 1), (2, 2)}, 11: {(1, 2), (0, 3), (1, 3)}, 14: {(0, 7), (0, 4), (2, 7), (0, 3), (0, 6), (1, 7), (0, 5)}, 16: {(0, 1), (6, 2), (3, 1), (1, 1), (5, 1), (4, 2), (9, 2), (0, 2), (7, 2), (2, 2), (8, 2), (3, 2), (4, 1), (10, 2)}, 17: {(4, 3), (9, 2), (9, 5), (0, 2), (8, 3), (2, 2), (10, 3), (1, 3), (6, 2), (6, 5), (3, 3), (5, 3), (8, 2), (9, 1), (9, 4), (6, 4), (7, 3), (5, 2), (9, 3), (0, 3), (2, 3), (7, 2), (6, 3)}, 24: {(0, 1), (1, 3), (0, 3), (0, 4)}, 33: {(0, 1), (1, 2)}, 34: {(2, 2)}, 36: {(0, 1), (0, 3), (2, 2)}}
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
for number,terms in {6: ['not successful episodes', 'changes training data'], 10: ['Seed 0', '1–10', 'Extra compute'], 14: ['Unequal budgets', '200', '500'], 16: ['48 scored episodes', 'denominator stays 50'], 17: ['authorized retries', '180→500', 'not fresh', 'not verified identical'], 24: ['100 episodes', 'excluded'], 33: ['4 plotted traces', 'conditional retries', 'not pooled pass@1'], 34: ['40-episode', 'No reset/retry', 'not published']}.items():
 assert all(term in slide(number)['html'] for term in terms),(number,terms)
assert all(term in slide(36)['script'] for term in ['4.5/3.2/2.0','不是同一组数','整队 token rate'])
assert all(len(slide(n)['title'])<=40 for n in range(1,N+1))
# Demo slides stay sparse and labels retain medium/speed boundaries.
for n in [12,25,35]:
 assert len(re.sub('<[^>]+>',' ',slide(n)['html']).split())<100
assert '20×' in slide(12)['html'] and '12×' in slide(12)['html']
assert sum(r['minutes'] for r in deck['slides'])==60
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
expected_media={2: {'painting'}, 11: {'astra_bowl', 'astra_insertion'}, 12: {'keyboard', 'policy_plug'}, 13: {'asim_delta', 'asim_waypoint'}, 15: {'anon_hybrid_pack', 'anon_direct_sort'}, 21: {'ar2s_real', 'ar2s_sim'}, 25: {'office_newton', 'astra_real2sim'}, 30: {'enpire_reset', 'enpire_verify'}, 35: {'wenli_icl', 'quad_rl'}, 26: {'hand'}}
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
assert [r['slide'] for r in ui['addedFigures']]==[15,22,27,29,31] and all(r['open'] and r['loaded'] for r in ui['addedFigures'])
report.update(browser_audits='passed for this hash',desktop_text_overflow=0,mobile_button_overflow=0)
(B/'standalone_delivery_audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False));print(json.dumps(report,indent=2,ensure_ascii=False))
