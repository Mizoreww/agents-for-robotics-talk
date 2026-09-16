# v0.9 review closeout · 2026-09-14

Fixed comparison: `.build/revision_0_9_baseline/manifest.json` (verified v0.8), not older Git HEAD. Local revision, no new commits. Workflow: Matt Pocock code-review, independent Codex-native Standards and Spec axes.

## Standards

Initial finding: **P2, source identities were reauthorized by normal derivation**. The generator hashed current source bytes and replaced the result authority, so a valid-JSON change to Hi Robot IA 76→77 could be blessed as new input.

Resolution: independently freeze all 13 reviewed identities in `research/results_v0_9_sources.json`. Derivation checks identities before reading values and cannot rewrite the manifest. Builder and validator require the same identities. Three regression tests reproduce the authority, reject byte drift in every source, and reject the valid-JSON 76→77 mutation before publication. Every test intercepts writes in memory.

Independent reviewer recheck: **resolved, no remaining finding**. No additional code-smell refactor required.

## Spec

**Pass, 0 findings.** All 11 result groups and critical caveats covered. RPent T/S arithmetic independently checked. Added/modified table screenshots readable, original axes and legends preserved. RoboDojo and RoboLab separate; ENPIRE metrics, retry rules and costs distinct. All 18 video payloads and 33 prior image assets preserved. 36 pages, suggested 60 minutes.

## Verification

- `python3 .build/test_results_v09.py`: 3 tests passed, including source-drift rejection across all 13 files.
- Full `.build/validate_standalone.py`: passed for delivered hash.
- Desktop: 36 pages, zero measured text overflow, all images loaded.
- Playback: all 18 clips play / pause / restart; 5 supplemental clips completed uninterrupted playback.
- UI: overview navigation, keyboard, fullscreen, enlarged figures, Chinese script and 390px controls passed.
- Visual: all layouts and all new/modified result pages inspected; figures and script/button views checked.
- Source-identity repair rebuild reproduced the identical HTML; fresh browser/visual audits still bind to it.

HTML SHA-256: `eb25dad97e0adc4947b19d76b165dfb7ecb27a1276702c3068ee344cfc8e14f7`.
Audit authorities: `.build/standalone_delivery_audit.json`, `.build/standalone_visual_audit.json`, `.build/v0_9_extended_audit.json`.

No source experiments rerun. No Claude/Anthropic service calls, push, release, or historical PPTX/PDF/ZIP update. Timing remains unmeasured.

## New user reference after v0.9

The subsequent WeChat link is blocked by the browser site-safety policy. Its article identity, taxonomy and embedded references have **not** been verified or incorporated. Await user-provided text/screenshots/PDF; independent taxonomy discussion must not be attributed to that article.
