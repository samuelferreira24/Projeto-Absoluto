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
    """Escolhe, executa, aprende e reavalia tarefas preservando a história."""

    def __init__(self, grafo: GrafoTarefas) -> None:
        self.grafo = grafo
        self.historico: list[dict[str, object]] = []
        self.perfis: dict[str, dict[str, float]] = {}

    @staticmethod
    def pontuacao(tarefa: NoTarefa, perfil: dict[str, float] | None = None) -> float:
        """Valor marginal ajustado por risco, custo, prazo e experiência observada."""
        perfil = perfil or {}
        valor = tarefa.valor_estimado if tarefa.valor_estimado > 0 else tarefa.prioridade
        custo = tarefa.custo_estimado if tarefa.custo_estimado > 0 else 1.0
        risco = max(0.0, min(1.0, tarefa.risco))
        urgencia = 1.0 / max(1.0, tarefa.prazo) if tarefa.prazo is not None else 1.0
        confiabilidade_observada = perfil.get("confiabilidade", 1.0)
        fator_tempo = perfil.get("fator_tempo", 1.0)
        return (valor * urgencia * (1.0 - risco) * confiabilidade_observada) / (custo * max(0.1, fator_tempo))

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

        ordenadas = sorted(
            prontas,
            key=lambda t: (-self.pontuacao(t, self.perfis.get(t.id)), -t.prioridade, t.id),
        )
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
            perfil = self.perfis.get(tarefa.id, {})
            tempo_tarefa = max(0.0, tarefa.tempo_estimado) * perfil.get("fator_tempo", 1.0)
            selecionadas.append(tarefa)
            usados.update(recursos)
            custo += custo_tarefa
            valor += max(0.0, tarefa.valor_estimado or tarefa.prioridade)
            risco += max(0.0, min(1.0, tarefa.risco))
            tempo += tempo_tarefa
            prioridade += tarefa.prioridade

        plano = PlanoExecucao(
            tuple(selecionadas),
            custo,
            valor,
            prioridade,
            risco / len(selecionadas) if selecionadas else 0.0,
            tempo,
            "valor marginal ajustado por risco/custo/prazo + experiência + paralelismo por recursos",
        )
        self._registrar_historico(plano, evento="PLANEJAMENTO")
        return plano

    def executar_inicio(self, plano: PlanoExecucao) -> None:
        for tarefa in plano.tarefas:
            self.grafo.marcar(tarefa.id, EstadoTarefa.EXECUTANDO)
        self._registrar_historico(plano, evento="INICIO_EXECUCAO")

    def registrar_resultado(
        self,
        tarefa_id: str,
        sucesso: bool,
        *,
        observacao: str | None = None,
        custo_real: float | None = None,
        tempo_real: float | None = None,
        qualidade: float | None = None,
    ) -> None:
        """Registra o resultado e atualiza um perfil local para o próximo planejamento."""
        tarefa = self.grafo.tarefas[tarefa_id]
        self.grafo.marcar(tarefa_id, EstadoTarefa.CONCLUIDA if sucesso else EstadoTarefa.FALHOU)
        perfil = self.perfis.setdefault(tarefa_id, {"execucoes": 0.0, "sucessos": 0.0, "confiabilidade": 1.0, "fator_tempo": 1.0})
        perfil["execucoes"] += 1.0
        if sucesso:
            perfil["sucessos"] += 1.0
        perfil["confiabilidade"] = perfil["sucessos"] / perfil["execucoes"]
        if tempo_real is not None and tarefa.tempo_estimado > 0:
            observado = max(0.1, tempo_real / tarefa.tempo_estimado)
            perfil["fator_tempo"] = (perfil["fator_tempo"] * (perfil["execucoes"] - 1.0) + observado) / perfil["execucoes"]
        self.historico.append({
            "evento": "RESULTADO",
            "tarefa": tarefa_id,
            "sucesso": sucesso,
            "observacao": observacao or "",
            "custo_real": custo_real,
            "tempo_real": tempo_real,
            "qualidade": qualidade,
            "perfil_atualizado": dict(perfil),
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
        """Recalcula a partir do estado atual e da experiência observada."""
        plano = self.planejar(recursos_disponiveis, **kwargs)
        self.historico.append({
            "evento": "REPLANEJAMENTO",
            "tarefas": [t.id for t in plano.tarefas],
            "motivo": "estado do grafo, resultados, experiência ou recursos alterados",
        })
        return plano

    def perfil_tarefa(self, tarefa_id: str) -> dict[str, float]:
        return dict(self.perfis.get(tarefa_id, {}))

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
