from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any

TIPOS = {"OBJETIVO", "REQUISITO", "CAPACIDADE", "COMPONENTE", "IMPLEMENTACAO", "TESTE", "EVIDENCIA", "VALIDACAO", "DECISAO", "PROBLEMA"}
RELACOES = {"ATENDE", "HABILITA", "IMPLEMENTADA_POR", "DEPENDE_DE", "TESTADA_POR", "EVIDENCIADA_POR", "VALIDADA_POR", "SUBSTITUI", "AFETA"}
ESTADOS = {"NAO_INICIADO", "EM_PLANEJAMENTO", "EM_CONSTRUCAO", "EM_TESTE", "EM_VALIDACAO", "VALIDADO", "BLOQUEADO", "SUPERADO", "ARQUIVADO"}


@dataclass
class ElementoConstrucao:
    id: str
    tipo: str
    titulo: str
    estado: str = "NAO_INICIADO"
    versao: str = "0.1"
    origem: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.tipo = self.tipo.upper()
        if self.tipo not in TIPOS:
            raise ValueError(f"Tipo inválido: {self.tipo}")
        if self.estado not in ESTADOS:
            raise ValueError(f"Estado inválido: {self.estado}")
        if not self.id or not self.titulo:
            raise ValueError("id e titulo são obrigatórios")


@dataclass
class RelacaoConstrucao:
    origem: str
    relacao: str
    destino: str
    evidencia: str | None = None

    def __post_init__(self) -> None:
        if self.relacao not in RELACOES:
            raise ValueError(f"Relação inválida: {self.relacao}")
        if not self.origem or not self.destino:
            raise ValueError("origem e destino são obrigatórios")


@dataclass
class MapaConstrucao:
    elementos: dict[str, ElementoConstrucao] = field(default_factory=dict)
    relacoes: list[RelacaoConstrucao] = field(default_factory=list)

    def adicionar(self, elemento: ElementoConstrucao) -> None:
        if elemento.id in self.elementos:
            raise ValueError(f"Elemento já existe: {elemento.id}")
        self.elementos[elemento.id] = elemento

    def relacionar(self, relacao: RelacaoConstrucao) -> None:
        if relacao.origem not in self.elementos or relacao.destino not in self.elementos:
            raise KeyError("Relação referencia elemento inexistente")
        self.relacoes.append(relacao)

    def dependencias(self, elemento_id: str) -> list[str]:
        return [r.origem for r in self.relacoes if r.destino == elemento_id and r.relacao == "DEPENDE_DE"]

    def impactos(self, elemento_id: str) -> list[str]:
        return [r.destino for r in self.relacoes if r.origem == elemento_id and r.relacao == "AFETA"]

    def validar(self) -> list[str]:
        erros: list[str] = []
        ids = set(self.elementos)
        for r in self.relacoes:
            if r.origem not in ids:
                erros.append(f"origem inexistente: {r.origem}")
            if r.destino not in ids:
                erros.append(f"destino inexistente: {r.destino}")
        return erros

    def to_dict(self) -> dict[str, Any]:
        return {"elementos": {k: asdict(v) for k, v in self.elementos.items()}, "relacoes": [asdict(r) for r in self.relacoes]}
