import fs from 'node:fs/promises';
import path from 'node:path';
import { Presentation, PresentationFile } from '@oai/artifact-tool';
import sharp from 'sharp';
const ROOT='/home/limx/Desktop/agent_for_robotics';
const BUILD=path.join(ROOT,'.build');
const C={teal:'#2ba39b',dark:'#1d7d76',ink:'#1a1a1a',gray:'#646464',light:'#eaf5f3',line:'#c6d9d6',red:'#aa514a',pale:'#f7eeec',cite:'#96958e'};
const FONT='Noto Sans',SERIF='Noto Serif';
const deck=Presentation.create({slideSize:{width:1280,height:720}});
const media=[], records=[];
const timelog=[0.5,2.5,2.5,1,3,3.5,3,3,2,3,4,3,3,3,4.5,3,3.5,2.5,2,2,4,1.5];
const catalog=JSON.parse(await fs.readFile(path.join(ROOT,'research/sources.json'),'utf8'));
const SOURCE={
 S01:['SayCan (2022)','https://say-can.github.io/'],S02:['Inner Monologue (2022)','https://innermonologue.github.io/'],
 S03:['Code as Policies (2022)','https://code-as-policies.github.io/'],S04:['VoxPoser (2023)','https://voxposer.github.io/'],
 S05:['Eureka (2023)','https://eureka-research.github.io/'],S06:['DrEureka (2024)','https://eureka-research.github.io/dr-eureka/'],
 S07:['RoboGen (2024)','https://robogen-ai.github.io/'],S08:['AutoRT (2024)','https://auto-rt.github.io/'],
 S09:['Anthropic, Claude Plays Robotics (9 Jul 2026)','https://www.anthropic.com/research/claude-plays-robotics'],
 S10:['Robocurve, GPT-6 Astra on robotic manipulation (4 Sep 2026)','https://openai.robocurve.org/gpt-6-astra/'],
 S11:['@cdngdev, X demo and method thread (8 Sep 2026)','https://x.com/cdngdev/status/2097339677128982873'],
 S12:['@Lingxiao234, X Real2Sim and failure thread (8 Sep 2026)','https://x.com/Lingxiao234/status/2096992059731443923'],
 S13:['Agentic Real2Sim, arXiv:2607.19190v3 (24 Jul 2026)','https://arxiv.org/html/2607.19190v3'],
 S14:['SceneMosaic, arXiv:2609.05594v1 (Sep 2026)','https://arxiv.org/html/2609.05594v1'],
 S15:['ENPIRE, arXiv:2606.19980v1 (Jun 2026)','https://arxiv.org/html/2606.19980v1'],
 S16:['CaP-X, arXiv:2603.22435v2 (Jul 2026)','https://arxiv.org/html/2603.22435v2'],
 S17:['ASPIRE, arXiv:2607.00272v1 (Jun 2026)','https://arxiv.org/html/2607.00272v1'],
 S18:['Playful Agentic Robot Learning, arXiv:2606.19419v1 (Jun 2026)','https://arxiv.org/html/2606.19419v1'],
 S19:['Google DeepMind, Gemini Robotics ER 2 / Robotics 2 (accessed 10 Sep 2026)','https://deepmind.google/models/gemini-robotics/embodied-reasoning/'],
 S20:['Physical Intelligence, π0.7 (16 Apr 2026)','https://www.pi.website/blog/pi07'],
 S23:['@k7agar, X wiping demo (6 Sep 2026)','https://x.com/k7agar/status/2096593654320341027'],
 S24:['@earthtojake, X hand design and limitation thread (10 Sep 2026)','https://x.com/earthtojake/status/2097789988670709821']
};
function shape(s,g,x,y,w,h,fill='none',line='none',lw=0,name){return s.shapes.add({geometry:g,name,position:{left:x,top:y,width:w,height:h},fill,line:{fill:line,width:lw}});}
function txt(s,str,x,y,w,h,size=23,color=C.ink,bold=false,opt={}){const t=shape(s,'textbox',x,y,w,h,'none','none',0,opt.name);t.text=str;t.text.style={typeface:opt.serif?SERIF:FONT,fontSize:size,color,bold,autoFit:'none',wrap:'square',alignment:opt.align??'left',verticalAlignment:opt.valign??'top',insets:{left:0,right:0,top:0,bottom:0}};if(opt.link)t.text.get(str).link={uri:opt.link,isExternal:true};return t;}
function line(s,x,y,w,color=C.line,width=1){return shape(s,'rect',x,y,w,width,color);}
const imageCache=new Map();
async function imageData(file){
 const full=file.startsWith('/')?file:path.join(BUILD,'assets',file);
 if(!imageCache.has(full))imageCache.set(full,(async()=>{const bytes=await sharp(full).png().toBuffer();const meta=await sharp(bytes).metadata();return {bytes,meta};})());
 return imageCache.get(full);
}
async function img(s,file,x,y,w,h,alt='',fit='contain') {
 const {bytes}=await imageData(file);
 return s.images.add({blob:new Uint8Array(bytes),contentType:'image/png',alt,fit,position:{left:x,top:y,width:w,height:h}});
}
async function logo(s,cover=false){await img(s,'logo_clear.png',1087,30,153,38,'CLEAR logo');if(cover)await img(s,'logo_sustech.png',44,32,247,46,'SUSTech logo');}
function footer(s,n,ids=[],extra=''){const cite=ids.map(id=>SOURCE[id]?.[0]??id).join('  ·  ');txt(s,extra?[cite,extra].filter(Boolean).join('  |  '):cite,64,679,1090,28,11,C.cite);txt(s,String(n),1192,667,46,26,16,C.cite,false,{align:'right'});}
async function slide(title,section,ids=[],extra=''){const s=deck.slides.add();s.background.fill='#ffffff';const n=deck.slides.items.length;await logo(s);if(section)txt(s,section,64,57,45,48,36,C.teal,true,{serif:true});txt(s,title,section?110:64,57,section?965:1011,48,36,C.ink,true,{serif:true,name:`Slide ${n} title`});line(s,64,111,1152,C.teal,3);footer(s,n,ids,extra);records.push({number:n,title,section,ids,notes:''});return s;}
function note(s,minutes,text,ids=[],extraUrls=[]){const refs=ids.map(id=>`${id}: ${SOURCE[id]?.[0]}\n${SOURCE[id]?.[1]}`).join('\n\n');const out=`TIME: ${minutes} minutes\n\n${text}\n\nSOURCES\n${refs}\n${extraUrls.join('\n')}`;s.speakerNotes.textFrame.setText(out);records[records.length-1].notes=out;records[records.length-1].minutes=minutes;}
function statement(s,str,y=594,color=C.dark){shape(s,'rect',64,y,1152,58,color===C.red?C.pale:C.light);txt(s,str,84,y+14,1112,36,23,color,true);}
function pairText(s,head,body,x,y,w=320){txt(s,head,x,y,w,36,25,C.dark,true);txt(s,body,x,y+42,w,100,21,C.gray);}
function box(s,title,sub,x,y,w=220,h=124,accent=false){const b=shape(s,'rect',x,y,w,h,accent?C.teal:'#f4f6f5',accent?C.teal:C.line,1);txt(s,title,x+14,y+(h>=110?16:10),w-28,h>=110?58:33,23,accent?'#ffffff':C.ink,true,{align:'center'});if(sub)txt(s,sub,x+10,y+(h>=110?80:48),w-20,h>=110?h-84:h-51,16,accent?'#e2f3ef':C.gray,false,{align:'center'});return b;}
function connect(s,a,b,opt={}){return s.shapes.connect(a,b,{kind:'straight',fromSide:opt.from??'right',toSide:opt.to??'left',line:{fill:opt.color??C.gray,width:2},tail:{type:'arrow',width:'sm',length:'sm'}});}
function flow(s,items,x=80,y=260,w=220,gap=58){const a=items.map((it,i)=>box(s,it[0],it[1],x+i*(w+gap),y,w,124,it[2]));for(let i=0;i<a.length-1;i++)connect(s,a[i],a[i+1]);return a;}
async function poster(s,stem,x,y,w,h,label,url,clip){
 const {meta}=await imageData(`${stem}.jpg`);const scale=Math.min(w/meta.width,h/meta.height);
 const iw=meta.width*scale,ih=meta.height*scale,ix=x+(w-iw)/2,iy=y+(h-ih)/2;
 await img(s,`${stem}.jpg`,ix,iy,iw,ih,`VIDEO:${stem}`);
 txt(s,(clip?'▷  ':'')+label,x,y+h+9,w,42,17,C.gray);
 if(clip){media.push({slide:deck.slides.items.length,alt:`VIDEO:${stem}`,file:path.join(BUILD,'clips',clip),sourceUrl:url,x:ix,y:iy,w:iw,h:ih});}
 else if(url)txt(s,'View original video',x,y+h+49,w,25,17,C.dark,true,{link:url});
}
function chart(s,x,y,w,h,categories,series,max=1,format='0%'){return s.charts.add('bar',{position:{left:x,top:y,width:w,height:h},categories,series,barOptions:{direction:'column',grouping:'clustered',gapWidth:110},hasLegend:true,legend:{position:'bottom',overlay:false,textStyle:{typeface:FONT,fontSize:18,fill:C.gray}},xAxis:{textStyle:{typeface:FONT,fontSize:19,fill:C.ink},majorGridlines:null,line:{fill:C.line,width:1}},yAxis:{min:0,max,majorUnit:max/4,numberFormatCode:format,textStyle:{typeface:FONT,fontSize:16,fill:C.gray},majorGridlines:{fill:'#e5e8e7',width:1}},dataLabels:{showValue:true,position:'outEnd',textStyle:{typeface:FONT,fontSize:19,bold:true,fill:C.ink}},chartFill:'#ffffff',chartLine:{fill:'none',width:0},plotAreaFill:'#ffffff',plotAreaLine:{fill:'none',width:0}});}
function table(s,values,x,y,w,h,widths,size=20){const t=s.tables.add({rows:values.length,columns:values[0].length,left:x,top:y,width:w,height:h,values,columnWidths:widths});t.borders.assign({style:'solid',fill:'#ffffff',width:2});for(let r=0;r<values.length;r++)for(let c=0;c<values[0].length;c++){const cell=t.getCell(r,c);cell.fill=r===0?C.light:r%2===0?'#f6f7f6':'#ffffff';cell.text.style={typeface:FONT,fontSize:size,color:r===0?C.dark:C.ink,bold:r===0,insets:{left:14,right:12,top:10,bottom:8}};}return t;}

