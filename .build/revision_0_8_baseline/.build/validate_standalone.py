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
deck=json.loads(p.scripts['deck-data']);N=21;V=9
assert len(deck['slides'])==N and len(deck['media'])==V
assert [r['number'] for r in deck['slides']]==list(range(1,N+1))
expected_order=[1,2,None,None,None,None,None,None,None,10,11,12,None,None,14,15,16,17,18,19,None]
assert [r['old_slide'] for r in deck['slides']]==expected_order
assert [r['new_slide_key'] for r in deck['slides'] if r['new_slide_key']]==['questions','control','background','protocol','control_results','control_summary','world','world_summary','improve','end']
opening_slides=[r['number'] for r in deck['slides'] if r['chapter_opening']]
assert opening_slides==[4,9,14]
assert [r['diagram_key'] for r in deck['slides'] if r['diagram_key']]==['control','world','improve']
for number in opening_slides:
 chapter=deck['slides'][number-1]
 assert next(r['number'] for r in deck['slides'] if r['group']==chapter['group'])==number
 assert 'Chapter overview' in chapter['html'] or 'Original report control architecture' in chapter['html']
groups=[r['group'] for r in deck['slides']]
assert groups==['Introduction']*3+['1 · Agent Controls Robot']*5+['2 · Agent Produces Data']*5+['3 · Agent Improves Robot']*6+['Other Applications / Closing']*2
expected_titles=['Agents for Robotics','Demo: Painting with Feedback','Three Questions, Three Studies','Agent Controls Robot','Context: Models and Interfaces','What Enters and Leaves Each Model?','RoboDojo: Results and Examples','Control: What Did We Learn?','Agent Produces Data','Real Episode and Its Twin','Agentic Real2Sim: Method','DROID-100: Protocol and Results','Data: Replay Is Not Prediction','Agent Improves Robot','ENPIRE: The Real Task','ENPIRE: Environment and Improvement','ENPIRE: Reset and Verification','ENPIRE: Pin Insertion Curve','ENPIRE: Cost and Chapter Summary','Beyond: Structural Design','Three Studies, Three Conclusions']
assert [r['title'] for r in deck['slides']]==expected_titles
assert all(len(t)<=40 for t in expected_titles)
# Exactly one representative per chapter; only slide5 may cite the two brief background works.
for n in [4,6,7,8]:assert deck['slides'][n-1]['ids']==['ANON']
assert deck['slides'][4]['ids']==['S09','RPENT']
for n in range(9,14):assert deck['slides'][n-1]['ids']==['S13']
for n in range(14,20):assert deck['slides'][n-1]['ids']==['S15']
assert all(term in deck['slides'][5]['html'] for term in ['50 × 14','1–15 steps','1–5 steps','25 Hz','14D','xhigh'])
assert all(term in deck['slides'][4]['html'] for term in ['Claude Plays Robotics','RPent','older findings need re-testing','not established'])
assert 'Motion · code · learned policy' in deck['slides'][4]['html']
assert 'IK · code · learned policy' not in deck['slides'][4]['html']
assert all(term in deck['slides'][6]['html'] for term in ['13 / 50','24 / 50','different tasks','excludes LLM waiting'])
assert all(term in deck['slides'][3]['script'] for term in ['OR','FK trajectory','内部的网络结构','h_t'])
assert all(term in deck['slides'][11]['script'] for term in ['48','8','44','最多选五个','8/10'])
assert 'one-shot' in deck['slides'][17]['script'] and 'tokens' in deck['slides'][18]['script']
assert 'Not a validated' in deck['slides'][19]['html']
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
community=json.loads((B/'clip_manifest_v2.json').read_text())+json.loads((B/'clip_manifest_v3.json').read_text());community_by_name={c['name']:c for c in community}
active_new={'anon_direct_sort','anon_hybrid_pack'}
retained={'painting','ar2s_real','ar2s_sim','enpire_task','enpire_reset','enpire_verify','hand'}
assert {m['name'] for m in deck['media']}==retained|active_new
for m in deck['media']:
 if m['name'] in original_by_name:
  assert deck['slides'][m['slide']-1]['old_slide']==original_by_name[m['name']]['slide']
  assert m['sha256']==original_by_name[m['name']]['sha256']
 else:
  assert m['sha256']==community_by_name[m['name']]['sha256'] and m['sourceUrl']==community_by_name[m['name']]['source_url']
assert {m['name'] for m in deck['media'] if m['slide']==7}==active_new
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
assert [r['slide'] for r in ui['addedFigures']]==[11,16] and all(r['open'] and r['loaded'] for r in ui['addedFigures'])
report.update(browser_audits='passed for this hash',desktop_text_overflow=0,mobile_button_overflow=0)
(B/'standalone_delivery_audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False));print(json.dumps(report,indent=2,ensure_ascii=False))
