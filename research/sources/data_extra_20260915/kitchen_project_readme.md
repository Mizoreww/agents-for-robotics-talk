# Lab kitchen twin — interactive 3D reconstruction

A room filmed once with a phone, reconstructed into named 3D assets and shown in the browser:
32 modelled assets with 138 working joints (doors, drawers), a modelled room shell, and a
Compare wipe against the raw metric scan.

Built by video2sim: a phone video goes through a metric scan (ViPE), instance segmentation and
per-asset measurement; GPT-6 Astra then authors every asset in a small Blender modelling language
and an independent verifier session judges each model against the video frames and the scan before
it is accepted.

**This repository is published output, not source.** It holds the generated page, the scene and its
metadata so the reconstruction can be looked at; the pipeline that produced it is maintained in a
private repository and is not published here.

## The files

| file | what it is |
| --- | --- |
| `index.html` | the viewer (three.js from a CDN, no build step) |
| `scene.glb` | the scene: room shell, modelled assets, the decimated scan |
| `viewer_meta.json` | per-asset metrics the page shows (sizes, scores, joints) |
| `.nojekyll` | tells GitHub Pages to serve these files as they are |

## Look at it locally

The page loads `scene.glb` from beside it, so it needs a web server (opening `index.html`
directly through `file://` is blocked by the browser):

```bash
python3 -m http.server 8000    # in this folder
# then open http://localhost:8000
```

## Publish on GitHub Pages

```bash
# in this folder
git init -b main
git add .
git commit -m "Interactive 3D reconstruction of the lab kitchen"
gh repo create kitchen-twin --public --source=. --push        # or: git remote add origin …; git push -u origin main
gh api -X POST repos/:owner/kitchen-twin/pages -f source[branch]=main -f source[path]=/   # or Settings → Pages → main / (root)
```

The site is then at `https://<user>.github.io/kitchen-twin/` (the first build takes a minute).

Two notes for later updates: `scene.glb` is ~15 MB, so use Git LFS (`git lfs track "*.glb"`) if you
will push many versions, and re-run the build with

```bash
python -m video2sim.report.viewer --workspace workspaces/<name> --site <this folder> --site-only \
    --title "…" --static-faces 80000 --asset-faces 3000 --part-faces 2000
```
