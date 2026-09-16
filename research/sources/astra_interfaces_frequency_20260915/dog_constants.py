"""Shared Go1 action and observation contracts."""

from __future__ import annotations

import numpy as np
from inspect_robots import ActionSemantics, Box, ObservationSpace, StateField, StateSpec

JOINT_LABELS = (
    "FR_hip",
    "FR_thigh",
    "FR_calf",
    "FL_hip",
    "FL_thigh",
    "FL_calf",
    "RR_hip",
    "RR_thigh",
    "RR_calf",
    "RL_hip",
    "RL_thigh",
    "RL_calf",
)

ACTION_SPACE = Box(
    shape=(12,),
    low=np.full(12, -1.0, dtype=np.float32),
    high=np.full(12, 1.0, dtype=np.float32),
    semantics=ActionSemantics(
        control_mode="joint_pos",
        frame="base",
        dim_labels=JOINT_LABELS,
    ),
)

STATE_FIELDS = (
    StateField("policy_obs", (48,), "mixed", "float32"),
    StateField("base_lin_vel", (3,), "m/s", "float32"),
    StateField("base_gyro", (3,), "rad/s", "float32"),
    StateField("projected_gravity", (3,), "unit_vector", "float32"),
    StateField("joint_pos_delta", (12,), "rad", "float32"),
    StateField("joint_vel", (12,), "rad/s", "float32"),
    StateField("last_action", (12,), "normalized", "float32"),
    StateField("last_applied_action", (12,), "normalized", "float32"),
    StateField("command", (3,), "m/s,m/s,rad/s", "float32"),
    StateField("base_pos", (3,), "m", "float32"),
    StateField("base_quat", (4,), "quat_wxyz", "float32"),
    StateField("joint_pos", (12,), "rad", "float32"),
    StateField("actuator_force", (12,), "N*m", "float32"),
)

OBSERVATION_SPACE = ObservationSpace(state=StateSpec(fields=STATE_FIELDS))
POLICY_OBSERVATION_SPACE = ObservationSpace(state_keys=frozenset({"policy_obs"}))
AGENT_OBSERVATION_SPACE = ObservationSpace(
    state_keys=frozenset({"policy_obs", "last_applied_action"})
)

EMBODIMENT_DOCS = """Unitree Go1 velocity-tracking simulation.
Actions are 12 absolute normalized residual joint targets in FR, FL, RR, RL leg order;
each leg is hip, thigh, calf. The simulator applies
target = nominal_angle + 0.5 * action radians through its PD controller.
Every action must be finite and inside [-1, 1]. Control runs at 50 Hz.
The command state is [forward_m_s, left_m_s, yaw_rad_s]. policy_obs is the exact
48-value actor observation used by the upstream trainer and ONNX policy.
Its last_action slice is one control step behind the latest applied target.
last_applied_action separately reports the target actually sent to the simulator
after controller/guardrail processing (zero at reset); it is not a new sensor.
"""


def split_policy_observation(value: np.ndarray) -> dict[str, np.ndarray]:
    """Split the upstream 48-vector without changing its values."""
    obs = np.asarray(value, dtype=np.float32).reshape(-1)
    if obs.shape != (48,):
        raise ValueError(f"Go1 policy observation must have shape (48,), got {obs.shape}")
    return {
        "policy_obs": obs.copy(),
        "base_lin_vel": obs[0:3].copy(),
        "base_gyro": obs[3:6].copy(),
        "projected_gravity": obs[6:9].copy(),
        "joint_pos_delta": obs[9:21].copy(),
        "joint_vel": obs[21:33].copy(),
        "last_action": obs[33:45].copy(),
        "command": obs[45:48].copy(),
    }
