# GPT Dog Eval

Headless evaluation of arbitrary policies on the Unitree Go1 velocity-tracking
task from Google DeepMind's MuJoCo Playground. The simulator owns the physics,
observations, reward terms, and termination logic used by the upstream trainer.
This package only adapts that environment to Inspect Robots and records the
trainer's individual reward and cost terms.

The project includes deterministic and ONNX baselines plus a bounded
`joint-chunk` agent loop. The agent can use an OpenAI-compatible Responses
endpoint, an in-process fake provider, or a provider registered by Python code.

See the [experiment journal](docs/experiment-journal.md) for all historical runs,
review corrections, action-feedback v2 verification, and planned comparisons.

## Setup

The target machine does not need a GPU. `uv` installs Python 3.12 and a CPU JAX
runtime into the project environment.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
cd ~/gpt-dog-eval
~/.local/bin/uv sync --extra dev
```

The first environment reset downloads the MuJoCo Menagerie assets pinned by
MuJoCo Playground and compiles the MJX step function for CPU. That first reset
is much slower than later steps.

## Run

List the registered components:

```bash
uv run inspect-robots list
```

Run a 50-step headless smoke test with a zero-action policy:

```bash
JAX_PLATFORM_NAME=cpu uv run inspect-robots run \
  --task go1-velocity-smoke -T steps=50 -T scenes=stand \
  --policy go1-zero --embodiment go1-playground --no-prompt
```

Run the upstream pretrained ONNX locomotion policy on all four commands:

```bash
JAX_PLATFORM_NAME=cpu uv run inspect-robots run \
  --task go1-velocity-smoke -T steps=250 \
  --policy go1-onnx --embodiment go1-playground --no-prompt --disable-guardrails
```

Each step records the exact weighted trainer terms plus their unscaled values
under `StepResult.info["trainer"]`. Task scorers report episode return, survival,
tracking rewards, and the main regularization costs.

## Joint-chunk agent

Copy `secret.example.toml` to the ignored `secret.toml` and fill in the usual
endpoint settings:

```toml
[inference]
provider = "responses"
base_url = "https://api.openai.com/v1"
api_key = "replace-me"
model = "gpt-6-astra"
reasoning_effort = "medium"
timeout_s = 120.0
```

The API key can instead come from `GPT_DOG_API_KEY`. Do not pass a real key on
the command line because shells and process listings may retain it.

The model calls `run_joint_chunk`, `hold`, or `give_up`. A joint chunk has at
most four keyframes and 15 simulator steps (300 ms). The compiler interpolates
from the last action, rejects values outside `[-1, 1]`, and rejects changes
larger than `0.1` per 20 ms control step. Interpolation, hold, and stop use the
actual post-guardrail `last_applied_action`. Chunk receipts retain requested and
executed step counts, the actual final target, and modified steps/joints,
including when the final chunk is interrupted or the trial errors. The simulator
is paused during model inference, so API latency affects wall time but not robot dynamics.

```bash
JAX_PLATFORM_NAME=cpu uv run inspect-robots run \
  --task go1-velocity-smoke -T steps=250 \
  --policy go1-joint-chunk --embodiment go1-playground --no-prompt
```

The model receives the upstream policy's 48-value proprioceptive observation
plus its actual applied action and execution receipts. The original actor
vector remains unchanged for ONNX; its action-history slice is one control step
older than the most recently applied target. No contact or foot-position sensors
are added. Trainer reward and cost terms remain hidden from the agent.

### Free end-to-end tests

Explicitly select the deterministic fake provider to emit standing chunks
without inference network calls, regardless of the provider in `secret.toml`:

```bash
JAX_PLATFORM_NAME=cpu uv run inspect-robots run \
  --task go1-velocity-smoke -T steps=20 -T scenes=stand \
  -P provider=fake -P episode_steps=20 \
  --policy go1-joint-chunk --embodiment go1-playground --no-prompt
```

To exercise the complete HTTP path with the same `base_url` and `api_key`
format as a real endpoint, start the included fake Responses server:

```bash
uv run gpt-dog-fake-server --api-key fake-local-key
```

Then set `provider = "responses"`, `base_url =
"http://127.0.0.1:8765/v1"`, and `api_key = "fake-local-key"` in
`secret.toml` before running the same evaluation.

Python integrations can implement the small `InferenceProvider` protocol and
install it with `register_inference_provider(name, factory)`.

## Proprioception

Proprioception, or robot "body sense", is information measured from the robot
itself rather than from cameras: body linear velocity, gyroscope readings,
gravity direction in the body frame, joint positions, joint velocities, and
the previous motor command. In this benchmark the command vector is appended
to those measurements, producing the exact 48-value observation used by the
upstream locomotion policy.

## Components

- `go1-playground`: `Go1JoystickFlatTerrain`, CPU MJX, no window or rendering.
- `go1-zero`: emits twelve zeros, which requests the nominal standing pose.
- `go1-onnx`: upstream pretrained Go1 locomotion policy, CPU ONNX Runtime.
- `go1-joint-chunk`: tool-calling inference agent with bounded action chunks.
- `go1-velocity-smoke`: stand, forward, lateral, and left-turn commands.

Actions are normalized joint-position residuals in this order:

```text
FR_hip FR_thigh FR_calf FL_hip FL_thigh FL_calf
RR_hip RR_thigh RR_calf RL_hip RL_thigh RL_calf
```

MuJoCo Playground converts each value `a` to
`nominal_joint_angle + 0.5 * a` radians before its PD controller.
