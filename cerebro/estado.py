from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json


def agora() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class EstadoSistema:
    """Estado operacional mínimo, portátil e versionável do sistema."""
    schema_version: str = "0.1"
    project_id: str = "PROJETO-ABSOLUTO"
    state_id: str = "ESTADO-SISTEMA-0001"
    architecture_version: str = "FUNDACAO-V0.2"
    status: str = "EM_CONSTRUCAO"
    active_branch: str | None = None
    active_capabilities: list[str] = field(default_factory=list)
    in_construction: list[str] = field(default_factory=list)
    open_problems: list[str] = field(default_factory=list)
    pending_decisions: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    next_priority: str | None = None
    updated_at: str = field(default_factory=agora)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.project_id or not self.state_id:
            raise ValueError("project_id e state_id são obrigatórios")
        if self.status not in {"PLANEJADO", "EM_CONSTRUCAO", "OPERACIONAL", "BLOQUEADO", "SUPERADO"}:
            raise ValueError(f"Status inválido: {self.status}")

    def atualizar(self, **changes: Any) -> "EstadoSistema":
        permitido = set(self.__dataclass_fields__) - {"schema_version", "project_id", "state_id"}
        desconhecidos = set(changes) - permitido
        if desconhecidos:
            raise ValueError(f"Campos desconhecidos: {sorted(desconhecidos)}")
        for chave, valor in changes.items():
            setattr(self, chave, valor)
        self.__post_init__()
        self.updated_at = agora()
        return self

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def salvar(self, path: str | Path) -> None:
        destino = Path(path)
        destino.parent.mkdir(parents=True, exist_ok=True)
        self.updated_at = agora()
        destino.write_text(json.dumps(self.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    @classmethod
    def carregar(cls, path: str | Path) -> "EstadoSistema":
        dados = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(**dados)


def validar_estado(dados: dict[str, Any]) -> list[str]:
    erros: list[str] = []
    obrigatorios = {"schema_version", "project_id", "state_id", "architecture_version", "status", "updated_at"}
    erros.extend(f"campo obrigatório ausente: {campo}" for campo in sorted(obrigatorios - dados.keys()))
    if "status" in dados and dados["status"] not in {"PLANEJADO", "EM_CONSTRUCAO", "OPERACIONAL", "BLOQUEADO", "SUPERADO"}:
        erros.append("status inválido")
    if "schema_version" in dados and not isinstance(dados["schema_version"], str):
        erros.append("schema_version deve ser string")
    return erros
