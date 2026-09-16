# v0.22 — Concrete closing questions

User requests:
- P36: remove “Different artifacts. Different tests.” and “Re-test the division of
  work as models improve.” Replace the old artifact/evidence table with three paths.
- Control → thumbnails of the actual P6 and P17 → open problems: Latency? / Better interface?
- Data → Sim2Real?; Improvement → Efficiency?. Keep the page sparse and polished.
- P35: delete only “Open test: held-out tasks, matched budgets, no regression”.

Implementation: preserve the original Noto fonts/palette and 37-slide order. Use faithful,
click-to-enlarge captures for the two thumbnails; do not invent replacement conclusions.
Only P35 HTML and P36 content/narration/citation may change; retain all video bytes and
metadata, other slides and the v0.21 docked-script UI. Update the Chinese P36 narration.
No research, extra slides or historical export regeneration is needed.

Verify exact scope against `.build/v0_22_baseline/`, thumbnail source identities, deleted
text, sparse text, all existing source/data regressions, P35/P36 screenshots and thumbnail
enlargement. Rebuild CJK subset for the new script; verify final HTML in isolation.
