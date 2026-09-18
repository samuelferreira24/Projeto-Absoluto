from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
import json


@dataclass(frozen=True)
class Porta:
    """Contrato descritivo para uma capacidade externa substituível."""

    id: str
    nome: str
    categoria: str
    provedor: str
    ambiente: str
    capacidades: tuple[str, ...] = ()
    ferramentas: tuple[str, ...] = ()
    permissoes: tuple[str, ...] = ()
    endpoint: str | None = None
    modo: str = "externo"
    ativa: bool = True
    substituivel: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id or not self.nome or not self.categoria or not self.provedor:
            raise ValueError("id, nome, categoria e provedor são obrigatórios")
        if not self.ambiente:
            raise ValueError("ambiente é obrigatório")
        if self.modo not in {"local", "remoto", "externo", "hibrido"}:
            raise ValueError(f"modo inválido: {self.modo}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class RegistroPortas:
    """Registro portátil das portas disponíveis ao Cérebro.

    O registro descreve capacidades sem acoplar o Cérebro ao provedor.
    """

    def __init__(self, path: str | Path = "cerebro/data/portas.json") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def listar(self, *, ativas: bool | None = None) -> list[Porta]:
        if not self.path.exists():
            return []
        dados = json.loads(self.path.read_text(encoding="utf-8"))
        portas = [Porta(**item) for item in dados.get("portas", [])]
        if ativas is not None:
            portas = [porta for porta in portas if porta.ativa is ativas]
        return portas

    def registrar(self, porta: Porta) -> None:
        portas = {item.id: item for item in self.listar()}
        portas[porta.id] = porta
        self._salvar(list(portas.values()))

    def remover(self, porta_id: str) -> None:
        portas = [item for item in self.listar() if item.id != porta_id]
        self._salvar(portas)

    def por_capacidade(self, capacidade: str, *, ativas: bool = True) -> list[Porta]:
        termo = capacidade.casefold()
        return [
            porta
            for porta in self.listar(ativas=ativas)
            if any(termo == item.casefold() for item in porta.capacidades)
        ]

    def por_ambiente(self, ambiente: str, *, ativas: bool = True) -> list[Porta]:
        termo = ambiente.casefold()
        return [
            porta
            for porta in self.listar(ativas=ativas)
            if porta.ambiente.casefold() == termo
        ]

    def _salvar(self, portas: list[Porta]) -> None:
        payload = {
            "versao": "0.1",
            "portas": [porta.to_dict() for porta in sorted(portas, key=lambda item: item.id)],
        }
        self.path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
