"""Núcleo mínimo do tabuleiro de execução em rede.

O tabuleiro representa caminhos e relações; não transforma o planejamento em
uma fila fixa. A seleção de movimentos é contextual e pode mudar conforme o
estado, evidências e novas descobertas.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


RELACOES_VALIDAS = {
    "DEPENDE_DE",
    "HABILITA",
    "IMPULSIONA",
    "MULTIPLICA_VALOR",
    "CONVERGE_COM",
    "ALIMENTA",
    "VALIDA",
    "QUESTIONA",
    "CONTRADIZ",
    "SUBSTITUI",
    "DERIVA_DE",
    "REUTILIZA",
    "REVELA",
    "BLOQUEIA",
}

ESTADOS = {
    "IDEIA",
    "HIPOTESE",
    "PESQUISA",
    "DESENHO",
    "EXPERIMENTO",
    "EM_CONSTRUCAO",
    "EM_INTEGRACAO",
    "EM_TESTE",
    "VALIDACAO",
    "OPERACIONAL",
    "EVOLUCAO",
    "PAUSADA",
    "SUBSTITUIDA",
    "ABANDONADA_COM_MOTIVO",
}


@dataclass(frozen=True)
class Caminho:
    """Uma frente de trabalho independente dentro do tabuleiro."""

    id: str
    nome: str
    estado: str = "IDEIA"
    valor_multiplicador: float = 0.0
    incerteza: float = 0.0
    risco: float = 0.0
    reversibilidade: float = 1.0
    contexto: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id or not self.nome:
            raise ValueError("id e nome são obrigatórios")
        if self.estado not in ESTADOS:
            raise ValueError(f"Estado inválido: {self.estado}")
        for nome, valor in {
            "valor_multiplicador": self.valor_multiplicador,
            "incerteza": self.incerteza,
            "risco": self.risco,
            "reversibilidade": self.reversibilidade,
        }.items():
            if not 0.0 <= valor <= 1.0:
                raise ValueError(f"{nome} deve estar entre 0 e 1")


@dataclass(frozen=True)
class Relacao:
    origem: str
    tipo: str
    destino: str

    def __post_init__(self) -> None:
        if not self.origem or not self.destino:
            raise ValueError("origem e destino são obrigatórios")
        if self.tipo not in RELACOES_VALIDAS:
            raise ValueError(f"Relação inválida: {self.tipo}")
        if self.origem == self.destino:
            raise ValueError("uma relação não pode apontar para o próprio caminho")


class Tabuleiro:
    """Grafo de caminhos com navegação contextual, sem ordem fixa."""

    def __init__(self, caminhos: Iterable[Caminho] = ()) -> None:
        self._caminhos: dict[str, Caminho] = {c.id: c for c in caminhos}
        self._relacoes: list[Relacao] = []

    @property
    def caminhos(self) -> tuple[Caminho, ...]:
        return tuple(self._caminhos.values())

    @property
    def relacoes(self) -> tuple[Relacao, ...]:
        return tuple(self._relacoes)

    def adicionar_caminho(self, caminho: Caminho) -> None:
        if caminho.id in self._caminhos:
            raise ValueError(f"Caminho já existe: {caminho.id}")
        self._caminhos[caminho.id] = caminho

    def adicionar_relacao(self, relacao: Relacao) -> None:
        if relacao.origem not in self._caminhos or relacao.destino not in self._caminhos:
            raise ValueError("origem e destino precisam existir no tabuleiro")
        if relacao not in self._relacoes:
            self._relacoes.append(relacao)

    def relacionados(self, caminho_id: str) -> tuple[str, ...]:
        if caminho_id not in self._caminhos:
            raise KeyError(caminho_id)
        ids = {
            r.destino if r.origem == caminho_id else r.origem
            for r in self._relacoes
            if r.origem == caminho_id or r.destino == caminho_id
        }
        return tuple(sorted(ids))

    def habilitados_por(self, caminho_id: str) -> tuple[str, ...]:
        """Retorna caminhos diretamente marcados como habilitados por outro."""
        if caminho_id not in self._caminhos:
            raise KeyError(caminho_id)
        return tuple(sorted(
            r.destino for r in self._relacoes
            if r.origem == caminho_id and r.tipo in {"HABILITA", "IMPULSIONA", "MULTIPLICA_VALOR", "REVELA"}
        ))

    def candidatos(self, contexto: dict[str, float] | None = None) -> tuple[Caminho, ...]:
        """Retorna candidatos contextuais, sem declarar uma ordem obrigatória.

        O resultado é apenas uma visão para apoiar decisão. Não executa nem
        transforma a ordem retornada em regra do Projeto.
        """
        contexto = contexto or {}
        candidatos = [
            c for c in self._caminhos.values()
            if c.estado not in {"ABANDONADA_COM_MOTIVO", "SUBSTITUIDA"}
        ]

        def chave(c: Caminho) -> float:
            urgencia = float(contexto.get(c.id, 0.0))
            return (
                0.35 * c.valor_multiplicador
                + 0.25 * c.reversibilidade
                + 0.20 * urgencia
                + 0.20 * c.incerteza
                - 0.25 * c.risco
            )

        return tuple(sorted(candidatos, key=chave, reverse=True))

    def descobrir_impulsos(self) -> dict[str, tuple[str, ...]]:
        """Mostra onde relações de impulso/multiplicação podem abrir caminhos."""
        return {
            c.id: self.habilitados_por(c.id)
            for c in self._caminhos
            if self.habilitados_por(c.id)
        }
