from pathlib import Path
import base64, copy, hashlib, html, json, mimetypes, posixpath, re, zipfile
import xml.etree.ElementTree as ET
ROOT=Path('/home/limx/Desktop/agent_for_robotics')
B=ROOT/'.build'; OUT=ROOT/'output'
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
old=json.loads((B/'slide_records_focus.json').read_text())
media=json.loads((OUT/'offline_player/media_credits.json').read_text())
community=json.loads((B/'clip_manifest_v2.json').read_text())
clip_by_name={c['name']:c for c in community}
assets={}; layouts={}; image_audit=[]
def asset(data,mime):
 key=hashlib.sha256(data).hexdigest()
 assets.setdefault(key,{'mime':mime,'data':base64.b64encode(data).decode()})
 return key
with zipfile.ZipFile(B/'focus_draft.pptx') as z:
 for n in range(1,23):
  d=json.loads((B/'focus_rendered'/f'{n:02}.layout.json').read_text())
  xml=ET.fromstring(z.read(f'ppt/slides/slide{n}.xml'))
  rels={r.attrib['Id']:r.attrib['Target'] for r in ET.fromstring(z.read(f'ppt/slides/_rels/slide{n}.xml.rels'))}
  pics=xml.findall('.//p:pic',NS); imgs=[e for e in d['elements'] if e['kind']=='image']
  assert len(pics)==len(imgs),(n,len(pics),len(imgs))
  for p,e in zip(pics,imgs):
   target=rels[p.find('.//a:blip',NS).attrib['{'+NS['r']+'}embed']]
   target=target.lstrip('/') if target.startswith('/') else posixpath.normpath(posixpath.join('ppt/slides',target))
   data=z.read(target); e['assetKey']=asset(data,e['contentType'])
   image_audit.append({'old_slide':n,'alt':e.get('alt',''),'sha256':e['assetKey']})
  cx=xml.findall('.//p:cxnSp',NS)
  lines=[e for e in d['elements'] if 'Connector' in e.get('geometry','')]
  assert len(cx)==len(lines),(n,len(cx),len(lines))
  for c,e in zip(cx,lines):
   e['startArrow']=c.find('.//a:headEnd',NS) is not None and c.find('.//a:headEnd',NS).get('type')!='none'
   e['endArrow']=c.find('.//a:tailEnd',NS) is not None and c.find('.//a:tailEnd',NS).get('type')!='none'
  layouts[n]=d['elements']

def text(t,x,y,w,h,size=23,color='#1a1a1a',bold=False,serif=False,align='left'):
 return {'kind':'shape','bbox':[x,y,w,h],'text':t,'resolvedTextStyle':{'fontSize':size,'color':color,'bold':bold,'typeface':'Noto Serif' if serif else 'Noto Sans','alignment':align}}
def rect(x,y,w,h,fill,line=None):
 return {'kind':'shape','bbox':[x,y,w,h],'fillColor':fill,'lineColor':line,'lineWidth':1 if line else 0}
def connector(x1,y1,x2,y2,color='#646464',arrow=True):
 return {'kind':'shape','geometry':'straightConnector1','bbox':[min(x1,x2),min(y1,y2),abs(x2-x1),abs(y2-y1)],'horizontalFlip':x2<x1,'verticalFlip':y2<y1,'lineColor':color,'lineWidth':2,'endArrow':arrow}
def page(title,num=None,sub=None):
 els=[copy.deepcopy(layouts[4][0])]
 if num:els += [text(str(num),64,57,45,48,36,'#2ba39b',True,True),text(title,110,57,965,48,36,bold=True,serif=True)]
 else:els += [text(title,64,57,1011,48,36,bold=True,serif=True)]
 els += [rect(64,111,1152,3,'#2ba39b')]
 if sub:els += [text(sub,80,140,1120,35,22,'#646464')]
 return els
def band(msg):
 return [rect(64,612,1152,44,'#EAF5F3'),text(msg,84,620,1112,30,22,'#1d7d76',True)]
def fit(x,y,w,h,vw,vh):
 s=min(w/vw,h/vh);return [x,y,round(vw*s,2),round(vh*s,2)]
