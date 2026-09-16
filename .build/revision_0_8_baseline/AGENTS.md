# Agents for Robotics

One self-contained HTML technical talk — 21 English slides, Chinese speaker script, 9 embedded clips,
~100 MB — plus its research notes and build scripts. Speaker Zimo Huang, talk date 2026-09-16.

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
PYTHONPATH=.build/static_render_deps python3 .build/render_static_revision.py   # optional 21-page PDF
```

The copy into `.build/standalone_isolation/` must precede even `--static`: the validator asserts that
directory holds exactly one byte-identical file. `file://` navigation is blocked by app policy, so the
browser audit runs against loopback (`.claude/launch.json`, entry `deck-isolation`). System `node` is too
old for Playwright — use the bundled modern Node runtime path above. `qa_deps`, `font_deps` and `static_render_deps`
are vendored and excluded from the repo; reinstall with `pip install --target` (fontTools + brotli +
zopfli, WeasyPrint, defusedxml) and `npm i playwright`.

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
- Exactly one representative per chapter: the anonymous Direct/Hybrid report, Agentic Real2Sim, ENPIRE.
  Claude Plays Robotics and RPent appear only on the brief Control background page. Other previous
  supporting studies remain research history, not extra case studies in the current talk.
- Community demos from X and 小红书 are qualitative: author-reported, sped up, no trial counts. Never
  present them as measurements.
- Slide titles are at most 40 characters, and the added demo slides keep a sparse layout — both are
  asserted by `validate_standalone.py`.
- Numbers on slides come only from cited evaluations. No cross-paper success-rate leaderboard.

## Status

Version 0.7 (2026-09-14): Control 4–8, Data 9–13, Improvement 14–19, closing 20–21.
21 slides, 9 clips, 60-minute suggested timing. HTML SHA-256 `cccec9692b6470391539624e016cce0ee7860c3b0f4ebb8c3b0b8ac315cbd602`.

Current scope: `research/revision_0_7_spec.md`; it supersedes the v0.6 28-slide plan.
Chapter spine: `output/Chapter_Spine.md`. The original Direct/Hybrid diagram opens slide 4;
Astra internal network/training is not disclosed. RoboDojo prior/interface/segment length change
together; RoboLab final slots are not pooled. Real2Sim replay acceptance is not predictive validity;
ENPIRE setup, conditional retries and costs remain explicit. No claim of proven recursive enhancement.
Use `.build/standalone_delivery_audit.json` for the actual hash-bound validation status.

Next: rehearse before 2026-09-16; duration is not measured. This revision is local, not a new GitHub release.

<claude-mem-context>
# Memory Context

# [agent_for_robotics] recent context, 2026-09-14 2:51pm GMT+8

No previous sessions found.
</claude-mem-context>