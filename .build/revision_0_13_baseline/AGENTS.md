# Agents for Robotics

One self-contained HTML technical talk — 38 English slides, Chinese speaker script, 18 embedded clips,
~135 MB — plus its research notes and build scripts. Speaker Zimo Huang, talk date 2026-09-16.

## Build and verify

Never hand-edit `output/Agents_for_Robotics_Self_Contained.html`; it is generated. Edit the sources in
`.build/` and rebuild. Scripts hard-code the project path `/home/limx/Desktop/agent_for_robotics` — update
it if the repo moves. Run from the project root:

```bash
python3 .build/test_evidence_v011.py                          # new source identity and query-time gates
python3 .build/test_table_emphasis.py                          # comparison groups and ties
python3 .build/test_results_v09.py                            # fail-closed source identity regressions
python3 .build/derive_results_v09.py                          # validate pinned sources, derive results
python3 .build/build_selfcontained.py                          # slides, script, HTML, build audit
PYTHONPATH=.build/font_deps python3 .build/build_cjk_font.py   # CJK subset from the just-built script
python3 .build/build_selfcontained.py                          # rebuild to embed the refreshed subset
cp output/Agents_for_Robotics_Self_Contained.html .build/standalone_isolation/index.html
python3 .build/validate_standalone.py --static                 # static assertions only
python3 -m http.server 8765 --bind 127.0.0.1 --directory .build/standalone_isolation &
NODE_PATH=/home/limx/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules \
  /home/limx/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node .build/browser_audit.mjs http://127.0.0.1:8765/
python3 .build/validate_standalone.py                          # full run; binds the audits to the hash
PYTHONPATH=.build/static_render_deps python3 .build/render_static_revision.py   # optional static PDF; not part of this revision
```

The copy into `.build/standalone_isolation/` must precede even `--static`: the validator asserts that
directory holds exactly one byte-identical file. `file://` navigation is blocked by app policy, so the
browser audit runs against loopback (`.claude/launch.json`, entry `deck-isolation`). System `node` is too
old for Playwright — use the bundled modern Node runtime path above. `qa_deps`, `font_deps` and `static_render_deps`
are vendored and excluded from the repo; reinstall with `pip install --target` (fontTools + brotli +
zopfli, WeasyPrint, defusedxml) and `npm i playwright`.

The **main build interpreter also requires Pillow** for original-figure dimensions, not just the
optional PDF renderer. Install it into that interpreter's environment with `python3 -m pip install
Pillow` when pip is available. On this host system Python already provides it; if system pip is
unavailable, the bundled Python at
`/home/limx/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`
includes Pillow and can replace `python3` in the `build_selfcontained.py` invocations. Installing
Pillow only into `static_render_deps` does not satisfy the main builder's dependency.

## Stack

Python 3.12, bundled Node with Playwright driving `/opt/google/chrome/chrome` (needed for H.264 playback),
ffmpeg/ffprobe for clip preparation, Noto Sans / Noto Serif / subset Noto Sans CJK SC. Everything is
base64-embedded in the single HTML; CSP sets `connect-src 'none'`, no runtime network requests.

## Layout and conventions

- `.build/` — production. `build_selfcontained.py` defines slide order, titles and minutes;
  `script_revised.md` is the Chinese-script authority; `standalone_shell.html` / `standalone_player.css` /
  `standalone_player.js` are the page shell; `standalone_*_audit.json` record the last verified state.
- `output/` — deliverables plus `Speaker_Script_Revised.md`. The 22-slide PPTX/PDF/ZIP are history and do
  not match the current page order.
- `research/` — notes, `sources.json`, page snapshots in `sources/`, original figures in `assets/`.
- Slides are English; the script is Chinese, with paper, model and technical terms kept in English.
- Control follows the newly approved sequence: original overview; Hi Robot / Helix / Helix 02 on one
  page; Claude Plays Robotics experiments; one RPent framework page; Astra capability, interface and
  Direct/Hybrid evidence; summary. Data and Improvement each keep one detailed representative:
  Agentic Real2Sim and ENPIRE. Community demos stay within chapters, not extra paper deep dives.
- Community demos from X and 小红书 are qualitative: author-reported, sped up, no trial counts. Never
  present them as measurements.
- Slide titles are at most 40 characters, and the added demo slides keep a sparse layout — both are
  asserted by `validate_standalone.py`.
- Numbers on slides come only from cited evaluations. No cross-paper success-rate leaderboard.

## Status

Version 0.12 (2026-09-15): Control 4–19, Data 20–27, Improvement 28–36, closing 37–38.
38 slides, 18 clips, 60-minute suggested timing. HTML SHA-256 `a37c40df984ba507afcf6fce78443bc9c6c208c1ca9e02218bd7fb3ae0fb202c`.

Current scope: `research/revision_0_12_spec.md`. Fixed comparison is `.build/revision_0_12_baseline/`,
not older Git HEAD. Chapter spine: `output/Chapter_Spine.md`. Overview diagrams open 4/20/28;
three original hierarchy figures share 5; responsibility shift replaces Hi Robot results on 6; report architecture is 15; ENPIRE idea tree is 31.
Results come from `research/results_v0_9.json`, generated by `.build/derive_results_v09.py`.
The independent `research/results_v0_9_sources.json` pins reviewed source identities and is never regenerated by the normal build.
New source authority: `research/evidence_v0_11_sources.json`; loader `.build/evidence_v011.py` rejects byte drift.
Table implementation: `.build/results_slides_v09.py`; per-cell assertions live in the validator.

Hi Robot IA/TP are not episode success. Harness VLA v4 is few-shot, same frozen backend, extra compute.
Astra training recipe is undisclosed. Asim budgets differ. RoboDojo prior/interface/horizon co-vary;
RoboLab contains retained slots/retries and historical first-five baselines, never a fresh paired benchmark.
Real2Sim acceptance is replay-only. ENPIRE physical metrics allow conditional retries; RoboCasa evaluations
run each script once, without reset/retry APIs. Do not combine their denominators or Figure 3/7 times.
Original curves retain uncertainty; no estimated RoboCasa bar values. Community demos remain qualitative.

Use `.build/standalone_delivery_audit.json`, `.build/standalone_visual_audit.json` and
`.build/v0_12_extended_audit.json` for actual hash-bound status. v0.12 final QA/review passed with 0 unresolved findings; see `research/revision_0_12_review.md`. Prior v0.9 source-freeze P2 remains resolved.
No measured rehearsal duration, new GitHub release, push, or PPTX/PDF/ZIP regeneration.


<claude-mem-context>
# Memory Context

# [agent_for_robotics] recent context, 2026-09-14 6:23pm GMT+8

No previous sessions found.
</claude-mem-context>
Slide 19 now uses our independently grounded diagnostic synthesis, approved by the user. The WeChat article itself remains safety-blocked and unread; do not bypass it or attribute this synthesis to it. Await supplied article text/figures for article-specific claims.

Current presentation polish: merged learned tools on 4; one LLM and aligned interfaces on 7; capability summary on 19; Takeaways on 37 and Thank You on 38. Native table emphasis is tested per cell; resources and retained slots are descriptive, not an overall winner.

Data now includes Real-to-sim Replay / Data Rollout and the hand CAD case (26). DexGPT original comparison (27) is a failed physical-acceptance example, not a new detailed study. Control timing (18) separates Asim published query seconds from controller Hz and Go1 simulation-time feedback.