def video_el(name,x,y,w,h,caption):
 # The poster image is never drawn; the player reads it through the VIDEO: alt lookup.
 c=clip_by_name[name];bx=fit(x,y,w,h,c['width'],c['height'])
 key=asset(Path(c['poster']).read_bytes(),'image/jpeg')
 image_audit.append({'source':c['source_url'],'alt':'VIDEO:'+name,'sha256':key})
 return [{'kind':'image','bbox':bx,'assetKey':key,'alt':'VIDEO:'+name},text('▷  '+caption,bx[0],bx[1]+bx[3]+4,bx[2],30,17,'#646464')],bx
def summary(title,num,nodes,feedback,shown,open_,setup='',reference=False):
 els=page(title,num)+[text(setup or 'Chapter overview · our synthesis',80,160,1120,45,23,'#646464')]
 y=273
 for i,(a,b) in enumerate(nodes):
  x=80+290*i;accent=i==1
  els += [rect(x,y,250,98,'#2ba39b' if accent else '#f4f6f5', '#2ba39b' if accent else '#c6d9d6'),text(a,x+8,y+14,234,35,23,'#ffffff' if accent else '#1a1a1a',True,align='center'),text(b,x+8,y+57,234,31,17,'#e2f3ef' if accent else '#646464',align='center')]
  if i<3:els += [connector(x+250,y+49,x+290,y+49)]
 els += [connector(1075,371,1075,421,'#2ba39b',False),connector(1075,421,495,421,'#2ba39b',False),connector(495,421,495,373,'#2ba39b'),text(feedback,550,432,500,30,19,'#1d7d76',align='center')]
 if reference:
  els += [connector(205,273,205,231,'#96958e',False),connector(205,231,1075,231,'#96958e',False),connector(1075,231,1075,271,'#96958e'),text('Reference recording',493,203,320,25,17,'#646464',align='center')]
 els += [text('Evidence',80,507,158,35,23,'#1d7d76',True),text(shown,260,507,935,58,24),text('Still open',80,581,158,35,23,'#aa514a',True),text(open_,260,581,935,66,24)]
 return els

def execution_tools():
 els=page('Agent Controls Robot',1)
 els += [text('Our synthesis · IK and WAM extend the report’s tested interfaces',80,148,1120,38,22,'#646464')]
 els += [text('Task + observations',112,286,276,34,22,align='center'),connector(250,322,250,365),rect(140,365,220,88,'#2ba39b'),text('Agent',148,379,204,34,27,'#ffffff',True,align='center'),text('act or call tools',148,418,204,28,18,'#e2f3ef',align='center')]
 els += [rect(500,210,350,60,'#edf7f4','#2ba39b'),text('Direct action output',511,215,328,29,22,'#1d7d76',True),text('q / EEF Pose · numeric commands',511,244,328,25,17,'#646464'),text('Agent Tools',500,284,350,30,22,'#1d7d76',True)]
 tools=[('IK / motion planner','Pose targets to joint motion'),('Controller code','Fast local feedback'),('VLA / learned policy','Grounded action skills'),('WAM','Joint world + action generation')]
 centers=[240]
 els += [connector(412,240,500,240),connector(850,240,939,240,arrow=False)]
 for i,(label,benefit) in enumerate(tools):
  y=323+i*56;centers.append(y+25)
  els += [rect(500,y,350,50,'#f4f6f5','#c6d9d6'),text(label,511,y+2,328,27,21,bold=True),text(benefit,511,y+28,328,22,16,'#646464')]
  els += [connector(412,y+25,500,y+25),connector(850,y+25,939,y+25,arrow=False)]
 els += [connector(360,409,412,409,arrow=False),connector(412,centers[0],412,centers[-1],arrow=False),connector(939,centers[0],939,centers[-1],arrow=False),connector(939,409,1010,409),text('Action outputs',984,317,233,32,19,'#646464',align='center')]
 els += [rect(1010,365,190,88,'#f4f6f5','#c6d9d6'),text('Execution',1018,379,174,34,24,bold=True,align='center'),text('servo / controller',1018,418,174,28,17,'#646464',align='center')]
 # Feedback is observed state, not an assertion that every tool emits motor actions.
 els += [connector(1105,453,1105,595,'#2ba39b',False),connector(1105,595,850,595,'#2ba39b'),text('Observations',878,552,213,30,19,'#1d7d76',align='center'),rect(500,565,350,60,'#edf7f4','#c6d9d6'),text('Perception / state tools',511,570,328,29,22,'#1d7d76',True),text('pose · depth · heading',511,599,328,25,17,'#646464'),connector(500,595,250,595,'#2ba39b',False),connector(250,595,250,453,'#2ba39b')]
 els += [text('Direct commands or tools: the runtime still closes low-level loops.',80,639,1120,30,22,'#1d7d76',True)]
 return els

