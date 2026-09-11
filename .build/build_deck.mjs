import fs from 'node:fs/promises';
import path from 'node:path';
import { Presentation, PresentationFile } from '@oai/artifact-tool';
import sharp from 'sharp';
const ROOT='/home/limx/Desktop/agent_for_robotics';
const BUILD=path.join(ROOT,'.build');
const C={teal:'#2ba39b',dark:'#1d7d76',ink:'#1a1a1a',gray:'#646464',light:'#eaf5f3',line:'#c6d9d6',red:'#aa514a',pale:'#f7eeec',cite:'#96958e'};
const FONT='Arial',SERIF='Georgia';
const deck=Presentation.create({slideSize:{width:1280,height:720}});
const media=[], records=[];
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
 S23:['@k7agar, X wiping demo (6 Sep 2026)','https://x.com/k7agar/status/2096593654320341027']
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
function box(s,title,sub,x,y,w=220,h=124,accent=false){const b=shape(s,'rect',x,y,w,h,accent?C.teal:'#f4f6f5',accent?C.teal:C.line,1);txt(s,title,x+14,y+16,w-28,58,23,accent?'#ffffff':C.ink,true,{align:'center'});if(sub)txt(s,sub,x+10,y+80,w-20,h-84,16,accent?'#e2f3ef':C.gray,false,{align:'center'});return b;}
function connect(s,a,b,opt={}){return s.shapes.connect(a,b,{kind:'straight',fromSide:opt.from??'right',toSide:opt.to??'left',line:{fill:opt.color??C.gray,width:2},tail:{type:'arrow',width:'sm',length:'sm'}});}
function flow(s,items,x=80,y=260,w=220,gap=58){const a=items.map((it,i)=>box(s,it[0],it[1],x+i*(w+gap),y,w,124,it[2]));for(let i=0;i<a.length-1;i++)connect(s,a[i],a[i+1]);return a;}
async function poster(s,stem,x,y,w,h,label,url,clip){
 const {meta}=await imageData(`${stem}.jpg`);const scale=Math.min(w/meta.width,h/meta.height);
 const iw=meta.width*scale,ih=meta.height*scale,ix=x+(w-iw)/2,iy=y+(h-ih)/2;
 await img(s,`${stem}.jpg`,ix,iy,iw,ih,`VIDEO:${stem}`);
 txt(s,(clip?'▶  ':'')+label,x,y+h+9,w,42,17,C.gray);
 if(clip){media.push({slide:deck.slides.items.length,alt:`VIDEO:${stem}`,file:path.join(BUILD,'clips',clip),sourceUrl:url,x:ix,y:iy,w:iw,h:ih});}
 else if(url)txt(s,'View original video',x,y+h+49,w,25,17,C.dark,true,{link:url});
}
function chart(s,x,y,w,h,categories,series,max=1,format='0%'){return s.charts.add('bar',{position:{left:x,top:y,width:w,height:h},categories,series,barOptions:{direction:'column',grouping:'clustered',gapWidth:110},hasLegend:true,legend:{position:'bottom',overlay:false,textStyle:{typeface:FONT,fontSize:18,fill:C.gray}},xAxis:{textStyle:{typeface:FONT,fontSize:19,fill:C.ink},majorGridlines:null,line:{fill:C.line,width:1}},yAxis:{min:0,max,majorUnit:max/4,numberFormatCode:format,textStyle:{typeface:FONT,fontSize:16,fill:C.gray},majorGridlines:{fill:'#e5e8e7',width:1}},dataLabels:{showValue:true,position:'outEnd',textStyle:{typeface:FONT,fontSize:19,bold:true,fill:C.ink}},chartFill:'#ffffff',chartLine:{fill:'none',width:0},plotAreaFill:'#ffffff',plotAreaLine:{fill:'none',width:0}});}
function table(s,values,x,y,w,h,widths,size=20){const t=s.tables.add({rows:values.length,columns:values[0].length,left:x,top:y,width:w,height:h,values,columnWidths:widths});t.borders.assign({style:'solid',fill:'#ffffff',width:2});for(let r=0;r<values.length;r++)for(let c=0;c<values[0].length;c++){const cell=t.getCell(r,c);cell.fill=r===0?C.light:r%2===0?'#f6f7f6':'#ffffff';cell.text.style={typeface:FONT,fontSize:size,color:r===0?C.dark:C.ink,bold:r===0,insets:{left:14,right:12,top:10,bottom:8}};}return t;}

