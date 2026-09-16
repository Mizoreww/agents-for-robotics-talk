# Agents for Robotics

One self-contained HTML technical talk — 28 English slides, Chinese speaker script, 18 embedded clips,
~132 MB — plus its research notes and build scripts. Speaker Zimo Huang, talk date 2026-09-16.

## Build and verify

Never hand-edit `output/Agents_for_Robotics_Self_Contained.html`; it is generated. Edit the sources in
`.build/` and rebuild. Scripts hard-code the project path `/home/limx/Desktop/agent_for_robotics` — update
it if the repo moves. Run from the project root:

```bash
python3 .build/build_selfcontained.py                          # slides, script, HTML, build audit
PYTHONPATH=.build/font_deps python3 .build/build_cjk_font.py   # CJK subset from the just-built script
python3 .build/build_selfcontained.py                          # rebuild to embed the refreshed subset
cp output/Agents_for_Robotics_Self_Contained.html .build/standalone_isolation/index.html
python3 .build/validate_standalone.py --static                 # static assertions only
python3 -m http.server 8765 --bind 127.0.0.1 --directory .build/standalone_isolation &
NODE_PATH=/home/limx/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules \
  /home/limx/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node .build/browser_audit.mjs http://127.0.0.1:8765/
python3 .build/validate_standalone.py                          # full run; binds the audits to the hash
PYTHONPATH=.build/static_render_deps python3 .build/render_static_revision.py   # optional 28-page PDF
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
  Direct/Hybrid evidence; summary. Simulation and Improvement each keep one detailed representative:
  Agentic Real2Sim and ENPIRE. Community demos stay within chapters, not extra paper deep dives.
- Community demos from X and 小红书 are qualitative: author-reported, sped up, no trial counts. Never
  present them as measurements.
- Slide titles are at most 40 characters, and the added demo slides keep a sparse layout — both are
  asserted by `validate_standalone.py`.
- Numbers on slides come only from cited evaluations. No cross-paper success-rate leaderboard.

## Status

Version 0.8 (2026-09-14): Control 4–13, Simulation 14–19, Improvement 20–26, closing 27–28.
28 slides, 18 clips, 60-minute suggested timing. HTML SHA-256 `01505a9c7b51801eb5593b8113fcd3a3b21ca05053e2c79122977d08b9b3b868`.

Current scope: `research/revision_0_8_spec.md`; it supersedes v0.7's brief-background restriction.
Chapter spine: `output/Chapter_Spine.md`. The original Agent/action/tools diagram opens slide 4;
three prior-talk hierarchy figures share slide 5. Anonymous report architecture is slide 12.
Astra internal network/training is undisclosed. Asim budgets are unequal; RoboDojo prior/interface/
horizon change together; RoboLab slots are not pooled. Real2Sim replay acceptance is not predictive
validity. ENPIRE setup, conditional retries and costs stay explicit; the idea tree is not a causal
ablation. Training, code revision and ICL are distinct; no proven recursive-enhancement claim.
Use `.build/standalone_delivery_audit.json` and `.build/standalone_visual_audit.json` for actual
hash-bound verification status, not a past version's green result.

Final v0.8 static/browser/visual QA passed; next rehearse before 2026-09-16. Duration is not measured. This revision
is local, not a new GitHub release. Fixed review baseline: `.build/revision_0_8_baseline/`, not Git HEAD.
