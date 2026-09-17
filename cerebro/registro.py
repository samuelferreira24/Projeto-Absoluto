"""Registro central e portável de agentes, contas, sessões e recursos do Projeto Absoluto."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

TIPOS = {"AGENTE", "CONTA", "SESSAO", "RECURSO", "SISTEMA", "INTERFACE"}
ESTADOS = {"ATIVO", "INATIVO", "SUSPENSO", "REVOGADO", "DESCONHECIDO"}


def agora() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Participante:
    id: str
    tipo: str
    nome: str
    estado: str = "ATIVO"
    capacidades: list[str] = field(default_factory=list)
    interfaces: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    criado_em: str = field(default_factory=agora)
    atualizado_em: str = field(default_factory=agora)

    def __post_init__(self) -> None:
        if not self.id.strip() or not self.nome.strip():
            raise ValueError("id e nome são obrigatórios")
        if self.tipo not in TIPOS:
            raise ValueError(f"tipo inválido: {self.tipo}")
        if self.estado not in ESTADOS:
            raise ValueError(f"estado inválido: {self.estado}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class RegistroParticipantes:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _ler(self) -> dict[str, Participante]:
        if not self.path.exists():
            return {}
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return {x["id"]: Participante(**x) for x in data.get("participantes", [])}

    def salvar(self, participante: Participante) -> None:
        registros = self._ler()
        if participante.id in registros:
            raise ValueError(f"id já registrado: {participante.id}")
        registros[participante.id] = participante
        self._escrever(registros)

    def atualizar(self, participante: Participante) -> None:
        registros = self._ler()
        if participante.id not in registros:
            raise KeyError(participante.id)
        participante.atualizado_em = agora()
        registros[participante.id] = participante
        self._escrever(registros)

    def obter(self, participante_id: str) -> Participante | None:
        return self._ler().get(participante_id)

    def listar(self, tipo: str | None = None, estado: str | None = None) -> list[Participante]:
        values = list(self._ler().values())
        return [x for x in values if (tipo is None or x.tipo == tipo) and (estado is None or x.estado == estado)]

    def _escrever(self, registros: dict[str, Participante]) -> None:
        payload = {"versao": 1, "atualizado_em": agora(), "participantes": [x.to_dict() for x in registros.values()]}
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
        tmp.replace(self.path)
