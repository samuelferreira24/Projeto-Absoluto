from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
import json


@dataclass(frozen=True)
class CerebroRemoto:
    """Contrato mínimo para outro núcleo do Cérebro, sem exigir topologia única.

    Um núcleo pode ser local, remoto, temporário ou apenas descoberto.
    O contrato descreve identidade e capacidades; não define hierarquia.
    """

    id: str
    nome: str
    ambiente: str
    modo: str = "remoto"
    endpoint: str | None = None
    capacidades: tuple[str, ...] = ()
    ativo: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id or not self.nome or not self.ambiente:
            raise ValueError("id, nome e ambiente são obrigatórios")
        if self.modo not in {"local", "remoto", "hibrido", "temporario"}:
            raise ValueError(f"modo inválido: {self.modo}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class RegistroCerebros:
    """Registro de núcleos do Cérebro sem impor quantidade, hierarquia ou topologia."""

    def __init__(self, path: str | Path = "cerebro/data/cerebros.json") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def listar(self, *, ativos: bool | None = None) -> list[CerebroRemoto]:
        if not self.path.exists():
            return []
        dados = json.loads(self.path.read_text(encoding="utf-8"))
        cerebros = [CerebroRemoto(**item) for item in dados.get("cerebros", [])]
        if ativos is not None:
            cerebros = [cerebro for cerebro in cerebros if cerebro.ativo is ativos]
        return cerebros

    def registrar(self, cerebro: CerebroRemoto) -> None:
        cerebros = {item.id: item for item in self.listar()}
        cerebros[cerebro.id] = cerebro
        self._salvar(list(cerebros.values()))

    def remover(self, cerebro_id: str) -> None:
        self._salvar([item for item in self.listar() if item.id != cerebro_id])

    def por_capacidade(self, capacidade: str, *, ativos: bool = True) -> list[CerebroRemoto]:
        termo = capacidade.casefold()
        return [
            cerebro
            for cerebro in self.listar(ativos=ativos)
            if any(termo == item.casefold() for item in cerebro.capacidades)
        ]

    def por_ambiente(self, ambiente: str, *, ativos: bool = True) -> list[CerebroRemoto]:
        termo = ambiente.casefold()
        return [
            cerebro
            for cerebro in self.listar(ativos=ativos)
            if cerebro.ambiente.casefold() == termo
        ]

    def _salvar(self, cerebros: list[CerebroRemoto]) -> None:
        payload = {
            "versao": "0.1",
            "cerebros": [
                cerebro.to_dict()
                for cerebro in sorted(cerebros, key=lambda item: item.id)
            ],
        }
        self.path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
