"""Inference-time joint-chunk agent policy for the Unitree Go1."""

from __future__ import annotations

import copy
import json
import time
from dataclasses import dataclass
from typing import Any

import numpy as np
from inspect_robots import Action, ActionChunk, Observation, PolicyConfig, PolicyInfo, Scene

from gpt_dog_eval.constants import ACTION_SPACE, AGENT_OBSERVATION_SPACE, JOINT_LABELS
from gpt_dog_eval.inference import (
    InferenceProvider,
    InferenceRequest,
    ToolCall,
    create_inference_provider,
    resolve_inference_config,
)
from gpt_dog_eval.robot_spec import robot_spec_context, robot_spec_sha256

_SYSTEM_PROMPT = """You are the inference-time control policy for a simulated Unitree Go1.
There is no training and no parameter update. Control the robot only through the provided tools.

The simulator pauses while you think. Each action advances physics at 50 Hz. The task lasts for
the stated horizon unless the robot falls. Actions are normalized residual joint targets in this
fixed order: FR_hip, FR_thigh, FR_calf, FL_hip, FL_thigh, FL_calf, RR_hip, RR_thigh, RR_calf,
RL_hip, RL_thigh, RL_calf. The simulator maps each action a to nominal_joint_angle + 0.5*a
radians through its PD controller. Every value must be finite and inside [-1, 1].

Maintain balance while tracking the commanded [forward, left, yaw] velocity. Prefer short,
smooth chunks and reassess the body velocity, gravity direction, joint motion, and prior action
after each chunk. Trainer rewards and costs are hidden from you. Do not claim success: the
evaluator scores the complete trajectory. Call exactly one tool per turn."""

_SYSTEM_PROMPT += """

last_applied_action is the normalized target actually sent to the simulator after guardrails.
Use it as the start of each chunk and for hold. actor_previous_action is the unchanged upstream
actor observation, one control step older; do not use it as the current target. Tool results
report execution counts, the actual final target, and any modified steps/joints. Completed
means the requested number of steps ran, not that every proposed target was applied unchanged."""


class ToolValidationError(ValueError):
    """A provider emitted a syntactically valid but unsafe tool call."""


@dataclass(frozen=True)
class _PendingMotion:
    call_id: str
    tool_name: str
    requested_steps: int
    start_step: int
    actions: np.ndarray


