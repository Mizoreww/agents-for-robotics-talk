from pathlib import Path
import base64, copy, hashlib, html, json, mimetypes, posixpath, re, zipfile
import xml.etree.ElementTree as ET
ROOT=Path('/home/limx/Desktop/agent_for_robotics')
B=ROOT/'.build'; OUT=ROOT/'output'
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
old=json.loads((B/'slide_records_focus.json').read_text())
media=json.loads((OUT/'offline_player/media_credits.json').read_text())
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
def summary(title,num,nodes,feedback,shown,open_,setup='',reference=False):
 els=[copy.deepcopy(layouts[4][0]),text(str(num),64,57,45,48,36,'#2ba39b',True,True),text(title,110,57,965,48,36,bold=True,serif=True),rect(64,111,1152,3,'#2ba39b'),text(setup or 'Chapter overview · our synthesis',80,160,1120,45,23,'#646464')]
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
 title='Execution: An Agent with Many Tools'
 els=[copy.deepcopy(layouts[4][0]),text('1',64,57,45,48,36,'#2ba39b',True,True),text(title,110,57,965,48,36,bold=True,serif=True),rect(64,111,1152,3,'#2ba39b')]
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
 els=[copy.deepcopy(layouts[4][0]),text('Three Core Roles, Broader Applications',64,57,1011,48,36,bold=True,serif=True),rect(64,111,1152,3,'#2ba39b')]
 rows=[('Execution: direct actions and tools','Claude Plays Robotics → RPent'),('World building','Agentic Real2Sim'),('Improvement through experiments','ENPIRE'),('Other applications','Structural design · debugging · engineering tools')]
 for i,(title,detail) in enumerate(rows):
  y=169+i*120
  els += [text(str(i+1),82,y,60,48,34,'#2ba39b',True,True),text(title,186,y,1010,40,27,bold=True),text(detail,186,y+46,1010,35,22,'#646464')]
 return els

def toolkit_example():
 raw=(ROOT/'research/assets/rpent_framework.png').read_bytes()
 key=asset(raw,'image/png')
 image_audit.append({'source':'https://github.com/RLinf/RPent','alt':'Official RPent service-oriented framework','sha256':key})
 return [copy.deepcopy(layouts[4][0]),text('1',64,57,45,48,36,'#2ba39b',True,True),text('RPent: Packaging Robotics as Agent Tools',110,57,965,48,36,bold=True,serif=True),rect(64,111,1152,3,'#2ba39b'),text('Recursive Physical Agent · official project architecture',80,140,1120,35,23,'#646464'),{'kind':'image','bbox':[64,187,1152,418],'assetKey':key,'alt':'Official RPent service-oriented framework'},text('Related: ROSA (ROS agent) · ROS-MCP (MCP–ROS bridge)',80,610,1120,30,21,'#1d7d76',True),text('Architecture scope is broader than verified integrations; DreamZero is not marked supported.',80,644,1120,25,17,'#646464')]

def conclusion():
 els=[copy.deepcopy(layouts[4][0]),text('Conclusion',64,57,1011,48,36,bold=True,serif=True),rect(64,111,1152,3,'#2ba39b')]
 rows=[('Execution: match model capability and interface.','Direct actions, controllers and learned policies need different support.'),('World building: distinguish replay from prediction.','New actions test whether a reconstructed scene is useful.'),('Improvement: make real experiments repeatable.','Fixed interfaces, reset and verification support policy iteration.'),('Other applications: create engineering artifacts.','Designs and repaired programs need their own validation.')]
 for i,(title,detail) in enumerate(rows):
  y=170+i*107
  els += [text(str(i+1),79,y,64,45,31,'#2ba39b',True,True),text(title,172,y,1038,40,26,bold=True),text(detail,172,y+44,1038,34,20,'#646464')]
 els += [text('What does the Agent produce, and how do we know it works?',172,626,1038,35,25,'#1d7d76',True)]
 return els

