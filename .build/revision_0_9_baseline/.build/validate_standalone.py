"""Static and browser-bound checks for the self-contained deck.

Usage: python3 validate_standalone.py            # static checks + browser audits bound to the current hash
       python3 validate_standalone.py --static   # static checks only; records that browser audits are pending
"""
from pathlib import Path
from html.parser import HTMLParser
import base64, hashlib, json, re, sys
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
deck=json.loads(p.scripts['deck-data']);N=28;V=18
assert len(deck['slides'])==N and len(deck['media'])==V
assert [r['number'] for r in deck['slides']]==list(range(1,N+1))
expected_keys=[1,2,'questions','control','hierarchy','claude_method','claude_results','rpent','astra_direct','control_demos','interfaces','hybrid','control_summary','world',10,11,12,'simulation_demos','world_summary','improve',15,16,'idea_tree',17,'improvement_demos',18,19,'end']
assert [(r['old_slide'] if r['old_slide'] is not None else r['new_slide_key']) for r in deck['slides']]==expected_keys
opening_slides=[r['number'] for r in deck['slides'] if r['chapter_opening']]
assert opening_slides==[4,14,20]
assert [r['diagram_key'] for r in deck['slides'] if r['diagram_key']]==['control','world','improve']
for number in opening_slides:
 chapter=deck['slides'][number-1]
 assert next(r['number'] for r in deck['slides'] if r['group']==chapter['group'])==number
 assert 'Chapter overview' in chapter['html']
assert [r['group'] for r in deck['slides']]==['Introduction']*3+['1 · Agent Controls Robot']*10+['2 · Agent Builds Simulation']*6+['3 · Agent Improves Policy']*7+['Other Applications / Closing']*2
expected_titles=['Agents for Robotics','Demo: Painting with Feedback','Three Roles for Robotics Agents','Agent Controls Robot','Hierarchical Robot Control','Claude Plays Robotics: Interfaces','Claude: The Value of a Motor Prior','RPent: Organizing Robot Tools','Astra: Direct Actions in Practice','Astra: Visual Feedback in Action','Same Astra, Different Action Outputs','Astra: Direct or Hybrid?','Where Should the Boundary Sit?','Agent Builds Simulation','Real Episode and Its Twin','Agentic Real2Sim: Method','DROID-100: Protocol and Results','Astra Builds Simulation Workflows','From Replay to Prediction','Agent Improves Policy','ENPIRE: Environment and Improvement','ENPIRE: Reset and Verification','ENPIRE: What Did the Agent Change?','ENPIRE: Pin Insertion Curve','Astra: Training and Context','ENPIRE: Cost and Chapter Summary','Beyond: Structural Design','Changing the Division of Work']
assert [r['title'] for r in deck['slides']]==expected_titles
assert all(len(t)<=40 for t in expected_titles)
def slide(n):return deck['slides'][n-1]
# Each promised source remains scoped to its role: architecture, evidence, or community demo.
assert slide(5)['ids']==['HIROBOT','HELIX','HELIX02']
assert len(re.findall(r'class="art original"',slide(5)['html']))==3
for n in [6,7]:assert slide(n)['ids']==['S09']
assert slide(8)['ids']==['RPENT'] and slide(12)['ids']==['ANON']
for n in [14,15,16,17,19]:assert slide(n)['ids']==['S13']
for n in [20,21,22,23,24,26]:assert slide(n)['ids']==['S15']
assert all(t in slide(4)['html'] for t in ['q / EEF Pose','Agent Tools','IK / motion planner','VLA / learned policy','WAM','servo / controller'])
assert all(t in slide(6)['html'] for t in ['7D EEF','40 tasks × 5 seeds','Training supervision'])
assert all(t in slide(7)['html'] for t in ['3.5%','76%','86%'])
assert 'different y-axis scales' in slide(7)['footer']
assert all(t in slide(9)['html'] for t in ['19 / 20','2 / 20','No independent VLA'])
assert all(t in slide(11)['html'] for t in ['1 / 20','18 / 20','16 / 20','200 steps','500 steps','unequal control'])
assert all(t in slide(11)['script'] for t in ['256.6','不是 joint q','proprio','没有重跑'])
assert all(t in slide(12)['script'] for t in ['50×14','1–15','1–5','25 Hz','14D','OR','FK trajectory','内部网络'])
assert all(t in slide(12)['html'] for t in ['13 / 50','24 / 50'])
assert 'simulation' in slide(12)['html'] and 'omit LLM waiting' in slide(12)['footer']
assert 'control-time playback' in slide(12)['script'] and '不能用来比较端到端 latency' in slide(12)['script']
assert all(t in slide(17)['html'] for t in ['48 accepted','8 partial','44 failed','3 VLM judges','8/10'])
assert all(t in slide(23)['script'] for t in ['I37','10.8','I66','I76','不是三项独立'])
assert 'one-shot' in slide(24)['script'] and 'tokens' in slide(26)['script']
assert all(t in slide(25)['footer'] for t in ['4 experts','FULL EVAL NOT MET','8×'])
assert 'Not a validated' in slide(27)['html']
# Demo slides stay sparse and labels retain medium/speed boundaries.
for n in [10,18,25]:
 assert len(re.sub('<[^>]+>',' ',slide(n)['html']).split())<100
assert '20×' in slide(10)['html'] and '12×' in slide(10)['html']
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
expected_media={2:{'painting'},9:{'astra_bowl','astra_insertion'},10:{'policy_plug','keyboard'},11:{'asim_delta','asim_waypoint'},12:{'anon_direct_sort','anon_hybrid_pack'},15:{'ar2s_real','ar2s_sim'},18:{'astra_real2sim','office_newton'},22:{'enpire_reset','enpire_verify'},25:{'quad_rl','wenli_icl'},27:{'hand'}}
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
assert [r['slide'] for r in ui['addedFigures']]==[12,16,21,23] and all(r['open'] and r['loaded'] for r in ui['addedFigures'])
report.update(browser_audits='passed for this hash',desktop_text_overflow=0,mobile_button_overflow=0)
(B/'standalone_delivery_audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False));print(json.dumps(report,indent=2,ensure_ascii=False))