// Focused revision: three case studies, with original media as the main narrative.
const R=(file)=>path.join(ROOT,'research/assets',file);
function speak(s,text,ids=[],urls=[]){note(s,timelog[records.length-1],text,ids,urls);}
function caption(s,str,x,y,w=1100){txt(s,str,x,y,w,44,17,C.gray);}
function barNote(s,str,y=598){statement(s,str,y);}
function arrowSegment(s,x1,y1,x2,y2,arrow=false,color=C.gray){
 const a=shape(s,'rect',x1,y1,1,1,'none'),b=shape(s,'rect',x2,y2,1,1,'none');
 return s.shapes.connect(a,b,{kind:'straight',line:{fill:color,width:2},...(arrow?{tail:{type:'arrow',width:'sm',length:'sm'}}:{})});
}
// 1
{
 const s=deck.slides.add();s.background.fill='#ffffff';await logo(s,true);
 records.push({number:1,title:'Agents for Robotics',section:'',ids:[],notes:''});
 txt(s,'Agents for Robotics',94,202,1100,94,60,C.ink,true,{serif:true});
 txt(s,'Reliable Action and Improvement',96,306,1090,68,39,C.teal,true,{serif:true});
 txt(s,'Three case studies and emerging applications',98,408,1070,40,23,C.gray);
 txt(s,'Technical talk\n10 September 2026',98,512,970,70,22,C.gray);
 footer(s,1,[],'Primary sources through 10 September 2026');
 speak(s,'This is a focused technical talk about general-purpose agents in robotics. We will study only three works in depth: Claude Plays Robotics, Agentic Real2Sim, and ENPIRE. They address three different questions: what a general model can execute, what kind of world it can construct, and how it can organize experiments that improve a robot. Original application videos will interrupt the technical sections. Treat those clips as examples of possibility, while the case studies tell us what has actually been measured. The talk follows a goal, a problem, a mechanism, evidence and limitations, rather than a catalog of papers. All source links and the detailed qualifications are in these notes.');
}
// 2
{
 const s=await slide('Demo: A Robot Paints with Feedback','',['S11'],'Original author demonstration');
 await poster(s,'painting',74,155,792,466,'SO-101 painting demonstration','https://x.com/cdngdev/status/2097339677128982873','painting.mp4');
 pairText(s,'What looks new?','A general agent plans and revises physical actions.',910,208,292);
 pairText(s,'What remains?','Anchors, calibration and human feedback.',910,397,292);
 speak(s,'Play the original painting clip, which lasts roughly a minute. The robot motion is compelling because the agent must connect a visual goal to a sequence of physical marks, inspect what happened, and revise the plan. Ask the audience what they think is being learned. The original author describes initial anchor points, calibration, roughly one minute of action planning, and human feedback across iterations and sometimes during execution. The agent changes instructions and calibration. This does not establish that the model weights update online. Nor can the pace of an edited social video tell us the true inference latency. The point of the clip is to expose the useful workflow: observe, propose, execute, inspect and revise. It also introduces the talk’s central question. Which parts of that workflow are reusable robot capability, and which parts still depend on the particular setup and human support? Keep the distinction open until the case studies. The clip is muted for a narrated presentation and has no additional speedup applied by this deck.',['S11']);
}
// 3
{
 const s=await slide('Our Ultimate Goal','',[],'Our synthesis');
 txt(s,'Finish the current job. Make the next job easier.',84,172,1100,55,32,C.ink,true);
 const a=box(s,'Human goal','task and constraints',92,303,256,118);
 const b=box(s,'Robot execution','actions with feedback',506,303,268,118,true);
 const c=box(s,'Reusable capability','program, skill or policy',932,303,256,118);
 connect(s,a,b);connect(s,b,c);
 arrowSegment(s,1060,424,1060,514);arrowSegment(s,1060,514,640,514);arrowSegment(s,640,514,640,427,true,C.teal);
 caption(s,'Capability retained for later tasks',723,528,460);
 speak(s,'Start from the desired capability. A person should be able to state an intent, and the robot should finish the job despite uncertainty in geometry, contact or task progress. The stronger goal is that useful experience persists so a later job requires less search and less human intervention. These two time scales are different. Within-task feedback may rescue the current attempt without changing what the system knows next time. Across-task improvement requires a concrete artifact that survives the session, such as a program, skill library or trained policy. The diagram is our synthesis, not a published architecture and not a claim that one surveyed system solves the full problem. The return arrow means that retained capability can support a future execution. It does not mean the general model necessarily updates its weights. Use this distinction throughout the talk: what changes during the run, what persists afterward, and what independent test would demonstrate that the change is useful? We will look at execution first, then world construction, then real experimental improvement.');
}
// 4
{
 const s=await slide('Three Questions, Three Case Studies','',[]);
 const rows=[['1','What can the model execute?','Claude Plays Robotics'],['2','What makes a world testable?','Agentic Real2Sim'],['3','Can real experiments improve a policy?','ENPIRE']];
 rows.forEach((r,i)=>{const y=186+i*149;txt(s,r[0],82,y,60,68,46,C.teal,true,{serif:true});txt(s,r[1],186,y,1010,43,30,C.ink,true);txt(s,r[2],186,y+53,1010,40,25,C.gray);});
 speak(s,'The three case studies are selected because each sharpens a different question. Claude Plays Robotics controls the interface and tests where a general model succeeds or fails. Agentic Real2Sim standardizes a complex conversion pipeline and evaluates all attempted episodes, including failures. ENPIRE puts real robot rollouts inside an improvement workflow. The demonstration interludes broaden the application picture without adding more full paper sections. These are not mandatory stages of one pipeline: ENPIRE can improve directly on hardware without first building a simulator. Do not compare their success percentages as a leaderboard. They measure different units: completing a control task, accepting a replay, and solving a task under a real experimental protocol.');
}
// 5
{
 const s=await slide('Claude Plays Robotics','1',['S09'],'Original report figure');
 await img(s,R('claude_interfaces.png'),74,157,1140,490,'Original Claude Plays Robotics interface-level results');
 speak(s,'This report is useful as a capability assessment rather than just another successful robot demonstration. Read the original figure by interface. The model may output actions directly, synthesize a controller in code, or reason above a more capable execution scaffold. Those settings assign different amounts of perception, geometry, stabilization and motor control to the language model. Scores across those columns cannot be treated as interchangeable task-success rates. First explain what each interface permits, then ask why performance differs. Code can contain a fast feedback controller even if the model that wrote it is slow. A VLA can execute a grounded skill while a supervisor decides when to change the instruction. These are meaningful ways to use general reasoning, but they do not show that the model itself has acquired every lower-level capability. The report uses multiple models, task families and protocols. The original chart preserves that context. Our focus is the experimental lesson: control the interface before attributing progress to model intelligence. No Claude service was invoked to produce this talk; the slide uses the publicly published report and figure.',['S09']);
}
// 6
{
 const s=await slide('Direct Control Meets Physical Constraints','1',['S09'],'Original report animations');
 await poster(s,'claude_humanoid',76,199,652,268,'Humanoid controller example','https://www.anthropic.com/research/claude-plays-robotics','claude_humanoid.mp4');
 await poster(s,'claude_manip',839,158,334,334,'Manipulation example','https://www.anthropic.com/research/claude-plays-robotics','claude_manip.mp4');
 txt(s,'Control frequency',84,537,442,38,26,C.dark,true);
 txt(s,'Precise grounding and contact',691,537,510,38,26,C.dark,true);
 barNote(s,'Direct manipulation: 0–5.5% full success in the report’s setting.');
 speak(s,'Play the two original animations and distinguish their roles. The humanoid animation compares a generated Python controller against zero commands. It illustrates the value of an executable controller, not high-frequency reasoning by the language model. The manipulation clip is a qualitative example and must not be read as the typical success rate. In the report’s direct manipulation setting, complete task success remains around zero to 5.5 percent. The report also separates successful intermediate subgoals from complete task success. Ask why touching or grasping an object might be easier than finishing the entire task. Precision, contact, coordinate grounding and timing all matter. For locomotion, some experiments pause simulation during model calls. The report discusses roughly 83 Hz control requirements and about 0.2 to 0.4 Hz model calls, which are different time scales. A result in paused simulation is not evidence of real-time physical control. A sensible response is to delegate fast control to a suitable controller or policy, and give the general model a slower, well-defined role. The next slide tests whether that supervisory role always helps.',['S09']);
}
// 7
{
 const s=await slide('A Supervisor Can Disrupt a Capable VLA','1',['S09'],'Original report figure');
 await img(s,R('claude_vla.png'),79,177,1120,374,'Original report VLA supervision results on familiar LIBERO-40 tasks');
 const a=box(s,'Agent','task-level decisions',163,559,237,78);const b=box(s,'VLA policy','motor execution',522,559,237,78,true);const c=box(s,'Robot','task outcome',881,559,237,78);connect(s,a,b);connect(s,b,c);
 speak(s,'This figure reports familiar LIBERO-40 tasks. Read it from the perspective of the base VLA. On tasks the VLA already knows, an added supervisor can introduce an unnecessary instruction change, an incorrect progress judgment, or an interruption to a policy that would otherwise succeed. Elsewhere in the same report, novel-task results show that a supervisor can help by decomposing the goal or choosing useful instructions. That separate result is not plotted here. The important result is that supervision is not uniformly beneficial. Separate rescue of failed cases from damage to already successful cases. The small diagram below is our simplified interface interpretation rather than a reproduction of the report’s exact implementation. It shows the model choosing at a slower task level while a policy handles execution. A good comparison holds the low-level policy fixed and measures task completion, intervention frequency, latency, and harmful interventions. The report’s LIBERO-40 setting has 40 tasks and five seeds, giving 200 trials, but it is not comparable to the small real-robot assessment in the next slide. Close the case study with a bounded conclusion: general reasoning can be useful when its interface and time scale match the job.',['S09']);
}
// 8
{
 const s=await slide('Demo: Placement and Fine Insertion','',['S10'],'Independent Robocurve assessment');
 txt(s,'Bowl placement',77,169,533,45,29,C.dark,true);txt(s,'Fine insertion',675,169,533,45,29,C.dark,true);
 await poster(s,'astra_bowl',76,229,537,279,'Astra: 19/20 trials','https://openai.robocurve.org/gpt-6-astra/','astra_bowl.mp4');
 await poster(s,'astra_insertion',675,229,537,279,'Astra: 2/20 trials','https://openai.robocurve.org/gpt-6-astra/','astra_insertion.mp4');
 barNote(s,'Three cameras, absolute end-effector poses, IK, and a 20-call budget.');
 speak(s,'Play the placement and insertion clips sequentially. Robocurve is an independent evaluator; its domain is not an official OpenAI robotics report. The evaluated system receives three camera views and proprioceptive state. It calls move_to with absolute end-effector poses, while inverse kinematics handles joints. Trials use a 20-model-call budget, medium reasoning, a 25 percent speed cap, and safety limits. The observed Astra completion count is 19 out of 20 for bowl placement and two out of 20 for insertion. The Fable 5.1 comparison is eight out of 20 for placement and two out of 20 for insertion. This small assessment suggests that coarse placement and fine contact remain quite different challenges. It does not isolate all causes of the gap. The comparison includes different placement rigs, non-interleaved runs, manual reset, and unblinded scoring. Do not merge these denominators with the previous LIBERO results. The insertion clip is a published failed run. Its value is to keep failure visible beside an impressive success. The apparent clip speed does not establish end-to-end model latency.',['S10']);
}
// 9
{
 const s=await slide('Demo: Wiping a Table','',['S23'],'Original X application demo');
 await poster(s,'wiping',99,144,580,476,'@k7agar, 6 September 2026','https://x.com/k7agar/status/2096593654320341027','wiping.mp4');
 txt(s,'A sustained physical task',743,236,437,88,32,C.ink,true);
 txt(s,'What controls contact?\nWhat happens after a mistake?',743,390,430,110,25,C.gray);
 speak(s,'This is an application interlude, not a fourth benchmark study. Play the original wiping demonstration. Compared with one discrete pick-and-place command, wiping highlights sustained interaction with a surface. Ask the audience which quantities would need to be controlled: tool pose, contact, coverage and progress. The post demonstrates a behavior, but the available public description does not establish a complete interface specification, force-control measurements, or repeated evaluation. We should not infer those details from the animation or from the author’s commentary about general intelligence. A visible chain of thought is also not a causal measurement of the controller. The useful question is whether a flexible agent can coordinate a practical task through the tools it has, and what experimental evidence would make that claim reliable. Keep the excitement of the demo, but do not attach an unsupported success rate or autonomy label.',['S23']);
}
// 10
{
 const s=await slide('Agentic Real2Sim: A Real Episode and Its Twin','2',['S13'],'Original project videos');
 await poster(s,'ar2s_real',76,211,538,315,'Recorded DROID episode','https://agentic-real2sim.github.io/','ar2s_real.mp4');
 await poster(s,'ar2s_sim',675,211,538,315,'Simulated replay','https://agentic-real2sim.github.io/','ar2s_sim.mp4');
 barNote(s,'Does matching this recording predict what happens under a new action?');
 speak(s,'Play the real and simulated episode as a pair. The project provides both videos for the same recorded episode. Their role here is illustrative; this presentation does not perform a synchronized numerical error analysis. The case study converts an interaction episode, not just a static mesh. It must recover actors, objects, camera geometry, poses, trajectories, and contact relationships sufficiently well to run a simulator. This is a significant engineering problem because the visual scene does not uniquely determine the physics. A wrong collision shape, friction coefficient, or camera pose can partly compensate for another error on one observed trajectory. Ask what happens if we move faster, contact the object elsewhere, or start from a new pose. That counterfactual question separates a replay from a predictive world. The paper’s main evaluation concerns replay acceptance. We will first understand how the agent organizes the conversion, then inspect the exact acceptance protocol, and finally use an author-disclosed social demo failure to make the boundary concrete.',['S13']);
}
// 11
{
 const s=await slide('Agentic Real2Sim: The Conversion Pipeline','2',['S13'],'Original architecture figure');
 await img(s,'ar2s_pipeline.png',72,137,1140,517,'Agentic Real2Sim original architecture: visual processing, physical priors, scene preparation, refinement');
 speak(s,'Follow the original architecture figure from the recorded input to a runnable scene. The visual stage extracts objects, segmentation, depth and poses. A physical-prior stage supplies structured hypotheses about object properties. Scene preparation assembles actors, geometry, cameras and trajectories. Simulator-in-the-loop refinement then runs the episode, compares the outcome and updates the construction. The agent is not producing every geometric estimate directly. SAM3, SAM3D, FoundationStereo, FoundationPose and deterministic optimization or search do specialized work. The key contribution is a constrained, inspectable workflow that coordinates those components. Identify which intermediate artifacts each stage passes to the next. Then consider how an early segmentation or pose error can propagate into a later physics mismatch. This is why replacing the language-model backend alone may not fix the entire pipeline. The figure establishes an architecture, not proof that every output has correct dynamics. A useful ablation would hold the episode and downstream tools fixed while changing one uncertain component. The paper provides an episode-level comparison; the following slide shows what that comparison actually counts.',['S13']);
}
// 12
{
 const s=await slide('Replay Acceptance on DROID-100','2',['S13'],'Original paper Figure 3');
 await img(s,R('agentic_replay_results.png'),79,177,1120,380,'Original DROID-100 outcomes and model-call cost; all failures and logarithmic axis retained');
 barNote(s,'Best backend: 48 accepted, 8 partial, 44 failed, out of all 100 episodes.');
 speak(s,'Read the entire left plot, including failures. The best reported backend, Gemma 4 31B, has 48 accepted replays, eight partial results and 44 failures out of all 100 attempted DROID episodes. Other backends have success counts between 37 and 45. Explain the acceptance rule before interpreting the bars. The pipeline filters candidates using grasp, video and motion statistics, retains at most five, and asks three VLM judges to score them. Each judge chooses its best candidate. A replay succeeds if any judge’s best score is at least eight out of ten. This is not majority voting, not agreement among all judges, and not an average score threshold. The criteria concern target identity, final location, action similarity and end-effector position. They do not directly measure identified physical parameters or predictions under new actions. The right plot has a logarithmic cost axis. Reported dollar costs count model calls only, not the whole perception pipeline, simulator compute or human preparation. The result is useful because it includes a full denominator and shows where conversion still fails. The next scientific step is held-out intervention or downstream policy utility, not simply a more attractive replay.',['S13']);
}
// 13
{
 const s=await slide('Demo: Real2Sim and a Disclosed Failure','',['S12'],'Original X thread, including its limitation');
 await poster(s,'astra_real2sim',74,170,542,404,'Astra-assisted Real2Sim workflow','https://x.com/Lingxiao234/status/2096992059731443923','astra_real2sim.mp4');
 await poster(s,'astra_microphone',674,170,542,404,'Microphone: kinematic replay','https://x.com/Lingxiao234/status/2096992132527702382','astra_microphone.mp4');
 caption(s,'The author reports failed dynamics in the microphone example.',80,633,1110);
 speak(s,'These videos are original author demonstrations, separate from the Agentic Real2Sim paper and its evaluation. The thread describes an agent coordinating multi-view RGB, known robot actions, camera calibration, asset creation, MuJoCo execution and Blender rendering. This is an interesting example of a general coding agent coordinating a long robotics toolchain. The microphone example is especially informative because the author explicitly discloses that the dynamics failed. The displayed result is a kinematic replay. A rigid proxy could not express the compliant snap-fit behavior required by the task. Do not present that clip as a successful recovery of physical dynamics. Instead, use it to explain a model-class limitation: more parameter search cannot necessarily repair a simulator representation that lacks the required contact behavior. This is a synthesis motivated by the disclosed failure, not a claim that all Real2Sim approaches fail. The supplied microphone excerpt is the 35-to-60-second portion of the original, with no additional speedup. A compelling rendering and a useful engineering workflow can coexist with an unresolved predictive model.',['S12']);
}
// 14
{
 const s=await slide('ENPIRE: Real Experiments Inside the Loop','3',['S15'],'Original project demonstration');
 await poster(s,'enpire_task',75,157,812,457,'Pin insertion on real hardware (excerpt)','https://research.nvidia.com/labs/gear/enpire/','enpire_task.mp4');
 pairText(s,'What changes?','The policy and the experiment strategy.',929,223,274);
 pairText(s,'What returns?','Real rollout evidence.',929,397,274);
 speak(s,'Play the 300-to-330-second excerpt of the original pin-insertion task video. This excerpt illustrates the hardware interaction and is not a complete rollout. ENPIRE stands for a workflow that includes the environment, policy improvement, rollout and experiment analysis. It is the work intended by the earlier reference to EMPIRE in this robotics-autoresearch context. The central shift is that a coding agent can propose a policy change, run a real robot experiment, inspect the resulting logs and observations, and choose a next change. The artifact may be a heuristic program, a policy or a training recipe. The general language model does not have to change its own weights. Nor should a successful video be confused with the full experimental result. We need to know who established safety, how the robot resets, how success is detected, what the agent may modify, and how retries count. The next three slides examine exactly those components. Compared with a one-off demonstration, the important opportunity is repeatability: a robot experiment that can run again and return a signal useful for the next decision. The environment infrastructure is therefore part of the method, not a footnote.',['S15']);
}
// 15
{
 const s=await slide('ENPIRE: Environment and Improvement','3',['S15'],'Original Figure 2, method panel');
 await img(s,'enpire_framework_method.png',74,171,1138,445,'ENPIRE original framework, including human-assisted environment construction');
 caption(s,'Environment construction precedes autonomous policy improvement.',79,633,1100);
 speak(s,'Walk through the method panel of the original framework. The crop removes the separate timeline and task-photo rows while retaining the human, environment, tools, and policy-improvement loop. First the agent constructs an environment with human feedback. This phase includes the control tools, hard safety constraints, automatic reset, and success verification. After those components are established, the environment API is fixed for the autonomous improvement phase. Policy improvement proposes and implements a change. Real rollout executes it. Experiment analysis uses observations, logs and outcomes to diagnose failures and decide the next change. ENPIRE supports different policy mechanisms, including heuristic code, behavior cloning, online or offline reinforcement learning, and VLA combinations. Do not collapse those choices into a single model that learns everything. The separation between environment and policy is important because it gives the improvement process a stable contract. If the agent could quietly change the success test whenever its policy failed, apparent progress would become hard to interpret. Ask the audience where their current manual robotics workflow spends the most effort: proposing changes, running trials, resetting hardware, or deciding what the failure means. ENPIRE’s contribution is an executable workflow around those activities. Its limits include the initial engineering, the quality of feedback and the scope of tasks tested.',['S15']);
}
// 16
{
 const s=await slide('ENPIRE: Reset and Verification','3',['S15'],'Original project videos');
 await poster(s,'enpire_reset',75,188,540,345,'Automatic pin-task reset','https://research.nvidia.com/labs/gear/enpire/','enpire_reset.mp4');
 await poster(s,'enpire_verify',675,188,540,345,'Zip-tie verification signal','https://research.nvidia.com/labs/gear/enpire/','enpire_verify.mp4');
 barNote(s,'A repeatable experiment needs a reliable starting state and a trustworthy test.');
 speak(s,'Play the reset example and then the verification clip. These are two different tasks, selected to expose the experimental infrastructure rather than to imply a synchronized pipeline. The pin reset makes another trial possible without a person manually restoring every object. The zip-tie verifier uses image cropping and segmentation to determine whether the strap passes through the head. The paper considers two camera views to reduce false positives. Other task verifiers can combine vision with proprioception or torque. This is part of the real scientific bottleneck: the agent only improves against the feedback it receives. A false positive rewards the wrong behavior; an unreliable reset changes the experimental distribution. Some reset procedures start at the hardest task phase rather than at an arbitrary full-task initial state, and the setup phase uses human assistance. Those choices are legitimate when explicitly reported. They change what success means and where the method can be transferred. Ask what independent audit would catch a verifier exploiting a visual shortcut. Keep hard safety constraints, reset correctness, and evaluation correctness conceptually separate. Passing one does not prove the other two.',['S15']);
}
// 17
{
 const s=await slide('ENPIRE: Improvement on Pin Insertion','3',['S15'],'Original Figure 3, pin panel; axes and legend retained');
 await img(s,'enpire_pin_results.png',74,174,1138,405,'Original ENPIRE pin-insertion learning and scaling curves, cropped with full axes and legend');
 barNote(s,'High final success includes up to eight conditional retries within a rollout.');
 speak(s,'This is the pin-insertion panel of the original Figure 3. The crop removes the Push-T row but keeps the pin axes, legends and example photograph. The left curves compare coding-agent backends as research time increases. The middle curves compare team size, showing how multiple workers can reach a useful result sooner. Read research time as wall-clock experimental development time, not policy inference latency. The task protocol matters just as much as the curve. ENPIRE allows up to eight conditional retries in a rollout. A later attempt can use information from an earlier failure. Therefore a final success figure near 99 percent is not one-shot insertion precision and is not an independent best-of-eight experiment. We cannot invert it using an independent Bernoulli formula to infer a per-attempt success probability. Recovery is a real capability and deserves credit, but it must remain visible. Some resets also begin at a hard subphase. The correct claim is that the workflow improves policies under the stated environment, reset and retry protocol. It does not establish unrestricted autonomy from arbitrary initial conditions. The next slide separates faster discovery from resource efficiency.',['S15']);
}
// 18
{
 const s=await slide('More Robots Shorten Time, but Raise Cost','3',['S15'],'Original paper resource-utilization figure');
 await img(s,'enpire_utilization.png',73,199,1140,355,'Original ENPIRE resource utilization, token use and time-to-success plots');
 barNote(s,'Time to result, token use, and robot utilization measure different things.');
 speak(s,'The original figure separates three outcomes of scaling from one to four to eight agents or robot workers. More resources can reduce wall-clock time to a successful result. At the same time, token consumption increases, GPU utilization can rise, and per-robot utilization can fall. The middle panel contrasts observed mean token utilization with a simple linear projection; keep that distinction visible. The right panel puts token cost and time on separate axes. Do not call the system more efficient merely because the line for time falls. Depending on the deployment objective, lower time-to-result may be worth substantially higher total compute, but it remains a tradeoff. This closes the ENPIRE case study: the workflow is a concrete advance in organizing real experiments, yet reliable resets, trustworthy feedback, human preparation and total cost remain central. A stronger future result would show that the retained policy transfers and lowers the cost of solving new tasks, under an independent evaluator. Process activity or a busy robot fleet alone is not evidence of better capability.',['S15']);
}
// 19
{
 const s=await slide('Demo: Designing a Tendon-Driven Hand','',['S24'],'Original X design demonstration');
 await poster(s,'hand',88,152,827,485,'Astra-assisted CAD and visualization','https://x.com/earthtojake/status/2097789988670709821','hand.mp4');
 txt(s,'Design artifact',950,247,263,75,29,C.dark,true);
 txt(s,'Not a validated\nphysical hand',950,367,263,95,25,C.gray);
 speak(s,'This is a different kind of robotics application: design and visualization rather than robot execution. Play the author’s CAD animation. The thread reports roughly 48 hours of work, build123d-generated STEP geometry, JavaScript animation and GLB visualization. The visual complexity is impressive, but the author explicitly states that the current design cannot directly work in reality. It has not established a manufactured hand, validated tendon dynamics or reliable mechanical operation. We should therefore describe the output as a design artifact that a general agent helped create. Ask what the next engineering test should be: tendon routing clearance, friction, actuator sizing, tolerances, or a physical prototype. The point is that agents now contribute to more of the robotics workflow than high-level task planning. The evidence standard depends on the artifact: a geometric rendering is useful, but it supports a different claim from a working mechanism on a bench. Keep the demonstration and the author’s limitation together.',['S24'],['https://x.com/earthtojake/status/2097789991426335015','https://x.com/earthtojake/status/2097801101890207893']);
}
// 20
{
 const s=await slide('Demo: Inspecting and Repairing an Execution','',['S17'],'Original ASPIRE project demonstration');
 await poster(s,'aspire_trace',74,151,1138,458,'Multimodal execution trace and program debugging','https://research.nvidia.com/labs/gear/aspire/','aspire_trace.mp4');
 speak(s,'This brief project demonstration broadens the picture of what an agent can retain. ASPIRE records multimodal execution traces, localizes failures, repairs code, and accumulates reusable skills. Play the trace inspection excerpt and point out the connection between a visual observation and the program being repaired. We do not add another full paper analysis or another headline success percentage here. The conceptual distinction is the update target. A repaired skill library is external memory and executable code, not necessarily a change to the foundation model’s weights. A meaningful claim of accumulation would require showing that retained skills help later tasks and survive beyond the debugging session. The original paper evaluates particular task and transfer splits, so this clip alone cannot establish open-world continual learning. Use it as the bridge into the synthesis: across action, world construction and experimental improvement, what exactly is the agent allowed to change, what evidence comes back, and what useful artifact remains?',['S17']);
}
// 21
{
 const s=await slide('Our Synthesis: What the Agent Can Change','',[],'Conceptual comparison, not a unified published architecture');
 const rows=[
  {label:'Execution',y:188,nodes:[['Goal',''],['Agent','decision'],['Controller','action'],['Robot','observation']]},
  {label:'World building',y:352,nodes:[['Recording',''],['Agent + tools','model parameters'],['Simulator','replay'],['Comparison','mismatch']]},
  {label:'Improvement',y:516,nodes:[['Task + API',''],['Agent','policy changes'],['Real rollout','experiment'],['Verifier','outcome']]}
 ];
 for(const row of rows){
  txt(s,row.label,76,row.y-43,1130,34,24,C.dark,true);
  const ns=row.nodes.map((it,j)=>box(s,it[0],it[1],80+j*290,row.y,250,83,j===1));
  for(let i=0;i<3;i++)connect(s,ns[i],ns[i+1]);
  arrowSegment(s,1075,row.y+86,1075,row.y+118,false,C.teal);
  arrowSegment(s,1075,row.y+118,495,row.y+118,false,C.teal);
  arrowSegment(s,495,row.y+118,495,row.y+88,true,C.teal);
 }
 speak(s,'This diagram is our synthesis and deliberately simplifies each route. Read each row separately. For execution, the agent changes a decision that a controller can execute, and robot observations inform the next decision. For world building, the agent and its tools change a scene or model, run a simulator, and use mismatch as feedback. For improvement, the agent changes a policy or training procedure, runs a real experiment, and uses a verifier’s outcome to choose a next change. The return arrows represent the corresponding feedback loops. They do not imply that all three systems share one implementation, use the same objective, or update the language model’s weights. The leftmost inputs remain distinct. ENPIRE does not require a reconstructed world before it can operate. Across all three rows, an impressive outcome becomes scientifically useful only when we can name the editable object, the feedback signal, the retained artifact, and the evaluation distribution. The next experiment should test whether the output works beyond the condition used to construct it: a new contact state, a held-out action, or a new task.');
}
// 22
{
 const s=await slide('Conclusion','',[]);
 const rows=[['Useful reasoning needs an executable interface.','Precision and timing still belong in the system design.'],['A replay needs a separate predictive test.','New actions reveal errors that one recording can hide.'],['Improvement needs an artifact and a credible test.','Retained skill matters only when the next task benefits.']];
 rows.forEach((r,i)=>{const y=198+i*137;txt(s,String(i+1),79,y,64,58,42,C.teal,true,{serif:true});txt(s,r[0],172,y,1038,44,29,C.ink,true);txt(s,r[1],172,y+53,1038,42,24,C.gray);});
 speak(s,'Close by returning to the opening painting demo. General agents can already coordinate useful pieces of robotics: choosing actions, building simulator scenes, designing mechanisms, inspecting traces and running real experiments. The three case studies make the boundaries clearer. Claude Plays Robotics shows that the interface and control time scale determine what the model must solve. Agentic Real2Sim shows a standardized conversion pipeline with a complete replay denominator, while leaving counterfactual prediction to separate tests. ENPIRE shows that real hardware can sit inside an iterative improvement workflow, provided reset, safety and verification are in place. The social demonstrations broaden the application space but do not replace those tests. The practical question to take away is simple: what capability remains after this run, and how would we know it makes the next task easier? Invite discussion on one concrete proposed test, rather than on whether an exciting video should be labeled general intelligence.');
}
if(records.length!==22)throw new Error(`Expected 22 slides, got ${records.length}`);
const total=records.reduce((s,r)=>s+r.minutes,0);if(total!==60)throw new Error(`Timing total ${total}, expected 60`);
await fs.writeFile(path.join(BUILD,'slide_records_focus.json'),JSON.stringify(records,null,2));
await fs.writeFile(path.join(BUILD,'video_placements_focus.json'),JSON.stringify(media,null,2));
await fs.mkdir(path.join(BUILD,'focus_rendered'),{recursive:true});
console.log(`Exporting ${records.length} slides, ${media.length} videos...`);
await (await PresentationFile.exportPptx(deck)).save(path.join(BUILD,'focus_draft.pptx'));
for(let i=0;i<deck.slides.items.length;i++){
 const s=deck.slides.items[i];const n=String(i+1).padStart(2,'0');
 const png=await deck.export({slide:s,format:'png',scale:1.25});
 await fs.writeFile(path.join(BUILD,'focus_rendered',n+'.png'),new Uint8Array(await png.arrayBuffer()));
 await fs.writeFile(path.join(BUILD,'focus_rendered',n+'.layout.json'),await (await s.export({format:'layout'})).text());
 console.log(`Rendered ${i+1}/${records.length}`);
}
console.log('FOCUSED_DRAFT_COMPLETE');
