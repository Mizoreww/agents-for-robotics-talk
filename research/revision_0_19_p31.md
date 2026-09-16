# P31 table and takeaway removal

2026-09-16. Final HTML SHA-256: `af875ba3287d3e805baa042bfe4af4bfccf06060acd054ae960f8d3476af0642`.

Removed only the native resource table (20 elements) and the bottom takeaway band (2 elements). The original three-panel Figure 7, title, academic footer, font, placement and all other slides remain unchanged. The Chinese narration now refers to the left/middle plots instead of the deleted table.

31 tests passed, including an exact before/after deletion test against `.build/v0_19_p31_before.json`. All media metadata and asset identities are unchanged. Current-hash static, all-slide layout, basic play/pause/restart, navigation, original-figure, script and mobile checks passed. No overflow or unloaded images. P31 was rendered and visually inspected; the citation retains its original size/color/position.

Full uninterrupted playback was not unnecessarily repeated for this text-only change. The previous `.build/v0_19_polish_extended_audit.json` remains evidence for the identical video bytes; it is not relabeled with the new HTML hash. Fresh checks are `.build/standalone_delivery_audit.json`, `.build/standalone_visual_audit.json` and `.build/v0_19_p31_layout_audit.json`.
