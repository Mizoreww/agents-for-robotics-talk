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
deck=json.loads(p.scripts['deck-data']);N=28;V=20
assert len(deck['slides'])==N and len(deck['media'])==V,(len(deck['slides']),len(deck['media']))
assert [r['number'] for r in deck['slides']]==list(range(1,N+1))
expected_order=[1,2,3,4,None,6,5,7,8,None,None,None,None,None,None,10,11,12,13,None,14,15,16,17,18,20,19,22]
assert [r['old_slide'] for r in deck['slides']]==expected_order,'Three parts must keep their case order.'
assert [r['new_slide_key'] for r in deck['slides'] if r['new_slide_key']]==['exec','community','simdex','harness','toolkits','gaps','world','improve']
opening_slides=[r['number'] for r in deck['slides'] if r['chapter_opening']]
assert opening_slides==[5,15,20]
assert [r['diagram_key'] for r in deck['slides'] if r['diagram_key']]==['exec','world','improve']
for number in opening_slides:
 chapter=deck['slides'][number-1]
 assert next(r['number'] for r in deck['slides'] if r['group']==chapter['group'])==number
 assert any(s in chapter['html'] for s in ['Chapter overview','Human-assisted setup','Our synthesis'])
groups=[r['group'] for r in deck['slides']]
assert groups[:4]==['Introduction']*4 and groups[4:14]==['1 · Agent Controls Robot']*10 and groups[14:19]==['2 · Agent Produces Data']*5 and groups[19:26]==['3 · Agent Post-trains Robot']*7 and groups[26:]==['Closing']*2,groups
titles={r['number']:r['title'] for r in deck['slides']}
expected_titles={1:'Agents for Robotics',2:'Demo: Painting with Feedback',3:'Our Goal',4:'Three Roles',5:'Agent Controls Robot',6:'Direct Actions and Code',7:'Model and Interface',8:'VLA as a Tool',9:'Demo: Placement and Insertion',10:'Demo: Zero-shot Real Arms',11:'Demo: Dexterity in Simulation',12:'Harness: Semantic Actions',13:'RPent: Robotics as Tools',14:'Gaps and Directions',15:'Agent Produces Data',16:'Real Episode and Its Twin',17:'Conversion Pipeline',18:'Replay Acceptance on DROID-100',19:'Demo: Real2Sim and a Failure',20:'Agent Post-trains Robot',21:'ENPIRE: Real Experiments in the Loop',22:'ENPIRE: Environment and Improvement',23:'ENPIRE: Reset and Verification',24:'ENPIRE: Pin Insertion Curve',25:'Faster Research, Higher Token Use',26:'ASPIRE: Repairing Skills',27:'Beyond: Structural Design',28:'Conclusion'}
assert titles==expected_titles,[(k,titles[k],expected_titles[k]) for k in titles if titles[k]!=expected_titles.get(k)]
assert all(len(t)<=40 for t in titles.values()),'Titles must stay short.'
for label in ['Direct action output','q / EEF Pose','servo / controller','Agent Tools','IK / motion planner','Controller code','VLA / learned policy','WAM','Perception / state tools']:
 assert label in deck['slides'][4]['html'],label
assert 'extend the report' in deck['slides'][4]['html']
for label in ['MV_FWD','GRASP','89%','Parallel-jaw']:
 assert label in deck['slides'][11]['html'],label
for label in ['Gaps','Directions','Part 2','Part 3','19/20']:
 assert label in deck['slides'][13]['html'],label
# Added slides keep the deck's sparse style: few text blocks, no small dense paragraphs.
for n in (10,11,12,14):
 blocks=re.findall(r'font-size:(\d+)px[^>]*>([^<]*)</div>',deck['slides'][n-1]['html'])
 assert all(int(size)>=17 for size,_ in blocks),n
 assert sum(len(t) for size,t in blocks if int(size)<=21)<=260,(n,[t for size,t in blocks if int(size)<=21])
