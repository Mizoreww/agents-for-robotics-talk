# v0.21 — Docked speaker script

User request: opening Script should reveal a right sidebar and proportionally shrink the
presentation into the remaining left area, without covering it.

## Scope and design
- Preserve all 37 slides, notes, media bytes, original fonts and pale green/gray controls.
- Desktop: a real layout column for a right-hand script panel, with a restrained slide-in
  transition. The 16:9 stage and its toolbar fit the left column at every animation frame.
- The panel has a visible Close button, current/full-script toggle, fixed header and its
  own scrolling content. Slide navigation synchronizes current-slide notes.
- N toggles the panel; Escape closes it (a figure dialog takes precedence). Closing restores
  focus to the script toggle if focus was in the panel. Hidden content is not focusable.
- Fullscreen/focus view retains the split layout. Opening/closing never recreates videos
  or changes their playback state. Reduced-motion preference disables the animation.
- At widths up to 700 px, stack the script below the stage/controls rather than overlaying
  or squeezing either column. No horizontal overflow; script remains independently scrollable.
- Preserve printing of notes. Do not change the content or regenerate historical exports.

## Verification
Fixed comparison: `.build/v0_21_baseline/`, frozen from the delivered v0.20, not Git HEAD.
Check payload identity; desktop/mobile/short landscape and reduced-motion layouts; animation,
rapid toggles, keyboard/focus, scrolling, full-script/slide sync, fullscreen, figure precedence,
and uninterrupted video playback. Rebuild the isolated single HTML, rerun existing browser
checks, and visually inspect open/closed/sidebar screenshots bound to the final HTML hash.
