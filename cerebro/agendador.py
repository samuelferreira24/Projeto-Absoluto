from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .grafo_tarefas import EstadoTarefa, GrafoTarefas, NoTarefa


@dataclass(frozen=True)
class PerfilRecurso:
    id: str
    capacidade: float = 1.0
    custo: float = 0.0


@dataclass(frozen=True)
class PlanoExecucao:
    tarefas: tuple[NoTarefa, ...]
    custo_estimado: float
    prioridade_total: float
    motivo: str


class AgendadorAdaptativo:
    """Seleciona o próximo lote considerando valor, custo, risco e recursos."""

    def __init__(self, grafo: GrafoTarefas) -> None:
        self.grafo = grafo
        self.historico: list[dict[str, object]] = []

    def planejar(
        self,
        recursos_disponiveis: set[str] | None = None,
        *,
        orcamento: float | None = None,
        limite: int | None = None,
    ) -> PlanoExecucao:
        prontas = self.grafo.prontas(recursos_disponiveis)
        if not prontas:
            return PlanoExecucao((), 0.0, 0.0, "nenhuma tarefa pronta")

        selecionadas: list[NoTarefa] = []
        usados: set[str] = set()
        custo = 0.0
        for tarefa in prontas:
            if limite is not None and len(selecionadas) >= limite:
                break
            recursos = set(tarefa.recursos)
            if recursos & usados:
                continue
            custo_tarefa = max(0.0, 1.0 / max(tarefa.prioridade, 0.1))
            if orcamento is not None and custo + custo_tarefa > orcamento:
                continue
            selecionadas.append(tarefa)
            usados.update(recursos)
            custo += custo_tarefa

        plano = PlanoExecucao(
            tuple(selecionadas),
            custo,
            sum(t.prioridade for t in selecionadas),
            "valor-prioridade com exclusão de conflitos de recurso",
        )
        self.historico.append({
            "tarefas": [t.id for t in plano.tarefas],
            "custo": plano.custo_estimado,
            "prioridade": plano.prioridade_total,
            "motivo": plano.motivo,
        })
        return plano

    def executar_inicio(self, plano: PlanoExecucao) -> None:
        for tarefa in plano.tarefas:
            self.grafo.marcar(tarefa.id, EstadoTarefa.EXECUTANDO)

    def registrar_resultado(self, tarefa_id: str, sucesso: bool) -> None:
        self.grafo.marcar(tarefa_id, EstadoTarefa.CONCLUIDA if sucesso else EstadoTarefa.FALHOU)

    def replanejar(self, recursos_disponiveis: set[str] | None = None, **kwargs: object) -> PlanoExecucao:
        """Recalcula o plano a partir do estado atual do grafo, sem apagar o histórico."""
        return self.planejar(recursos_disponiveis, **kwargs)
