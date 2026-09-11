from pathlib import Path
from html.parser import HTMLParser
import base64, hashlib, json, re
ROOT=Path('/home/limx/Desktop/agent_for_robotics');B=ROOT/'.build';out=ROOT/'output';f=out/'Agents_for_Robotics_Self_Contained.html'
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
deck=json.loads(p.scripts['deck-data']);assert len(deck['slides'])==26 and len(deck['media'])==15
assert [r['number'] for r in deck['slides']]==list(range(1,27))
expected_order=[1,2,3,4,None,6,5,7,8,9,None,None,10,11,12,13,None,14,15,16,17,18,None,19,20,22]
assert [r['old_slide'] for r in deck['slides']]==expected_order,'Chapter diagrams must open their chapters.'
opening_slides=[r['number'] for r in deck['slides'] if r['chapter_opening']]
assert opening_slides==[5,12,17,23]
assert [r['diagram_key'] for r in deck['slides'] if r['diagram_key']]==['exec','world','improve','other']
for number in opening_slides:
 chapter=deck['slides'][number-1]
 assert next(r['number'] for r in deck['slides'] if r['group']==chapter['group'])==number
 assert any(s in chapter['html'] for s in ['Chapter overview','Human-assisted setup','Our synthesis'])
for label in ['Direct action output','q / EEF Pose','servo / controller','Agent Tools','IK / motion planner','Controller code','VLA / learned policy','WAM','Perception / state tools']:
 assert label in deck['slides'][4]['html'],label
assert 'extend the report' in deck['slides'][4]['html']
assert deck['slides'][5]['title']=='Direct Actions and Controller Code'
assert deck['slides'][6]['title']=='Claude Plays Robotics: Model and Interface'
assert deck['slides'][9]['title']=='Agent + Tools: Strengths and Gaps'
for label in ['Semantic goals','Continuity','contact-state estimation','generative action policies','Long-horizon planning']:
 assert label in deck['slides'][9]['html'],label
assert deck['slides'][10]['new_slide_key']=='toolkits' and not deck['slides'][10]['chapter_opening']
assert deck['slides'][10]['group']=='1 · Execution' and deck['slides'][11]['chapter_opening']
assert 'Official RPent service-oriented framework' in deck['slides'][10]['html']
assert 'DreamZero is not marked supported' in deck['slides'][10]['html']
assert '用 RPent 收束第一章' in deck['slides'][10]['script']
assert '接下来先看 RPent' not in deck['slides'][4]['script']
assert 'Structural Design' in deck['slides'][23]['title']
assert 'Not a validated' in deck['slides'][23]['html']
assert all(r['group']=='4 · Other applications' for r in deck['slides'][22:25])
assert deck['slides'][25]['group']=='Conclusion'
assert not any(s in deck['scriptMarkdown'] for s in ['接下来，我们用一张图把 execution 这一章收束起来','现在可以把 world-building 这一章整理成一张反馈图'])
assert sum(r['minutes'] for r in deck['slides'])==60
assert deck['scriptMarkdown']==(out/'Speaker_Script_Revised.md').read_text()
assert all(re.search(r'[\u4e00-\u9fff]',r['script']) for r in deck['slides'])
headings=dict((int(n),t) for n,t in re.findall(r'^## (\d{2})\. (.+)$',deck['scriptMarkdown'],re.M))
assert all(headings[r['number']]==r['title'] for r in deck['slides'])
for key,a in deck['assets'].items():assert hashlib.sha256(base64.b64decode(a['data'],validate=True)).hexdigest()==key
for m in deck['media']:
 raw=base64.b64decode(p.scripts[m['payloadId']],validate=True)
 assert hashlib.sha256(raw).hexdigest()==m['sha256']
 assert raw==(B/'clips'/f'{m["name"]}.mp4').read_bytes()
 assert m['speed_multiplier']==1
old_media=json.loads((out/'offline_player/media_credits.json').read_text())
original_by_name={m['name']:m for m in old_media}
assert {m['name'] for m in deck['media']}==set(original_by_name)
for m in deck['media']:
 assert deck['slides'][m['slide']-1]['old_slide']==original_by_name[m['name']]['slide']
js=(B/'standalone_player.js').read_text()
assert not re.search(r'\b(fetch|XMLHttpRequest|WebSocket|importScripts)\s*\(',js)
assert ' / 24 · ' not in js and '24 slides' not in js and 'show(24)' not in js
assert 'show(deck.slides.length)' in js
assert "connect-src 'none'" in text and text.count('@font-face')==4
assert len(list((B/'standalone_isolation').iterdir()))==1
assert (B/'standalone_isolation/index.html').read_bytes()==f.read_bytes()
html_sha256=hashlib.sha256(f.read_bytes()).hexdigest()
layout=json.loads((B/'standalone_layout_audit.json').read_text())
assert isinstance(layout,dict) and layout['html_sha256']==html_sha256,'Fresh layout audit required.'
assert len(layout['slides'])==26 and all(not r['overflow'] and r['images'] and all(i['loaded'] for i in r['images']) for r in layout['slides'])
assert [r['number'] for r in layout['slides']]==list(range(1,27))
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
assert ui['keyboard']['endSlide']==26
report={'html_sha256':html_sha256,'chapter_opening_slides':opening_slides,'slide_count':len(deck['slides']),'embedded_video_count':15,'embedded_image_count':len(deck['assets']),'font_faces':4,'all_media_byte_identical':True,'media_slide_mapping_verified':True,'external_runtime_resources':0,'all_scripts_chinese':True,'script_file_equals_embedded_script':True,'isolated_directory_only_html':True,'desktop_text_overflow':0,'mobile_button_overflow':0,'html_bytes':f.stat().st_size}
(B/'standalone_delivery_audit.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
