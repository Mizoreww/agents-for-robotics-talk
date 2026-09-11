import fs from 'node:fs/promises';
import {finalizePresentation} from '/home/limx/.cache/codex-runtimes/codex-primary-runtime/plugins/openai-primary-runtime/plugins/presentations/skills/presentations/container_tools/artifact_tool_utils.mjs';
process.env.RUNTIME_NODE_MODULES='/home/limx/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const ROOT='/home/limx/Desktop/agent_for_robotics';
const SKILL='/home/limx/.cache/codex-runtimes/codex-primary-runtime/plugins/openai-primary-runtime/plugins/presentations/skills/presentations';
await fs.mkdir(ROOT+'/output',{recursive:true});
const result=await finalizePresentation({
 workspaceDir:ROOT,candidatePath:ROOT+'/.build/focus_media.pptx',
 finalPath:ROOT+'/output/Agents_for_Robotics_Focused.pptx',
 pythonExecutable:'/home/limx/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',
 integrityValidatorPath:SKILL+'/container_tools/inspect_presentation_package_integrity.py',
 layoutValidatorPath:SKILL+'/container_tools/inspect_presentation_layout_geometry.py',
 explicitTotalSlideCount:22,requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[],
 layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],
 // The template is HTML, which the reference-policy validator does not accept.
 // These explicit installed families reproduce its Linux fontconfig fallback.
 fontPolicy:{basis:'design',families:['Noto Serif','Noto Sans']},
 verifyArtifactToolImport:true,receiptPath:ROOT+'/.build/focused_validation.json'
});
console.log(JSON.stringify(result,null,2));
