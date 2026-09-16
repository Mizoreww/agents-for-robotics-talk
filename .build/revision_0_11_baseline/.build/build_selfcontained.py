from pathlib import Path
import base64, copy, hashlib, html, json, mimetypes, posixpath, re, zipfile
import xml.etree.ElementTree as ET
ROOT=Path('/home/limx/Desktop/agent_for_robotics')
B=ROOT/'.build'; OUT=ROOT/'output'
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
old=json.loads((B/'slide_records_focus.json').read_text())
media=json.loads((OUT/'offline_player/media_credits.json').read_text())
community=[]
for manifest in ['clip_manifest.json','clip_manifest_v2.json','clip_manifest_v3.json','clip_manifest_v4.json']:
 community += json.loads((B/manifest).read_text())
for c in community:
 c.setdefault('source_url',next((m['sourceUrl'] for m in media if m['name']==c['name']),''))
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
 s=min(w/vw,h/vh);return [round(x+(w-vw*s)/2,2),round(y+(h-vh*s)/2,2),round(vw*s,2),round(vh*s,2)]
def video_el(name,x,y,w,h,caption):
 # The poster image is never drawn; the player reads it through the VIDEO: alt lookup.
 c=clip_by_name[name];bx=fit(x,y,w,h,c['width'],c['height'])
 key=asset(Path(c['poster']).read_bytes(),'image/jpeg')
 image_audit.append({'source':c['source_url'],'alt':'VIDEO:'+name,'sha256':key})
 return [{'kind':'image','bbox':bx,'assetKey':key,'alt':'VIDEO:'+name},text('▷  '+caption,x,y+h+4,w,30,17,'#646464')],bx
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
CLAUDE_URL='https://www.anthropic.com/research/claude-plays-robotics'
A8=B/'assets/v0_8'
new_placements={}
def figure(file,alt,x,y,w,h,source):
 from PIL import Image
 vw,vh=Image.open(file).size
 scale=min(w/vw,h/vh);bw,bh=vw*scale,vh*scale
 return original_image(file,alt,x+(w-bw)/2,y+(h-bh)/2,bw,bh,source)
def pair_videos(key,title,num,left,right,labels,caption):
 els=page(title,num)
 for name,x,label in zip([left,right],[64,656],labels):
  els += [text(label,x,157,560,34,24,'#1d7d76',True)]
  ve,bx=video_el(name,x,215,560,333,'Selected clip · fullscreen in video controls')
  els += ve
  new_placements.setdefault(key,[]).append((name,bx))
 els += band(caption)
 return els

def questions():
 els=page('Three Roles for Robotics Agents')
 rows=[('Control','Who generates the next action?','Direct commands, tools and learned policies'),('Simulation','Can recorded interaction become a scene?','Agentic Real2Sim + emerging Astra workflows'),('Improvement','What makes the next policy better?','ENPIRE + training and in-context adaptation')]
 for i,(role,q,work) in enumerate(rows):
  y=173+i*130
  els += [text(str(i+1),80,y,70,42,32,'#2ba39b',True,True),text(role,168,y,230,38,28,'#1d7d76',True),text(q,422,y,785,38,27,bold=True),text(work,422,y+48,785,32,21,'#646464')]
 return els+band('Established experiments explain mechanisms; new demos reopen the boundaries.')

