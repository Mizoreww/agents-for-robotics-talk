from pathlib import Path
import base64, copy, hashlib, html, json, mimetypes, posixpath, re, zipfile
import xml.etree.ElementTree as ET
ROOT=Path('/home/limx/Desktop/agent_for_robotics')
B=ROOT/'.build'; OUT=ROOT/'output'
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
old=json.loads((B/'slide_records_focus.json').read_text())
media=json.loads((OUT/'offline_player/media_credits.json').read_text())
community=json.loads((B/'clip_manifest_v2.json').read_text()) + json.loads((B/'clip_manifest_v3.json').read_text())
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


def original_image(file,alt,x,y,w,h,source):
 raw=Path(file).read_bytes();key=asset(raw,mimetypes.guess_type(str(file))[0])
 image_audit.append({'source':source,'alt':alt,'sha256':key})
 return {'kind':'image','bbox':[x,y,w,h],'assetKey':key,'alt':alt}

ANON_URL='https://anonymous-report-421.github.io/public-website/?lang=en&view=1'
new_placements={}
def questions():
 els=page('Three Questions, Three Studies')
 rows=[('Control','Who should generate the action?','GPT 6 Astra as an Embodied Policy'),('Data','Can a real episode become a simulator?','Agentic Real2Sim'),('Improvement','Can real experiments improve a policy?','ENPIRE')]
 for i,(role,q,work) in enumerate(rows):
  y=173+i*130
  els += [text(str(i+1),80,y,70,42,32,'#2ba39b',True,True),text(role,168,y,230,38,28,'#1d7d76',True),text(q,422,y,785,38,28,bold=True),text(work,422,y+48,785,32,22,'#646464')]
 els += band('For each study: question → method → experiment → bounded conclusion.')
 return els

def control():
 els=page('Agent Controls Robot',1)
 els += [original_image(B/'assets/v0_7/report_architecture_original.png','Original report control architecture: pi0.5 + Astra versus Astra Direct',64,141,727,514,ANON_URL)]
 els += [text('Question',834,153,374,34,23,'#1d7d76',True),text('Can a learned action prior\nhelp the same Agent?',834,196,374,86,28,bold=True)]
 els += [text('Hybrid',834,326,374,33,24,'#1d7d76',True),text('π0.5 proposes\nAstra accepts or corrects',834,370,374,70,23)]
 els += [text('Direct',834,483,374,33,24,'#1d7d76',True),text('Astra generates\nbimanual EEF targets',834,527,374,70,23)]
 return els

def background():
 els=page('Context: Models and Interfaces',1)
 els += [text('Claude Plays Robotics',64,157,700,38,27,'#1d7d76',True),text('A comparison of control responsibilities',64,204,720,32,22,'#646464')]
 rows=[('Direct action','LLM → action → controller'),('Controller code','LLM → program → action'),('Policy supervision','LLM + learned policy → action')]
 for i,(label,flow) in enumerate(rows):
  y=270+i*75
  els += [text(label,64,y,265,32,23,bold=True),text(flow,342,y,520,32,22)]
 els += [text('RPent',923,157,293,38,27,'#1d7d76',True),text('Agent\n↓\nComposable services\n↓\nRobot / simulator',923,239,293,188,23)]
 els += [text('Motion · code · learned policy',923,470,293,30,18,'#646464')]
 els += [text('Robot-data training changes the premise; older findings need re-testing.',64,553,1152,39,25,'#1d7d76',True),text('Astra-specific robot pretraining details are not established by the cited sources.',64,608,1152,32,20,'#646464')]
 return els

def protocol():
 els=page('What Enters and Leaves Each Model?',1)
 els += [text('RoboDojo · dual ARX X5 · 10 tasks × 5 paired cases per arm',64,144,1152,35,24,'#646464')]
 xs=[64,460,865];widths=[360,365,350]
 for x,w,label in zip(xs,widths,['Shared input','Direct','Hybrid']):
  els += [text(label,x,211,w,35,26,'#1d7d76',True)]
 columns=[['3 RGB views','14D proprioception','Task instruction','Astra history + notes'],['GPT 6 Astra · xhigh','No π0.5 service','Bimanual EEF (x, R, g)','Execute 1–5 steps'],['π0.5: 50 × 14 joint targets','Astra reviews + FK poses','Accept: 1–15 steps','EEF correction: 1–5 steps']]
 for x,w,rows in zip(xs,widths,columns):
  for i,label in enumerate(rows):els += [text(label,x,273+i*62,w,48,22)]
 els += [text('EEF → local IK → execution → new observation; native control is 25 Hz.',64,547,1152,34,23,'#646464')]
 els += band('The comparison changes the action prior AND the executed segment length.')
 return els

def control_results():
 els=page('RoboDojo: Results and Examples',1)
 v1,b1=video_el('anon_direct_sort',64,168,560,250,'Direct · sorting · successful rollout')
 v2,b2=video_el('anon_hybrid_pack',656,168,560,250,'Hybrid · packing · successful-rollout excerpt')
 els += v1+v2
 els += [text('Direct: 13 / 50',64,477,560,44,32,'#1d7d76',True),text('Hybrid: 24 / 50',656,477,560,44,32,'#1d7d76',True)]
 els += [text('10 selected tasks × 5 paired cases; videos show different tasks.',64,544,1152,34,23,'#646464')]
 els += band('RoboDojo simulation footage excludes LLM waiting time.')
 new_placements['control_results']=[('anon_direct_sort',b1),('anon_hybrid_pack',b2)]
 return els