class JointChunkAgentPolicy:
    """Ask a pluggable inference provider for bounded Go1 joint trajectories."""

    def __init__(
        self,
        *,
        config_path: str | None = "secret.toml",
        provider: str | None = None,
        base_url: str | None = None,
        api_key: str | None = None,
        model: str | None = None,
        reasoning_effort: str | None = None,
        timeout_s: float | None = None,
        max_llm_calls: int = 60,
        max_chunk_steps: int = 15,
        max_keyframes: int = 4,
        max_action_delta: float = 0.1,
        episode_steps: int = 250,
        inference_provider: InferenceProvider | None = None,
        robot_spec: dict[str, Any] | None = None,
    ) -> None:
        if max_llm_calls < 1:
            raise ValueError("max_llm_calls must be >= 1")
        if max_chunk_steps < 1:
            raise ValueError("max_chunk_steps must be >= 1")
        if max_keyframes < 1:
            raise ValueError("max_keyframes must be >= 1")
        if not 0 < max_action_delta <= 2:
            raise ValueError("max_action_delta must be in (0, 2]")
        if episode_steps < 1:
            raise ValueError("episode_steps must be >= 1")

        self.inference_config = resolve_inference_config(
            config_path=config_path,
            provider=provider,
            base_url=base_url,
            api_key=api_key,
            model=model,
            reasoning_effort=reasoning_effort,
            timeout_s=timeout_s,
        )
        self._provider = inference_provider or create_inference_provider(self.inference_config)
        self._max_llm_calls = max_llm_calls
        self._max_chunk_steps = max_chunk_steps
        self._max_keyframes = max_keyframes
        self._max_action_delta = max_action_delta
        self._episode_steps = episode_steps
        self._robot_spec = copy.deepcopy(robot_spec)
        self._instructions = _SYSTEM_PROMPT
        if self._robot_spec is not None:
            self._instructions += robot_spec_context(self._robot_spec)
        self.info = PolicyInfo(
            name="go1-joint-chunk",
            action_space=ACTION_SPACE,
            observation_space=AGENT_OBSERVATION_SPACE,
            control_hz=50.0,
        )
        self.config = PolicyConfig(action_horizon=max_chunk_steps, replan_interval=None)
        self._tools = _tool_schemas(max_chunk_steps, max_keyframes)
        self._history: list[dict[str, Any]] = []
        self._transcript: list[dict[str, Any]] = []
        self._pending: _PendingMotion | None = None
        self._chunk_executions: list[dict[str, Any]] = []
        self._calls_used = 0
        self._usage: dict[str, int] = {}
        self._goal = ""

    def reset(self, scene: Scene) -> None:
        self._goal = scene.instruction
        self._history = [{"role": "user", "content": f"Goal: {scene.instruction}"}]
        self._transcript = [
            {"role": "system", "content": self._instructions},
            {"role": "user", "content": f"Goal: {scene.instruction}"},
        ]
        self._pending = None
        self._chunk_executions = []
        self._calls_used = 0
        self._usage.clear()

    def act(self, observation: Observation) -> ActionChunk:
        obs = _policy_observation(observation)
        current = _last_applied_action(observation)
        step = _observation_step(observation)
        if self._pending is not None:
            feedback = observation.extra.get("action_execution", {})
            execution_steps = (
                feedback.get("steps", [])
                if feedback.get("tool_call_id") == self._pending.call_id
                else []
            )
            self._finish_pending(
                max(0, step - self._pending.start_step), execution_steps=execution_steps
            )

        context = _format_observation(
            obs,
            current=current,
            step=step,
            episode_steps=self._episode_steps,
            calls_left=self._max_llm_calls - self._calls_used,
        )
        self._history.append({"role": "user", "content": context})
        self._transcript.append({"role": "user", "content": context})
        started = time.perf_counter()

        while self._calls_used < self._max_llm_calls:
            response = self._provider.complete(
                InferenceRequest(
                    model=self.inference_config.model,
                    instructions=self._instructions,
                    input_items=tuple(self._history),
                    tools=self._tools,
                    reasoning_effort=self.inference_config.reasoning_effort,
                )
            )
            self._calls_used += 1
            for key, value in response.usage.items():
                self._usage[key] = self._usage.get(key, 0) + int(value)
            self._history.extend(copy.deepcopy(response.output_items))
            self._transcript.append(
                {
                    "role": "assistant",
                    "tool_calls": [
                        {"id": call.call_id, "name": call.name, "arguments": call.arguments}
                        for call in response.tool_calls
                    ],
                }
            )

            if len(response.tool_calls) != 1:
                error = f"expected exactly one tool call, got {len(response.tool_calls)}"
                for call in response.tool_calls:
                    self._append_tool_result(call.call_id, {"error": error})
                if not response.tool_calls:
                    self._history.append({"role": "user", "content": error})
                    self._transcript.append({"role": "tool", "content": error})
                continue

            call = response.tool_calls[0]
            try:
                chunk = self._execute(call, current, step)
            except ToolValidationError as exc:
                self._append_tool_result(call.call_id, {"error": str(exc)})
                continue
            latency = time.perf_counter() - started
            return ActionChunk(
                actions=chunk.actions,
                control_hz=50.0,
                inference_latency_s=latency,
                meta=chunk.meta,
            )

        return self._stop_chunk(current, "LLM call budget exhausted", time.perf_counter() - started)

    def _execute(self, call: ToolCall, current: np.ndarray, step: int) -> ActionChunk:
        if call.name == "run_joint_chunk":
            actions = _compile_joint_chunk(
                call.arguments,
                current=current,
                max_chunk_steps=self._max_chunk_steps,
                max_keyframes=self._max_keyframes,
                max_action_delta=self._max_action_delta,
            )
        elif call.name == "hold":
            steps = _bounded_int(call.arguments.get("steps"), "steps", 1, self._max_chunk_steps)
            _required_note(call.arguments)
            actions = np.repeat(current[None, :], steps, axis=0)
        elif call.name == "give_up":
            reason = call.arguments.get("reason")
            if not isinstance(reason, str) or not reason.strip():
                raise ToolValidationError("give_up.reason must be a non-empty string")
            return self._stop_chunk(current, reason.strip(), 0.0)
        else:
            raise ToolValidationError(
                f"unknown tool {call.name!r}; use run_joint_chunk, hold, or give_up"
            )

        self._pending = _PendingMotion(
            call.call_id, call.name, len(actions), step, actions.astype(np.float32)
        )
        wrapped = tuple(
            Action(
                data=np.asarray(action, dtype=np.float32),
                meta={
                    "inference_call_id": call.call_id,
                    "chunk_index": index,
                    "chunk_final": index + 1 == len(actions),
                },
            )
            for index, action in enumerate(actions)
        )
        return ActionChunk(actions=wrapped, control_hz=50.0)

    def _stop_chunk(self, current: np.ndarray, reason: str, latency: float) -> ActionChunk:
        return ActionChunk(
            actions=(
                Action(
                    data=np.asarray(current, dtype=np.float32),
                    meta={
                        "request_stop": True,
                        "stop_reason": "give_up",
                        "stop_detail": reason,
                    },
                ),
            ),
            control_hz=50.0,
            inference_latency_s=latency,
        )

    def _append_tool_result(self, call_id: str, result: dict[str, Any]) -> None:
        content = json.dumps(result, separators=(",", ":"), sort_keys=True)
        item = {"type": "function_call_output", "call_id": call_id, "output": content}
        self._history.append(item)
        self._transcript.append({"role": "tool", "tool_call_id": call_id, "content": result})

    def _finish_pending(
        self,
        executed_steps: int,
        *,
        execution_steps: list[dict[str, Any]],
        stop_reason: str | None = None,
    ) -> None:
        pending = self._pending
        if pending is None:
            return
        executed = min(pending.requested_steps, max(0, int(executed_steps)))
        result: dict[str, Any] = {
            "status": "completed" if executed == pending.requested_steps else "interrupted",
            "requested_steps": pending.requested_steps,
            "executed_steps": executed,
        }
        rows = sorted(execution_steps, key=lambda row: row["sim_step"])
        complete = len(rows) == executed and all(
            row["sim_step"] == pending.start_step + index + 1 and row["chunk_index"] == index
            for index, row in enumerate(rows)
        )
        result["execution_feedback_complete"] = complete
        result["last_applied_action"] = rows[-1]["applied_action"] if rows else None
        if complete:
            modifications = []
            largest_error = 0.0
            for index, row in enumerate(rows):
                applied = np.asarray(row["applied_action"], dtype=np.float64)
                difference = np.abs(applied - pending.actions[index])
                largest_error = max(largest_error, float(np.max(difference)))
                # Ignore float32 representation noise, not meaningful rewrites.
                changed = np.flatnonzero(difference > 1e-7)
                if changed.size:
                    modifications.append(
                        {
                            "chunk_step": index + 1,
                            "sim_step": row["sim_step"],
                            "joints": [JOINT_LABELS[j] for j in changed],
                            "requested": pending.actions[index, changed].tolist(),
                            "applied": applied[changed].tolist(),
                        }
                    )
            result.update(
                modified_steps=len(modifications),
                max_action_error=largest_error,
                modifications=modifications,
            )
        if stop_reason is not None:
            result["stop_reason"] = stop_reason
        self._append_tool_result(pending.call_id, result)
        self._chunk_executions.append(
            {
                "tool_call_id": pending.call_id,
                "tool_name": pending.tool_name,
                **copy.deepcopy(result),
            }
        )
        self._pending = None

    def transcript(self) -> list[dict[str, Any]]:
        return copy.deepcopy(self._transcript)

    def on_trial_end(self, record: Any, log_dir: str, run_id: str) -> None:
        if self._pending is not None:
            call_id = self._pending.call_id
            actions = [
                step.action
                for step in record.steps
                if getattr(getattr(step, "action", None), "meta", {}).get("inference_call_id")
                == call_id
            ]
            execution_steps = [
                {
                    "sim_step": self._pending.start_step + index + 1,
                    "chunk_index": action.meta.get("chunk_index"),
                    "applied_action": np.asarray(action.data, dtype=np.float32).tolist(),
                }
                for index, action in enumerate(actions)
            ]
            stop_reason = (
                getattr(record, "termination_reason", None)
                or getattr(record, "error", None)
                or getattr(record, "status", None)
                or "trial_end"
            )
            self._finish_pending(
                len(actions), execution_steps=execution_steps, stop_reason=str(stop_reason)
            )

        record.metadata["inference"] = {
            "provider": self.inference_config.provider,
            "base_url": self.inference_config.base_url,
            "model": self.inference_config.model,
            "reasoning_effort": self.inference_config.reasoning_effort,
        }
        record.metadata["llm_usage"] = {"llm_calls": self._calls_used, **self._usage}
        record.metadata["chunk_executions"] = copy.deepcopy(self._chunk_executions)
        record.metadata["action_feedback_version"] = 2
        record.metadata["robot_spec"] = (
            {
                "schema_version": self._robot_spec["schema_version"],
                "sha256": robot_spec_sha256(self._robot_spec),
            }
            if self._robot_spec is not None
            else None
        )
        # rollout() collects the transcript before this hook runs. Replace the
        # captured copy so the final pending chunk result is not lost at trial end.
        record.policy_transcript = self.transcript()

    def close(self) -> None:
        self._provider.close()