# Original chapter-wide Agent/action/tools diagram is retained, not replaced by a case-study diagram.
def execution_tools():
 els=page('Agent Controls Robot',1)
 els += [text('Chapter overview · direct commands and composable Agent Tools',80,148,1120,38,22,'#646464')]
 els += [text('Task + observations',112,286,276,34,22,align='center'),connector(250,322,250,365),rect(140,365,220,88,'#2ba39b'),text('Agent',148,379,204,34,27,'#ffffff',True,align='center'),text('act or call tools',148,418,204,28,18,'#e2f3ef',align='center')]
 els += [rect(500,210,350,60,'#edf7f4','#2ba39b'),text('Direct action output',511,215,328,29,22,'#1d7d76',True),text('q / EEF Pose · numeric commands',511,244,328,25,17,'#646464'),text('Agent Tools',500,284,350,30,22,'#1d7d76',True)]
 tools=[('IK / motion planner','Pose targets to joint motion'),('Controller code','Fast local feedback'),('VLA / WAM / Learned policy','Learned action / world-action priors')]
 centers=[240]
 els += [connector(412,240,500,240),connector(850,240,939,240,arrow=False)]
 for i,(label,benefit) in enumerate(tools):
  y=323+i*72;centers.append(y+30)
  els += [rect(500,y,350,60,'#f4f6f5','#c6d9d6'),text(label,511,y+5,328,29,20,bold=True),text(benefit,511,y+34,328,22,16,'#646464')]
  els += [connector(412,y+30,500,y+30),connector(850,y+30,939,y+30,arrow=False)]
 els += [connector(360,409,412,409,arrow=False),connector(412,centers[0],412,centers[-1],arrow=False),connector(939,centers[0],939,centers[-1],arrow=False),connector(939,409,1010,409),text('Action outputs',984,317,233,32,19,'#646464',align='center')]
 els += [rect(1010,365,190,88,'#f4f6f5','#c6d9d6'),text('Execution',1018,379,174,34,24,bold=True,align='center'),text('servo / controller',1018,418,174,28,17,'#646464',align='center')]
 # Feedback is observed state, not an assertion that every tool emits motor actions.
 els += [connector(1105,453,1105,595,'#2ba39b',False),connector(1105,595,850,595,'#2ba39b'),text('Observations',878,552,213,30,19,'#1d7d76',align='center'),rect(500,565,350,60,'#edf7f4','#c6d9d6'),text('Perception / state tools',511,570,328,29,22,'#1d7d76',True),text('pose · depth · heading',511,599,328,25,17,'#646464'),connector(500,595,250,595,'#2ba39b',False),connector(250,595,250,453,'#2ba39b')]
 els += [text('Direct commands or tools: the runtime still closes low-level loops.',80,639,1120,30,22,'#1d7d76',True)]
 return els

def hierarchy():
 els=page('Hierarchical Robot Control',1)
 els += [text('Hi Robot',64,149,495,32,25,'#1d7d76',True),figure(A8/'hirobot.png','Hi Robot original architecture: high-level VLM and pi0',64,204,495,350,'https://www.pi.website/research/hirobot')]
 els += [text('Helix',602,143,145,29,23,'#1d7d76',True),text('S2 latent → S1 action',813,147,397,27,19,'#646464'),figure(A8/'helix01.png','Figure Helix original architecture: System 2 to System 1',602,178,608,171,'https://www.figure.ai/news/helix')]
 els += [text('Helix 02',602,358,150,29,23,'#1d7d76',True),text('S2 → S1 joint targets → S0',813,362,397,27,19,'#646464'),figure(A8/'helix02.png','Figure Helix 02 original architecture with System 0',602,392,608,209,'https://www.figure.ai/news/helix-02')]
 els += [text('VLM → subtask language → π0 → action',64,552,510,45,20,'#646464')]
 return els+band('Reasoning → visuomotor policy → low-level control: a common division, not a law.')

def claude_method():
 els=page('Claude Plays Robotics: Interfaces',1)
 els += [text('Foundation model',64,151,232,31,21,'#646464',align='center'),
         text('Interfaces',392,151,464,31,23,'#1d7d76',True,align='center'),
         text('Execution / training output',938,151,278,31,19,'#646464',align='center')]
 els += [rect(80,332,200,90,'#2ba39b'),text('LLM',88,352,184,47,34,'#ffffff',True,align='center')]
 rows=[(210,'Direct action','7D EEF motion',False),(302,'Controller code','Python feedback program',False),
       (394,'Policy supervision','MolmoAct proposal · accept / edit / replace',False),
       (508,'Training supervision','RL training code',True)]
 els += [connector(280,377,336,377,arrow=False),connector(336,247,336,545,arrow=False)]
 for y,label,detail,training_output in rows:
  els += [connector(336,y+37,392,y+37),rect(392,y,464,74,'#f1f7f5','#c6d9d6'),
          text(label,404,y+7,440,31,23,bold=True,align='center'),
          text(detail,404,y+42,440,26,18,'#646464',align='center')]
  els += [connector(856,y+37,958 if training_output else 912,y+37,arrow=training_output)]
 els += [connector(912,247,912,431,arrow=False),connector(912,339,958,339),
         rect(958,297,258,84,'#eaf5f3','#2ba39b'),text('Controller',966,315,242,36,26,'#1d7d76',True,align='center'),
         text('robot execution',966,351,242,25,17,'#646464',align='center'),
         rect(958,503,258,84,'#eaf5f3','#2ba39b'),text('Learned policy',966,521,242,36,26,'#1d7d76',True,align='center'),
         text('training output',966,557,242,25,17,'#646464',align='center')]
 return els+band('Manipulation results next: LIBERO-40 · 40 tasks × 5 seeds per condition.')

