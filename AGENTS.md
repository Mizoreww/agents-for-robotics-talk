# Agents for Robotics

One self-contained HTML technical talk — 37 English slides, Chinese speaker script, 28 embedded clips,
~138 MB — plus its research notes and build scripts. Speaker Zimo Huang, talk date 2026-09-16.

## Build and verify

Never hand-edit `output/Agents_for_Robotics_Self_Contained.html`; it is generated. Edit the sources in
`.build/` and rebuild. Scripts hard-code the project path `/home/limx/Desktop/agent_for_robotics` — update
it if the repo moves. Run from the project root:

```bash
python3 .build/test_report_figures_v013.py                     # original report images and quantitative lineage
python3 .build/test_v014.py                                  # code replay identity and interface highlight
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
  page; responsibility-shift diagram; then Astra capability, interface and
  Direct/Hybrid evidence; summary. Data is demo-only: Office scene, articulated kitchen, tendon-hand CAD,
  rope-driven hand reconstruction, multi-view replay and DexGPT rollout, all discovered through Awesome-Astra. No Agentic Real2Sim paper pages.
  Improvement deep-dives ENPIRE with official media and a scoped RSI synthesis; no CAD/RL or unrelated ICL clip. P9 adds Cube and Claw simulation demos.
- Community demos from X and 小红书 are qualitative: author-reported, sped up, no trial counts. Never
  present them as measurements.
- Slide titles are at most 40 characters, and the added demo slides keep a sparse layout — both are
  asserted by `validate_standalone.py`.
- Numbers on slides come only from cited evaluations. No cross-paper success-rate leaderboard.

## Status

Version 0.23 (2026-09-16): Control 4–17, Data 18–22, Improvement 23–35, closing 36–37.
37 slides, 28 clips, 60-minute suggested timing. HTML SHA-256 `1ad493bd19bb81264f4b7543600ed1124451586af34b424c56ec00d230014507`.

Base scope: `research/revision_0_19_spec.md`; current scope: `research/revision_0_20.md`. Fixed comparison is `.build/revision_0_19_baseline/`,
not older Git HEAD. Chapter spine: `output/Chapter_Spine.md`. Overview diagrams open 4/18/23;
three original hierarchy figures share 5; responsibility shift replaces Hi Robot results on 6; report architecture is 12; original results are 13–15; ENPIRE idea tree is 28.
Results come from `research/results_v0_9.json`, generated by `.build/derive_results_v09.py`.
The independent `research/results_v0_9_sources.json` pins reviewed source identities and is never regenerated by the normal build.
New source authority: `research/evidence_v0_11_sources.json`; loader `.build/evidence_v011.py` rejects byte drift.
Original report captures are pinned by `research/report_figures_v0_13_sources.json`; loader `.build/report_figures_v013.py` verifies images and query data. Heatmap export expands original DOM overflow only.
Code replay authority: `research/code_video_v0_14_sources.json`, checked by `.build/code_video_v014.py`. v0.15 removed ar2s_real/ar2s_sim and added DexGPT. v0.16 added rope_hand; v0.17 adds kitchen and pairs the Data chapter. All existing clip bytes remain unchanged.
RoboDojo public baselines are reweighted published references, not paired reruns; native Score denominators are 48/50.
Table implementation: `.build/results_slides_v09.py`; per-cell assertions live in the validator.

Claude/RPent pages are removed from the active talk. Historical evidence remains archived.
Astra training recipe is undisclosed. Asim budgets differ. RoboDojo prior/interface/horizon co-vary;
RoboLab contains retained slots/retries and historical first-five baselines, never a fresh paired benchmark.
Data demos do not establish downstream training benefit. DexGPT physical validation is not met. ENPIRE physical metrics allow conditional retries; RoboCasa evaluations
run each script once, without reset/retry APIs. Do not combine their denominators or Figure 3/7 times.
Original curves retain uncertainty; no estimated RoboCasa bar values. Community demos remain qualitative.

Use `.build/standalone_delivery_audit.json`, `.build/standalone_visual_audit.json` and
`.build/v0_20_changed_slides_audit.json` for current status. P31 keeps the cleaned original figure and centers it vertically only; P34 is Limitations, P35 is Toward Recursive Self-Improvement, P36 is Takeaways, and P37 says Thanks for listening! See `research/revision_0_20.md`. Previous full-clip playback is retained in `.build/v0_19_polish_extended_audit.json`, and exact media preservation is asserted by `.build/test_p31_cleanup.py`. User-approved follow-up order: system 24, evaluation/reset 25–26, policy improvement 27–28, coding-agent results 29, fleet/cost 30–31, simulation 32, learned-policy demos 33, limitations 34 and recursive improvement 35. ENPIRE footers now use academic author/title/arXiv/year citations. The previous content review passed with 0 unresolved findings; this narrow follow-up has separate verification in `research/revision_0_19_polish.md` (final-hash QA passed).
No measured rehearsal duration or PPTX/PDF/ZIP regeneration. User authorized GitHub publication of v0.23 on 2026-09-16; retain the existing Private visibility and publish the >100 MB HTML as a Release asset, not a Git blob.


<claude-mem-context>
# Memory Context

# [agent_for_robotics] recent context, 2026-09-14 6:23pm GMT+8

No previous sessions found.
</claude-mem-context>
Slide 17 now uses our independently grounded diagnostic synthesis, approved by the user. The WeChat article itself remains safety-blocked and unread; do not bypass it or attribute this synthesis to it. Await supplied article text/figures for article-specific claims.

Current presentation polish: merged learned tools on 4; Astra begins on 7; capability summary on 17; Takeaways on 35 and Thank You on 36. Native table emphasis is tested per cell; resources and retained slots are descriptive, not an overall winner.

Data pairs six demos: Office + kitchen (19), hand CAD + rope-hand (20), multi-view replay + DexGPT rollout (21), opening (18) and summary (22). Control timing (16) separates Asim published query seconds from controller Hz and Go1 simulation-time feedback.

P16 is now latency-only (ASIM); P17 has four authored inline SVG icons and two open problems. Page-number typos in user edits are resolved by the exact quoted text. P11 Waypoint proprio is a highlighted column, not a universal winner; Can delta18/20 exceeds waypoint17/20. Current polish/build scope is v0.23 (P36 native SVG redesign; docked-script UI remains v0.21).

Data demo provenance: `research/data_demos_v0_15_sources.json`; `.build/data_demos_v015.py` fails closed on byte drift. Run `.build/test_data_demos_v015.py` after rebuilding to verify Data demo-only scope. `.build/test_enpire_v018.py` owns the current cross-chapter preservation checks.

Case22/23 authority: `research/data_extra_v0_16_sources.json`; same loader checks both source manifests. Kitchen now uses the complete author-posted X video, pinned by `research/kitchen_v0_17_sources.json`; LinkedIn confirms human-in-the-loop modelling and simulation still being added. The original Rednote browser tool was unavailable; no login bypass was used. Rope video is the original10 Sep24.67-second clip, not the12 Sep follow-up.

ENPIRE source pins: `research/enpire_v0_18_sources.json` (seven original clips) and `research/enpire_v0_19_sources.json` (three added reset clips); P9 puzzle pins: `research/puzzle_v0_18_sources.json`. Loaders: `.build/enpire_v018.py` and `.build/enpire_order_v019.py`. Regressions: `.build/test_enpire_v018.py`, `.build/test_enpire_order_v019.py`, and `.build/test_enpire_polish.py` (academic citations, late demos and exact body/media preservation). The deck has 28 clips, including 10 ENPIRE official clips. Extended QA plays all 10 ENPIRE clips plus both puzzles to completion (12 clips). RSI remains a scoped discussion, not a demonstrated self-updating foundation model.

Current exact-scope regression: `.build/test_v020.py` asserts P31 y-only movement, the single added Limitations page, the closing text, unchanged media and all other slide objects.

Current UI revision v0.21: right-hand docked speaker script; stage scales into the remaining column without covering slides or resetting video playback. Fullscreen retains docking; <=700px uses a stacked reader with a 360px minimum panel height. Spec: `research/revision_0_21_spec.md`. Test `.build/test_sidebar_v021.py` and run `.build/audit_sidebar_v021.mjs` with the bundled Node in addition to existing audits. Baseline: `.build/v0_21_baseline/`; content and media are byte-identical to v0.20.

Current closing revision v0.22: P36 uses exact P6/P17 thumbnails followed by Latency? / Better interface?, Data → Sim2Real?, Improvement → Efficiency?. P35 deletes only the Open test line. Baseline `.build/v0_22_baseline/`; exact regression `.build/test_takeaways_v022.py`; visual audit `.build/audit_takeaways_v022.mjs`. 37 slides, 28 videos, 48 embedded images. Historical scope tests explicitly delegate these two later changes to the v0.22 regression.

Current v0.23: P36 diagram source is `.build/takeaways_v023.svg`, embedded inline (no foreignObject or raster thumbnails); 24px Noto Sans throughout the diagram, with deck title/footer conventions unchanged. Agent branches to three role lanes; four open questions remain. Current assets: 46 images / 28 video clips. Run `.build/test_takeaways_v023.py` and `.build/audit_takeaways_v023.mjs`; baseline `.build/v0_23_baseline/`. P35 and all other slide records remain identical to v0.22.
