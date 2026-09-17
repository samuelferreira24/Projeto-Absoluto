from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import hashlib
import json


def agora() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class RecursoCapacidade:
    """Registro portátil de um recurso que pode alimentar uma capacidade."""

    id: str
    tipo: str
    quantidade: float
    unidade: str
    origem: str
    estado: str = "DISPONIVEL"
    custo: float | None = None
    moeda: str | None = None
    validade: str | None = None
    restricoes: list[str] = field(default_factory=list)
    motores_compativeis: list[str] = field(default_factory=list)
    consumido: float = 0.0
    valor_gerado: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)
    criado_em: str = field(default_factory=agora)
    atualizado_em: str = field(default_factory=agora)

    def __post_init__(self) -> None:
        if not self.id or not self.tipo or not self.unidade or not self.origem:
            raise ValueError("id, tipo, unidade e origem são obrigatórios")
        if self.quantidade < 0 or self.consumido < 0:
            raise ValueError("quantidade e consumido não podem ser negativos")
        if self.consumido > self.quantidade:
            raise ValueError("consumido não pode superar quantidade")
        if self.estado not in {"DISPONIVEL", "RESERVADO", "ESGOTADO", "EXPIRADO", "BLOQUEADO"}:
            raise ValueError(f"estado inválido: {self.estado}")

    @property
    def disponivel(self) -> float:
        return self.quantidade - self.consumido

    def consumir(self, quantidade: float, valor_gerado: float = 0.0) -> "RecursoCapacidade":
        if quantidade <= 0:
            raise ValueError("quantidade consumida deve ser positiva")
        if quantidade > self.disponivel:
            raise ValueError("recurso insuficiente")
        if valor_gerado < 0:
            raise ValueError("valor_gerado não pode ser negativo")
        self.consumido += quantidade
        self.valor_gerado += valor_gerado
        if self.disponivel == 0:
            self.estado = "ESGOTADO"
        self.atualizado_em = agora()
        return self

    def reservar(self) -> "RecursoCapacidade":
        if self.estado == "DISPONIVEL" and self.disponivel > 0:
            self.estado = "RESERVADO"
            self.atualizado_em = agora()
        return self

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class EstoqueCapacidade:
    """Estoque JSONL simples e portátil para recursos digitais/físicos futuros."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _linhas(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return [json.loads(linha) for linha in self.path.read_text(encoding="utf-8").splitlines() if linha.strip()]

    def adicionar(self, recurso: RecursoCapacidade) -> RecursoCapacidade:
        if any(item["id"] == recurso.id for item in self._linhas()):
            raise ValueError(f"recurso já existe: {recurso.id}")
        with self.path.open("a", encoding="utf-8") as arquivo:
            arquivo.write(json.dumps(recurso.to_dict(), ensure_ascii=False) + "\n")
        return recurso

    def obter(self, recurso_id: str) -> RecursoCapacidade | None:
        itens = [item for item in self._linhas() if item["id"] == recurso_id]
        return RecursoCapacidade(**itens[-1]) if itens else None

    def salvar(self, recurso: RecursoCapacidade) -> None:
        itens = self._linhas()
        if not any(item["id"] == recurso.id for item in itens):
            raise ValueError(f"recurso inexistente: {recurso.id}")
        substituidos = [recurso.to_dict() if item["id"] == recurso.id else item for item in itens]
        self.path.write_text("".join(json.dumps(item, ensure_ascii=False) + "\n" for item in substituidos), encoding="utf-8")

    def listar(self, tipo: str | None = None, estado: str | None = None) -> list[RecursoCapacidade]:
        itens = self._linhas()
        if tipo is not None:
            itens = [item for item in itens if item["tipo"] == tipo]
        if estado is not None:
            itens = [item for item in itens if item["estado"] == estado]
        return [RecursoCapacidade(**item) for item in itens]

    def total_disponivel(self, tipo: str | None = None, unidade: str | None = None) -> float:
        recursos = self.listar(tipo=tipo)
        if unidade is not None:
            recursos = [r for r in recursos if r.unidade == unidade]
        return sum(r.disponivel for r in recursos)

    @staticmethod
    def chave_idempotencia(origem: str, identificador_externo: str, quantidade: float, unidade: str) -> str:
        bruto = f"{origem}|{identificador_externo}|{quantidade}|{unidade}".encode("utf-8")
        return hashlib.sha256(bruto).hexdigest()