def claude_results():
 els=page('Claude: The Value of a Motor Prior',1)
 els += [figure(A8/'claude_direct_sr.png','Original Direct LIBERO-40 success-rate panel; uncertainty and all model labels retained',64,143,556,340,CLAUDE_URL),figure(A8/'claude_vla_sr.png','Original supervised LIBERO-40 panel; VLA-alone baseline and uncertainty retained',660,143,556,340,CLAUDE_URL)]
 els += result_table(['LIBERO-40', 'Opus 4.6 Direct', 'Opus 4.6 + MolmoAct', 'MolmoAct alone'],
                     [['Success rate', '3.5%', '76%', '86%'], ['Trials / condition', '200', '200', '200']],
                     [260,290,332,270],y=497,row_h=38,head_h=39,size=21,
                     comparisons=[([(0,1),(0,2),(0,3)],'max')])
 return els+result_note('40 tasks × 5 seeds. Adding a supervisor does not always improve an already capable motor policy.',626,18)

def rpent():
 els=page('RPent: Organizing Robot Tools',1)
 els += [figure(ROOT/'research/assets/rpent_framework.png','RPent original framework',64,145,1152,445,'https://github.com/RLinf/RPent')]
 return els+band('Memory, tools and action primitives make capabilities composable.')

def astra_direct():
 els=page('Astra: Direct Actions in Practice',1)
 for name,x,label in [('astra_bowl',64,'Block into bowl'),('astra_insertion',656,'Puzzle into groove')]:
  els += [text(label,x,145,560,31,24,'#1d7d76',True)]
  ve,bx=video_el(name,x,185,560,249,'Absolute EEF → IK · model waiting omitted')
  els+=ve;new_placements.setdefault('astra_direct',[]).append((name,bx))
 rows=[]
 for task in ['Block into bowl','Puzzle into groove']:
  records=[r for r in results_data['robocurve'] if r['task']==task]
  rows.append([task]+[f"{r['successes']} / {r['n']}" for r in records])
 els += result_table(['Completions', 'Fable 5', 'Fable 5.1', 'GPT-6 Astra'],rows,
                     [432,240,240,240],y=486,row_h=37,head_h=39,size=22,
                     comparisons=row_maxima(rows,[1,2,3]))
 return els+result_note('20 calls/run; same insertion rig, different bowl rigs; Astra ran two days later. Grading was not blinded.\nNo independent VLA. This is not a robot-pretraining causal ablation.',611,17)

def control_demos():
 return pair_videos('control_demos','Astra: Visual Feedback in Action',1,'policy_plug','keyboard',['Plug insertion · real robot · 12×','Keyboard correction · real robot · 20×'],'Selected demonstrations, not success-rate estimates.')

def action_interfaces():
 els=page('Same Astra, Different Action Outputs',1)
 labels=['ΔEEF chunks','EEF waypoints','Code → waypoints']
 for x,label,count,budget in zip([64,460,856],labels,['1 / 20','18 / 20','16 / 20'],['≤200 steps · 10 queries','≤500 steps · 16 queries','≤500 steps · 3 revisions']):
  els += [text(label,x,151,360,35,25,'#1d7d76',True),text(count,x,505,360,44,32,'#1d7d76',True),text(budget,x,557,360,28,18,'#646464')]
 for name,x in [('asim_delta',88),('asim_waypoint',484)]:
  ve,bx=video_el(name,x,218,300,260,'Square ep00 · simulation replay')
  els+=ve;new_placements.setdefault('interfaces',[]).append((name,bx))
 els += [rect(888,259,280,64,'#f1f7f5','#c6d9d6'),text('plan(scene)',900,275,256,34,25,align='center'),connector(1028,323,1028,367),rect(888,367,280,64,'#f1f7f5','#c6d9d6'),text('≤12 waypoints',900,385,256,30,23,align='center')]
 return els+band('Square · same model / proprio setting · unequal control and query budgets.')

