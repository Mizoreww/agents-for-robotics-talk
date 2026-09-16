# v0.23 — A coherent SVG recap

User correction: P36 looks ugly; add Agent at the far left, use pure SVG, and make
font sizes consistent. Preserve the already requested research questions.

- One Agent branches into Control / Data / Improvement.
- Replace the two raster thumbnails with a concise vector synthesis of P6/P17:
  System 2 → action primitives; semantic/spatial strengths vs fast/contact-rich gaps.
- Control ends at Latency? / Better interface?; Data at Sim2Real?; Improvement at Efficiency?.
- All diagram text uses Noto Sans at 24 px. Use weight/color, not competing sizes, for
  hierarchy. Retain the deck's 36 px serif title and existing logo/footer convention.
- Use native inline SVG paths, nodes and text, not images or foreignObject. No new player
  behavior. Keep P35 deletion, all other slides, video payloads and docked Script unchanged.
- Update the P36 Chinese reading guide and footer; remove obsolete thumbnail instructions.

Fixed baseline: `.build/v0_23_baseline/`. Verify exact P36-only record scope, SVG text/font
and geometry, absence of raster thumbnails, preserved player/media, updated narration,
whole-deck regressions and current-hash visual checks at full and sidebar-reduced sizes.