summaries={
 'exec':('Execution: An Agent with Many Tools',execution_tools(),['S09','S10','WAM']),
 'toolkits':('RPent: Packaging Robotics as Agent Tools',toolkit_example(),['RPENT','ROSA','ROS_MCP']),
 'world':('World Building: Replay and Prediction',summary('World Building: Replay and Prediction',2,[('Recording','real interaction'),('Agent + tools','scene and parameters'),('Simulator','candidate replay'),('Comparison','replay mismatch')],'Mismatch guides the next revision','A structured workflow converts 48 of 100 recorded episodes.','Does the scene predict outcomes under new actions?',reference=True),['S13']),
 'improve':('Improvement: A Repeatable Real Experiment',summary('Improvement: A Repeatable Real Experiment',3,[('Task + API','fixed environment'),('Agent','policy / training edits'),('Real rollout','robot experiment'),('Verifier + logs','outcome and trace')],'Evidence guides the next policy change','The workflow improves policies under its stated protocol.','Reset, verifier errors, conditional retries and transfer.','Human-assisted setup; environment API fixed during improvement'),['S15']),
 'other':('Other Applications: Design and Engineering',summary('Other Applications: Design and Engineering',4,[('Engineering goal','requirements'),('Agent + Tools','CAD · code · analysis'),('Artifact','design or program'),('Validation','prototype or tests')],'Test results guide the next revision','Design proposals and repaired programs.','Do the artifacts work beyond the demonstration?','Our synthesis · broader applications, not a fourth benchmark'),['S24','S17'])
}
# Each chapter opens with its synthesis, then develops the case and evidence.
order=[1,2,3,4,'exec',6,5,7,8,9,'toolkits','world',10,11,12,13,'improve',14,15,16,17,18,'other',19,20,22]
assert len(order)==26
chapter_keys={'exec','world','improve','other'}
minutes=[.5,2,2.5,1,2,2.5,3,2.5,2,2,2.5,2,2.5,3.5,3,2,2,3,4,3.5,3,2,1.5,2,2,1.5]
assert sum(minutes)==60,sum(minutes)
# The source-backed figures retain their exact original bytes.
# The script includes distinct narration, media cues and chapter transitions.
script_text=(B/'script_revised.md').read_text()
chunks=re.split(r'^## (\d{2})\. (.+)\n',script_text,flags=re.M)
script_sections={int(chunks[i]):chunks[i+2].strip() for i in range(1,len(chunks),3)}
script_titles={int(chunks[i]):chunks[i+1] for i in range(1,len(chunks),3)}
assert len(script_sections)==len(order)
slides=[]; new_media=[]
for n,key in enumerate(order,1):
 if isinstance(key,int):
  r=copy.deepcopy(old[key-1]);els=copy.deepcopy(layouts[key])
 else:
  title,els,ids=summaries[key];r={'title':title,'ids':ids};els=copy.deepcopy(els)
 r.pop('notes',None)
 r.update(number=n,minutes=minutes[n-1],script=script_sections[n],old_slide=key if isinstance(key,int) else None,new_slide_key=key if isinstance(key,str) else None,diagram_key=key if key in chapter_keys else None,chapter_opening=key in chapter_keys)
 r['group']='Introduction' if n<=4 else '1 · Execution' if n<=11 else '2 · World building' if n<=16 else '3 · Improvement' if n<=22 else '4 · Other applications' if n<=25 else 'Conclusion'
 # Use new numbering and consistent linked source footers.
 els=[e for e in els if not(e['kind']=='shape' and e['bbox'][1]>=660)]
 if key==1:
  for e in els:
   if e.get('text')=='Reliable Action and Improvement':e['text']='Tools, Experiments and Engineering'
   if e.get('text')=='Three case studies and emerging applications':e['text']='Three case studies and broader applications'
 if key==3:
  replacements={'Finish the current job. Make the next job easier.':'Useful robotics work through tools and feedback','Robot execution':'Agent + Tools','actions with feedback':'act, build and evaluate','Reusable capability':'Useful artifacts','program, skill or policy':'design, code or policy','Capability retained for later tasks':'Validated artifacts support later tasks'}
  for e in els:
   if e.get('text') in replacements:e['text']=replacements[e['text']]
 if key==4:
  r['title']='Three Core Roles, Broader Applications';els=agenda()
 if key==5:
  r['title']='Claude Plays Robotics: Model and Interface'
  for e in els:
   if e.get('text')=='Claude Plays Robotics':e['text']=r['title']
 if key==6:
  r['title']='Direct Actions and Controller Code'
  for e in els:
   if e.get('text')=='Direct Control Meets Physical Constraints':e['text']=r['title']
 if key==7:
  r['title']='VLA Tools: Grounding and Supervision'
  replacements={'A Supervisor Can Disrupt a Capable VLA':r['title'],'Agent':'VLA tool','task-level decisions':'proposed actions','VLA policy':'Agent','motor execution':'accept · edit · replace','task outcome':'execute + observe'}
  for e in els:
   if e.get('text') in replacements:e['text']=replacements[e['text']]
 if key==9:
  r['title']='Agent + Tools: Strengths and Gaps'
  els=[e for e in els if e.get('text') not in ['A sustained physical task','What controls contact?\nWhat happens after a mistake?']]
  for e in els:
   if e.get('text')=='Demo: Wiping a Table':e['text']=r['title']
  els += [text('Where Agents help',720,175,480,36,26,'#1d7d76',True),text('Semantic goals · task decomposition\nTransfer through reusable tools',720,220,480,76,24),text('Where execution still struggles',720,326,480,35,25,'#aa514a',True),text('Continuity · contact-state estimation\nFine manipulation often favors\ntrained generative action policies',720,373,480,116,23),text('Long-horizon planning ≠ reliable execution',720,526,480,58,21,'#646464'),text('Qualitative synthesis · task-dependent',720,604,480,28,18,'#646464')]
  r['ids']=list(dict.fromkeys(['S09','S10',*r['ids']]))
 if key==18:
  r['title']='Faster Research, Higher Token Use'
  for e in els:
   if e.get('text')=='More Robots Shorten Time, but Raise Cost':e['text']=r['title']
 if key in (19,20):
  original_title=r['title']
  if key==19:r['title']='Demo: Structural Design of a Robot Hand'
  for e in els:
   if e.get('text')==original_title:
    e['text']=r['title'];e['bbox']=[110,57,965,48]
   if key==19 and e.get('text')=='Design artifact':e['text']='Structural design\nCAD proposal'
  els += [text('4',64,57,45,48,36,'#2ba39b',True,True)]
 if key==22:
  els=conclusion()
 assert script_titles[n]==r['title'],(n,script_titles[n],r['title'])
 if key=='world':
  # Keep "48/100" explicitly tied to replay acceptance, not predictive fidelity.
  for e in els:
   if e.get('text')=='A structured workflow converts 48 of 100 recorded episodes.':e['text']='48 of 100 episodes meet the replay-acceptance rule.'
 r['elements']=els;slides.append(r)
 if isinstance(key,int):
  for m in media:
   if m['slide']==key:
    m=copy.deepcopy(m);m['slide']=n
    raw=(B/'clips'/f'{m["name"]}.mp4').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==m['sha256']
    m['payloadId']='video-'+m['name'];m.pop('file',None);m.pop('poster',None)
    new_media.append(m)