assert 'Official RPent service-oriented framework' in deck['slides'][12]['html'] and 'DreamZero is not marked supported' in deck['slides'][12]['html']
assert 'runnable simulated episode' in deck['slides'][14]['html']
assert 'Not a validated' in deck['slides'][26]['html']
assert 'Three Roles' in deck['slides'][3]['html'] and 'Agent Post-trains Robot' in deck['slides'][3]['html']
assert '第二部分' in deck['slides'][13]['script'] and '第三部分' in deck['slides'][18]['script']
assert '@ZeYanjie' in deck['slides'][10]['html'] and 'MuJoCo' in deck['slides'][10]['html']
assert '小红书' in deck['slides'][13]['html']
assert sum(r['minutes'] for r in deck['slides'])==60
assert deck['scriptMarkdown']==(out/'Speaker_Script_Revised.md').read_text()
assert all(re.search(r'[一-鿿]',r['script']) for r in deck['slides'])
headings=dict((int(n),t) for n,t in re.findall(r'^## (\d{2})\. (.+)$',deck['scriptMarkdown'],re.M))
assert all(headings[r['number']]==r['title'] for r in deck['slides'])
for key,a in deck['assets'].items():assert hashlib.sha256(base64.b64decode(a['data'],validate=True)).hexdigest()==key
for m in deck['media']:
 raw=base64.b64decode(p.scripts[m['payloadId']],validate=True)
 assert hashlib.sha256(raw).hexdigest()==m['sha256']
 assert raw==(B/'clips'/f'{m["name"]}.mp4').read_bytes()
 assert m['speed_multiplier']==1 and m.get('posterKey') in deck['assets']
 slide=deck['slides'][m['slide']-1]
 assert 'VIDEO:'+m['name'] not in slide['html'],'Posters are player-only.'
old_media=json.loads((out/'offline_player/media_credits.json').read_text())
original_by_name={m['name']:m for m in old_media}
community=json.loads((B/'clip_manifest_v2.json').read_text());community_by_name={c['name']:c for c in community}
retained={n for n in original_by_name if n!='wiping'}
assert {m['name'] for m in deck['media']}==retained|set(community_by_name),{m['name'] for m in deck['media']}
for m in deck['media']:
 if m['name'] in original_by_name:
  assert deck['slides'][m['slide']-1]['old_slide']==original_by_name[m['name']]['slide']
  assert m['sha256']==original_by_name[m['name']]['sha256']
 else:
  assert m['sha256']==community_by_name[m['name']]['sha256'] and m['sourceUrl']==community_by_name[m['name']]['source_url']
assert {m['name'] for m in deck['media'] if m['slide']==10}=={'wenli_icl','arx_knob'} and {m['name'] for m in deck['media'] if m['slide']==11}=={'ze_rubik','juggle'}
assert {m['name'] for m in deck['media'] if m['slide']==12}=={'show_harness'} and {m['name'] for m in deck['media'] if m['slide']==14}=={'xhs_piper'}
# Every embedded clip must sit inside the 1280x720 stage and above the footer.
for m in deck['media']:assert m['x']>=0 and m['y']>=0 and m['x']+m['w']<=1280.5 and m['y']+m['h']<=660,m['name']
# All Chinese characters used by script, slide text and player UI must exist in the embedded CJK subset.
from fontTools.ttLib import TTFont
sys.path.insert(0,str(B/'font_deps'))
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
assert all(b['rect']['left']>=0 and b['rect']['right']<=phone['viewport']+.5 for b in phone['buttons'])
playback=json.loads((B/'standalone_playback_audit.json').read_text());assert playback['html_sha256']==html_sha256
observed_clips=[v['clip'] for row in playback['slides'] for v in row['playing']]
assert sorted(observed_clips)==sorted(m['name'] for m in deck['media'])
for row in playback['slides']:
 assert all(v['time']>0 and not v['paused'] and not v['error'] for v in row['playing'])
 assert all(v['paused'] for v in row['pause'])
 assert all(v['paused'] and v['time']<=.05 for v in row['restart'])
ui=json.loads((B/'standalone_ui_audit.json').read_text());assert ui['html_sha256']==html_sha256
assert ui['fullScriptHeadings']==[f'{r["number"]:02}. {r["title"]}' for r in deck['slides']]
assert all(r['back']==r['opening'] for r in ui['transitions'])
assert ui['focusView']['enabled'] and ui['keyboard']['focusExited']
assert ui['figureDialog']['open'] and ui['figureDialog']['loaded']
assert ui['keyboard']['endSlide']==N
report.update(browser_audits='passed for this hash',desktop_text_overflow=0,mobile_button_overflow=0)
(B/'standalone_delivery_audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False));print(json.dumps(report,indent=2,ensure_ascii=False))
