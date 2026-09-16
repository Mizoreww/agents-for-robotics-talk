"""Pluggable inference providers for the joint-chunk agent."""

from __future__ import annotations

import json
import os
import tomllib
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Protocol

import httpx


@dataclass(frozen=True)
class InferenceConfig:
    """Connection settings shared by real and fake inference providers."""

    provider: str = "fake"
    base_url: str = "http://127.0.0.1:8765/v1"
    api_key: str = "fake-local-key"
    model: str = "fake-go1"
    reasoning_effort: str | None = "medium"
    timeout_s: float = 120.0

    @classmethod
    def from_toml(cls, path: str | Path) -> InferenceConfig:
        source = Path(path).expanduser()
        with source.open("rb") as handle:
            document = tomllib.load(handle)
        raw = document.get("inference")
        if not isinstance(raw, dict):
            raise ValueError(f"{source} must contain an [inference] table")
        allowed = {field for field in cls.__dataclass_fields__}
        unknown = sorted(set(raw) - allowed)
        if unknown:
            raise ValueError(f"unknown inference settings in {source}: {unknown}")
        return cls(**raw)

    def validate(self) -> InferenceConfig:
        if not self.provider.strip():
            raise ValueError("provider must not be empty")
        if not self.base_url.strip():
            raise ValueError("base_url must not be empty")
        if not self.api_key.strip():
            raise ValueError("api_key must not be empty")
        if not self.model.strip():
            raise ValueError("model must not be empty")
        if self.timeout_s <= 0:
            raise ValueError("timeout_s must be > 0")
        return self


def resolve_inference_config(
    *,
    config_path: str | None = "secret.toml",
    provider: str | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
    model: str | None = None,
    reasoning_effort: str | None = None,
    timeout_s: float | None = None,
) -> InferenceConfig:
    """Load TOML settings, then apply explicit constructor overrides."""
    config = InferenceConfig()
    if config_path is not None:
        path = Path(config_path).expanduser()
        if path.is_file():
            config = InferenceConfig.from_toml(path)
        elif config_path != "secret.toml":
            raise FileNotFoundError(f"inference config not found: {path}")

    env_key = os.environ.get("GPT_DOG_API_KEY")
    overrides: dict[str, Any] = {}
    for key, value in (
        ("provider", provider),
        ("base_url", base_url),
        ("api_key", api_key or env_key),
        ("model", model),
        ("reasoning_effort", reasoning_effort),
        ("timeout_s", timeout_s),
    ):
        if value is not None:
            overrides[key] = value
    return replace(config, **overrides).validate()


@dataclass(frozen=True)
class InferenceRequest:
    """Provider-neutral request for one agent turn."""

    model: str
    instructions: str
    input_items: tuple[dict[str, Any], ...]
    tools: tuple[dict[str, Any], ...]
    reasoning_effort: str | None = None


@dataclass(frozen=True)
class ToolCall:
    """A parsed function call emitted by an inference provider."""

    call_id: str
    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True)
class InferenceResponse:
    """Provider output retained both for execution and transcript replay."""

    tool_calls: tuple[ToolCall, ...]
    output_items: tuple[dict[str, Any], ...]
    usage: Mapping[str, int]


class InferenceProvider(Protocol):
    """Small boundary implemented by real, fake, and third-party providers."""

    def complete(self, request: InferenceRequest) -> InferenceResponse:
        """Return one model turn."""
        ...

    def close(self) -> None:
        """Release provider resources."""
        ...