def agenda():
 els=page('Three Roles')
 rows=[('Agent Controls Robot','Claude Plays Robotics · community demos · harnesses · RPent'),('Agent Produces Data','Agentic Real2Sim · replay acceptance versus prediction'),('Agent Post-trains Robot','ENPIRE · ASPIRE · repeatable real experiments')]
 for i,(title,detail) in enumerate(rows):
  y=172+i*128
  els += [text(str(i+1),82,y,60,48,34,'#2ba39b',True,True),text(title,186,y,1010,42,30,bold=True),text(detail,186,y+50,1010,35,22,'#646464')]
 els += [text('Closing: structural design as one further application outside the three roles',186,572,1010,30,20,'#646464')]
 return els

def toolkit_example():
 raw=(ROOT/'research/assets/rpent_framework.png').read_bytes()
 key=asset(raw,'image/png')
 image_audit.append({'source':'https://github.com/RLinf/RPent','alt':'Official RPent service-oriented framework','sha256':key})
 return page('RPent: Robotics as Tools',1)+[text('Recursive Physical Agent · official project architecture',80,140,1120,35,23,'#646464'),{'kind':'image','bbox':[64,187,1152,418],'assetKey':key,'alt':'Official RPent service-oriented framework'},text('Related: ROSA (ROS agent) · ROS-MCP (MCP–ROS bridge)',80,610,1120,30,21,'#1d7d76',True),text('Architecture scope is broader than verified integrations; DreamZero is not marked supported.',80,644,1120,25,17,'#646464')]

new_placements={}
def community_demos():
 els=page('Demo: Zero-shot Real Arms',1)
 v1,b1=video_el('wenli_icl',64,150,600,338,'@_wenlixiao · 8× playback')
 v2,b2=video_el('arx_knob',740,150,476,336,'@ARXrobotics · 16× playback')
 els += v1+v2
 els += [text('Human video → robot arm',64,540,640,40,27,'#1d7d76',True),text('Author-reported first pass',64,586,640,32,21,'#646464')]
 els += [text('One instruction, one task',740,540,476,40,27,'#1d7d76',True),text('About four minutes at 16×',740,586,476,32,21,'#646464')]
 new_placements['community']=[('wenli_icl',b1),('arx_knob',b2)]
 return els
def sim_dexterity():
 els=page('Demo: Dexterity in Simulation',1)
 v1,b1=video_el('ze_rubik',64,150,704,396,'@ZeYanjie · Rubik’s Cube, MuJoCo replay')
 v2,b2=video_el('juggle',800,150,416,234,'@thermalpastor · juggling, MuJoCo 1×')
 els += v1+v2
 els += [text('Agent-built\nMuJoCo scene',800,436,416,84,27,'#1d7d76',True),text('Simulation only\nno real hands',800,536,416,74,25,'#aa514a',True)]
 new_placements['simdex']=[('ze_rubik',b1),('juggle',b2)]
 return els
def harness():
 els=page('Harness: Semantic Actions',1)
 v1,b1=video_el('show_harness',64,150,640,360,'Show-Harness project video excerpt · Show Lab, NUS')
 els += v1
 els += [text('Discrete action units',740,158,476,36,25,'#1d7d76',True),text('MV_FWD · ROTATE_CW · GRASP · DONE',740,200,476,32,21,'#646464')]
 els += [text('Zero-shot 89% · fine-tuned 86%',740,268,476,40,27,bold=True),text('Cross-task average, 10 trials per task\nVLA baselines 35–39%',740,314,476,64,21,'#646464')]
 els += [text('Parallel-jaw arms only',740,420,476,36,25,'#aa514a',True),text('No tactile or force feedback',740,462,476,32,21,'#646464')]
 els += [rect(64,598,1152,58,'#EAF5F3'),text('Interpreters ground each unit; the VLM decides each step.',84,612,1112,36,23,'#1d7d76',True)]
 new_placements['harness']=[('show_harness',b1)]
 return els