def control_summary():
 els=page('Control: What Did We Learn?',1)
 rows=[('Observed','Hybrid completed more of the 50 selected paired cases.'),('Not isolated','Action prior and executed segment length both changed.'),('Still open','Which division wins at matched latency and total budget?')]
 for i,(label,body) in enumerate(rows):
  y=188+i*116;els += [text(label,80,y,220,42,27,'#1d7d76',True),text(body,325,y,875,72,28)]
 els += band('Neither “LLMs must delegate” nor “Direct always wins” follows.')
 return els

def world_summary():
 els=page('Data: Replay Is Not Prediction',2)
 rows=[('Problem','Turn real observations into a runnable simulated episode.'),('Established','48/100 accepted replays under the stated judge rule.'),('Still open','Does the same scene predict a new action or initial state?')]
 for i,(label,body) in enumerate(rows):
  y=188+i*116;els += [text(label,80,y,220,42,27,'#1d7d76',True),text(body,325,y,875,72,28)]
 els += band('A replay-acceptance score is not a physical-parameter accuracy test.')
 return els

def conclusion():
 els=page('Three Studies, Three Conclusions')
 rows=[('Control','Direct / Hybrid changes who proposes the action.','A benefit in selected tasks is not a universal division of work.'),('Data','Agentic Real2Sim builds runnable replays.','Novel-action prediction remains a separate test.'),('Improvement','ENPIRE organizes real policy-improvement experiments.','Setup, retries, verifier quality and resource costs define the claim.')]
 for i,(label,body,bound) in enumerate(rows):
  y=175+i*129
  els += [text(label,80,y,220,40,28,'#1d7d76',True),text(body,325,y,875,40,27,bold=True),text(bound,325,y+50,875,52,22,'#646464')]
 els += band('Control, reconstruction and policy improvement need different tests.')
 return els

