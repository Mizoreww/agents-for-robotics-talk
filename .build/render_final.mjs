import fs from 'node:fs/promises';
import {FileBlob,PresentationFile} from '@oai/artifact-tool';
const root='/home/limx/Desktop/agent_for_robotics';
const p=await PresentationFile.importPptx(await FileBlob.load(root+'/output/Agents_for_Robotics_Focused.pptx'));
await fs.mkdir(root+'/.build/final_artifact_rendered',{recursive:true});
for(let i=0;i<p.slides.items.length;i++){
 const png=await p.export({slide:p.slides.items[i],format:'png',scale:1.25});
 await fs.writeFile(root+'/.build/final_artifact_rendered/'+String(i+1).padStart(2,'0')+'.png',new Uint8Array(await png.arrayBuffer()));
 console.log('Rendered final slide',i+1);
}