def gaps_directions():
 els=page('Gaps and Directions',1)
 v1,b1=video_el('xhs_piper',64,150,520,295,'小红书 @虽然不但是 · Piper, 70× playback')
 els += v1
 els += [text('Three failed grasps, then success',64,492,520,36,23,'#1d7d76',True)]
 els += [text('Gaps',620,150,596,36,25,'#aa514a',True),text('Contact and precision\nLatency between model calls\nDynamics and dexterity\nEmbodied memory',620,192,596,140,23)]
 els += [text('Directions',620,352,596,36,25,'#1d7d76',True),text('Harnesses and tool libraries\nScaled action models\nSimulation and data → Part 2\nRepeatable real experiments → Part 3',620,394,596,140,23)]
 els += [rect(64,598,1152,58,'#EAF5F3'),text('Placement 19/20, insertion 2/20 · minutes per task behind 16–70× playback',84,612,1112,36,23,'#1d7d76',True)]
 new_placements['gaps']=[('xhs_piper',b1)]
 return els

def conclusion():
 els=page('Conclusion')
 rows=[('Agent Controls Robot: match model and interface.','Direct actions, harnesses and learned policies need different support; contact and latency stay open.'),('Agent Produces Data: distinguish replay from prediction.','New actions test whether a reconstructed scene is useful.'),('Agent Post-trains Robot: make real experiments repeatable.','Fixed interfaces, reset, verification and repaired skills support iteration.')]
 for i,(title,detail) in enumerate(rows):
  y=172+i*122
  els += [text(str(i+1),79,y,64,45,31,'#2ba39b',True,True),text(title,172,y,1038,40,26,bold=True),text(detail,172,y+44,1038,34,20,'#646464')]
 els += [text('What does the Agent produce, and how do we know it works?',172,556,1038,35,25,'#1d7d76',True),text('Beyond the three roles: engineering artifacts such as designs need their own validation.',172,604,1038,30,19,'#646464')]
 return els

summaries={
 'exec':('Agent Controls Robot',execution_tools(),['S09','S10','WAM']),
 'community':('Demo: Zero-shot Real Arms',community_demos(),['WENLI','ARX']),
 'simdex':('Demo: Dexterity in Simulation',sim_dexterity(),['ZE','JUGGLE']),
 'harness':('Harness: Semantic Actions',harness(),['SHOWH','MAXFU']),
 'toolkits':('RPent: Robotics as Tools',toolkit_example(),['RPENT','ROSA','ROS_MCP']),
 'gaps':('Gaps and Directions',gaps_directions(),['XHS_PIPER','S10','S09','MALIK','HUMANCLAW','ROBODOJO','YUXIANG','MAXFU','ESPEJEL']),
 'world':('Agent Produces Data',summary('Agent Produces Data',2,[('Recording','real interaction'),('Agent + tools','scene and parameters'),('Simulator','candidate replay'),('Comparison','replay mismatch')],'Mismatch guides the next revision','48 of 100 episodes meet the replay-acceptance rule.','Does the scene predict outcomes under new actions?','Chapter overview · the product is a runnable simulated episode, not a model update',reference=True),['S13']),
 'improve':('Agent Post-trains Robot',summary('Agent Post-trains Robot',3,[('Task + API','fixed environment'),('Agent','policy / training edits'),('Real rollout','robot experiment'),('Verifier + logs','outcome and trace')],'Evidence guides the next policy change','The workflow improves policies under its stated protocol.','Reset, verifier errors, conditional retries and transfer.','Human-assisted setup; environment API fixed during improvement'),['S15'])
}
# Three parts, each opening with its synthesis diagram; the hand design closes outside the three roles.
order=[1,2,3,4,'exec',6,5,7,8,'community','simdex','harness','toolkits','gaps','world',10,11,12,13,'improve',14,15,16,17,18,20,19,22]
assert len(order)==28
chapter_keys={'exec','world','improve'}
new_titles={1:'Agents for Robotics',2:'Demo: Painting with Feedback',3:'Our Goal',4:'Three Roles',6:'Direct Actions and Code',5:'Model and Interface',7:'VLA as a Tool',8:'Demo: Placement and Insertion',10:'Real Episode and Its Twin',11:'Conversion Pipeline',12:'Replay Acceptance on DROID-100',13:'Demo: Real2Sim and a Failure',14:'ENPIRE: Real Experiments in the Loop',15:'ENPIRE: Environment and Improvement',16:'ENPIRE: Reset and Verification',17:'ENPIRE: Pin Insertion Curve',18:'Faster Research, Higher Token Use',20:'ASPIRE: Repairing Skills',19:'Beyond: Structural Design',22:'Conclusion'}
minutes=[.5,2,2.5,1, 1.5,2,3,2,2,2,2,2,2,2.5, 1.5,2,3,3,2, 1.5,2.5,4,3,3.5,2,2, 1.5,1.5]
assert len(minutes)==28 and sum(minutes)==60,sum(minutes)
script_text=(B/'script_revised.md').read_text()
chunks=re.split(r'^## (\d{2})\. (.+)\n',script_text,flags=re.M)
script_sections={int(chunks[i]):chunks[i+2].strip() for i in range(1,len(chunks),3)}
script_titles={int(chunks[i]):chunks[i+1] for i in range(1,len(chunks),3)}
assert len(script_sections)==len(order),(len(script_sections),len(order))
def group_of(n):
 return 'Introduction' if n<=4 else '1 · Agent Controls Robot' if n<=14 else '2 · Agent Produces Data' if n<=19 else '3 · Agent Post-trains Robot' if n<=26 else 'Closing'