class ResponsesInferenceProvider:
    """OpenAI-compatible ``POST /responses`` inference provider."""

    def __init__(self, config: InferenceConfig) -> None:
        self._client = httpx.Client(
            base_url=config.base_url.rstrip("/") + "/",
            headers={"Authorization": f"Bearer {config.api_key}"},
            timeout=config.timeout_s,
        )

    def complete(self, request: InferenceRequest) -> InferenceResponse:
        body: dict[str, Any] = {
            "model": request.model,
            "instructions": request.instructions,
            "input": list(request.input_items),
            "tools": list(request.tools),
            "tool_choice": "required",
            "parallel_tool_calls": False,
            "store": False,
            "include": ["reasoning.encrypted_content"],
        }
        if request.reasoning_effort is not None:
            body["reasoning"] = {"effort": request.reasoning_effort}
        try:
            response = self._client.post("responses", json=body)
        except httpx.HTTPError as exc:
            raise RuntimeError(f"inference request failed: {exc}") from exc
        if response.status_code != 200:
            raise RuntimeError(
                f"inference endpoint returned HTTP {response.status_code}: {response.text[:500]}"
            )
        payload = response.json()
        if payload.get("status") == "failed":
            raise RuntimeError(f"inference response failed: {payload.get('error')!r}")
        output = tuple(payload.get("output") or ())
        calls: list[ToolCall] = []
        for item in output:
            if item.get("type") != "function_call":
                continue
            try:
                arguments = json.loads(item["arguments"])
            except (KeyError, TypeError, ValueError) as exc:
                raise RuntimeError("provider returned invalid function-call arguments") from exc
            if not isinstance(arguments, dict):
                raise RuntimeError("provider function-call arguments must be a JSON object")
            calls.append(
                ToolCall(
                    call_id=str(item["call_id"]),
                    name=str(item["name"]),
                    arguments=arguments,
                )
            )
        usage = {
            str(key): int(value)
            for key, value in (payload.get("usage") or {}).items()
            if isinstance(value, int) and not isinstance(value, bool)
        }
        return InferenceResponse(tool_calls=tuple(calls), output_items=output, usage=usage)

    def close(self) -> None:
        self._client.close()


class FakeInferenceProvider:
    """Deterministic, zero-cost provider that emits valid nominal-pose chunks."""

    def __init__(self, config: InferenceConfig | None = None, *, chunk_steps: int = 15) -> None:
        if chunk_steps < 1:
            raise ValueError("chunk_steps must be >= 1")
        self.chunk_steps = chunk_steps
        self.calls = 0

    def complete(self, request: InferenceRequest) -> InferenceResponse:
        self.calls += 1
        maximum = _tool_total_steps_max(request.tools)
        steps = min(self.chunk_steps, maximum)
        call_id = f"fake_call_{self.calls}"
        arguments = {
            "keyframes": [{"step": steps, "target": [0.0] * 12}],
            "total_steps": steps,
            "note": "Fake provider holds the nominal standing target.",
        }
        item = {
            "type": "function_call",
            "id": f"fc_{self.calls}",
            "call_id": call_id,
            "name": "run_joint_chunk",
            "arguments": json.dumps(arguments, separators=(",", ":")),
            "status": "completed",
        }
        return InferenceResponse(
            tool_calls=(ToolCall(call_id, "run_joint_chunk", arguments),),
            output_items=(item,),
            usage={"input_tokens": 0, "output_tokens": 0, "total_tokens": 0},
        )

    def close(self) -> None:
        return None


def _tool_total_steps_max(tools: Sequence[dict[str, Any]]) -> int:
    for tool in tools:
        if tool.get("name") == "run_joint_chunk":
            value = (
                tool.get("parameters", {})
                .get("properties", {})
                .get("total_steps", {})
                .get("maximum", 15)
            )
            if isinstance(value, int) and value >= 1:
                return value
    return 15


ProviderFactory = Callable[[InferenceConfig], InferenceProvider]
_PROVIDERS: dict[str, ProviderFactory] = {
    "responses": ResponsesInferenceProvider,
    "fake": FakeInferenceProvider,
}


def register_inference_provider(
    name: str, factory: ProviderFactory, *, replace_existing: bool = False
) -> None:
    """Register an inference provider for Python callers and plugins."""
    key = name.strip().lower()
    if not key:
        raise ValueError("provider name must not be empty")
    if key in _PROVIDERS and not replace_existing:
        raise ValueError(f"inference provider already registered: {key}")
    _PROVIDERS[key] = factory


def create_inference_provider(config: InferenceConfig) -> InferenceProvider:
    """Instantiate the provider named by ``config.provider``."""
    key = config.provider.strip().lower()
    try:
        factory = _PROVIDERS[key]
    except KeyError as exc:
        raise ValueError(
            f"unknown inference provider {config.provider!r}; available: {sorted(_PROVIDERS)}"
        ) from exc
    return factory(config)
