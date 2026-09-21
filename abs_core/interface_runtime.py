from __future__ import annotations

from dataclasses import dataclass, field
from threading import RLock
from typing import Any


@dataclass(frozen=True)
class InterfaceMode:
    id: str
    name: str
    kind: str = "experience"
    description: str = ""
    capabilities: tuple[str, ...] = ()


@dataclass
class InterfaceState:
    mode_id: str = "control"
    input_channel: str = "text"
    context: dict[str, Any] = field(default_factory=dict)


class InterfaceRuntime:
    """Extensible runtime for ABS interface modes and input channels.

    This layer owns interface experience state. It does not own ABS execution,
    capabilities, devices, or external services. Those remain below it.
    """

    def __init__(self) -> None:
        self._lock = RLock()
        self._modes: dict[str, InterfaceMode] = {}
        self._inputs: set[str] = set()
        self._state = InterfaceState()
        self.register_mode(
            InterfaceMode(
                "control",
                "Controle",
                description="Controle operacional do ABS.",
                capabilities=("execute", "status"),
            )
        )
        self.register_mode(
            InterfaceMode(
                "capabilities",
                "Capacidades",
                description="Visão das capacidades disponíveis.",
                capabilities=("capabilities",),
            )
        )
        self.register_mode(
            InterfaceMode(
                "devices",
                "Dispositivos",
                description="Visão dos recursos e dispositivos.",
                capabilities=("devices",),
            )
        )
        self.register_mode(
            InterfaceMode(
                "browser",
                "Navegador",
                kind="navigation",
                description="Modo reservado para navegação web integrada.",
                capabilities=("web_navigation",),
            )
        )
        for channel in ("text", "voice", "image", "camera"):
            self.register_input(channel)

    def register_mode(self, mode: InterfaceMode) -> None:
        with self._lock:
            if mode.id in self._modes:
                raise ValueError(f"Interface mode already registered: {mode.id}")
            self._modes[mode.id] = mode

    def register_input(self, channel: str) -> None:
        value = channel.strip().lower()
        if not value:
            raise ValueError("input_channel_required")
        with self._lock:
            self._inputs.add(value)

    def list_modes(self) -> list[InterfaceMode]:
        with self._lock:
            return list(self._modes.values())

    def list_inputs(self) -> list[str]:
        with self._lock:
            return sorted(self._inputs)

    def set_mode(self, mode_id: str) -> InterfaceState:
        with self._lock:
            if mode_id not in self._modes:
                raise KeyError(mode_id)
            self._state.mode_id = mode_id
            return self.state()

    def set_input(self, channel: str) -> InterfaceState:
        value = channel.strip().lower()
        with self._lock:
            if value not in self._inputs:
                raise KeyError(value)
            self._state.input_channel = value
            return self.state()

    def update_context(self, **values: Any) -> InterfaceState:
        with self._lock:
            self._state.context.update(values)
            return self.state()

    def state(self) -> InterfaceState:
        with self._lock:
            return InterfaceState(
                mode_id=self._state.mode_id,
                input_channel=self._state.input_channel,
                context=dict(self._state.context),
            )

    def public_state(self) -> dict[str, Any]:
        state = self.state()
        mode = self._modes[state.mode_id]
        return {
            "mode": {
                "id": mode.id,
                "name": mode.name,
                "kind": mode.kind,
                "description": mode.description,
                "capabilities": list(mode.capabilities),
            },
            "input_channel": state.input_channel,
            "context": state.context,
        }

    def public_modes(self) -> list[dict[str, Any]]:
        return [
            {
                "id": m.id,
                "name": m.name,
                "kind": m.kind,
                "description": m.description,
                "capabilities": list(m.capabilities),
            }
            for m in self.list_modes()
        ]