def is_title(e):
 return e['kind']=='shape' and 'text' in e and abs(e['bbox'][1]-57)<1 and e.get('resolvedTextStyle',{}).get('fontSize')==36 and e['text'] not in ('1','2','3','4')
def clip_media(name,slide_number,bx):
 c=clip_by_name[name]
 return {'slide':slide_number,'alt':'VIDEO:'+name,'sourceUrl':c['source_url'],'x':bx[0],'y':bx[1],'w':bx[2],'h':bx[3],'name':name,'start_seconds':c['start_seconds'],'duration_seconds':c['duration_seconds'],'speed_multiplier':1,'audio':'removed for narrated talk','width':c['width'],'height':c['height'],'codec':c['codec'],'pixel_format':c['pixel_format'],'sha256':c['sha256'],'full_decode':c['full_decode'],'payloadId':'video-'+name,'community':True}
slides=[]; new_media=[]
for n,key in enumerate(order,1):
 if isinstance(key,int):
  r=copy.deepcopy(old[key-1]);els=copy.deepcopy(layouts[key])
 else:
  title,els,ids=summaries[key];r={'title':title,'ids':ids};els=copy.deepcopy(els)
 r.pop('notes',None)
 r.update(number=n,minutes=minutes[n-1],script=script_sections[n],old_slide=key if isinstance(key,int) else None,new_slide_key=key if isinstance(key,str) else None,diagram_key=key if key in chapter_keys else None,chapter_opening=key in chapter_keys,group=group_of(n))
 # Use new numbering and consistent linked source footers.
 els=[e for e in els if not(e['kind']=='shape' and e['bbox'][1]>=660)]
 if isinstance(key,int) and key in new_titles:
  r['title']=new_titles[key]
  for e in els:
   if is_title(e):e['text']=r['title']
 if key==1:
  # Title slide: speaker name and talk date; the sources cut-off stays in the footer.
  els=[e for e in els if e.get('text')!='Three case studies and emerging applications']
  for e in els:
   if e.get('text')=='Reliable Action and Improvement':e['text']='Control, Data and Post-training'
   if e.get('text')=='Technical talk\n10 September 2026':e['text']='Zimo Huang\n16 September 2026'
 if key==3:
  replacements={'Finish the current job. Make the next job easier.':'Useful robotics work through tools and feedback','Robot execution':'Agent + Tools','actions with feedback':'act, build and evaluate','Reusable capability':'Useful artifacts','program, skill or policy':'data, code or policy','Capability retained for later tasks':'Validated artifacts support later tasks'}
  for e in els:
   if e.get('text') in replacements:e['text']=replacements[e['text']]
 if key==4:els=agenda()
 if key==7:
  replacements={'Agent':'VLA tool','task-level decisions':'proposed actions','VLA policy':'Agent','motor execution':'accept · edit · replace','task outcome':'execute + observe'}
  for e in els:
   if e.get('text') in replacements:e['text']=replacements[e['text']]
 if key==20:
  # ASPIRE now closes the post-training part.
  for e in els:
   if is_title(e):e['bbox']=[110,57,965,48]
  els += [text('3',64,57,45,48,36,'#2ba39b',True,True)]
 if key==19:
  for e in els:
   if e.get('text')=='Design artifact':e['text']='Structural design\nCAD proposal'
 if key==22:els=conclusion()
 assert script_titles[n]==r['title'],(n,script_titles[n],r['title'])
 r['elements']=els;slides.append(r)
 if isinstance(key,int):
  for m in media:
   if m['slide']==key:
    m=copy.deepcopy(m);m['slide']=n
    raw=(B/'clips'/f'{m["name"]}.mp4').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==m['sha256']
    m['payloadId']='video-'+m['name'];m.pop('file',None);m.pop('poster',None)
    new_media.append(m)
 else:
  for name,bx in new_placements.get(key,[]):
   new_media.append(clip_media(name,n,bx))