def direct_hybrid():
 els=page('Astra: Direct or Hybrid?',1)
 els += [figure(B/'assets/v0_7/report_architecture_original.png','Original anonymous Direct/Hybrid execution architecture; click to inspect inputs and step horizons',64,139,715,508,ANON_URL)]
 for name,y,caption in [('anon_direct_sort',154,'Direct · 13 / 50 · sorting simulation'),('anon_hybrid_pack',391,'Hybrid · 24 / 50 · packing simulation')]:
  ve,bx=video_el(name,821,y,395,196,caption);els+=ve;new_placements.setdefault('hybrid',[]).append((name,bx))
 return els

def control_summary():
 els=page('Where Should the Boundary Sit?',1)
 els += [text('What limits this control loop?',64,162,1152,43,30,'#1d7d76',True)]
 nodes=[('Semantic intent','Goal, objects, constraints'),('Spatial grounding','Pose, frame, alignment'),
        ('Physical interaction','Contact, timing, recovery')]
 for i,(label,detail) in enumerate(nodes):
  x=64+392*i
  els += [rect(x,255,368,109,'#f1f7f5','#c6d9d6'),text(label,x+14,273,340,36,27,bold=True,align='center'),
          text(detail,x+14,322,340,29,20,'#646464',align='center'),connector(x+184,364,x+184,412,arrow=False)]
 els += [connector(248,412,1032,412,arrow=False),connector(640,412,640,456),
         rect(385,456,510,76,'#2ba39b'),text('Choose the division of work',399,476,482,38,28,'#ffffff',True,align='center'),
         text('Model + interface + feedback',385,547,510,35,24,'#1d7d76',align='center')]
 return els+band('Stronger models can move the boundary. Test the task and budget again.')
def world_summary():
 els=page('From Replay to Prediction',2)
 for y,label,outcome,color in [(242,'Recorded action','Matching replay','#1d7d76'),(418,'New action / state','Predictive simulation?','#aa514a')]:
  els += [text(label,98,y,357,43,29,color,True),connector(460,y+20,700,y+20),text(outcome,757,y,425,43,29,color,True)]
 els += [text('Observed: accepted episode twins',98,304,1030,35,23,'#646464'),text('Next test: interventions beyond the reference trajectory',98,480,1030,35,23,'#646464')]
 return els+band('A runnable scene is a useful artifact; new-action prediction is a separate test.')

def simulation_demos():
 return pair_videos('simulation_demos','Astra Builds Simulation Workflows',2,'astra_real2sim','office_newton',['Multi-view RGB + actions → replay','Office reference → Newton / G1'],'Author-reported construction workflows; clips show outputs, not predictive accuracy.')

def idea_tree():
 els=page('ENPIRE: What Did the Agent Change?',3)
 els += [figure(A8/'enpire_idea_tree_original.png','ENPIRE Figure 12: original idea tree and hill-climbing curve, including no-gain nodes',64,139,728,512,'https://arxiv.org/html/2606.19980v1#A2.F12')]
 for y,label,detail in [(204,'Change the learning objective','I37 · BC regularization'),(325,'Tune the training procedure','I66 · batch size 1024 → 512'),(446,'Adjust execution behavior','I76 · controller compensation')]:
  els += [text(label,830,y,386,68,25,'#1d7d76',True),text(detail,830,y+68,386,35,19,'#646464')]
 els += [text('Filled nodes improve the best score.\nOpen nodes show no gain.',830,586,386,68,20,'#646464')]
 return els

def improvement_demos():
 return pair_videos('improvement_demos','Astra: Training and Context',3,'quad_rl','wenli_icl',['CAD + RL · development preview','Physical in-context learning · 8×'],'Different mechanisms: training/code revision versus adaptation through context.')

