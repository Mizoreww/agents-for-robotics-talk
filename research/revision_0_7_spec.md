# v0.7 — user-corrected presentation scope

2026-09-14. This supersedes v0.6's28-slide scope. User says each part must have one representative work, a clear problem/method/results argument, and the anonymous Direct/Hybrid report's concrete architecture. User permits exactly one short Control background page naming Claude Plays Robotics and RPent and explaining why robot-data training changes applicability of older conclusions.

## Acceptance
1.21English slides, Chinese script/English technical names; Noto fonts and white/teal controls retained; single fully embedded HTML.60minute target remains unmeasured.
2.Control4–8: original report diagram at chapter opening4; brief prior-work architecture5; exact model inputs/outputs and paired protocol6; RoboDojo results/demo7; bounded summary8. One representative: anonymous GPT6Astra EmbodiedPolicy report. No other full control cases.
3.Data9–13: Agentic Real2Sim only. Opening diagram9, real/twin10, original method11, DROID100judge protocol/results12, replay-vs-prediction summary13. No external Real2Sim demos or inferred metrics.
4.Improvement14–19: ENPIRE only. Opening diagram14, task15, original method16, reset/verifier17, curve18, cost+summary19. Keep setup, fixed APIs, conditional retries, costs. No ASPIRE/RoboRSI detours. Do not call this proven recursive enhancement.
5.Painting2 and hand20 are separately labelled qualitative applications, not evidence for the three studies. Closing21 compares questions, not success rates.9retained clips; no clip bytes changed.
6.Architecture is an original English webpage capture of the user's supplied figure. Explain3views,14Dproprio,ℓ/history,π0.5joint-space50×14candidate,FKtrajectory/Astrareview,ORaccept1–15steps versusEEFcorrection1–5steps,DirectEEF1–5,25Hznativecontrol notLLMfrequency. InternalAstra network/training not disclosed.
7.RoboDojo main result13/50vs24/50,10tasks×5pairedcases. Segmentlength andprior bothchange; notpurecausalpriorablation. Different-taskdemo clips excludeLLMlatency. Do not poolRoboLabselectedfinalslots/publicbaseline into this table.
8.BackgroundmentionsClaudePlaysRoboticsdirect/code/policysupervision,andRPentservicecompositiononly. Trainingwithrobotdatacanchangepremises; oldexperimentsremainvalidintheirsettings; oldconclusionsnotuniversal. Astra-specificrobotpretrainingnotconfirmed.
9.Real2Sim48accepted8partial44failure/all100;eligiblecandidate≤5;3judges;anybest≥8/10;notmajorityvote;modelbillnotfullcost.
10.ENPIREpin1→8pairsresearchtime>1.5h→~40min,withconditionalretryprotocol(notone-shot/independentsampling).Fasterresearchcanusemoretokens.
11.Regeneratefont/build/static/browser/visualchecks; preservev0.6backupandarchivedsources. No publication requested.

Review baseline: `.build/revision_0_7_baseline/` contains the previous verified v0.6 sources and delivery. Use `diff -u` against current builder/script/validator/browser_audit; old Git HEAD predates both revisions. No new issue is needed for this user-directed content edit.
