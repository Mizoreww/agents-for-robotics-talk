# v0.11 — Data taxonomy and actual Astra control loop

Requested 2026-09-15. Fixed comparison is `.build/revision_0_11_baseline/manifest.json` (delivered v0.10). New source findings must come from current primary sources, with dated snapshots; no WeChat retry or attribution.

## User requirements

- Rename category 2 to **Data**, including **Real-to-sim Replay / Data Rollout**. Move the existing structural-design hand demo into that chapter as asset generation. Preserve its explicit non-working-design limitation.
- Survey deployed Astra interfaces: numeric joint targets (including whether full-body), EEF/IK goals, controller programs, atomic skills and learned-policy tools. Distinguish what the model returns from what downstream software computes.
- Report actual inference/decision timing where disclosed. Separate model-call latency, full decision-cycle time, action-segment horizon, low-level Controller Hz, simulator Hz and video playback speed. Do not estimate real decision frequency from accelerated demos or control-step rates.
- Control summary clearly contrasts demonstrated semantic understanding / spatial generalization with remaining high-frequency-control / physical-generalization limitations. Retain task/observation/budget boundaries and distinguish absent evidence from demonstrated failure. Do not assert permanent impossibility or undisclosed robot-pretraining causality.
- Preserve existing diagrams, original figures, videos, table emphasis, English slide text, Chinese narration with English terminology, matched Noto/player styling, Takeaways and Thank You.

## Implementation plan

1. Freeze v0.10 and research current interface/frequency and Data examples.
2. Add one compact interface/timing evidence page if the source audit supports it; otherwise avoid an empty numerical comparison. Do not turn this into more paper deep dives.
3. Reframe the Data opening and summary, move hand to Data, update cross-chapter transitions and Takeaways. Keep replay acceptance, generated rollouts and proven training benefit separate.
4. Update and validate all slide IDs, narration, media mappings, titles and result comparisons. Same-media payloads must be byte-identical to v0.10.
5. Rebuild, refresh CJK subset, isolate and audit browser playback/layout/mobile controls and every changed diagram. Use independent Matt Pocock Standards / Spec review before delivery.

## Evidence boundary

The community list supplies discovery and the user's preferred taxonomy, not an evaluation authority. A rollout is not necessarily a curated dataset; a CAD animation is not a validated robot or validated training asset. A VLA proposal that contains joint targets is not a direct full-body joint output by Astra. Reciprocal latency may be displayed as a derived sequential query rate only with explicit source and qualifier.

No push, release or historical PPTX/PDF/ZIP regeneration. Timing remains suggested, not rehearsed.