summaries={
 'questions':('Three Questions, Three Studies',questions(),[]),
 'control':('Agent Controls Robot',control(),['ANON']),
 'background':('Context: Models and Interfaces',background(),['S09','RPENT']),
 'protocol':('What Enters and Leaves Each Model?',protocol(),['ANON']),
 'control_results':('RoboDojo: Results and Examples',control_results(),['ANON']),
 'control_summary':('Control: What Did We Learn?',control_summary(),['ANON']),
 'world':('Agent Produces Data',summary('Agent Produces Data',2,[('Recording','real interaction'),('Agent + tools','scene and parameters'),('Simulator','candidate replay'),('Comparison','replay mismatch')],'Mismatch guides the next revision','48 of 100 episodes meet the replay-acceptance rule.','Does the scene predict outcomes under new actions?','Chapter overview · Agentic Real2Sim: recording → runnable simulated episode',reference=True),['S13']),
 'world_summary':('Data: Replay Is Not Prediction',world_summary(),['S13']),
 'improve':('Agent Improves Robot',summary('Agent Improves Robot',3,[('Task + API','fixed environment'),('Agent','policy / training edits'),('Real rollout','robot experiment'),('Verifier + logs','outcome and trace')],'Evidence guides the next policy change','Policy improvement under a stated real-world protocol.','Setup, retry accounting, verifier errors and resource cost.','Chapter overview · ENPIRE: can real experiments improve a policy?'),['S15']),
 'end':('Three Studies, Three Conclusions',conclusion(),['ANON','S13','S15'])
}
# Three parts, each opening with its synthesis diagram; the hand design closes outside the three roles.
order=[1,2,'questions','control','background','protocol','control_results','control_summary','world',10,11,12,'world_summary','improve',14,15,16,17,18,19,'end']
assert len(order)==21
chapter_keys={'control','world','improve'}
new_titles={1:'Agents for Robotics',2:'Demo: Painting with Feedback',10:'Real Episode and Its Twin',11:'Agentic Real2Sim: Method',12:'DROID-100: Protocol and Results',14:'ENPIRE: The Real Task',15:'ENPIRE: Environment and Improvement',16:'ENPIRE: Reset and Verification',17:'ENPIRE: Pin Insertion Curve',18:'ENPIRE: Cost and Chapter Summary',19:'Beyond: Structural Design'}
minutes=[.5,2,1.5, 4,2,3,5,2, 2,2,4,6,2, 2,2,5,4,5,3, 1.5,1.5]
assert len(minutes)==21 and sum(minutes)==60,sum(minutes)
script_text=(B/'script_revised.md').read_text()
chunks=re.split(r'^## (\d{2})\. (.+)\n',script_text,flags=re.M)
script_sections={int(chunks[i]):chunks[i+2].strip() for i in range(1,len(chunks),3)}
script_titles={int(chunks[i]):chunks[i+1] for i in range(1,len(chunks),3)}
assert len(script_sections)==len(order),(len(script_sections),len(order))
def group_of(n):
 return 'Introduction' if n<=3 else '1 · Agent Controls Robot' if n<=8 else '2 · Agent Produces Data' if n<=13 else '3 · Agent Improves Robot' if n<=19 else 'Other Applications / Closing'
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
   if e.get('text')=='Reliable Action and Improvement':e['text']='Control, Data and Policy Improvement'
   if e.get('text')=='Technical talk\n10 September 2026':e['text']='Zimo Huang\n16 September 2026'
 if key==19:
  for e in els:
   if e.get('text')=='Design artifact':e['text']='Structural design\nCAD proposal'
 if key==18:
  for e in els:
   if e.get('text')=='Time to result, token use, and robot utilization measure different things.':e['text']='Faster policy research uses more tokens; improvement remains protocol-bound.'
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
source_map['POLICYEVAL']={'label':'GPT-Policy-Eval · selected visual-context robot trials (Sep 2026)','url':'https://github.com/cheng-haha/GPT-Policy-Eval'}
source_map['AWESOME']={'label':'Awesome-Astra-Embodied-AI · curated discovery list, not an evaluation','url':'https://github.com/zjwzcx/Awesome-Astra-Embodied-AI'}
source_map['ANON']={'label':'Anonymous technical report · GPT 6 Astra as an Embodied Policy (accessed 14 Sep 2026)','url':'https://anonymous-report-421.github.io/public-website/?lang=en&view=1'}
source_map['ROBORSI']={'label':'RoboRSI · Noematrix research report (Sep 2026)','url':'https://lab.noematrix.ai/blog/2-roborsi/'}
source_map['ROBORSI_CODE']={'label':'RoboRSI · official source and evaluation boundaries','url':'https://github.com/nssmd/RoboRSI'}
source_map['ROBORSI_EVIDENCE']={'label':'RoboRSI · ACT corrective transport evidence','url':'https://lab.noematrix.ai/assets/roborsi/evidence/simulation-showcase-v1.json'}
source_map['ASPIRE']={'label':'ASPIRE · reusable repair knowledge and held-out library transfer, §2.2 / §3.5','url':'https://arxiv.org/abs/2607.00272'}
for r,key in zip(slides,order):
 if key==1:r['ids']=[]
 if key in {10,11,12}:r['ids']=['S13']
 if key in {14,15,16,17,18}:r['ids']=['S15']
 r['sources']=[source_map[sid] for sid in r['ids']]
 if key==19:
  r['sources'] += [{'label':'Author limitation and follow-up','url':u} for u in ['https://x.com/earthtojake/status/2097789991426335015','https://x.com/earthtojake/status/2097801101890207893']]
 if isinstance(key,int):r['footer']=next((e.get('text','') for e in layouts[key] if e['kind']=='shape' and e['bbox'][1]==679),'')
 else:r['footer']='Our synthesis of '+r['sources'][0]['label'] if r['sources'] else 'One representative study per part · question, method, experiment, conclusion'
 if key=='control':r['footer']='Anonymous report · original control-system diagram, English page capture · click to enlarge'
 if key=='background':r['footer']='Background only: Claude Plays Robotics and RPent · not additional case studies'
 if key=='protocol':r['footer']='Anonymous report · RoboDojo method and paired evaluation; control-step rate is not model decision frequency'
 if key=='control_results':r['footer']='Anonymous report · 10-task RoboDojo panel only; both videos are selected illustrations, not a video-to-video comparison'
 if key=='control_summary':r['footer']='Anonymous report · bounded interpretation of the RoboDojo comparison; RoboLab is not pooled into these results'
 if key=='end':r['footer']='Synthesis of the three representative studies; no cross-paper ranking'
 if key==1:r['footer']='Primary sources checked 14 September 2026'
 r['footer']=r['footer'].replace(' | ',' · ')
 for m in new_media:
  if m['slide']==r['number']:m['posterKey']=next(e['assetKey'] for e in r['elements'] if e.get('alt')=='VIDEO:'+m['name'])

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
used_assets={key for r in slides for key in re.findall(r'data-asset="([a-f0-9]+)"',r['html'])}|{m['posterKey'] for m in new_media}
assets={key:value for key,value in assets.items() if key in used_assets}
image_audit=[record for record in image_audit if record['sha256'] in used_assets]
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
assert len(new_media)==9,len(new_media)
report={'slides':len(slides),'videos':len(new_media),'media_seconds':sum(m['duration_seconds'] for m in new_media),'minutes':sum(minutes),'chapter_opening_slides':[n for n,key in enumerate(order,1) if key in chapter_keys],'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'standalone_file':str(dest),'media':[{k:m[k] for k in ['name','slide','sha256','duration_seconds']} for m in new_media],'images':image_audit,'native_text':True,'all_fonts_embedded':True}
(B/'standalone_build_audit.json').write_text(json.dumps(report,indent=2))
(B/'slide_records_revised.json').write_text(json.dumps([{k:v for k,v in r.items() if k not in ['html','notesHtml']} for r in slides],ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k not in ['images','media']},indent=2))
