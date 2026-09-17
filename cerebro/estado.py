"""Estado operacional portável do Cérebro.

Mantém um snapshot explícito do estado da construção sem acoplar a base a
GitHub, banco de dados ou fornecedor de IA.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "0.1"


def agora() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass
class EstadoSistema:
    project_id: str
    state_id: str
    architecture_version: str
    status: str = "EM_CONSTRUCAO"
    active_branch: str | None = None
    active_capabilities: list[str] = field(default_factory=list)
    in_construction: list[str] = field(default_factory=list)
    open_problems: list[dict[str, Any]] = field(default_factory=list)
    risks: list[dict[str, Any]] = field(default_factory=list)
    pending_decisions: list[dict[str, Any]] = field(default_factory=list)
    next_priority: str | None = None
    last_validation: dict[str, Any] = field(default_factory=dict)
    continuity_package: list[str] = field(default_factory=list)
    updated_at: str = field(default_factory=agora)

    def __post_init__(self) -> None:
        if not self.project_id or not self.state_id or not self.architecture_version:
            raise ValueError("project_id, state_id e architecture_version sao obrigatorios")
        if not isinstance(self.active_capabilities, list) or not isinstance(self.in_construction, list):
            raise TypeError("listas de capacidades e construcao sao obrigatorias")

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["schema_version"] = SCHEMA_VERSION
        return data

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2) + "\n"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EstadoSistema":
        if data.get("schema_version") != SCHEMA_VERSION:
            raise ValueError(f"schema_version incompatível: {data.get('schema_version')!r}")
        fields = {f.name for f in cls.__dataclass_fields__.values()}
        payload = {k: v for k, v in data.items() if k in fields}
        return cls(**payload)

    @classmethod
    def from_json(cls, text: str) -> "EstadoSistema":
        return cls.from_dict(json.loads(text))

    @classmethod
    def load(cls, path: str | Path) -> "EstadoSistema":
        return cls.from_json(Path(path).read_text(encoding="utf-8"))

    def save(self, path: str | Path) -> None:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        self.updated_at = agora()
        target.write_text(self.to_json(), encoding="utf-8")

    def atualizar(self, **changes: Any) -> "EstadoSistema":
        fields = set(self.__dataclass_fields__)
        unknown = set(changes) - fields
        if unknown:
            raise ValueError(f"campos desconhecidos: {sorted(unknown)}")
        for key, value in changes.items():
            setattr(self, key, value)
        self.updated_at = agora()
        return self


def validar_estado(data: dict[str, Any]) -> list[str]:
    erros: list[str] = []
    obrigatorios = ("schema_version", "project_id", "state_id", "architecture_version", "status")
    for campo in obrigatorios:
        if campo not in data:
            erros.append(f"campo obrigatorio ausente: {campo}")
    if data.get("schema_version") != SCHEMA_VERSION:
        erros.append("schema_version invalida")
    for campo in ("active_capabilities", "in_construction", "continuity_package"):
        if campo in data and not isinstance(data[campo], list):
            erros.append(f"campo deve ser lista: {campo}")
    if "risks" in data and not isinstance(data["risks"], list):
        erros.append("campo deve ser lista: risks")
    return erros
