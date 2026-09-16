# v0.21 — Right-hand speaker script

Date: 2026-09-16. HTML SHA-256:
`085ddbf4a6519f1335fa5d54b50b7cd3c22815d35053b550028861eaa4831abe`.

## Changes

Speaker script now docks on the right in a real layout column. The presentation
and toolbar fit the remaining left region; the stage preserves its 16:9 aspect
ratio. The script panel has a stationary header, an independently scrolling reader,
current/full-script switch and Close button. N toggles; Escape closes. The sidebar
is not modal and never recreates videos or pauses playback.

Fullscreen retains the split. At <=700px, the reader stacks below the presentation
and has a minimum 360px panel height for short landscapes. Reduced-motion preferences
disable transitions. Existing note printing remains supported.

All 37 slides, Chinese notes, fonts, images, video metadata and 28 payloads are unchanged
from v0.20. No revised scientific claims, new media, historical exports or release.

## Verification

- Fixed baseline: `.build/v0_21_baseline/`.
- 36 Python regressions passed, including exact deck-data/payload identity and new UI structure.
- Final-hash full-deck browser audit: all 37 slides, 46 images, 28 basic clip play/pause/restart
  checks, navigation, figure dialogs, current/full script, fullscreen and mobile controls passed.
- Sidebar audit binds streaming HTTP hashes before/after browser load and the actual loaded
  deck-data DOM hash. It checks animated non-overlap, proportional sizing, independent scrolling,
  stationary header, slide synchronization, rapid reversals, focus, Escape/N/Close, figure precedence,
  live video element/playhead continuity, fullscreen, print and reduced-motion behavior.
- Viewports: 1600×1000, 1280×800, 1024×768, 820×430, 701×500, 390×844 and 568×320.
- Standards and Spec independent rechecks: zero residual findings. Initial short-landscape
  reading-height and selector-focused Escape defects were repaired before final delivery.
- Existing uninterrupted full-clip evidence remains historical under the original v0.19 hash.
  It was not relabeled as a new playback run.

Records: `.build/standalone_delivery_audit.json`, `.build/standalone_visual_audit.json`,
`.build/v0_21_sidebar_audit.json`, `.build/v0_21_manifest.json`,
`research/revision_0_21_review.md`.
