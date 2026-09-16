# v0.20 — centering, chapter-ending split and thanks

Date: 2026-09-16. Final HTML SHA-256: `a310089992e6969c0434b56aa7dc293419760bf5947565e9f3092d8b2994f1df`.

## Scope

- P31: interpret the user's “数值居中” in context as vertical centering of the remaining plots. Change only the original figure y-coordinate from 135 to 238; x=126, width=1027, height=320, title and academic citation remain unchanged. The deleted table and takeaway stay deleted.
- P34: ENPIRE Limitations, containing the existing resource-idle and token-cost points.
- P35: Toward Recursive Self-Improvement, preserving the policy-improvement loop, retained experience and open validation question. Remove the limitations callouts from this page; shift the remaining body vertically by −40 without changing horizontal alignment.
- P36: unchanged Takeaways, renumbered.
- P37: central text becomes Thanks for listening!, keeping the existing typeface, size and other elements.

Chinese narration is split and synchronized. One minute is added for the dedicated limitations page: 37 slides, 28 clips, suggested 60 minutes without measured rehearsal. No new scientific results or media are introduced.

## Verification

- Fixed baseline: `.build/v0_20_baseline/`, captured from the previous `af875ba3287d3e805baa042bfe4af4bfccf06060acd054ae960f8d3476af0642` delivery.
- 34 tests passed, including exact scope, split-content, media identity, earlier deletion/centering, source pins and table-emphasis regressions.
- Current-hash static and browser checks passed across all 37 slides, all 28 clips' basic play/pause/restart, 46 images, four fonts, navigation, original-figure dialogs, Chinese script and mobile controls. Zero text overflow, unloaded images or mobile-button overflow.
- P31/P34/P35/P37 were rendered and visually inspected. Footer geometry and style remain unchanged. The targeted browser audit binds streamed HTTP bytes and loaded deck-data to the final HTML hash.
- All video metadata and bytes are unchanged. Previous uninterrupted full-clip evidence remains in `.build/v0_19_polish_extended_audit.json` under its original hash; it is not relabeled as a new run.
- Current authorities: `.build/standalone_delivery_audit.json`, `.build/standalone_visual_audit.json`, `.build/v0_20_changed_slides_audit.json`, `.build/v0_20_manifest.json`.

No public release, push, new paper claims, robot experiments or historical PPTX/PDF/ZIP rebuild.
