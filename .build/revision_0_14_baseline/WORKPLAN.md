# Agents for Robotics — current work

## Revision 0.13 · 2026-09-15

- [x] Preserve verified v0.12 baseline.
- [x] Locate report result screenshots and heatmap.
- [x] Remove Claude / RPent and revise Astra spine.
- [x] Replace two tables with original results graphics; add heatmap.
- [x] Renumber slides, notes, provenance and tests.
- [x] Build, visual/offline QA and Standards / Spec review.

Final HTML SHA-256: `614151be450e730e6cbd2b905af76143ac3aedb90fbfd4aa9d54287e5ab479a5`. Standards: 0 findings. Spec: 1 P3 transition fixed and rechecked; 0 unresolved. 20 tests passed, 35-page layout and 18-clip controls passed, 5 full-length playback checks passed.

## v0.13 slide4/5 polish
- Direct action box now uses the same gray fill/border as neighboring tools. Removed requested bottom sentences on slides4 and5.
- Rebuilt; final browser/layout/media controls/mobile and static checks passed. Visual inspection of4/5 passed. All35 pages and18 clips retained.
- Current HTML SHA-256: `3eda1d3fbd2b8a92a4712d916c5916ae59d6cc6594bcab4477ab7393adae52f1`. Earlier extended playback and two-axis review remain evidence for the pre-polish revision, not rerun for this cosmetic follow-up.

## Slide6 interface notation
- Added l/a and c=(k,g)/a to four links; lower System1 is π(a | o,c), upper remains π(a | o,l). Definitions and functional-not-neural interpretation synchronized in Chinese notes.
- Final static/browser/layout/media-control/mobile gates passed. Slide6 visual inspection passed; current hash `7dd72dc9dc888b6edd7aac19d5b64220770c1fb94e02ce386872d0157d87e3cf`. No new experiments or full-length extended playback.

## P7 capability framing and P4 tool colors
- P7 title: Astra: Stronger Real-Robot Performance. Removed the requested on-slide protocol paragraph; task values/video unchanged and interpretation boundaries retained in notes. Narration now leads with capability gains.
- P4 IK / motion planner shares Perception / state tools light-teal fill and text; Direct remains gray.
- Current build `ae50f078af71bb8f931b4ea421359411b72483073032bd68130c7f173a51dee9`; final audit status is in standalone_delivery_audit.json.

## P8 demo framing and control interfaces
- Title changed to Astra: More Real-Robot Demos. Removed the requested large summary band. Gray per-video notes now read Control interface: not disclosed.
- Current primary-source check: GPT-Policy-Eval still README/media only; keyboard original post does not specify API. X replies were not accessible, so no claim to an exhaustive thread audit. See research/p8_control_interfaces_2026-09-15.md.
- Narration and CJK subset synchronized. Current HTML `9861057cad1b284c1ce17a6c313fbab02ec0662542ee73c8bb26bc1eda6af57c`; final verification recorded in standalone_delivery_audit.json.
