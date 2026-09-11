import fs from 'node:fs/promises';
import {Presentation} from '@oai/artifact-tool';
const p=Presentation.create({slideSize:{width:1280,height:480}});const s=p.slides.add();s.background.fill='#ffffff';
for(const [i,f] of ['Georgia','Times New Roman','Noto Serif CJK SC','Noto Sans CJK SC'].entries()){
 const q=s.shapes.add({geometry:'textbox',position:{left:50,top:20+i*110,width:1160,height:100},fill:'none'});q.text='Agents for Robotics — '+f;q.text.style={typeface:f,fontSize:40,bold:true};
}
await fs.writeFile('/home/limx/Desktop/agent_for_robotics/.build/font_probe.png',new Uint8Array(await (await p.export({slide:s,format:'png'})).arrayBuffer()));