source_map={}
for r in old:
 tail=r['notes'].split('SOURCES\n',1)[-1]
 for match in re.finditer(r'(S\d+): ([^\n]+)\n(https?://[^\s]+)',tail):
  sid,label,url=match.groups();source_map[sid]={'label':label,'url':url}
source_map['WAM']={'label':'DreamZero · World Action Models are Zero-shot Policies (2026)','url':'https://dreamzero0.github.io/'}
source_map['RPENT']={'label':'RPent · Recursive Physical Agent (RLinf), official framework and source','url':'https://github.com/RLinf/RPent'}
source_map['ROSA']={'label':'ROSA · Robot Operating System Agent (NASA JPL)','url':'https://github.com/nasa-jpl/rosa'}
source_map['ROS_MCP']={'label':'ROS-MCP Server · MCP–ROS bridge','url':'https://github.com/robotmcp/ros-mcp-server'}
source_map['WENLI']={'label':'Wenli Xiao (@_wenlixiao), X · human video to robot arm with GPT-6 Astra (9 Sep 2026)','url':'https://x.com/_wenlixiao/status/2097801944119349455'}
source_map['ARX']={'label':'ARX Robotics (@ARXrobotics), X · washing-machine knob demo (5 Sep 2026)','url':'https://x.com/ARXrobotics/status/2096328304794210604'}
source_map['ZE']={'label':'Yanjie Ze (@ZeYanjie), X · GPT-6 Astra solved a Rubik’s Cube with robot hands, MuJoCo (10 Sep 2026)','url':'https://x.com/ZeYanjie/status/2098118164626501669'}
source_map['ZE_PAGE']={'label':'Dexterous Cube Solving · project page (physics replay, contact-driven MuJoCo)','url':'https://dex-rubik-cube.yanjieze.com/'}
source_map['JUGGLE']={'label':'@thermalpastor, X · two robots juggling in MuJoCo at 1× speed (9 Sep 2026)','url':'https://x.com/thermalpastor/status/2097496200631210136'}
source_map['SHOWH']={'label':'Show-Harness: Just a VLM Agent Can Play Robots · arXiv 2609.10522 (9 Sep 2026)','url':'https://arxiv.org/abs/2609.10522'}
source_map['SHOWH_POST']={'label':'Zechen Bai (@ZechenBai), X · Show-Harness announcement thread and video (10 Sep 2026)','url':'https://x.com/ZechenBai/status/2097879130356498603'}
source_map['MAXFU']={'label':'Max Fu (@letian_fu), X · harnesses, tool calls and skill libraries (6 Sep 2026)','url':'https://x.com/letian_fu/status/2096673034325381268'}
source_map['MALIK']={'label':'Jitendra Malik (@JitendraMalikCV), X · dexterity and dynamics need high-frequency control (8 Sep 2026)','url':'https://x.com/JitendraMalikCV/status/2097173961264284039'}
source_map['HUMANCLAW']={'label':'Jiawei Gu (@Kuvvius), X · GPT-6 Astra on HumanCLAW-Bench, single low-thinking run (10 Sep 2026)','url':'https://x.com/Kuvvius/status/2098038921301311753'}
source_map['ROBODOJO']={'label':'@XuefW82242, X · one GPT-6 Astra run on RoboDojo, 11/60 (10 Sep 2026)','url':'https://x.com/XuefW82242/status/2097972885860311314'}
source_map['YUXIANG']={'label':'Yu Xiang (@YuXiang_IRVL), X · “VLA is not dead” (10 Sep 2026)','url':'https://x.com/YuXiang_IRVL/status/2098085522182664439'}
source_map['ESPEJEL']={'label':'Omar Espejel (@omarespejel), X · same model, same task, different tools and memory (9 Sep 2026)','url':'https://x.com/omarespejel/status/2097485274137686415'}
source_map['XHS_PIPER']={'label':'小红书 @虽然不但是 · Piper + RealSense carrot pick-and-place with Codex + GPT-6, 70× (6 Sep 2026)','url':'https://www.xiaohongshu.com/explore/6a9bd4c80000000028037f67'}
source_map['XHS_R2S']={'label':'小红书 @Hello燕Sir · GPT-6 Astra Real2Sim 初试流程, Blender replay from three views (7 Sep 2026)','url':'https://www.xiaohongshu.com/explore/6a9e29e6000000002603a68a'}
for r,key in zip(slides,order):
 if key=='simdex':r['ids']=['ZE','ZE_PAGE','JUGGLE']
 if key=='harness':r['ids']=['SHOWH','SHOWH_POST','MAXFU']
 if key==13:r['ids']=list(dict.fromkeys([*r['ids'],'XHS_R2S']))
 r['sources']=[source_map[sid] for sid in r['ids']]
 if key==19:
  r['sources'] += [{'label':'Author limitation and follow-up','url':u} for u in ['https://x.com/earthtojake/status/2097789991426335015','https://x.com/earthtojake/status/2097801101890207893']]
 if isinstance(key,int):
  r['footer']=next((e.get('text','') for e in layouts[key] if e['kind']=='shape' and e['bbox'][1]==679),'')
 else:r['footer']='Our synthesis · based on '+r['sources'][0]['label']
 if key=='exec':r['footer']='Our synthesis · Claude Plays Robotics; Robocurve (IK); DreamZero (WAM) · not one evaluated stack'
 if key=='toolkits':r['footer']='RPent official project figure · supporting ecosystem example, not a fourth deep case study · ROSA / ROS-MCP: see notes'
 if key=='community':r['footer']='@_wenlixiao (9 Sep 2026) and @ARXrobotics (5 Sep 2026), X · community demonstrations, not controlled evaluations'
 if key=='simdex':r['footer']='@ZeYanjie (10 Sep 2026) and @thermalpastor (9 Sep 2026), X · MuJoCo demonstrations built with GPT-6 Astra'
 if key=='harness':r['footer']='Show-Harness, arXiv 2609.10522 (9 Sep 2026) · project video excerpt · numbers as reported by the authors'
 if key=='gaps':r['footer']='Synthesis: Robocurve, Claude Plays Robotics, HumanCLAW, one RoboDojo run, X / 小红书 discussion · Piper demo: 小红书 @虽然不但是'
 if key==1:r['footer']=r['footer'].replace('10 September 2026','11 September 2026')
 r['footer']=r['footer'].replace(' | ',' · ')
 for m in new_media:
  if m['slide']==r['number']:
   m['posterKey']=next(e['assetKey'] for e in r['elements'] if e.get('alt')=='VIDEO:'+m['name'])