def _policy_observation(observation: Observation) -> np.ndarray:
    try:
        value = observation.state["policy_obs"]
    except KeyError as exc:
        raise ValueError("joint-chunk policy requires observation.state['policy_obs']") from exc
    obs = np.asarray(value, dtype=np.float64).reshape(-1)
    if obs.shape != (48,) or not bool(np.all(np.isfinite(obs))):
        raise ValueError("policy_obs must contain 48 finite values")
    return obs


def _observation_step(observation: Observation) -> int:
    if observation.state_time is None:
        return 0
    return max(0, round(float(observation.state_time) * 50.0))


def _last_applied_action(observation: Observation) -> np.ndarray:
    try:
        current = np.asarray(observation.state["last_applied_action"], dtype=np.float64)
    except KeyError as exc:
        raise ValueError(
            "joint-chunk policy requires last_applied_action from the updated embodiment; "
            "policy_obs[33:45] is a stale action and cannot be used as a fallback"
        ) from exc
    if current.shape != (12,) or not bool(np.all(np.isfinite(current))):
        raise ValueError("last_applied_action must contain 12 finite values")
    return current.copy()


def _format_observation(
    obs: np.ndarray, *, current: np.ndarray, step: int, episode_steps: int, calls_left: int
) -> str:
    def vector(values: np.ndarray) -> str:
        return "[" + ",".join(f"{float(value):.3f}" for value in values) + "]"

    return "\n".join(
        (
            f"Observation step={step}/{episode_steps}; calls_left={max(0, calls_left)}",
            f"command_forward_left_yaw={vector(obs[45:48])}",
            f"base_linear_velocity={vector(obs[0:3])}",
            f"base_gyro={vector(obs[3:6])}",
            f"projected_gravity={vector(obs[6:9])}",
            f"joint_position_delta_{'_'.join(JOINT_LABELS)}={vector(obs[9:21])}",
            f"joint_velocity_{'_'.join(JOINT_LABELS)}={vector(obs[21:33])}",
            f"actor_previous_action_{'_'.join(JOINT_LABELS)}={vector(obs[33:45])}",
            "last_applied_action=" + json.dumps(current.tolist(), separators=(",", ":")),
        )
    )


