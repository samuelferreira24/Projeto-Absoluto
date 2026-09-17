from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .grafo_tarefas import EstadoTarefa, GrafoTarefas, NoTarefa


@dataclass(frozen=True)
class Recurso:
    id: str
    disponivel: float = 0.0
    custo_unidade: float = 0.0
    capacidade: float = 1.0


@dataclass(frozen=True)
class ResultadoCombinacao:
    tarefas: tuple[str, ...]
    resultado: float
    custo: float
    tempo: float
    qualidade: float


@dataclass(frozen=True)
class Sinergia:
    fatores: tuple[str, ...]
    ganho_observado: float
    confianca: float
    observacoes: tuple[str, ...] = ()


@dataclass
class OrquestradorAdaptativo:
    """Coordena tarefas sob restrições e aprende com combinações executadas."""

    grafo: GrafoTarefas
    recursos: dict[str, Recurso] = field(default_factory=dict)
    resultados: list[ResultadoCombinacao] = field(default_factory=list)
    sinergias: list[Sinergia] = field(default_factory=list)
    decisoes: list[dict[str, object]] = field(default_factory=list)

    def alocar(self, ids: Iterable[str]) -> dict[str, float]:
        uso: dict[str, float] = {}
        for tarefa_id in ids:
            tarefa = self.grafo.tarefas[tarefa_id]
            for recurso in tarefa.recursos:
                uso[recurso] = uso.get(recurso, 0.0) + 1.0
        return uso

    def plano_adaptativo(
        self,
        recursos_disponiveis: set[str] | None = None,
        *,
        orcamento: float | None = None,
        capacidade_de_tempo: float | None = None,
        limite: int | None = None,
    ) -> tuple[NoTarefa, ...]:
        prontas = self.grafo.prontas(recursos_disponiveis)
        escolhidas: list[NoTarefa] = []
        usados: set[str] = set()
        uso_por_recurso: dict[str, float] = {}
        custo = 0.0
        duracoes: list[float] = []
        for tarefa in sorted(prontas, key=self._chave):
            if limite is not None and len(escolhidas) >= limite:
                break
            if set(tarefa.recursos) & usados:
                continue
            if not self._recursos_suportam(tarefa, uso_por_recurso):
                continue
            if orcamento is not None and custo + max(0.0, tarefa.custo_estimado) > orcamento:
                continue
            if capacidade_de_tempo is not None and tempo + max(0.0, tarefa.tempo_estimado) > capacidade_de_tempo:
                continue
            escolhidas.append(tarefa)
            usados.update(tarefa.recursos)
            for recurso in tarefa.recursos:
                uso_por_recurso[recurso] = uso_por_recurso.get(recurso, 0.0) + 1.0
            custo += max(0.0, tarefa.custo_estimado)
            duracoes.append(max(0.0, tarefa.tempo_estimado))
        tempo = max(duracoes, default=0.0)
        self.decisões_guardadas(escolhidas, custo, tempo)
        return tuple(escolhidas)

    def _recursos_suportam(self, tarefa: NoTarefa, uso: dict[str, float]) -> bool:
        for recurso_id in tarefa.recursos:
            recurso = self.recursos.get(recurso_id)
            if recurso is None:
                continue
            if uso.get(recurso_id, 0.0) + 1.0 > max(0.0, recurso.capacidade):
                return False
        return True

    def registrar_resultado(self, tarefas: Iterable[str], resultado: float, custo: float, tempo: float, qualidade: float) -> Sinergia | None:
        fatores = tuple(sorted(tarefas))
        self.resultados.append(ResultadoCombinacao(fatores, resultado, custo, tempo, qualidade))
        if len(fatores) < 2:
            return None
        base = [r for r in self.resultados if len(r.tarefas) == 1 and r.tarefas[0] in fatores]
        if len(base) < 2:
            return None
        baseline = sum(r.resultado for r in base) / len(base)
        ganho = resultado - baseline
        confianca = min(1.0, len(base) / len(fatores))
        sinergia = Sinergia(fatores, ganho, confianca, ("comparação contra resultados individuais disponíveis",))
        self.sinergias.append(sinergia)
        return sinergia

    def replanejar_apos_resultado(self, tarefa_id: str, sucesso: bool, **kwargs: object) -> tuple[NoTarefa, ...]:
        self.grafo.marcar(tarefa_id, EstadoTarefa.CONCLUIDA if sucesso else EstadoTarefa.FALHOU)
        self.decisões_guardadas([], 0.0, 0.0, motivo=f"resultado de {tarefa_id}: {'sucesso' if sucesso else 'falha'}")
        return self.plano_adaptativo(**kwargs)

    def decisões_guardadas(self, tarefas: Iterable[NoTarefa], custo: float, tempo: float, *, motivo: str = "otimização sob restrições atuais") -> None:
        self.decisões.append({
            "tarefas": [t.id for t in tarefas],
            "custo": custo,
            "tempo": tempo,
            "motivo": motivo,
        })

    @staticmethod
    def _chave(tarefa: NoTarefa) -> tuple[float, float, float, str]:
        valor = tarefa.valor_estimado if tarefa.valor_estimado > 0 else tarefa.prioridade
        custo = max(tarefa.custo_estimado, 1.0)
        risco = max(0.0, min(1.0, tarefa.risco))
        urgencia = 1.0 / max(1.0, tarefa.prazo) if tarefa.prazo is not None else 1.0
        score = valor * urgencia * (1.0 - risco) / custo
        return (-score, -tarefa.prioridade, tarefa.tempo_estimado, tarefa.id)