def conclusion():
 els=page('Takeaways')
 els += [text('Different artifacts. Different tests.',64,151,1152,37,27,'#1d7d76',True)]
 for x,w,label in [(342,210,'Role'),(637,210,'Artifact'),(932,284,'Evidence')]:
  els += [text(label,x,218,w,31,20,'#646464',align='center')]
 els += [rect(64,371,200,82,'#2ba39b'),text('Agent',74,392,180,38,30,'#ffffff',True,align='center'),
         connector(264,412,300,412,arrow=False),connector(300,292,300,532,arrow=False)]
 rows=[('Control','Action','Reliable execution'),('Simulation','Scene','New-action validity'),
       ('Improvement','Policy update','Held-out gain + cost')]
 for i,(role,artifact,evidence) in enumerate(rows):
  y=258+120*i
  els += [connector(300,y+34,342,y+34)]
  for x,w,label,emphasis in [(342,210,role,False),(637,210,artifact,True),(932,284,evidence,False)]:
   els += [rect(x,y,w,68,'#eaf5f3' if emphasis else '#f4f6f5','#c6d9d6'),
           text(label,x+8,y+18,w-16,34,23,'#1d7d76' if emphasis else '#1a1a1a',emphasis,align='center')]
  els += [connector(552,y+34,637,y+34),connector(847,y+34,932,y+34)]
 return els+band('Re-test the division of work as models improve.')

def thank_you():
 return [copy.deepcopy(layouts[4][0]),
         text('Thank you',64,245,1152,108,76,'#1a1a1a',True,True,'center'),
         rect(552,382,176,4,'#2ba39b'),
         text('Questions & discussion',64,419,1152,48,32,'#1d7d76',align='center'),
         text('Zimo Huang · 16 September 2026',64,565,1152,35,23,'#646464',align='center')]

