from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .agendador import PlanoExecucao
from .grafo_tarefas import EstadoTarefa, GrafoTarefas


@dataclass(frozen=True)
class CenarioSimulacao:
    nome: str
    fator_tempo: float = 1.0
    fator_custo: float = 1.0
    fator_risco: float = 1.0


@dataclass(frozen=True)
class ResultadoSimulacao:
    cenario: str
    tarefas: tuple[str, ...]
    executaveis: bool
    makespan: float
    custo: float
    risco_medio: float
    valor_esperado: float
    robustez: float
    bloqueios: tuple[str, ...] = ()


class SimuladorOrquestracao:
    """Avalia planos sem alterar o grafo real."""

    def __init__(self, grafo: GrafoTarefas) -> None:
        self.grafo = grafo

    def simular(self, plano: PlanoExecucao, cenarios: Iterable[CenarioSimulacao] | None = None) -> list[ResultadoSimulacao]:
        cenarios = tuple(cenarios or (
            CenarioSimulacao("BASE"),
            CenarioSimulacao("LENTO", fator_tempo=1.25),
            CenarioSimulacao("CUSTO_ALTO", fator_custo=1.25),
            CenarioSimulacao("RISCO_ALTO", fator_risco=1.25),
        ))
        return [self._simular_cenario(plano, cenario) for cenario in cenarios]

    def selecionar_robusto(self, planos: Iterable[PlanoExecucao], cenarios: Iterable[CenarioSimulacao] | None = None) -> tuple[PlanoExecucao | None, dict[str, object]]:
        candidatos = list(planos)
        avaliados: list[tuple[float, PlanoExecucao, list[ResultadoSimulacao]]] = []
        for plano in candidatos:
            resultados = self.simular(plano, cenarios)
            validos = [r for r in resultados if r.executaveis]
            if not validos:
                continue
            score = sum(r.valor_esperado - r.custo - r.makespan - r.risco_medio for r in validos) / len(validos)
            robustez = sum(r.robustez for r in validos) / len(validos)
            avaliados.append((score + robustez, plano, resultados))
        if not avaliados:
            return None, {"avaliados": 0, "motivo": "nenhum plano robusto"}
        _, escolhido, resultados = max(avaliados, key=lambda x: (x[0], -x[1].risco_estimado, -x[1].custo_estimado))
        return escolhido, {
            "avaliados": len(avaliados),
            "escolhido": [t.id for t in escolhido.tarefas],
            "resultados": [r.__dict__ for r in resultados],
        }

    def _simular_cenario(self, plano: PlanoExecucao, cenario: CenarioSimulacao) -> ResultadoSimulacao:
        ids = {t.id for t in plano.tarefas}
        bloqueios: list[str] = []
        for tarefa in plano.tarefas:
            for dep in tarefa.depende_de:
                if dep in ids:
                    continue
                if dep in self.grafo.tarefas and self.grafo.tarefas[dep].estado != EstadoTarefa.CONCLUIDA:
                    bloqueios.append(f"{tarefa.id}: dependência {dep} não concluída")
        if bloqueios:
            return ResultadoSimulacao(cenario.nome, tuple(ids), False, 0.0, 0.0, 1.0, 0.0, 0.0, tuple(bloqueios))
        duracoes = [max(0.0, t.tempo_estimado) * cenario.fator_tempo for t in plano.tarefas]
        custos = [max(0.0, t.custo_estimado) * cenario.fator_custo for t in plano.tarefas]
        riscos = [min(1.0, max(0.0, t.risco * cenario.fator_risco)) for t in plano.tarefas]
        valor = sum(max(0.0, t.valor_estimado + t.oportunidade) for t in plano.tarefas)
        risco_medio = sum(riscos) / len(riscos) if riscos else 0.0
        makespan = sum(duracoes) if plano.modo_execucao == "SEQUENCIAL" else max(duracoes, default=0.0)
        custo = sum(custos)
        valor_esperado = valor * (1.0 - risco_medio)
        robustez = max(0.0, 1.0 - ((cenario.fator_tempo - 1.0) + (cenario.fator_custo - 1.0) + (cenario.fator_risco - 1.0)))
        return ResultadoSimulacao(cenario.nome, tuple(t.id for t in plano.tarefas), True, makespan, custo, risco_medio, valor_esperado, robustez)