// 1. The supplied reference is an HTML deck. Rebuild its visual structure natively.
{
 const s=deck.slides.add();s.background.fill='#ffffff';await logo(s,true);records.push({number:1,title:'Agents for Robotics',section:'',ids:[],notes:''});
 txt(s,'Agents for Robotics',64,216,1120,85,60,C.ink,true,{serif:true});
 txt(s,'Reliable Action and Cumulative Improvement',64,306,1120,67,38,C.teal,true,{serif:true});
 txt(s,'Foundations, technical reports and emerging systems',66,414,1080,38,23,C.gray);
 txt(s,'Technical survey\n10 September 2026',66,505,750,72,21,C.gray);
 footer(s,1,[],'Research cutoff: 10 September 2026. Primary-source survey.');
 note(s,0.5,'This talk asks how general-purpose agents acquire reliable robot capabilities. We will examine both robot execution and the engineering process behind it. Recent demonstrations motivate the question, but the organizing structure is the gap between a plausible plan, a successful physical action, and a reusable capability. The evidence includes foundational papers, industrial reports, independent evaluations and original author demonstrations. These source types carry different evidential weight.');
}
{
 const s=await slide('Outline','',[],'Background → problems → methods → conclusion');
 const rows=[['1','Background','The goal and the current workflow'],['2','Problems','Action, world and improvement gaps'],['3','Methods','Executable interfaces, testable worlds, cumulative learning'],['4','Conclusion','What is established and what remains open']];
 rows.forEach((r,i)=>{const y=206+i*90;txt(s,r[0],80,y,52,44,30,C.teal,true,{serif:true});txt(s,r[1],142,y,240,44,29,C.ink,true);txt(s,r[2],400,y+5,800,40,23,C.gray);});
 note(s,0.5,'The structure follows a problem-driven technical talk. First, define the desired capability and the current execution and development workflow. Next derive three distinct gaps. Each method section then gives a big picture, the key mechanism, quantitative or qualitative evidence, and the limitations of that evidence. The three routes can be combined, but they are not mandatory sequential stages. ENPIRE, for example, can improve policies directly on hardware without first constructing a digital twin.');
}
// Background: the desired capability and the work already done by the stack.
{
 const s=await slide('Our Ultimate Goal','1',[], 'Conceptual target, not an achieved system');
 txt(s,'A human gives a goal. The robot finishes the job.',104,177,1080,52,32,C.ink,true);
 flow(s,[['Human intent','open-ended goals'],['Reliable action','changing physical conditions',true],['Reusable capability','better on the next task']],170,300,270,64);
 txt(s,'Within a task',435,442,310,32,21,C.dark,true,{align:'center'});
 txt(s,'Across tasks',770,442,320,32,21,C.dark,true,{align:'center'});
 statement(s,'Success now — and useful experience that survives the current conversation.');
 note(s,1.5,'Start with the desired capability rather than the latest model name. A person should be able to state an intent, while the robot grounds that intent in the current scene, acts safely, detects when its plan is wrong, and still completes the task. A stronger requirement is that useful experience survives the current interaction. These are two distinct time horizons: adaptation within a task, and capability improvement across tasks. Neither is established by a single impressive video. The rest of the talk asks which parts of this target current systems actually address. This is our analytical target, not a claim attributed to any one paper.');
}
{
 const s=await slide('Execution and Development Are Different Loops','1',['S08','S15']);
 txt(s,'RUN THE ROBOT',74,168,380,33,22,C.dark,true);
 flow(s,[['Observe','images + state'],['Act','policy + controller',true],['Check','task outcome']],74,225,208,50);
 txt(s,'IMPROVE THE ROBOT',74,395,390,33,22,C.dark,true);
 txt(s,'Interfaces  ·  data  ·  rewards  ·  training  ·  validation',74,449,765,74,27,C.ink);
 await img(s,'autort.png',866,184,350,329,'AutoRT: foundation models organize real-world robot data collection');
 statement(s,'A strong policy does not remove the engineering work around it.');
 note(s,1.5,'Separate the execution loop from the development loop. A deployed policy already handles a substantial part of perception-to-action mapping. Robotics engineers still configure coordinate systems, sensing, reset procedures, datasets, reward definitions, training schedules and success tests. AutoRT is an early example of foundation models organizing the real data-collection workflow rather than replacing every controller. ENPIRE later makes real experiments part of an improvement workflow. This framing avoids blaming every engineering limitation on VLAs. Ask the audience where most of their own time is spent: running a trained policy, or making the surrounding experiment reliable? The image is the original AutoRT system illustration; the execution chain is a synthesis, not its exact architecture.',['S08','S15']);
}
{
 const s=await slide('General Agents Now Enter Both Loops','1',['S10','S13','S15']);
 txt(s,'Act',74,172,344,41,30,C.dark,true);txt(s,'Build a world',469,172,344,41,30,C.dark,true);txt(s,'Inspect an experiment',864,172,344,41,30,C.dark,true);
 await poster(s,'astra_bowl',74,232,344,218,'Astra: placement','https://openai.robocurve.org/gpt-6-astra/','astra_bowl.mp4');
 await poster(s,'ar2s_teaser',469,232,344,218,'Agentic Real2Sim: conversion','https://agentic-real2sim.github.io/','ar2s_teaser.mp4');
 await poster(s,'enpire_verify',864,232,344,218,'ENPIRE: verification','https://research.nvidia.com/labs/gear/enpire/','enpire_verify.mp4');
 statement(s,'These clips motivate three questions. They are not a shared benchmark.');
 note(s,2,'Play the three clips sequentially, not simultaneously. First, Astra chooses placement actions through a robot interface; the author video compares model runs and is edited, so its apparent speed is not model response latency. Second, Agentic Real2Sim converts a recorded interaction into a simulator episode; matching a recording is not yet evidence for new actions. Third, the ENPIRE clip exposes a visual verification signal for zip-tie insertion. A check that reliably identifies task completion is part of the experimental infrastructure. Do not present these examples as three stages every robot must pass through. They establish three opportunities: action decisions, world construction, and experimental improvement. The next section derives what is still missing in each.',['S10','S13','S15']);
}
// Problems: derive the need for each method route before presenting results.
{
 const s=await slide('The First Step: Connect a Model to the Robot','2',['S01','S02','S03']);
 flow(s,[['Task + observation','language and perception'],['General model','reasoning + program synthesis',true],['Executable interface','skills, code or poses'],['Robot','physical action']],69,258,225,52);
 pairText(s,'SayCan','Choose a feasible skill',88,437,310);
 pairText(s,'Inner Monologue','Replan using feedback',485,437,310);
 pairText(s,'Code as Policies','Compose executable programs',874,437,310);
 statement(s,'Reasoning becomes useful only through a capability the robot can execute.');
 note(s,1.5,'The natural first step is to connect a general model to existing robot capabilities. SayCan combines linguistic usefulness with an affordance estimate so the planner selects skills the robot can execute. Inner Monologue returns environmental feedback to the planner instead of committing to one open-loop plan. Code as Policies expresses behavior as programs that compose perception and control APIs, enabling loops, geometry calculations and reuse. These foundational works already contain much of the conceptual structure behind current agent demos. Their limitation is not that language is useless, but that the interface determines what the language model can actually do. We will now examine the execution, world-model and improvement gaps left after making this connection.',['S01','S02','S03']);
}
{
 const s=await slide('Problem 1: A Plausible Plan Can Still Fail','2',['S09','S10']);
 txt(s,'“Insert the piece into the slot.”',84,183,1100,53,35,C.dark,true,{serif:true});
 await img(s,path.join(BUILD,'previews/astra_insertion_1.jpg'),78,268,727,257,'Original failed Astra insertion: three camera views');
 pairText(s,'Grounding','Which position and orientation?',854,249,350);
 pairText(s,'Contact','What happens after touching?',854,365,350);
 pairText(s,'Timing','How fast must feedback arrive?',854,479,350);
 statement(s,'The missing step is physical execution, not another sentence in the plan.');
 note(s,2,'Use the failed insertion frame as a concrete example. The semantic instruction is easy to understand; the robot still needs the correct position, orientation, approach direction, contact behavior and recovery strategy. A model may recognize what should happen without estimating these quantities accurately enough. It can also be too slow to correct a transient contact error. Claude Plays Robotics separates interfaces and exposes these differences; Robocurve records a real fine-insertion task where completion remains rare. This frame comes from an explicitly failed run in the published trial table, not from a success video relabeled as a failure. Do not generalize its appearance into a force-control diagnosis: the available evidence supports a fine-manipulation difficulty, not a measured decomposition of all causes.',['S09','S10']);
}
{
 const s=await slide('Problem 2: A Recording Is Not a Predictive World','2',['S12','S13']);
 await img(s,path.join(BUILD,'previews/ar2s_real_0.jpg'),75,204,531,299,'Real DROID episode input');
 await img(s,path.join(BUILD,'previews/ar2s_sim_2.jpg'),675,204,531,299,'Simulator replay of the same DROID episode');
 txt(s,'Observed interaction',75,521,531,37,25,C.ink,true);txt(s,'Fitted replay',675,521,531,37,25,C.ink,true);
 statement(s,'Would the world still behave correctly under a different action?');
 note(s,2,'The paired images are an original real episode and the published simulated version. They are illustrative frames, not a synchronized error measurement. A visually plausible reconstruction may have incorrect collision geometry, friction, stiffness or camera pose. Several wrong parameters can compensate for one another on the single recorded trajectory. The scientific question is whether the reconstruction predicts a different action, speed, contact point or initial condition. That requires held-out interventions, not merely a good replay. The Astra microphone example later makes this distinction explicit: the author reports failed dynamics and shows a kinematic replay instead. Scene construction, system identification and downstream policy usefulness should therefore be evaluated separately.',['S12','S13']);
}
{
 const s=await slide('Problem 3: Feedback Is Not Yet a Reusable Skill','2',['S15','S17','S18']);
 const a=flow(s,[['Attempt','execute a program'],['Feedback','success or failure',true],['Repair','change the current plan']],175,227,265,64);
 txt(s,'What remains after the session ends?',116,423,1050,51,34,C.ink,true,{align:'center'});
 txt(s,'A program?    A skill library?    Better world parameters?    New weights?',92,501,1110,41,25,C.dark,false,{align:'center'});
 statement(s,'Persistent capability requires an update target and a trustworthy test.');
 note(s,2,'A model can read a failure message, change its next command and succeed later in the same conversation. That is valuable but not necessarily lasting learning. If the context is discarded, the next task may start from the same capability level. To obtain accumulation, the system must specify what changes and persists: a reusable program, a retrieval library, environment parameters, a task policy or the general model weights. It also needs repeatable experiments and an evaluation that does not merely reward overfitting to the current setup. ENPIRE, ASPIRE and RATs make different choices about this update target. Their shared theme is not an unspecified arrow labeled self-improvement, but a concrete artifact produced by a feedback loop.',['S15','S17','S18']);
}
{
 const s=await slide('Three Places to Design the System','2',['S03','S13','S15','S17']);
 const rows=[['A','EXECUTION INTERFACE','Turn decisions into safe, observable action'],['B','TESTABLE WORLD','Turn observations into an executable hypothesis'],['C','IMPROVEMENT PROCESS','Turn experiments into persistent capability']];
 rows.forEach((r,i)=>{let y=184+130*i;txt(s,r[0],80,y,73,58,43,C.teal,true,{serif:true});txt(s,r[1],185,y+3,960,36,26,C.ink,true);txt(s,r[2],185,y+50,990,40,26,C.gray);});
 statement(s,'Task-time feedback and development-time feedback solve different problems.');
 note(s,1.5,'These are design locations, not mutually exclusive model categories. Route A concerns the contract between reasoning and physical execution. Route B concerns an executable model of a scene or interaction, and the evidence needed to trust it. Route C concerns experiment selection, iteration, verification and persistence. One system may occupy multiple locations, but these routes do not require a fixed order. In particular, direct real-world policy improvement can proceed without first building a simulator. Maintaining these distinctions also clarifies evaluation: task completion, replay acceptance and improvement rate are not interchangeable metrics. The next slide places the selected works under the question each one helps answer.',['S03','S13','S15','S17']);
}
{
 const s=await slide('Methods Organized by the Missing Capability','2',['S09','S10','S13','S15','S16','S17']);
 table(s,[['Question','Method route','Main cases'],['Can it act reliably?','A  Executable interfaces','Claude · Astra · CaP-X'],['Can it test new actions?','B  World construction','Astra Real2Sim · Agentic Real2Sim'],['Can it become better?','C  Cumulative improvement','ENPIRE · ASPIRE · CaP-RL']],74,211,1132,312,[322,344,466],24);
 txt(s,'Each route:  Big picture  →  Mechanism  →  Evidence  →  Limits',85,560,1100,41,27,C.dark,true,{align:'center'});
 note(s,1,'Explain why each selected work is present. Claude provides interface-controlled evaluation; Astra provides recent concrete hardware examples; CaP-X exposes the computation hidden inside robot APIs. Agentic Real2Sim turns an engineering demo into an episode-conversion workflow with reported acceptance results. ENPIRE is the main example of real experimental improvement, while ASPIRE and CaP-RL distinguish external skill accumulation from weight updates. Supporting foundations and industrial reports are introduced only where they explain a mechanism or boundary. We will not rank all these systems using their headline percentages because their tasks, budgets and success definitions differ.',['S09','S10','S13','S15','S16','S17']);
}
// Route A: interfaces, measured behavior and execution limits.
{
 const s=await slide('A · Big Picture: Reasoning Meets Fast Control','3',['S03','S09','S10']);
 const nodes=flow(s,[['Observation','images + robot state'],['Agent','program / pose / subtask',true],['Execution tools','grounding + IK + limits'],['Robot controller','fast physical feedback']],69,260,225,52);
 txt(s,'Slower deliberation',390,187,380,39,27,C.dark,true,{align:'center'});
 txt(s,'Faster control',889,187,315,39,27,C.dark,true,{align:'center'});
 line(s,124,436,1023,C.teal,3);txt(s,'Observe the outcome and revise',382,451,557,39,26,C.dark,true,{align:'center'});
 statement(s,'“Direct control” still has an interface and a control stack.');
 note(s,1.5,'Walk through the contract rather than attributing everything to the language model. The agent receives images and robot state and proposes a program, subtask or pose. Tools may perform target detection, coordinate conversion, inverse kinematics, trajectory generation and safety checks. A faster controller executes the resulting command. Feedback returns at the level the interface exposes. These clocks can differ by orders of magnitude: a model call is not a servo cycle. The horizontal feedback line summarizes outcome feedback; it is not intended as a claim that every listed system uses identical timing. This distinction matters when evaluating statements such as no policy training or direct manipulation. They can be true while substantial pretrained perception and classical control remain essential.',['S03','S09','S10']);
}
{
 const s=await slide('A · How Much Robotics Is Hidden in One API?','3',['S03','S04','S16']);
 await img(s,path.join(ROOT,'research/assets/capx_interface.png'),77,172,698,364,'CaP-X original comparison of high-level and low-level manipulation APIs');
 pairText(s,'Program structure','Loops, functions and geometry',822,189,374);
 pairText(s,'Spatial grounding','Coordinates and constraints',822,315,374);
 pairText(s,'Primitive abstraction','What does grasp() already solve?',822,441,374);
 statement(s,'Evaluate the model together with the perception and action interface.');
 note(s,2,'Read the original CaP-X figure from high-level to low-level API. A short grasp call can hide object localization, coordinate transforms, motion planning and gripper control. Asking a model to implement the lower-level equivalent is a substantially different problem, even if the natural-language task is unchanged. Code as Policies supplies the program-composition idea. VoxPoser supplies a complementary example where language produces spatial value maps and a planner executes the constraints. CaP-X explicitly analyzes primitive abstraction, iteration and perceptual grounding. The takeaway is a controlled-comparison principle: hold the API fixed when comparing model ability, and hold the model fixed when comparing interfaces. This figure demonstrates interface content; it is not itself a quantitative performance plot.',['S03','S04','S16']);
}
{
 const s=await slide('A · Claude: Capability Depends on the Interface','3',['S09']);
 await img(s,path.join(ROOT,'research/assets/claude_interfaces.png'),73,169,866,387,'Claude Plays Robotics original results grouped by interface');
 txt(s,'0–5.5%',976,224,227,73,54,C.red,true,{serif:true});
 txt(s,'complete success\nin direct manipulation',976,312,225,109,23,C.ink);
 txt(s,'Paused simulation\n≠ real-time control',976,461,225,84,23,C.red,true);
 statement(s,'Task decomposition and execution support can change the apparent model ceiling.');
 note(s,2.5,'The main figure preserves the report’s interface grouping and score definition. Do not compare its aggregate score with a real-world task percentage elsewhere in this talk. In the direct-manipulation experiments, complete task success is approximately zero to 5.5 percent. A VLA scaffold changes the task the model must solve and often improves performance. The report also pauses simulation during some low-level locomotion model calls. It discusses roughly 83 Hz control needs versus approximately 0.2–0.4 Hz model calls; success in that paused setting does not establish real-time feedback control. The manipulation evaluation includes LIBERO-40 with 40 tasks and five seeds, a different denominator from the two-task Robocurve hardware evaluation. These protocol details are central to interpreting the result, not footnote trivia.',['S09']);
}
{
 const s=await slide('A · Astra on Hardware: The Actual Action Contract','3',['S10']);
 await img(s,path.join(BUILD,'previews/astra_bowl_2.jpg'),74,189,674,379,'Robocurve original side-by-side placement evaluation frame');
 txt(s,'3 camera views + proprioception',790,184,425,66,27,C.dark,true);
 txt(s,'move_to(absolute end-effector pose)',790,286,422,82,27,C.ink,true);
 txt(s,'IK and safety limits\n20 model-call budget\n25% robot speed cap',790,403,416,121,25,C.gray);
 statement(s,'No task-specific policy training ≠ no robotics infrastructure.');
 note(s,2,'Describe the interface precisely. The published Robocurve evaluation uses a YAM dual-arm robot, three image views and proprioceptive state. The model calls move_to to specify an absolute end-effector pose; inverse kinematics produces the joint command. It operates with medium reasoning, a twenty-call budget, a twenty-five-percent speed limit and additional safety constraints. These choices define what direct means in this experiment. They do not amount to torque control at servo frequency. The page is an independent Robocurve evaluation, not an OpenAI research report despite the hostname. The image is a frame from the author’s edited comparison video, so it does not establish synchronized trial timing or end-to-end latency. The next slide uses the published trial counts rather than impressions from the video.',['S10']);
}
{
 const s=await slide('A · Placement Improves; Insertion Remains Hard','3',['S10']);
 chart(s,69,169,585,374,['Bowl placement','Fine insertion'],[
  {name:'GPT-6 Astra',values:[19,2],fill:C.teal},
  {name:'Fable 5.1',values:[8,2],fill:'#aeb8b6'}],20,'0');
 txt(s,'Successful trials out of 20 per task / model',78,544,572,40,20,C.gray);
 await poster(s,'astra_insertion',694,218,512,230,'Published failed insertion run',SOURCE.S10[1],'astra_insertion.mp4');
 txt(s,'19/20 versus 8/20\n2/20 versus 2/20',727,483,455,71,27,C.dark,true);
 statement(s,'Small samples; non-interleaved trials; placement baselines used different rigs.',594,C.red);
 note(s,2.5,'The chart reconstructs the exact reported counts, with a common denominator of twenty trials per model and task. Astra completes nineteen bowl-placement trials, compared with eight for Fable 5.1. On puzzle insertion, both complete only two trials. Play the failed insertion clip to focus discussion on the gap between approaching the object and satisfying the final contact constraint. The baseline also includes Fable 5 at one out of twenty for placement, omitted from the chart to keep the two-task comparison legible. Treat the difference as an observed result under the author’s setup: placement comparisons involve different rigs, trials were not interleaved, resets were manual and human scoring was not blinded. These limitations prevent a clean causal attribution of the entire gap to the model. The footage is edited and cannot be used to infer inference latency.',['S10']);
}
{
 const s=await slide('A · Painting: Planning, Calibration and Human Feedback','3',['S11','S23']);
 await poster(s,'painting',72,190,781,356,'SO-101 painting · excerpt at published speed',SOURCE.S11[1],'painting.mp4');
 pairText(s,'Plan a motion segment','About one minute of actions',889,196,315);
 pairText(s,'Observe and recalibrate','Initial anchor points matter',889,323,315);
 pairText(s,'Human feedback','Between and within runs',889,451,315);
 statement(s,'The agent updates instructions and calibration — not necessarily model weights.');
 note(s,2,'This original-author demonstration is useful because the method thread explains what sits around the video. The robot is an SO-101 arm. The author describes planning roughly a minute of actions, monitoring the execution, using initial anchor points and supplying human feedback between runs and sometimes during a run. The agent modifies instructions and calibration. None of these statements imply online weight training or a fully autonomous high-frequency contact controller. The excerpt preserves the published playback speed; the original presentation may itself be edited. Ask the audience which parts of a drawing error would come from global geometry, calibration, contact or timing. The separate wiping post broadens the set of demonstrated behaviors, but provides insufficient repeated evaluation or contact-force measurements to support a stronger reliability claim.',['S11','S23'],['https://x.com/cdngdev/status/2097339677745516710']);
}
{
 const s=await slide('A · A Supervisor Can Help — or Disrupt a Good Policy','3',['S09','S19','S20']);
 await img(s,path.join(ROOT,'research/assets/claude_vla.png'),72,175,1135,312,'Claude Plays Robotics original VLA-supervisor versus VLA-alone comparison');
 txt(s,'Reasoning layer: decide, inspect, intervene',80,512,1090,39,25,C.dark,true);
 txt(s,'Action layer: execute with learned dynamics and fast feedback',80,557,1090,39,25,C.gray);
 note(s,1.5,'The original report compares VLA supervision with the VLA acting alone. On some familiar tasks, adding a supervisor performs worse than the standalone policy; on tasks beyond the original policy’s capability, supervision can help. This makes intervention policy itself a research question. Google’s current Gemini Robotics ER 2 and Robotics 2 pages explicitly separate reasoning and action execution. Physical Intelligence’s pi-zero-point-seven provides another reference for a steerable action policy, using multimodal guidance and an action expert. These industry pages are architectural context, not additional measurements on this figure. Do not transfer results from the 2025 first-generation Gemini report to newer product names. Route A has made interfaces more flexible, but grounding, contact, timing and safe handoff remain open.',['S09','S19','S20']);
}
// Route B: executable scene hypotheses, not unqualified digital twins.
{
 const s=await slide('B · Big Picture: Build, Replay, Compare, Revise','3',['S12','S13']);
 flow(s,[['Real episode','RGB + known actions'],['Scene hypothesis','geometry + physical priors',true],['Simulator','execute the action'],['Comparison','replay and task evidence']],69,247,225,52);
 txt(s,'Camera pose',94,429,237,38,25,C.dark,true);txt(s,'Object geometry',364,429,250,38,25,C.dark,true);txt(s,'Physical parameters',645,429,298,38,25,C.dark,true);txt(s,'Action alignment',972,429,247,38,25,C.dark,true);
 statement(s,'These parameters solve different problems — and can compensate for one another.');
 note(s,1.5,'A Real2Sim system takes observations and known actions and proposes an executable scene. The simulator runs those actions, allowing the system to compare the resulting interaction with the recorded one. The agent may revise cameras, assets, poses or physical parameters, but these are distinct estimation problems. Better camera alignment can improve video similarity without fixing contact. Better geometry can still coexist with incorrect friction. The feedback loop is only as informative as its observable comparisons and as expressive as the simulator’s model family. This diagram is a synthesis of the workflow, not an exact replication of one implementation. Route B asks what the loop actually validates and where it needs stronger held-out tests.',['S12','S13']);
}
{
 const s=await slide('B · Astra Real2Sim: Demo and Dynamics Failure','3',['S12']);
 txt(s,'Tool orchestration and reconstruction',76,161,550,36,25,C.dark,true);
 txt(s,'Microphone: kinematic replay',665,161,546,36,25,C.red,true);
 await poster(s,'astra_real2sim',76,211,542,326,'Original author demo',SOURCE.S12[1],'astra_real2sim.mp4');
 await poster(s,'astra_microphone',665,211,542,326,'Author reports failed dynamics','https://x.com/Lingxiao234/status/2096992132527702382','astra_microphone.mp4');
 statement(s,'A rigid proxy cannot recover snap-fit compliance just by fitting the video.',594,C.red);
 note(s,2,'The original thread supplies multiview RGB and robot actions, then describes calibration, asset construction, system identification, MuJoCo execution and Blender rendering. It demonstrates broad tool orchestration rather than a controlled benchmark. Play the short overview, then the microphone excerpt. The author explicitly states that the microphone dynamics failed and the shown result is kinematic replay. A rigid-body proxy could not capture the compliant snap-fit interaction. This is not evidence that all Real2Sim is impossible; it identifies a model-class limitation in a particular example. A better optimizer cannot identify dynamics outside the simulator’s representational family. Both excerpts retain the author’s video speed. No new dynamics test or robot experiment was run for this survey.',['S12'],['https://x.com/Lingxiao234/status/2096992132527702382']);
}
{
 const s=await slide('B · Agentic Real2Sim and Its Specialized Tools','3',['S13']);
 await img(s,'ar2s_teaser.png',73,167,744,394,'Original Agentic Real2Sim input and reconstructed interaction examples');
 pairText(s,'Visual processing','SAM3 / SAM3D\nFoundationStereo / Pose',866,165,334);
 pairText(s,'Physical priors','Identity, materials and mass hints',866,321,334);
 pairText(s,'Simulation refinement','Scene assembly + bounded search',866,457,334);
 statement(s,'The agent coordinates the pipeline; specialist tools provide much of its geometry.');
 note(s,2,'The paper processes a recorded episode rather than only a static room. Visual processing extracts masks, depth, geometry and object poses using specialized backends including SAM3, SAM3D, FoundationStereo and FoundationPose. A physical-prior stage supplies identity, material class and mass hints. Scene preparation assembles the robot, cameras and reconstructed objects. Simulator-in-the-loop refinement uses deterministic optimization or search to improve placements and grasp execution. The distinction between tool and agent matters: the VLM is not independently solving every geometric subproblem. Table 1 of the paper lists the tools and schema-constrained skills by stage. The original teaser preserves real-versus-sim examples, while the labels here summarize their computational roles. Next, inspect the acceptance rule before interpreting the reported success rate.',['S13'],['https://arxiv.org/html/2607.19190v3#S3.T1']);
}
{
 const s=await slide('B · What Does 48/100 Actually Measure?','3',['S13']);
 await img(s,path.join(ROOT,'research/assets/agentic_replay_results.png'),75,174,1130,301,'Original DROID-100 outcomes and logarithmic model-cost chart');
 txt(s,'48 success   /   8 partial   /   44 failure',88,495,1100,44,30,C.dark,true,{align:'center'});
 txt(s,'Up to 5 candidates  ·  3 judges  ·  any judge’s best score ≥ 8/10',90,551,1100,41,24,C.ink,false,{align:'center'});
 note(s,2,'The figure retains all one hundred attempted DROID episodes and the logarithmic cost axis. For the best backend, Gemma 4 31B, forty-eight are accepted as success, eight as partial and forty-four as failures. The acceptance procedure first filters candidates using grasp, video and motion information, then evaluates up to five candidates. Three VLM judges score candidates separately and choose their own best one. If any judge’s best score reaches eight out of ten, the episode is accepted. This is not majority voting or an average-score threshold. The rubric emphasizes identity, final location, action similarity and end-effector position. It measures replay acceptance, not ground-truth physical-parameter accuracy or counterfactual prediction. Likewise the low dollar value in the figure is model-call cost, not the total cost of perception, simulation, compute and labor.',['S13'],['https://arxiv.org/html/2607.19190v3#S4.F3']);
}
{
 const s=await slide('B · SceneMosaic: Improve the Scene Locally','3',['S14']);
 await img(s,path.join(ROOT,'research/assets/scenemosaic_pipeline.webp'),75,174,1130,359,'SceneMosaic original object-centric local scene evolution pipeline');
 txt(s,'Initialize  →  stabilize  →  local Critic–Actor edits  →  compose variants',84,547,1115,40,25,C.dark,true,{align:'center'});
 statement(s,'Reported ~24× speedup concerns the specified scene-generation baseline.');
 note(s,1.5,'SceneMosaic starts from a reference signal, reconstructs a scene and decomposes it into object-centric local units. Physics-based layout stabilization addresses implausible placements. Critic–Actor iterations edit local units, then combine selected variants to generate diverse scenes. The important design idea is to make the agent solve a smaller, checkable local problem rather than repeatedly rebuilding the full scene. On SceneEval-100 the authors report approximately twenty-four times faster generation relative to their stated agentic baseline, together with layout quality, physical violation and human-evaluation measures. This is not a twenty-four-fold speedup for full contact-dynamics identification or robot learning. Its room-scale layout scope and the distinction between static plausibility and dynamic prediction must remain visible.',['S14']);
}
{
 const s=await slide('B · Four Different Tests of a Reconstructed World','3',['S12','S13','S14']);
 const rows=[['1','Appearance','Does the scene look similar?'],['2','Replay','Does a known action reproduce the recording?'],['3','New interaction','Does an unseen action have the right consequence?'],['4','Policy utility','Does the world improve real action or learning?']];
 rows.forEach((r,i)=>{let y=169+i*98;txt(s,r[0],87,y,63,48,34,C.teal,true,{serif:true});txt(s,r[1],179,y+3,311,42,29,C.ink,true);txt(s,r[2],515,y+7,692,58,26,C.gray);});
 statement(s,'Passing one test does not establish the next.');
 note(s,1,'Conclude Route B by separating the evaluation targets. Appearance checks whether a reconstruction looks right. Replay checks whether known actions resemble a recording. New-interaction tests vary the action or state to assess prediction. Policy-utility tests ask whether the model helps select actions, train policies or transfer to reality. These form a useful analytical progression, not a formal theorem or a metric introduced by the cited papers. Current results are strongest on scene generation and recorded-episode replay. Stronger counterfactual and downstream tests would be required before claiming a reliable training world. A failure at a later level does not erase progress at an earlier one, but it limits what the result establishes.',['S12','S13','S14']);
}
// Route C: experimental infrastructure and the artifact that persists.
{
 const s=await slide('C · Automation Still Needs an Experimental Loop','3',['S05','S06','S07','S08']);
 table(s,[['Work','What the agent changes','What the system still needs'],['Eureka','Reward code','RL training and evaluation'],['DrEureka','Reward + domain randomization','A valid sim-to-real setup'],['RoboGen','Tasks, scenes and skill learning','Useful difficulty and coverage'],['AutoRT','Real-world task / data collection','Safety and operational support']],73,182,1134,354,[264,415,455],24);
 statement(s,'Who chooses the next experiment, checks the result and keeps the improvement?');
 note(s,1.5,'Before presenting ENPIRE, locate four existing automation components in the development workflow. Eureka searches over reward programs, uses reinforcement learning to train policies and reflects on results. DrEureka extends language-model involvement to domain randomization and sim-to-real recipe design. RoboGen generates tasks, scenes and skill-learning processes. AutoRT organizes real robot tasks and data collection with foundation models. These are important precursors, not four unrelated papers to memorize. They also clarify that the agent’s output is often not a robot action: it may be a reward, dataset or experiment configuration. The remaining systems question is how to connect proposal, execution, validation and persistence into a repeatable loop on actual hardware.',['S05','S06','S07','S08']);
}
{
 const s=await slide('C · ENPIRE: Real Experiments in the Agent Loop','3',['S15']);
 await img(s,path.join(ROOT,'research/assets/enpire_framework.png'),73,164,745,419,'ENPIRE original full framework including human-guided environment construction and policy improvement');
 const entries=[['EN','Environment: safety, reset, verification'],['PI','Policy improvement: program or training'],['R','Rollout: real robot experiments'],['E','Evaluate and reflect on the result']];
 entries.forEach((r,i)=>{let y=175+101*i;txt(s,r[0],854,y,66,45,30,C.teal,true,{serif:true});txt(s,r[1],930,y+3,269,77,23,C.ink);});
 statement(s,'The output can be a better program, policy or training recipe.');
 note(s,2,'Use the full original framework so the environment and human-feedback components remain visible. EN denotes the environment contract: hard safety limits, automatic reset and success verification. PI is the policy-improvement space, which can include heuristic programs, behavior cloning, online or offline reinforcement learning, and combinations with VLAs. R executes rollouts on real hardware. E analyzes the results and informs the next change. The source resolves the user’s EMPIRE reference to ENPIRE, Agentic Robot Policy Self-Improvement in the Real World. The key advance is not simply a language model suggesting an action, but coding agents conducting experiments and modifying candidate policies against a repeatable real environment. More compute or more robot stations changes how quickly that loop can acquire evidence.',['S15'],['https://arxiv.org/html/2606.19980v1#S2']);
}
{
 const s=await slide('C · Reliable Reset and Verification Come First','3',['S15']);
 await img(s,'enpire_verifier.png',77,187,1125,306,'ENPIRE original two-camera zip-tie verification mechanism');
 txt(s,'Human-guided environment construction',77,520,565,66,26,C.dark,true);
 txt(s,'Then fixed environment APIs for improvement',681,520,524,66,26,C.ink,true);
 statement(s,'The verifier is part of the method, not a detail outside the benchmark.');
 note(s,2,'This figure shows why real experimental autonomy depends on instrumentation. Zip-tie verification uses crops and image segmentation from two cameras to check whether the strap passes through the head, reducing false positives from a single view. The first phase of ENPIRE uses human feedback to construct safety, reset and verification procedures. During autonomous policy improvement, the environment API is then fixed. Some tasks reset directly to the beginning of a difficult substage rather than to an arbitrary full-task initial state. These choices make high-throughput experiments possible, but they define the scope of the final success claim. Ask what would happen if the agent could freely rewrite the success test while optimizing the policy: an apparently improving curve might no longer represent physical progress. Independent validation remains important even with a fixed environment API.',['S15'],['https://arxiv.org/html/2606.19980v1#S2.SS1','https://arxiv.org/html/2606.19980v1#S2.F4']);
}
{
 const s=await slide('C · ENPIRE: Improvement Under a Recovery Budget','3',['S15']);
 await img(s,'enpire_scaling.png',73,155,763,435,'ENPIRE original task improvement and multi-agent scaling results, with axes and legends');
 txt(s,'Up to ~99%',861,182,342,65,44,C.dark,true,{serif:true});
 txt(s,'Reported high completion\nunder the paper’s protocol',861,267,340,77,24,C.ink);
 txt(s,'Up to 8 conditional retries\nPrevious failure informs recovery\nSome resets start at a hard phase',861,392,339,158,24,C.gray);
 statement(s,'Not one-shot precision. Not independent best-of-eight.',594,C.red);
 note(s,2,'Read the original plots with their task-specific axes intact: the Push-T row reports a normalized score, while insertion uses success rate. The paper reports very high completion, including roughly ninety-nine percent, under its defined rollout protocol. That protocol includes up to eight conditional retries: later attempts can use information from earlier failures. It is therefore incorrect to interpret the result as one-shot insertion precision or as eight independent draws from a fixed Bernoulli probability. Do not use an independence formula to back-calculate a one-attempt rate. Recovery is a legitimate capability and part of the result, but it must be visible. Also retain the reset scope: some environments start at the hardest substage. The plots show progress under these operational conditions, not unrestricted deployment success.',['S15'],['https://arxiv.org/html/2606.19980v1#S3','https://arxiv.org/html/2606.19980v1#S1.F3']);
}
{
 const s=await slide('C · More Robots: Faster Results, Different Costs','3',['S15']);
 await img(s,'enpire_utilization.png',74,191,1131,353,'ENPIRE original mean resource utilization, token utilization, and time/token-to-success plots');
 statement(s,'Wall-clock time, token cost and per-robot utilization must be measured separately.');
 note(s,1.5,'The original three-panel figure compares one, four and eight agents or robot stations. The left panel distinguishes robot and GPU utilization. The middle panel reports mean token utilization and an explicit linear projection. The right panel places tokens to success and time to success on different axes. More stations can reduce time to a target performance while increasing token consumption and reducing per-robot utilization. Do not collapse these into a single statement that scaling is more efficient. It may be the right choice when wall-clock time is the priority, but a different conclusion follows when cost or hardware utilization matters. MRU and MTU provide separate views of the physical and inference resources. The error bars and full axes are retained from the paper rather than replaced with a decorative scaling curve.',['S15'],['https://arxiv.org/html/2606.19980v1#S3.F7']);
}
{
 const s=await slide('C · ASPIRE: Persist Skills Beyond the Conversation','3',['S17']);
 await poster(s,'aspire_trace',73,188,771,353,'Execution traces support debugging and skill reuse','https://research.nvidia.com/labs/gear/aspire/','aspire_trace.mp4');
 txt(s,'31%  vs  4%',881,218,321,66,44,C.dark,true,{serif:true});
 txt(s,'LIBERO-Pro Long\nheld-out transfer',881,304,317,78,25,C.ink);
 txt(s,'Multimodal trace\n→ failure diagnosis\n→ reusable skill',881,435,318,116,25,C.gray);
 statement(s,'Persistent external skills are different from updating the base model.');
 note(s,2,'ASPIRE records multimodal execution traces, localizes failures, repairs code, stores reusable skills and expands that library through exploration. The video exposes the execution trace interface, so use it to explain what feedback is available to a debugging agent. Its reported zero-shot transfer on LIBERO-Pro Long is thirty-one percent, compared with approximately four percent for the referenced prior methods under that evaluation. This number does not describe unrestricted real-world reliability. The real bimanual study transfers three selected simulation skills as context; one can-lift case improves from thirteen of twenty to nineteen of twenty trials while reducing debugging tokens. The persistent object is an external skill library, not automatically the foundation model’s weights. Both the discovery/test split and the retrieval policy determine whether that memory helps on a new task.',['S17'],['https://arxiv.org/html/2607.00272v1#S3']);
}
{
 const s=await slide('C · CaP-X: Test-Time Repair or Weight Training?','3',['S16']);
 txt(s,'CaP-Agent0',77,180,567,43,31,C.dark,true);
 flow(s,[['Execution feedback','visual differences'],['Better code + skills','test-time improvement',true]],78,244,252,55);
 txt(s,'CaP-RL',77,394,567,43,31,C.dark,true);
 txt(s,'GRPO post-training\nQwen2.5-Coder-7B',77,454,560,91,28,C.ink);
 chart(s,704,173,505,345,['Lift','Stack'],[{name:'CaP-RL success (%)',values:[84,76],fill:C.teal}],100,'0');
 txt(s,'Real robot · 25 trials per task',723,535,472,40,23,C.gray,false,{align:'center'});
 statement(s,'One trial can contain multiple interaction turns without a reset.');
 note(s,2,'CaP-X separates a benchmark and environment framework from two improvement mechanisms. CaP-Agent0 improves test-time execution through visual feedback, skill synthesis and additional reasoning or search. CaP-RL changes model weights through GRPO post-training of Qwen2.5-Coder-7B using code as the action representation. Table 4 reports eighty-four percent real lift success and seventy-six percent real stack success, with twenty-five trials per task: these correspond to twenty-one and nineteen successful trials. The chart shows the trained arm’s reported results, not a claim that all CaP-X components achieve those values or a comparison with Astra’s tasks. Another protocol trap is pass-at-one: in this benchmark one trial may contain multiple interactive turns without resetting the environment. It does not mean only one language-model call.',['S16'],['https://arxiv.org/html/2603.22435v2#S5.T4']);
}
{
 const s=await slide('C · RATs: Acquire Skills Before the Task Arrives','3',['S18']);
 await img(s,'rats_method.png',72,184,1136,327,'RATs original play-time exploration, planning, execution and verification workflow');
 txt(s,'PLAY TIME',84,532,535,35,23,C.dark,true);txt(s,'TEST TIME',684,532,523,35,23,C.dark,true);
 txt(s,'Self-proposed goals → verified skills',84,576,551,40,25,C.ink);txt(s,'Frozen library → held-out tasks',684,576,523,40,25,C.ink);
 note(s,1.5,'RATs shifts skill acquisition to a play phase before a particular downstream task is known. The agent proposes tasks, plans code, executes it, verifies results, diagnoses failures and stores useful skills. At downstream test time the skill library is frozen, separating exploration from evaluation. That is a different experimental question from fixing the current task while observing its outcome. The original method figure includes both the environment and memory components; the two labels below summarize the split rather than replace it. Most evidence is in simulation. Retrieval can also hurt when a skill or memory is inappropriate, so more stored experience is not monotonically better. The validator’s errors and the cost of play are part of the full accounting.',['S18']);
}
{
 const s=await slide('C · What Actually Persists After Improvement?','3',['S13','S15','S16','S17','S18']);
 table(s,[['Persistent object','Example','The next test'],['Program / task policy','ENPIRE','Independent rollout validation'],['Skill library','ASPIRE / RATs','Held-out transfer + retrieval harm'],['Model weights','CaP-RL','Matched baselines + inference cost'],['World parameters','Agentic Real2Sim','Unseen actions + policy utility']],74,190,1132,356,[328,327,477],24);
 statement(s,'Automatic execution is not the same as verified, generalizable improvement.');
 note(s,1.5,'Bring the third route back to the original improvement gap. A program can persist and still overfit to the current reset. A skill library can transfer useful procedures but also retrieve harmful ones. New weights can reduce test-time search but require controlled comparisons that include training and inference budgets. A fitted world can be reusable while failing outside the recorded actions. These are different carriers of experience, with different failure modes and tests. For all of them, report reset cost, human interventions, unsuccessful trials, validator errors and the total resource budget. Process activity, more generated code or more stored skills is not itself evidence that the robot has become more capable. Route C has made parts of the development loop executable; reliable lifelong improvement remains a stronger claim.',['S13','S15','S16','S17','S18']);
}
// Synthesis: return to the questions, not to a paper leaderboard.
{
 const s=await slide('What the Three Routes Establish','4',['S09','S10','S13','S15','S16','S17']);
 table(s,[['Route','What is established','What remains open'],['A  Action','Flexible reasoning-to-action interfaces','Precise contact and real-time handoff'],['B  World','Automated scene construction and replay','Counterfactual dynamics and policy utility'],['C  Improvement','Executable experiments and persistent artifacts','Reliable transfer at acceptable total cost']],74,213,1131,324,[248,444,439],25);
 statement(s,'The unit of progress is a verified capability under a stated interface and budget.');
 note(s,1.5,'Return to the three gaps rather than ranking headline results. Action systems show that general reasoning can enter robot execution through flexible interfaces, but precision, contact, grounding and timing remain limiting. World-building systems automate complex scene and episode pipelines, yet replay acceptance does not establish counterfactual dynamics or downstream learning value. Improvement systems can run experiments and retain programs, skills or weights, while reliable transfer and total cost remain unresolved. These are meaningful advances even when the strongest general claim fails. The comparison is an analytical synthesis across heterogeneous primary sources; it is not a joint benchmark. Ask for the exact capability, interface, update target, evaluation distribution and budget whenever a system is described as autonomous or self-improving.',['S09','S10','S13','S15','S16','S17']);
}
{
 const s=await slide('Open Questions That Need Better Experiments','4',['S09','S13','S15','S16','S17','S18']);
 const rows=[['When should the agent intervene?','Measure rescue, damage and response latency.'],['When should we trust a reconstructed world?','Hold out actions, speeds and contact conditions.'],['How does expensive exploration become cheap skill?','Count discovery cost and future execution cost.'],['Who verifies the autonomous experiment?','Audit resets, interventions and false success.']];
 rows.forEach((r,i)=>{let y=169+103*i;txt(s,String(i+1),78,y,55,46,31,C.teal,true,{serif:true});txt(s,r[0],161,y+1,1041,39,28,C.ink,true);txt(s,r[1],161,y+44,1041,39,24,C.gray);});
 note(s,1.5,'These questions are synthesis, not claims of a new method or completed novelty review. First, use a fixed low-level policy to measure both rescue of failed tasks and damage to previously successful tasks, including latency and contact risk. Second, hold out interventions to test whether a reconstructed world predicts beyond its fitting trajectory. Third, compare skill libraries, reusable code and weight updates under matched total budgets, including exploration and later execution. Fourth, separate the reward used for search from the evaluator used to report success where possible. Record reset failures, human takeovers and false positives instead of dropping them from the denominator. These experiments would turn compelling systems demonstrations into more defensible statements about generalizable capability.',['S09','S13','S15','S16','S17','S18']);
}
{
 const s=await slide('Conclusion','4',['S03','S13','S15','S17']);
 const rows=[['General agents now work at multiple robotics layers.','Execution, world construction and experimental development.'],['Interfaces and verification remain central.','A stronger model does not erase sensing, control or evaluation.'],['Cumulative capability is the long-term target.','Reliable transfer with affordable exploration and execution.']];
 rows.forEach((r,i)=>{let y=197+123*i;txt(s,String(i+1),83,y,68,57,39,C.teal,true,{serif:true});txt(s,r[0],184,y,1027,45,30,C.ink,true);txt(s,r[1],184,y+52,1027,43,24,C.gray);});
 note(s,1,'Close with three points. General agents are entering several layers of robotics, not just high-level planning. Their contributions range from action decisions to simulator construction and real experimental development. Second, the interface and the verification infrastructure remain central sources of capability: they determine what actions are feasible and what apparent progress means. Third, the target is not simply an impressive run but reusable capability that transfers and remains economical. The surveyed work gives concrete mechanisms and important evidence, while leaving precise contact, predictive worlds and reliable cumulative improvement open. Return to the opening goal: can the robot finish the job now, and will the next job become easier for a reason we can measure?',['S03','S13','S15','S17']);
}
if(records.length!==36)throw new Error(`Unexpected slide count: ${records.length}`);
if(Math.abs(records.reduce((a,r)=>a+r.minutes,0)-60)>1e-8)throw new Error('Timing does not total 60 minutes');
await fs.writeFile(path.join(BUILD,'slide_records.json'),JSON.stringify(records,null,2));
await fs.writeFile(path.join(BUILD,'video_placements.json'),JSON.stringify(media,null,2));
await fs.mkdir(path.join(BUILD,'rendered'),{recursive:true});
console.log('Exporting 36-slide draft...');
await (await PresentationFile.exportPptx(deck)).save(path.join(BUILD,'draft.pptx'));
console.log('PPTX exported. Rendering slides...');
for(let i=0;i<deck.slides.items.length;i++){
 const s=deck.slides.items[i];
 const png=await deck.export({slide:s,format:'png',scale:1.25});
 await fs.writeFile(path.join(BUILD,'rendered',`${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
 const layout=await s.export({format:'layout'});
 await fs.writeFile(path.join(BUILD,'rendered',`${String(i+1).padStart(2,'0')}.layout.json`),await layout.text());
 console.log(`Rendered ${i+1}/36`);
}
console.log('DRAFT_COMPLETE');
