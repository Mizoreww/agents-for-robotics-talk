# v0.22 — Takeaways and P35 cleanup

Date: 2026-09-16. Final HTML SHA-256:
`9735355c06fbf47f99d531a34a7b68c62f87c3a8e6c6d336a8d4d1221e8cc9d3`.

## Scope

- P36 replaces the old Role/Artifact/Evidence diagram and its two slogans with three
  horizontal paths. Control recalls P6 and P17 before asking Latency? / Better interface?.
  Data asks Sim2Real?; Improvement asks Efficiency?.
- The two images are exact captures of the existing P6/P17 slides, not redrawn conclusions.
  They are embedded and use the existing click-to-enlarge figure dialog.
- The Chinese P36 script follows the new path and questions. Its generated independent
  and embedded versions agree; the CJK font subset was refreshed.
- P35 only loses the specified Open test text node. No other element is moved and its
  narration and academic citation are unchanged.
- All other slide records, all media metadata and video bytes, and the three v0.21 player
  source files remain identical. 37 slides, 28 clips, 48 images, suggested 60 minutes.

## Validation

The fixed comparison is `.build/v0_22_baseline/`, captured from the delivered v0.21.
`test_takeaways_v022.py` tests exact slide scope, questions/deletions, thumbnail-to-source
identity, image additions, media equality and unchanged player files. Historical closing
scope tests now explicitly delegate P35/P36 changes to this regression; source pinning,
table emphasis and other slide comparisons remain enforced.

40 Python regressions and static validation passed. The targeted closing audit checks
P35/P36 overflow, both thumbnail enlargements and the updated sidebar narration. Streaming
HTTP hashes before/after browser load and the loaded deck-data DOM bind these observations
to the final artifact. P35/P36 screenshots were visually inspected: alignment, spacing and
fonts remain consistent; no clipped text or overlap was found.

The final general browser and docked-script audits are recorded under this same hash.
The general audit covers all 37 slides and 28 clips' basic play/pause/restart. Earlier
uninterrupted full-clip audits remain historical under their original hashes, not relabeled.

Current records: `.build/standalone_delivery_audit.json`, `.build/standalone_visual_audit.json`,
`.build/v0_22_closing_audit.json`, `.build/v0_21_sidebar_audit.json` (reusable UI audit, rerun),
`.build/v0_22_manifest.json`.

No new paper claims, external media downloads, historical exports, push or public release.