def _compile_joint_chunk(
    arguments: dict[str, Any],
    *,
    current: np.ndarray,
    max_chunk_steps: int,
    max_keyframes: int,
    max_action_delta: float,
) -> np.ndarray:
    _required_note(arguments)
    total_steps = _bounded_int(arguments.get("total_steps"), "total_steps", 1, max_chunk_steps)
    raw_keyframes = arguments.get("keyframes")
    if not isinstance(raw_keyframes, list) or not 1 <= len(raw_keyframes) <= max_keyframes:
        raise ToolValidationError(f"keyframes must contain 1..{max_keyframes} entries")

    keyframes: list[tuple[int, np.ndarray]] = []
    previous_step = 0
    for index, raw in enumerate(raw_keyframes):
        if not isinstance(raw, dict):
            raise ToolValidationError(f"keyframes[{index}] must be an object")
        frame_step = _bounded_int(raw.get("step"), f"keyframes[{index}].step", 1, total_steps)
        if frame_step <= previous_step:
            raise ToolValidationError("keyframe steps must be strictly increasing")
        target = np.asarray(raw.get("target"), dtype=np.float64).reshape(-1)
        if target.shape != (12,) or not bool(np.all(np.isfinite(target))):
            raise ToolValidationError(f"keyframes[{index}].target must contain 12 finite values")
        if bool(np.any(target < -1.0) or np.any(target > 1.0)):
            raise ToolValidationError(f"keyframes[{index}].target values must be inside [-1, 1]")
        keyframes.append((frame_step, target))
        previous_step = frame_step
    if keyframes[-1][0] != total_steps:
        raise ToolValidationError("the final keyframe step must equal total_steps")

    actions: list[np.ndarray] = []
    segment_start = np.asarray(current, dtype=np.float64)
    segment_step = 0
    for frame_step, target in keyframes:
        width = frame_step - segment_step
        for offset in range(1, width + 1):
            actions.append(segment_start + (target - segment_start) * (offset / width))
        segment_start = target
        segment_step = frame_step
    compiled = np.stack(actions)
    previous = np.vstack((current[None, :], compiled[:-1]))
    largest_delta = float(np.max(np.abs(compiled - previous)))
    if largest_delta > max_action_delta + 1e-7:
        raise ToolValidationError(
            f"joint chunk changes by {largest_delta:.4f} in one step; maximum is "
            f"{max_action_delta:.4f}; add steps or intermediate keyframes"
        )
    return compiled