source_map={}
for r in old:
 tail=r['notes'].split('SOURCES\n',1)[-1]
 for match in re.finditer(r'(S\d+): ([^\n]+)\n(https?://[^\s]+)',tail):
  sid,label,url=match.groups();source_map[sid]={'label':label,'url':url}
source_map['WAM']={'label':'DreamZero · World Action Models are Zero-shot Policies (2026)','url':'https://dreamzero0.github.io/'}
source_map['RPENT']={'label':'RPent · Recursive Physical Agent (RLinf), official framework and source','url':'https://github.com/RLinf/RPent'}
source_map['ROSA']={'label':'ROSA · Robot Operating System Agent (NASA JPL)','url':'https://github.com/nasa-jpl/rosa'}
source_map['ROS_MCP']={'label':'ROS-MCP Server · MCP–ROS bridge','url':'https://github.com/robotmcp/ros-mcp-server'}
for r,key in zip(slides,order):
 r['sources']=[source_map[sid] for sid in r['ids']]
 if key==19:
  r['sources'] += [{'label':'Author limitation and follow-up','url':u} for u in ['https://x.com/earthtojake/status/2097789991426335015','https://x.com/earthtojake/status/2097801101890207893']]
 if isinstance(key,int):
  r['footer']=next((e.get('text','') for e in layouts[key] if e['kind']=='shape' and e['bbox'][1]==679),'')
 else:r['footer']='Our synthesis · based on '+r['sources'][0]['label']
 if key=='exec':r['footer']='Our synthesis · Claude Plays Robotics; Robocurve (IK); DreamZero (WAM) · not one evaluated stack'
 if key=='other':r['footer']='Our synthesis · hand design demonstration and ASPIRE · see notes for source limitations'
 if key=='toolkits':r['footer']='RPent official project figure · supporting ecosystem example, not a fourth deep case study · ROSA / ROS-MCP: see notes'
 if key==9:r['footer']='Synthesis: Claude Plays Robotics / Robocurve · wiping: @k7agar, X (qualitative illustration)'
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
page=(B/'standalone_shell.html').read_text().replace('/* EMBEDDED_FONTS */',fontcss).replace('/* PLAYER_CSS */',(B/'standalone_player.css').read_text()).replace('<!-- DECK_DATA -->','<script type="application/json" id="deck-data">'+data_json+'</script>').replace('/* PLAYER_JS */',(B/'standalone_player.js').read_text())
# Keep binary payloads out of executable JS and materialize only active clips.
payloads=[]
for m in new_media:
 raw=(B/'clips'/f'{m["name"]}.mp4').read_bytes()
 payloads.append(f'<script id="{m["payloadId"]}" type="application/octet-stream" data-sha256="{m["sha256"]}">{base64.b64encode(raw).decode()}</script>')
page=page.replace('<!-- VIDEO_PAYLOADS -->','\n'.join(payloads))
dest=OUT/'Agents_for_Robotics_Self_Contained.html';dest.write_text(page)
assert len(new_media)==15
report={'slides':len(slides),'videos':len(new_media),'media_seconds':sum(m['duration_seconds'] for m in new_media),'minutes':sum(minutes),'chapter_opening_slides':[n for n,key in enumerate(order,1) if key in chapter_keys],'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'standalone_file':str(dest),'media':[{k:m[k] for k in ['name','slide','sha256','duration_seconds']} for m in new_media],'images':image_audit,'native_text':True,'all_fonts_embedded':True}
(B/'standalone_build_audit.json').write_text(json.dumps(report,indent=2))
(B/'slide_records_revised.json').write_text(json.dumps([{k:v for k,v in r.items() if k not in ['html','notesHtml']} for r in slides],ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k not in ['images','media']},indent=2))
