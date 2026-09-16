# v0.23 — Native SVG Takeaways

Date: 2026-09-16. HTML SHA-256:
`1ad493bd19bb81264f4b7543600ed1124451586af34b424c56ec00d230014507`.

## Design

P36 now begins with one Agent at the far left. A connected branch feeds three aligned
lanes: Control, Data and Improvement. The Control lane redraws the P6/P17 ideas rather
than embedding unreadable full-page screenshots: System 2 → Primitives, semantic/spatial
strengths and fast/contact-rich gaps. Four open questions remain at the right.

The diagram is native inline SVG with no image, foreignObject or script. All 15 diagram
labels use Noto Sans at 24 px; weight and color provide hierarchy. Rounded lane outlines,
consistent connectors and matching row centers replace the previous patchwork. The deck's
existing serif title, logo and citation convention remain separate from the diagram.

Only P36 HTML, its reading guide and footer changed. P35's deletion and all other slide
records remain exact; player sources and video metadata/bytes are unchanged. The two
thumbnail files remain archived but leave the active asset set: 46 images, 28 clips,
37 slides. Chinese narration and the regenerated CJK subset are synchronized.

## Verification

- Fixed baseline: `.build/v0_23_baseline/` from delivered v0.22.
- 43 regressions pass, including exact P36-only scope, source/media/player preservation,
  uniform SVG font declarations, absence of embedded raster content and deleted-text checks.
- The targeted audit binds streaming served hashes and the actual deck-data DOM to the
  artifact. It verifies all 15 computed font sizes/families and pairwise label non-overlap.
- Full-size and reduced-with-script P36 screenshots were visually inspected. Native vector
  text stays sharp, row/column alignment is consistent, and no labels clip or collide.
- Final full-deck browser/static audits cover 37 pages, image loading, 28 clips' basic
  play/pause/restart, figure dialogs, script switching, navigation and mobile controls.

Records: `.build/v0_23_closing_audit.json`, `.build/standalone_delivery_audit.json`,
`.build/standalone_visual_audit.json`, `.build/v0_23_manifest.json`.

Historical thumbnail captures and earlier uninterrupted playback records keep their
original identities. No new scientific claims, external media, historical exports or release.