def _required_note(arguments: dict[str, Any]) -> str:
    note = arguments.get("note")
    if not isinstance(note, str) or not note.strip():
        raise ToolValidationError("note must be a non-empty string")
    return note.strip()


def _bounded_int(value: Any, name: str, low: int, high: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not low <= value <= high:
        raise ToolValidationError(f"{name} must be an integer in [{low}, {high}]")
    return value


def _tool_schemas(max_chunk_steps: int, max_keyframes: int) -> tuple[dict[str, Any], ...]:
    note = {"type": "string", "minLength": 1}
    return (
        {
            "type": "function",
            "name": "run_joint_chunk",
            "description": (
                "Execute a bounded trajectory of normalized residual joint targets at 50 Hz. "
                "Keyframe steps are one-based and strictly increasing. The final keyframe step "
                "must equal total_steps."
            ),
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "keyframes": {
                        "type": "array",
                        "minItems": 1,
                        "maxItems": max_keyframes,
                        "items": {
                            "type": "object",
                            "properties": {
                                "step": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": max_chunk_steps,
                                },
                                "target": {
                                    "type": "array",
                                    "items": {"type": "number", "minimum": -1, "maximum": 1},
                                    "minItems": 12,
                                    "maxItems": 12,
                                },
                            },
                            "required": ["step", "target"],
                            "additionalProperties": False,
                        },
                    },
                    "total_steps": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": max_chunk_steps,
                    },
                    "note": note,
                },
                "required": ["keyframes", "total_steps", "note"],
                "additionalProperties": False,
            },
        },
        {
            "type": "function",
            "name": "hold",
            "description": "Repeat the previously applied joint target without changing it.",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "steps": {"type": "integer", "minimum": 1, "maximum": max_chunk_steps},
                    "note": note,
                },
                "required": ["steps", "note"],
                "additionalProperties": False,
            },
        },
        {
            "type": "function",
            "name": "give_up",
            "description": "Stop the trial as a failure when continuing is no longer useful.",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {"reason": {"type": "string", "minLength": 1}},
                "required": ["reason"],
                "additionalProperties": False,
            },
        },
    )


def go1_joint_chunk(**kwargs: Any) -> JointChunkAgentPolicy:
    """Create the registered Go1 joint-chunk agent policy."""
    return JointChunkAgentPolicy(**kwargs)
