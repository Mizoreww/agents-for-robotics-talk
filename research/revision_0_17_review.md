# v0.17 final review — 2026-09-16

Fixed baseline: `.build/revision_0_17_baseline/manifest.json`, verified v0.16, not Git HEAD.

## Standards
No actionable findings. Legacy media adapter preserves original bytes/metadata;
paired layout reuses the player. Kitchen sources, original video, remux and poster
have independent hash pins. Seven focused Data tests independently passed.

## Spec
One P2 found and resolved: the scene-pair introduction originally implied both
cases were already in a simulator. It now says editable 3D scene assets and
separates Office/Newton from Kitchen's still-pending simulation. A regression
requires the precise scope and rejects the old overclaim. Independent follow-up
closed the finding. Six cases, five chapter pages, sources and other chapters
match the request.

Final counts: Standards0; Spec0; no unresolved findings.

## Final verification
-30 regression tests passed;7 focused Data tests rerun after the wording fix.
-32 slides,20 embedded clips,36 images,4 fonts;765 required CJK/special glyphs covered.
- All19 prior clip payloads and all non-Data slide bodies remain unchanged.
- Self-contained static and final-hash browser checks pass: no external runtime
  dependencies, synchronized Chinese narration, no text or button overflow.
- All20 clips pass play/pause/restart. Six Data clips complete uninterrupted playback.
-12 original-figure zoom checks; served HTTP hashes before/after and loaded deck-data
  identity match the delivered file. Updated chapter transitions and mobile controls pass.
- Pair pages and chapter boundaries inspected; final screenshots captured after decoding
  video frames. Original kitchen video was also sampled at0/5/10/15seconds.
- Author X720p video is20.933333seconds after audio removal. Downloaded original with
  original audio is also delivered separately, byte-identical to the source download.
- No browser credential extraction, login bypass, release, push or legacy export.
-51 minutes is suggested timing, not a rehearsal result.

Final HTML SHA-256: `be67550534d0a2f2213ff8b6e0bf2fbc7222db04d16fdc4216a8a24b560bef38`.

## User-approved P21 wording follow-up — current delivery

The final question is now “How can we use it for downstream training?” with
synchronized Chinese narration. Exact deck comparison proves only slide21 differs;
all31 other slide records, all20 media records and all36 image assets are identical.
Seven Data regression tests and full final-hash static/browser/extended playback
audits passed again. P21 screenshot inspected: single line, centered, no overflow.
CJK subset refreshed:764 required glyphs covered. This is a user-approved wording
follow-up to the reviewed revision, not a new structural code review.

Current HTML SHA-256: `38910e30003ab8727c6826e5ec0d7832fed47d626036511329364d6217110a88`.
