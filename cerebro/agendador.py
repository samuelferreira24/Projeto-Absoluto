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
    valor_estimado: float
    prioridade_total: float
    risco_estimado: float
    tempo_estimado: float
    motivo: str


class AgendadorAdaptativo:
    """Escolhe, executa e reavalia tarefas preservando a história das decisões."""

    def __init__(self, grafo: GrafoTarefas) -> None:
        self.grafo = grafo
        self.historico: list[dict[str, object]] = []

    @staticmethod
    def pontuacao(tarefa: NoTarefa) -> float:
        """Valor marginal aproximado para o contexto atual."""
        valor = tarefa.valor_estimado if tarefa.valor_estimado > 0 else tarefa.prioridade
        custo = tarefa.custo_estimado if tarefa.custo_estimado > 0 else 1.0
        risco = max(0.0, min(1.0, tarefa.risco))
        # V0.1: prazo menor significa maior urgência quando prazo é tratado
        # como uma janela restante positiva; sem prazo, urgência neutra.
        urgencia = 1.0 / max(1.0, tarefa.prazo) if tarefa.prazo is not None else 1.0
        return (valor * urgencia * (1.0 - risco)) / custo

    def planejar(
        self,
        recursos_disponiveis: set[str] | None = None,
        *,
        orcamento: float | None = None,
        limite: int | None = None,
    ) -> PlanoExecucao:
        prontas = self.grafo.prontas(recursos_disponiveis)
        if not prontas:
            plano = PlanoExecucao((), 0.0, 0.0, 0.0, 0.0, 0.0, "nenhuma tarefa pronta")
            self._registrar_historico(plano, evento="PLANEJAMENTO")
            return plano

        ordenadas = sorted(prontas, key=lambda t: (-self.pontuacao(t), -t.prioridade, t.id))
        selecionadas: list[NoTarefa] = []
        usados: set[str] = set()
        custo = valor = risco = tempo = prioridade = 0.0
        for tarefa in ordenadas:
            if limite is not None and len(selecionadas) >= limite:
                break
            recursos = set(tarefa.recursos)
            if recursos & usados:
                continue
            custo_tarefa = max(0.0, tarefa.custo_estimado)
            if custo_tarefa == 0.0:
                custo_tarefa = 1.0 / max(tarefa.prioridade, 0.1)
            if orcamento is not None and custo + custo_tarefa > orcamento:
                continue
            selecionadas.append(tarefa)
            usados.update(recursos)
            custo += custo_tarefa
            valor += max(0.0, tarefa.valor_estimado or tarefa.prioridade)
            risco += max(0.0, min(1.0, tarefa.risco))
            tempo += max(0.0, tarefa.tempo_estimado)
            prioridade += tarefa.prioridade

        plano = PlanoExecucao(
            tuple(selecionadas),
            custo,
            valor,
            prioridade,
            risco / len(selecionadas) if selecionadas else 0.0,
            tempo,
            "valor marginal ajustado por risco/custo/prazo + paralelismo por recursos",
        )
        self._registrar_historico(plano, evento="PLANEJAMENTO")
        return plano

    def executar_inicio(self, plano: PlanoExecucao) -> None:
        for tarefa in plano.tarefas:
            self.grafo.marcar(tarefa.id, EstadoTarefa.EXECUTANDO)
        self._registrar_historico(plano, evento="INICIO_EXECUCAO")

    def registrar_resultado(self, tarefa_id: str, sucesso: bool, *, observacao: str | None = None) -> None:
        """Registra o resultado sem apagar o contexto que levou à decisão."""
        self.grafo.marcar(tarefa_id, EstadoTarefa.CONCLUIDA if sucesso else EstadoTarefa.FALHOU)
        self.historico.append({
            "evento": "RESULTADO",
            "tarefa": tarefa_id,
            "sucesso": sucesso,
            "observacao": observacao or "",
        })

    def retentar_tarefa(self, tarefa_id: str, *, motivo: str = "nova tentativa") -> None:
        """Reabre uma tarefa que falhou sem apagar o registro da falha anterior."""
        tarefa = self.grafo.tarefas[tarefa_id]
        if tarefa.estado != EstadoTarefa.FALHOU:
            raise ValueError(f"Só é possível retentar tarefa FALHOU: {tarefa_id}")
        self.grafo.marcar(tarefa_id, EstadoTarefa.PENDENTE)
        self.historico.append({
            "evento": "RETRY",
            "tarefa": tarefa_id,
            "motivo": motivo,
        })

    def replanejar(self, recursos_disponiveis: set[str] | None = None, **kwargs: object) -> PlanoExecucao:
        """Recalcula a partir do estado atual, preservando as decisões anteriores."""
        plano = self.planejar(recursos_disponiveis, **kwargs)
        self.historico.append({
            "evento": "REPLANEJAMENTO",
            "tarefas": [t.id for t in plano.tarefas],
            "motivo": "estado do grafo, resultado ou recursos alterados",
        })
        return plano

    def _registrar_historico(self, plano: PlanoExecucao, *, evento: str) -> None:
        self.historico.append({
            "evento": evento,
            "tarefas": [t.id for t in plano.tarefas],
            "custo": plano.custo_estimado,
            "valor": plano.valor_estimado,
            "prioridade": plano.prioridade_total,
            "risco": plano.risco_estimado,
            "tempo": plano.tempo_estimado,
            "motivo": plano.motivo,
        })