def style_bbox(b):
 x,y,w,h=b;return f'left:{x:g}px;top:{y:g}px;width:{w:g}px;height:{h:g}px;'
def render_element(e):
 b=e['bbox'];sty=style_bbox(b)
 if e['kind']=='image':
  if e.get('alt','').startswith('VIDEO:'):return ''
  cls='art original' if 'logo' not in e.get('alt','').lower() else 'art'
  return f'<img class="{cls}" data-asset="{e["assetKey"]}" style="{html.escape(sty,quote=True)}" alt="{html.escape(e.get("alt",""),quote=True)}"'+(' tabindex="0" role="button" title="Enlarge original figure"' if cls.endswith('original') else '')+'>'
 if 'Connector' in e.get('geometry',''):
  x,y,w,h=b;x1=x+w if e.get('horizontalFlip') else x;x2=x if e.get('horizontalFlip') else x+w;y1=y+h if e.get('verticalFlip') else y;y2=y if e.get('verticalFlip') else y+h
  col=e.get('lineColor','#646464');marker='teal' if col.lower()=='#2ba39b' else 'gray'
  return f'<svg class="connector" viewBox="0 0 1280 720" aria-hidden="true"><path d="M{x1:g} {y1:g} L{x2:g} {y2:g}" stroke="{col}" stroke-width="2" fill="none"'+(f' marker-end="url(#{marker})"' if e.get('endArrow') else '')+(f' marker-start="url(#{marker})"' if e.get('startArrow') else '')+'/></svg>'
 if e.get('fillColor'):sty+=f'background:{e["fillColor"]};'
 if e.get('lineColor') and e.get('lineWidth'):sty+=f'border:{e["lineWidth"]}px solid {e["lineColor"]};'
 if 'text' in e:
  s=e.get('resolvedTextStyle',{});sty+=f'font-size:{s.get("fontSize",23)}px;font-family:"{s.get("typeface","Noto Sans")}";color:{s.get("color","#1a1a1a")};font-weight:{700 if s.get("bold") else 400};text-align:{s.get("alignment","left")};'
  return f'<div class="text" style="{html.escape(sty,quote=True)}">{html.escape(e["text"])}</div>'
 return f'<div class="shape" style="{html.escape(sty,quote=True)}"></div>'

