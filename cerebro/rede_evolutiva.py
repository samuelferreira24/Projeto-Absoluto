from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any

TIPOS_NOS = {
    "OBJETIVO", "CAPACIDADE", "IDEIA", "HIPOTESE", "PESQUISA", "DECISAO",
    "EXPERIMENTO", "RESULTADO", "EXPERIENCIA", "APRENDIZADO", "SABEDORIA",
    "COMPONENTE", "RECURSO", "RISCO", "PROBLEMA", "CONCEITO", "PRINCIPIO",
}
TIPOS_RELACAO = {
    "DEPENDE_DE", "HABILITA", "IMPULSIONA", "MULTIPLICA", "INFORMA", "VALIDA",
    "CONTRADIZ", "CORRIGE", "CAUSA", "RESULTA_EM", "CONVERGE_COM", "ALIMENTA",
    "SUBSTITUI", "SUPERA", "DERIVA_DE",
}


@dataclass
class NoRede:
    id: str
    tipo: str
    titulo: str
    estado: str = "ATIVO"
    potencial_multiplicador: float = 0.0
    evidencia: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.tipo = self.tipo.upper()
        if self.tipo not in TIPOS_NOS:
            raise ValueError(f"Tipo de nó inválido: {self.tipo}")
        if not self.id or not self.titulo:
            raise ValueError("id e titulo são obrigatórios")
        if self.potencial_multiplicador < 0:
            raise ValueError("potencial_multiplicador não pode ser negativo")


@dataclass
class ArestaRede:
    origem: str
    relacao: str
    destino: str
    peso: float = 1.0
    evidencia: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.relacao not in TIPOS_RELACAO:
            raise ValueError(f"Relação inválida: {self.relacao}")
        if not self.origem or not self.destino:
            raise ValueError("origem e destino são obrigatórios")
        if self.peso < 0:
            raise ValueError("peso não pode ser negativo")


@dataclass
class RedeEvolutiva:
    nos: dict[str, NoRede] = field(default_factory=dict)
    arestas: list[ArestaRede] = field(default_factory=list)

    def adicionar_no(self, no: NoRede) -> None:
        if no.id in self.nos:
            raise ValueError(f"Nó já existe: {no.id}")
        self.nos[no.id] = no

    def conectar(self, aresta: ArestaRede) -> None:
        if aresta.origem not in self.nos or aresta.destino not in self.nos:
            raise KeyError("Aresta referencia nó inexistente")
        self.arestas.append(aresta)

    def sucessores(self, no_id: str, relacao: str | None = None) -> list[str]:
        return [
            a.destino for a in self.arestas
            if a.origem == no_id and (relacao is None or a.relacao == relacao)
        ]

    def predecessores(self, no_id: str, relacao: str | None = None) -> list[str]:
        return [
            a.origem for a in self.arestas
            if a.destino == no_id and (relacao is None or a.relacao == relacao)
        ]

    def caminhos_que_convergem(self, destino_id: str) -> list[str]:
        """Retorna nós com relação CONVERGE_COM direta ao destino."""
        return self.predecessores(destino_id, "CONVERGE_COM")

    def impulso_total(self, no_id: str) -> float:
        """Mede o potencial local de um nó somando impulsos e multiplicadores recebidos."""
        total = self.nos[no_id].potencial_multiplicador
        for a in self.arestas:
            if a.destino == no_id and a.relacao in {"IMPULSIONA", "MULTIPLICA", "HABILITA"}:
                total += a.peso * self.nos[a.origem].potencial_multiplicador
        return total

    def pontos_de_alavancagem(self, limite: int = 10) -> list[tuple[str, float]]:
        """Ordena pontos de alavancagem sem transformar a rede em uma fila obrigatória."""
        if limite < 1:
            raise ValueError("limite deve ser >= 1")
        valores = ((no_id, self.impulso_total(no_id)) for no_id in self.nos)
        return sorted(valores, key=lambda item: item[1], reverse=True)[:limite]

    def validar(self) -> list[str]:
        erros: list[str] = []
        ids = set(self.nos)
        for a in self.arestas:
            if a.origem not in ids:
                erros.append(f"origem inexistente: {a.origem}")
            if a.destino not in ids:
                erros.append(f"destino inexistente: {a.destino}")
        return erros

    def to_dict(self) -> dict[str, Any]:
        return {
            "nos": {k: asdict(v) for k, v in self.nos.items()},
            "arestas": [asdict(a) for a in self.arestas],
        }
