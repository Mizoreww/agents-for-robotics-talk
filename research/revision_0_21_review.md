# v0.21 — Standards / Spec review

Comparison: `.build/v0_21_baseline/` (delivered v0.20), against the three player
source files and the added Python/browser regressions. Not historical Git HEAD.
Two independent Codex reviewers followed the Matt Pocock `code-review` workflow.

## Standards

Initial P2: at 568×320, the mobile panel's 56dvh height left only a 29px reading
viewport below the fixed header. Fixed with a 360px minimum stacked-panel height.
Independent recheck at 568×320, 700×320 and 667×375 confirmed a 210px scrolling
viewport / 186px inner reading area for current and full script, without overflow.

**Residual findings: 0.**

## Spec

Initial findings: the same short-landscape defect; Escape did not close the sidebar
when the closed slide selector had focus. Escape now precedes the select/input key
guard, while the figure dialog retains precedence. Outside focus remains on the selector.
Both cases now have browser regressions. Independent served-artifact recheck passed.
Slide, script and media identity checks passed against v0.20.

**Residual findings: 0.**

No scope/content changes were requested by either reviewer. Final UI source is
bound by `.build/v0_21_manifest.json`; final browser evidence is
`.build/v0_21_sidebar_audit.json`.
