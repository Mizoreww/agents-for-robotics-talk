# DexGPT · GIF → Sharpa Wave

An approximate reconstruction of human manipulation from a monocular GIF, retargeted to two **22-DOF Sharpa Wave hands** and evaluated in **MuJoCo** with a passive object hinge.

## Main demo

[![Watch the comparison: source footage, kinematic reference, and contact physics](outputs/comparison_preview.jpg)](https://github.com/Hu-xiao-max/dexgpt/raw/refs/heads/main/outputs/comparison.mp4)

**[▶ Watch the comparison video · 20.3 s](https://github.com/Hu-xiao-max/dexgpt/raw/refs/heads/main/outputs/comparison.mp4)** · [Video file](outputs/comparison.mp4) · [Source GIF](human.gif)

| Left | Center | Right |
| --- | --- | --- |
| Original human demonstration | Kinematic reference with imposed hinge motion | Contact physics with a passive hinge |

The person raises and lowers a hinged toy mixer head with the right hand while the left hand steadies the body. The center panel shows the fitted reference; only the right panel evaluates contact-driven object motion.

> **EXPERIMENTAL — physical validation criteria not met.** Stable integration does not establish physically realistic manipulation.

[Results](#results) · [Features](#features) · [Quick start](#quick-start) · [Outputs](#outputs) · [Limitations](#assumptions-and-limitations)

## Results

Measured over 203 recorded states from the included replay:

| Metric | Result | Development criterion |
| --- | ---: | ---: |
| Passive hinge RMSE | **5.18°** | <10° |
| Maximum hand/object penetration | **5.62 mm** | <5 mm |
| Frames with hand/head contact | **99.5%** | >30% |
| Maximum sampled joint-limit overshoot | **1.34°** | <3° |
| Peak hand/object contact force | **314.7 N** | No acceptance threshold defined |

These checks are for simulation development, not hardware validation. See the [physics report](outputs/physics_report.json), [state audit](outputs/audit.json), and [validation plots](outputs/validation.png) for the measurements. Open [`outputs/index.html`](outputs/index.html) locally for the video and metrics dashboard.

## Features

- **Motion extraction.** MediaPipe hand landmarks with explicit missing-detection masks, interpolation, and temporal smoothing. Detected fractions are 97.0% for the right hand and 100.0% for the left; classifier confidence is not landmark accuracy. Pink-knob segmentation provides a manually anchored, orthographic hinge-angle estimate.
- **Bimanual retargeting.** The real Sharpa Wave meshes and joint models provide 44 finger DOFs in total. Bounded fingertip inverse kinematics (IK) and wrist-pose refinement map the observed hand shape to robot kinematics.
- **Grasp refinement.** Assumed thumb/finger pad contacts guide task-space fitting. The final right-hand grasp uses a four-finger cradle with the thumb retracted by collision-constrained IK, transported around the observed hinge trajectory. The left hand retains landmark IK.
- **Contact simulation.** Dynamic free-root hands use compliant wrist welds and position-controlled fingers, with gravity, collision, friction, joint limits, and upstream joint torque limits active. The rollout uses no object actuator, hand/object weld, hinge pose overwrite, or external hinge force.
- **Inspectable outputs.** Recorded states and controls, contact metrics, source provenance, comparison videos, validation plots, and an interactive replay viewer are included.

## Quick start

### Set up a fresh checkout

```bash
git clone https://github.com/Hu-xiao-max/dexgpt.git
cd dexgpt
python -m venv .venv
.venv/bin/pip install -r requirements.txt
```

The repository includes the fitted grasp seed, final scene, recorded outputs, and third-party assets. Linux headless rendering uses EGL; the interactive viewer requires a GUI display.

### Explore or reproduce the final replay

```bash
# Replay the recorded physics with a movable camera (space pauses).
.venv/bin/python -m dexgpt view-simulation

# Reproduce the final replay from the included fitted grasp seed and scene.
.venv/bin/python -m dexgpt project-grasp
.venv/bin/python -m dexgpt finalize
```

The final replay uses [`outputs/thumb_seed.npz`](outputs/thumb_seed.npz) and the final scene/configuration. `project-grasp` applies an object-clearance projection and tightens joint-limit compliance. Rebuilding the intermediate seed from new data requires grasp fitting and calibration; the seed is archived for exact replay.

<details>
<summary><strong>Recompute tracking or the landmark-only baseline</strong></summary>

If assets are absent, run `.venv/bin/python -m dexgpt setup-assets`, then `.venv/bin/python -m dexgpt extract-motion`. Keep the bundled third-party assets to reproduce the exact model revision; the downloader resolves upstream main when invoked.

Run `.venv/bin/python -m dexgpt run-pipeline` to recompute the landmark-only baseline. This rebuilds the scene with baseline compliance. [`outputs/baseline/`](outputs/baseline/) preserves the first landmark-only run; additional refinement snapshots are retained alongside it for comparison.

</details>

## Project layout

```text
dexgpt/
├── __main__.py           # python -m dexgpt command entry point
├── cli.py                # Command parsing and workflow dispatch
├── paths.py              # Shared repository and output paths
├── assets.py             # Third-party asset download
├── pipeline.py           # Baseline reconstruction workflow
├── motion/               # Landmark extraction and robot retargeting
├── simulation/           # Scene construction, contact rollout, GUI replay
├── refinement/           # Grasp fitting and contact/controller experiments
└── reporting/            # Audits, diagnostics, reports, and README template
tests/                    # CLI and workflow regression checks
outputs/                  # Recorded data, scenes, reports, and videos
third_party/              # Robot meshes, model definitions, and hand landmarker
```

Run commands from the repository root; no package installation is required. All workflows resolve assets and outputs through `dexgpt.paths`.

```bash
.venv/bin/python -m dexgpt --help
.venv/bin/python -m dexgpt run-pipeline --help
.venv/bin/python -m dexgpt audit
.venv/bin/python -m unittest discover -s tests -v
```

The former root scripts are now package modules. Use `python -m dexgpt <command>` with the old script name converted to hyphens and without `.py` (for example, `refine_thumb.py` becomes `refine-thumb`). Edit `dexgpt/reporting/templates/README.md.template` to change the generated README layout.

## Outputs

| Artifact | Contents |
| --- | --- |
| [comparison.mp4](outputs/comparison.mp4) | Main demo: source, kinematic reference, and contact physics |
| [index.html](outputs/index.html) | Local dashboard with videos and metrics |
| [scene.xml](outputs/scene.xml) | Complete MuJoCo scene; keep `third_party/` beside `outputs/` for relative mesh paths |
| [observations.npz](outputs/observations.npz) | Timestamps, 2D/3D landmarks, observed masks, knob observations, and estimated hinge angle; side order is right, left |
| [retargeted.npz](outputs/retargeted.npz) | Timestamped actuator targets in radians, names, and wrist poses in meters with `wxyz` quaternions |
| [physics_rollout.npz](outputs/physics_rollout.npz) | Actual `qpos`, `qvel`, controls, hinge angle, contacts, and forces |
| [tracking.mp4](outputs/tracking.mp4) | Hand tracking overlay: green for detected hands, orange for interpolated hands |
| [physics_report.json](outputs/physics_report.json) · [audit.json](outputs/audit.json) | Measured results and sampled-state checks |
| [contact_refinement.json](outputs/contact_refinement.json) · [physics_configuration.json](outputs/physics_configuration.json) | Grasp objective and model compliance changes |
| [validation.png](outputs/validation.png) | Hinge tracking and penetration plots |

The rollout is sampled every 0.1 s and integrates at 0.001 s. Recorded states span 0–20.2 s; the final video frame is held to 20.3 s. World axes are **x** right in the source image, **y** depth away from the camera, and **z** up.

## Assumptions and limitations

- **Uncalibrated reconstruction.** Scale is assumed at 1.5 mm/pixel, wrist depth is assumed, and MediaPipe supplies monocular relative hand depth. The hinge anchor is picked at image pixel (391, 226). The input has occluded fingers and no camera calibration, measured depth, dimensions, or force observations.
- **Approximate object and support.** The blue/cream/pink toy uses primitive rigid geometry with unmeasured dimensions, mass, friction, and stiffness. Its base is fixed to the table, so the left-hand trajectory does not establish free-object stabilization.
- **Simplified control.** Wrist drives stand in for arms without modeled robot-arm force limits. Contact refinement uses task knowledge inferred from the clip. No hardware control is included.
- **Measured feasibility.** Actual sampled joint-limit overshoot is reported in the audit and physics report; commanded limits alone do not establish feasibility. Recorded force maxima are simulation outputs under the stated assumptions.

<details>
<summary><strong>Interpreting contact, force, and IK diagnostics</strong></summary>

Contact counts count constraint samples across physics substeps, not distinct physical touches. Maximum penetration and force are recorded over substeps after the initial state; `audit.json` also checks sampled states including initialization.

`peak_actuator_force` in the physics report is the pre-joint-limit actuator force; MuJoCo separately applies the model's joint-level `actuatorfrcrange`.

The static IK error report describes the original landmark fit. In `retargeted.npz`, `fingertip_targets` and `ik_error_m` remain the original human-fit diagnostics after contact refinement; see `contact_refinement.json` for the refined grasp objective.

</details>

## Sources and licenses

- **Robot assets:** [MuJoCo Menagerie](https://github.com/google-deepmind/mujoco_menagerie/tree/8161bba264d7fa7c99ca301e91e7fb44737676ad/sharpa_wave), derived from [Sharpa's published hardware descriptions](https://github.com/sharpa-robotics/sharpa-urdf-usd-xml). The upstream license and README are in [`third_party/sharpa_wave/`](third_party/sharpa_wave/). Model revision: `8161bba264d7fa7c99ca301e91e7fb44737676ad`.
- **Hand tracking:** [Google MediaPipe Hand Landmarker](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker). Hand model SHA-256: `fbc2a30080c3c557093b5ddfc334698132eb341044ccee322ccf8bcf3607cde1`.
- **Simulation:** [MuJoCo Python bindings](https://mujoco.readthedocs.io/en/stable/python.html).
- **Input:** [`human.gif`](human.gif), preserved unmodified (203 frames, 20.3 s).