def prose_html(s):
 out=[]
 for para in s.split('\n\n'):
  if para.startswith('> '):out.append('<blockquote>'+html.escape(para[2:])+'</blockquote>')
  elif para:out.append('<p>'+html.escape(para).replace('\n','<br>')+'</p>')
 return ''.join(out)

elapsed=0;markdown=[script_text.split('\n## 01.')[0], '\n## 建议时间安排\n\n| Slide | Title | Minutes | Start |\n|---:|---|---:|---:|']
for r in slides:
 r['startMinutes']=elapsed;elapsed+=r['minutes']
 markdown.append(f'| {r["number"]:02} | {r["title"]} | {r["minutes"]:g} | {int(r["startMinutes"]):02}:{int(r["startMinutes"]%1*60):02} |')
for r in slides:
 r['html']=''.join(render_element(e) for e in r.pop('elements'))
 r['notesHtml']=prose_html(r['script'])
 markdown.append(f'\n## {r["number"]:02}. {r["title"]}\n\n建议 {r["minutes"]:g} 分钟（含读图、视频及停顿）。\n\n{r["script"]}\n')
 if r['sources']:markdown.append('### 参考来源\n\n'+'\n'.join(f'- [{s["label"]}]({s["url"]})' for s in r['sources']))
markdown='\n'.join(markdown)+'\n'
(OUT/'Speaker_Script_Revised.md').write_text(markdown)
fontcss=''
for family,file,weight in [('Noto Sans','NotoSans-Regular.ttf',400),('Noto Sans','NotoSans-Bold.ttf',700),('Noto Serif','NotoSerif-Bold.ttf',700)]:
 raw=(Path('/usr/share/fonts/truetype/noto')/file).read_bytes()
 fontcss+=f'@font-face{{font-family:"{family}";font-style:normal;font-weight:{weight};font-display:block;src:url(data:font/ttf;base64,{base64.b64encode(raw).decode()}) format("truetype");}}\n'
raw=(B/'assets/noto_cjk_script.woff2').read_bytes()
fontcss+='@font-face{font-family:"Noto Sans CJK SC";font-style:normal;font-weight:400;font-display:block;src:url(data:font/woff2;base64,'+base64.b64encode(raw).decode()+') format("woff2");}\n'
# Source URLs are passive citations. There are no remote runtime requests.
data={'slides':slides,'media':new_media,'assets':assets,'scriptMarkdown':markdown}
data_json=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
page_html=(B/'standalone_shell.html').read_text().replace('/* EMBEDDED_FONTS */',fontcss).replace('/* PLAYER_CSS */',(B/'standalone_player.css').read_text()).replace('<!-- DECK_DATA -->','<script type="application/json" id="deck-data">'+data_json+'</script>').replace('/* PLAYER_JS */',(B/'standalone_player.js').read_text())
# Keep binary payloads out of executable JS and materialize only active clips.
payloads=[]
for m in new_media:
 raw=(B/'clips'/f'{m["name"]}.mp4').read_bytes()
 assert hashlib.sha256(raw).hexdigest()==m['sha256'],m['name']
 payloads.append(f'<script id="{m["payloadId"]}" type="application/octet-stream" data-sha256="{m["sha256"]}">{base64.b64encode(raw).decode()}</script>')
page_html=page_html.replace('<!-- VIDEO_PAYLOADS -->','\n'.join(payloads))
dest=OUT/'Agents_for_Robotics_Self_Contained.html';dest.write_text(page_html)
assert len(new_media)==20,len(new_media)
report={'slides':len(slides),'videos':len(new_media),'media_seconds':sum(m['duration_seconds'] for m in new_media),'minutes':sum(minutes),'chapter_opening_slides':[n for n,key in enumerate(order,1) if key in chapter_keys],'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'standalone_file':str(dest),'media':[{k:m[k] for k in ['name','slide','sha256','duration_seconds']} for m in new_media],'images':image_audit,'native_text':True,'all_fonts_embedded':True}
(B/'standalone_build_audit.json').write_text(json.dumps(report,indent=2))
(B/'slide_records_revised.json').write_text(json.dumps([{k:v for k,v in r.items() if k not in ['html','notesHtml']} for r in slides],ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k not in ['images','media']},indent=2))
