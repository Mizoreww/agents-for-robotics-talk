# v0.19 follow-up: academic citations and late demos

Date: 2026-09-16. Final HTML SHA-256: `accf9c71db3afd0c4a2da64cf140bbeedffa485e889619c89056e472aaea1428`.

## Requested delta

- ENPIRE P23–34 gray footers use W. Xiao et al., the full paper title, arXiv:2606.19980, year 2026, and the relevant figure/section or project-website attribution. First author and title were checked against the pinned paper HTML. Adapted schematics and the talk's RSI discussion remain labeled.
- Original P24 learned-policy demos move to P33, after all quantitative results and before Limitations/RSI. System is now P24; Auto Evaluation/Reset P25–26; Policy Improvement P27–28; Coding Agents P29; Fleet/Cost P30–31; RoboCasa P32.
- Two Chinese narration transitions change to reflect this order. Page timing follows the moved slide. Overall timing remains an unmeasured suggestion of 59 minutes.
- All slide bodies, figure/video bytes, source URLs and media settings are unchanged. P1–22 and P35–36 remain intact. P23 keeps all prior text deletions and vertical-only positioning, with only its footer citation changed.

## Verification

The fixed follow-up baseline is `.build/v0_19_polish_baseline/`, captured from the delivered HTML `eb8011c95baa5e41b9f9fd1f09c35e611721c9d4c87fdf7793d2656d30972749`.

- 30 tests passed: 3 exact polish-scope tests plus the previous 27 source/order/preservation/emphasis/Data tests. The new tests failed on the old delivery before rebuilding and passed afterward.
- All 36 slides, 28 clips, 46 images and 4 fonts passed static and current-hash browser checks. Zero external runtime resources, unloaded images, desktop overflow or mobile-button overflow. Standalone and embedded Chinese narration match.
- All 28 clips passed play/pause/restart. Twelve chapter/puzzle clips played fully to completion in the final HTML without decoding errors.
- All 12 academic footers fit at their unchanged 11px font, gray color, x/y position and width. The dedicated audit binds served bytes and loaded deck-data to the delivered hash.
- P24, P27, P33 and P34 screenshots were visually inspected. The unchanged slide-body regression covers all remaining pages, and all pages have final-hash screenshots.
- The earlier independent Standards/Spec content review remains recorded in `research/revision_0_19_review.md`. This citation/order-only follow-up is verified separately by the scoped regressions and browser/visual audits above; it is not a new scientific review or reproduction.

## Current records

`.build/standalone_delivery_audit.json`, `.build/standalone_visual_audit.json`, `.build/v0_19_citation_layout_audit.json`, `.build/v0_19_polish_extended_audit.json`, and `.build/v0_19_polish_manifest.json` describe this delivered hash. Old v0.19 manifests retain the pre-follow-up version as historical evidence.