from results_slides_v09 import make_results
from table_emphasis import column_extrema, row_maxima
result_slides,result_table,result_note,results_data=make_results(ROOT,page,text,rect,figure,band)
summaries={
 'questions':('Three Roles for Robotics Agents',questions(),[]),
 'control':('Agent Controls Robot',execution_tools(),['S09','RPENT','WAM']),
 'hierarchy':('Hierarchical Robot Control',hierarchy(),['HIROBOT','HELIX','HELIX02']),
 'claude_method':('Claude Plays Robotics: Interfaces',claude_method(),['S09']),
 'claude_results':('Claude: The Value of a Motor Prior',claude_results(),['S09']),
 'rpent':('RPent: Organizing Robot Tools',rpent(),['RPENT']),
 'astra_direct':('Astra: Direct Actions in Practice',astra_direct(),['ROBOCURVE']),
 'control_demos':('Astra: Visual Feedback in Action',control_demos(),['POLICYEVAL','KEYBOARD','AWESOME']),
 'interfaces':('Same Astra, Different Action Outputs',action_interfaces(),['ASIM']),
 'hybrid':('Astra: Direct or Hybrid?',direct_hybrid(),['ANON']),
 'control_summary':('Where Should the Boundary Sit?',control_summary(),['HIROBOT_DISCUSSION','S09','ASIM','ANON']),
 'world':('Agent Builds Simulation',summary('Agent Builds Simulation',2,[('Recording','views · calibration · motion'),('Agent + tools','construct / repair scene'),('Simulator','candidate replay'),('Comparison','reference alignment')],'Mismatch guides the next revision','A runnable scene and its replay artifacts.','Can this automate manual episode conversion?','Chapter overview · Agentic Real2Sim: real recording → simulation',reference=True),['S13']),
 'simulation_demos':('Astra Builds Simulation Workflows',simulation_demos(),['S12','OFFICE','AWESOME']),
 'world_summary':('From Replay to Prediction',world_summary(),['S13']),
 'improve':('Agent Improves Policy',summary('Agent Improves Policy',3,[('Task + API','fixed environment'),('Agent','policy / training edits'),('Real rollout','robot experiment'),('Verifier + logs','outcome and trace')],'Evidence guides the next policy change','Policy / code changes that persist into later trials.','Can real experiments drive reusable improvement?','Chapter overview · ENPIRE: improve the next policy, not just the next action'),['S15']),
 'idea_tree':('ENPIRE: What Did the Agent Change?',idea_tree(),['S15']),
 'improvement_demos':('Astra: Training and Context',improvement_demos(),['QUAD','WENLI','AWESOME']),
 'end':('Takeaways',conclusion(),['ANON','S13','S15','AWESOME']),
 'thanks':('Thank You',thank_you(),[])
}
summaries.update(result_slides)
order=[1,2,'questions','control','hierarchy','hirobot_results','claude_method','claude_results','rpent','rpent_results','astra_direct','control_demos','interfaces','interface_results','hybrid','robodojo_results','robolab_results','control_summary','world',10,11,12,'real2sim_results','simulation_demos','world_summary','improve',15,16,'idea_tree',17,'enpire_results','enpire_robocasa','improvement_demos',18,19,'end','thanks']
assert len(order)==37
chapter_keys={'control','world','improve'}
new_titles={1:'Agents for Robotics',2:'Demo: Painting with Feedback',10:'Real Episode and Its Twin',11:'Agentic Real2Sim: Method',12:'DROID-100: Protocol and Results',15:'ENPIRE: Environment and Improvement',16:'ENPIRE: Reset and Verification',17:'ENPIRE: Pin Insertion Curve',18:'ENPIRE: Cost and Chapter Summary',19:'Beyond: Structural Design'}
minutes=[.5,1,1,1.5,2.5,2,2,2,1,1.5,2,1,2,1.5,3,2,2.5,1,1,1.5,3,1.5,2,1,1,1,2,1.5,2.5,2,2.5,1.5,1,2.5,1,1,.5]
assert len(minutes)==37 and sum(minutes)==60,sum(minutes)
script_text=(B/'script_revised.md').read_text()
chunks=re.split(r'^## (\d{2})\. (.+)\n',script_text,flags=re.M)
script_sections={int(chunks[i]):chunks[i+2].strip() for i in range(1,len(chunks),3)}
script_titles={int(chunks[i]):chunks[i+1] for i in range(1,len(chunks),3)}
assert len(script_sections)==len(order),(len(script_sections),len(order))
def group_of(n):
 return 'Introduction' if n<=3 else '1 · Agent Controls Robot' if n<=18 else '2 · Agent Builds Simulation' if n<=25 else '3 · Agent Improves Policy' if n<=34 else 'Other Applications / Closing'
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
   if e.get('text')=='Reliable Action and Improvement':e['text']='Control, Simulation and Policy Improvement'
   if e.get('text')=='Technical talk\n10 September 2026':e['text']='Zimo Huang\n16 September 2026'
 if key==19:
  for e in els:
   if e.get('text')=='Design artifact':e['text']='Structural design\nCAD proposal'
 if key==10:
  for e in els:
   if e.get('text','').startswith('Does matching this recording'):e['text']='A recorded interaction becomes a runnable simulator episode.'
 if key==12:
  els += [text('≤5 candidates · 3 VLM judges · any judge’s best candidate ≥8/10 passes',84,571,1112,28,18,'#646464')]
 if key==18:
  for e in els:
   if e.get('alt','').startswith('Original ENPIRE resource'):e['bbox']=[126,135,1027,320]
   if e.get('text')=='Time to result, token use, and robot utilization measure different things.':e['text']='More parallel experiments reduce research time, but tokens and idle time still count.'
  utilization=results_data['enpire_resources']['utilization'];tokens=results_data['enpire_resources']['tokenRate']
  cost_rows=[[str(r['agentCount']),f"{r['robotMean']:.1f} ± {r['robotStd']:.1f}%",f"{r['gpuMean']:.1f} ± {r['gpuStd']:.1f}%",f"{t['mean']/1000:.1f} ± {t['std']/1000:.1f}k"] for r,t in zip(utilization,tokens)]
  assert [r['agentCount'] for r in utilization]==[r['agentCount'] for r in tokens]
  els+=result_table(['Agent–robot pairs','Mean robot utilization','Mean GPU utilization','Mean tokens / minute'],cost_rows,[252,300,300,300],y=467,row_h=31,head_h=32,size=19,
                    comparisons=column_extrema(cost_rows,[(1,'max'),(2,'max'),(3,'min')]))
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
source_map['HARNESS']={'label':'Harness VLA v4 · Table 3, LIBERO-Pro; RPent publication (2 Sep 2026)','url':'https://arxiv.org/html/2607.08448v4#S3.T3'}
source_map['HIROBOT_DISCUSSION']={'label':'Hi Robot v2 §6 · model-level separation is not fundamental','url':'https://arxiv.org/html/2502.19417v2#S6'}
source_map['ENPIRE_SITE']={'label':'ENPIRE official interactive plots · model and resource data (accessed 14 Sep 2026)','url':'https://research.nvidia.com/labs/gear/enpire/'}
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
source_map.update({
 'HIROBOT':{'label':'Hi Robot · original hierarchical architecture (Feb 2025)','url':'https://www.pi.website/research/hirobot'},
 'HELIX':{'label':'Figure Helix · original S2/S1 architecture (Feb 2025)','url':'https://www.figure.ai/news/helix'},
 'HELIX02':{'label':'Figure Helix 02 · original S2/S1/S0 architecture (Jan 2026)','url':'https://www.figure.ai/news/helix-02'},
 'ROBOCURVE':{'label':'Robocurve · GPT-6 Astra direct EEF evaluation (Sep 2026)','url':'https://openai.robocurve.org/gpt-6-astra/'},
 'ASIM':{'label':'Astra control dashboard · prompt-v3, same-model interface records; unequal budgets','url':'https://asimfish.github.io/astra-control-dashboard/#sec3'},
 'KEYBOARD':{'label':'Kaifeng Zhang (@kaiwynd) · Astra keyboard feedback demo, 20×','url':'https://x.com/kaiwynd/status/2098823484474348008'},
 'OFFICE':{'label':'Jiarui Xu (@Jiarui_X) · office reference to Newton/G1 scene; author-reported workflow','url':'https://x.com/Jiarui_X/status/2098439950991806804'},
 'QUAD':{'label':'Akira Sasaki (@gclue_akira) · quadruped CAD/RL development preview; partial evaluation gates','url':'https://x.com/gclue_akira/status/2098300921658868185'},
})
footers={
 'control':'Chapter overview · our synthesis; q/EEF are options, not all tested in every cited work',
 'hierarchy':'Original figures · Hi Robot: two inference levels; Helix 02 adds S0 · checked Figure releases disclose no repeat-trial success table',
 'hirobot_results':'Hi Robot v2 Figure 5 + official chart averages · 20 trials/task/method; IA and TP are not episode success rates',
 'claude_method':'Claude Plays Robotics · interface synthesis grounded in report; manipulation is the detailed example',
 'claude_results':'Original success-rate panels; different y-axis scales · all models, uncertainty and VLA-alone baseline retained',
 'rpent':'RPent original framework · illustrated capabilities are not all independently evaluated backends',
 'rpent_results':'Harness VLA v4 Table 3 · same frozen backend; few-shot exploration memory and extra compute, not a pure interface ablation',
 'astra_direct':'Robocurve · selected episodes, model waiting omitted · official robot-pretraining recipe/cause not disclosed',
 'control_demos':'Community demonstrations · selected trials; no aggregate success rate · source playback 12× / 20×',
 'interfaces':'Author experiment dashboard, not a matched-budget ablation · 20 episodes/condition · model waiting omitted',
 'interface_results':'Asim prompt-v3 dashboard · all 3 tasks and 7 conditions retained; observation and execution/query budgets differ',
 'hybrid':'RoboDojo: 10 selected tasks × 5 paired cases · simulation clips omit LLM waiting · prior/interface/horizon vary',
 'robodojo_results':'Anonymous report · case counts recalculated from 100 public records; task subset and scored-episode denominator retained',
 'robolab_results':'Anonymous report · selected final-slot outcomes + historical first-five baselines; descriptive, not matched fresh attempts',
 'control_summary':'Our diagnostic synthesis · coupled task demands, not System 2 / 1 / 0 layers · Direct still uses low-level control',
 'simulation_demos':'Community demonstrations · source speed unspecified; workflow and physical fidelity are not independently validated',
 'real2sim_results':'Agentic Real2Sim v3 Figure 3 · partial: score 7; failed: ≤6 or no valid record · not a total-cost or predictive-validity metric',
 'idea_tree':'ENPIRE Appendix B.6, original Figure 12 · one team run, best-score trajectory; not independent causal ablations',
 'improvement_demos':'Quadruped: 4 experts, some FULL EVAL NOT MET, Wave/Sit CUT · ICL: existing motion tools, 8×, no trial denominator',
 'enpire_results':'ENPIRE Figure 3 + official plot data · Codex/GPT-5.5 xhigh; Claude/Opus 4.7 High; Kimi/K2.6 thinking',
 'enpire_robocasa':'ENPIRE Figure 6 + Appendix D.2 · autoresearch improves tool/policy programs; aggregate pooling details not fully disclosed',
 'end':'Different artifacts and different tests · community demos motivate questions, not cross-paper rankings',
 'thanks':'Agents for Robotics',
}
table_legends={
 'hirobot_results':'Bold: best model average; human oracle excluded.',
 'claude_results':'Bold: highest reported success rate.',
 'rpent_results':'Bold: column maximum; ties retained.',
 'astra_direct':'Bold: row maximum; descriptive, not a controlled model comparison.',
 'interface_results':'Bold: best reported Astra per task; observations and budgets differ.',
 'robodojo_results':'Bold: row maximum; prior, interface and horizon co-vary.',
 'robolab_results':'Bold: descriptive row maximum, not paired superiority.',
 'real2sim_results':'Bold: most Accepted, fewest Failed, lowest model-call bill.',
 'enpire_results':'Bold: highest reported mean per task; not statistical significance.',
 'enpire_robocasa':'Bold: reported highest aggregate bar; no estimated percentage.',
 18:'Bold: highest utilization / lowest fleet token rate; no overall efficiency winner.',
}
for r,key in zip(slides,order):
 if key==1:r['ids']=[]
 if key in {10,11,12}:r['ids']=['S13']
 if key in {14,15,16,17,18}:r['ids']=['S15']
 if key==18:r['ids']=['S15','ENPIRE_SITE']
 r['sources']=[source_map[sid] for sid in r['ids']]
 if key==19:
  r['sources'] += [{'label':'Author limitation and follow-up','url':u} for u in ['https://x.com/earthtojake/status/2097789991426335015','https://x.com/earthtojake/status/2097801101890207893']]
 if isinstance(key,int):r['footer']=next((e.get('text','') for e in layouts[key] if e['kind']=='shape' and e['bbox'][1]==679),'')
 else:r['footer']='Our synthesis of '+r['sources'][0]['label'] if r['sources'] else 'Three roles · mechanisms, experiments and emerging applications'
 if key in footers:r['footer']=footers[key]
 if key==18:r['footer']='ENPIRE Figure 7 · pin insertion · official mean ± std; aggregation not fully specified · robot/GPU time fractions; fleet tokens/min'
 if key==1:r['footer']='Primary sources checked 14 September 2026'
 if key in table_legends:r['footer']=table_legends[key]+' '+r['footer']
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
  metadata=''
  if 'tableCell' in e:
   row,col=e['tableCell'];metadata=f' data-table-cell="{row},{col}" data-result-best="{str(e["resultEmphasis"]).lower()}"'
  return f'<div class="text"{metadata} style="{html.escape(sty,quote=True)}">{html.escape(e["text"])}</div>'
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
assert len(new_media)==18,len(new_media)
report={'slides':len(slides),'videos':len(new_media),'media_seconds':sum(m['duration_seconds'] for m in new_media),'minutes':sum(minutes),'chapter_opening_slides':[n for n,key in enumerate(order,1) if key in chapter_keys],'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'standalone_file':str(dest),'media':[{k:m[k] for k in ['name','slide','sha256','duration_seconds']} for m in new_media],'images':image_audit,'native_text':True,'all_fonts_embedded':True}
(B/'standalone_build_audit.json').write_text(json.dumps(report,indent=2))
(B/'slide_records_revised.json').write_text(json.dumps([{k:v for k,v in r.items() if k not in ['html','notesHtml']} for r in slides],ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k not in ['images','media']},indent=2))
