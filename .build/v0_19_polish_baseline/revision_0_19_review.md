# v0.19 independent review

Date: 2026-09-16. Fixed baseline: `.build/revision_0_19_baseline/`, including the delivered v0.18 P3/P23 vertical-only adjustment and requested text removals.

Final HTML SHA-256: `eb8011c95baa5e41b9f9fd1f09c35e611721c9d4c87fdf7793d2656d30972749`.

## Scope and narrative

ENPIRE follows the official-site order: Learned Policy demos (24), System (25), Auto Evaluation (26), Auto Reset with official Cases 1–4 (27), Policy Improvement (28–29), Evaluate Coding Agents (30), Fleet Scaling and cost (31–32), Simulation Evaluation (33), Limitations and RSI (34). P23 keeps the original chapter-opening diagram. P1–23 and P35–36, including their per-slide narration, equal the fixed baseline.

The four learned-policy clips and the four reset clips remain explicitly distinct. Pin-to-GPU written-recipe transfer is explained in P34 narration, not a separate detour. The original fonts and horizontal layout are preserved.

## Standards

Codex reviewer `/root/v019_standards`: initial P2 for stale documentation counts and source/test references. Corrected the records to 28 total clips, 10 official ENPIRE clips and 12 extended-playback clips; included the v0.19 source pins, loader, tests and fixed baseline. Independent final follow-up: **0 unresolved findings**.

## Spec

Codex reviewer `/root/v019_spec`: **0 findings**. Verified the requested official order, source fidelity, media classification and preservation of earlier user edits.

## Final QA

- 27 focused tests passed: official order (5), vertical-only centering (4), ENPIRE preservation (4), table emphasis (5), results source identity (3), Data demos (6).
- All 36 slides passed layout checks; zero overflow and zero unloaded images.
- All 28 embedded clips passed basic playback, pause and restart checks.
- Twelve clips played to completion without errors: Cube, Claw, four learned-policy demos, Auto Evaluation, four Auto Reset demos and Fleet.
- Navigation, original-figure dialogs, synchronized Chinese narration and mobile buttons passed. Desktop text overflow and mobile button overflow: zero.
- New reset sequences were fully decoded and inspected through sequential contact sheets. Detailed visual checks covered P24/26/27/30/32/33/34; the entire P23–34 chapter was also checked as a contact sheet.
- `validate_standalone.py` exited 0 against the final hash: 137,952,788 bytes, 36 slides, 28 clips, 46 images, four fonts, zero external runtime resources, identical isolated copy and embedded/standalone Chinese scripts.
- Large-artifact identity uses streamed HTTP hashes before/after browser execution plus the loaded deck-data DOM hash; no CDP response-body workaround.

## Evidence boundary

This review did not run ENPIRE or independently reproduce its experiments. Physical pass@8 permits conditional retries; RoboCasa runs each script once. Figure 3 and Figure 7 time/cost denominators remain separate. Reset demos do not prove arbitrary-state recovery. RSI is an open question, not demonstrated recursive acceleration or coding-model weight updates. No measured rehearsal, public release, push, or historical PPTX/PDF/ZIP regeneration.

## Authorities

Final status is bound by `.build/standalone_delivery_audit.json`, `.build/standalone_visual_audit.json`, `.build/v0_19_extended_audit.json` and `.build/v0_19_final_review_manifest.json`. The pre-closeout reviewed closure `.build/v0_19_review_manifest.json` had zero drift before documentation finalization. Only final status documents, audit records and the current preview were changed after that review; the HTML and reviewed build sources stayed unchanged.
