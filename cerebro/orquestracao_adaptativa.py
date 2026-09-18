from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .agendador import AgendadorAdaptativo
from .grafo_tarefas import GrafoTarefas, NoTarefa
from .sinergia import DetectorSinergia, ResultadoCombinacao as EvidenciaCombinacao


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
    """Fachada compatível para orquestração; seleção e replanejamento vivem no scheduler."""

    grafo: GrafoTarefas
    recursos: dict[str, Recurso] = field(default_factory=dict)
    resultados: list[ResultadoCombinacao] = field(default_factory=list)
    sinergias: list[Sinergia] = field(default_factory=list)
    decisoes: list[dict[str, object]] = field(default_factory=list)
    agendador: AgendadorAdaptativo | None = None
    detector_sinergia: DetectorSinergia | None = None

    def __post_init__(self) -> None:
        if self.agendador is None:
            self.agendador = AgendadorAdaptativo(self.grafo)

    def alocar(self, ids: Iterable[str]) -> dict[str, float]:
        uso: dict[str, float] = {}
        for tarefa_id in ids:
            for recurso in self.grafo.tarefas[tarefa_id].recursos:
                uso[recurso] = uso.get(recurso, 0.0) + 1.0
        return uso

    def plano_adaptativo(self, recursos_disponiveis: set[str] | None = None, *, orcamento: float | None = None, capacidade_de_tempo: float | None = None, limite: int | None = None) -> tuple[NoTarefa, ...]:
        capacidades = {rid: recurso.capacidade for rid, recurso in self.recursos.items()}
        plano = self.agendador.planejar(recursos_disponiveis, orcamento=orcamento, limite=limite, capacidades_recursos=capacidades, capacidade_de_tempo=capacidade_de_tempo)
        self._sincronizar_decisoes()
        return plano.tarefas

    def replanejar_apos_resultado(self, tarefa_id: str, sucesso: bool, **kwargs: object) -> tuple[NoTarefa, ...]:
        """Registra resultado, alimenta evidência de combinação e replaneja em um único ciclo.

        As métricas de combinação são opcionais. Quando fornecidas, tornam o resultado
        observável pelo detector de sinergia; quando ausentes, o scheduler ainda
        aprende com o resultado da tarefa e replaneja normalmente.
        """
        resultado_keys = {"observacao", "custo_real", "tempo_real", "qualidade", "evidencia", "contexto", "aprendizado", "fallback_tarefa_id", "reintentar"}
        planejamento_keys = {"recursos_disponiveis", "orcamento", "limite", "objetivo", "capacidades_recursos", "capacidade_de_tempo"}
        capacidades = tuple(str(x) for x in kwargs.pop("capacidades", ()) or ())
        valor_observado = kwargs.pop("valor_observado", None)
        custo_observado = kwargs.pop("custo_observado", kwargs.get("custo_real", 0.0))
        tempo_observado = kwargs.pop("tempo_observado", kwargs.get("tempo_real", 0.0))
        qualidade_observada = kwargs.pop("qualidade_observada", kwargs.get("qualidade", 0.0))
        contexto_combinacao = dict(kwargs.pop("contexto_combinacao", kwargs.get("contexto", {})) or {})

        self.agendador.registrar_resultado(
            tarefa_id,
            sucesso,
            **{k: v for k, v in kwargs.items() if k in resultado_keys},
        )

        if self.detector_sinergia is not None and capacidades and valor_observado is not None:
            self.detector_sinergia.registrar(
                EvidenciaCombinacao(
                    combinacao_id=f"execucao:{tarefa_id}:{len(self.detector_sinergia.resultados) + 1}",
                    capacidades=capacidades,
                    valor_observado=float(valor_observado),
                    custo_observado=float(custo_observado or 0.0),
                    tempo_observado=float(tempo_observado or 0.0),
                    qualidade=float(qualidade_observada or 0.0),
                    contexto={str(k): str(v) for k, v in contexto_combinacao.items()},
                )
            )

        plano = self.agendador.replanejar(
            **{k: v for k, v in kwargs.items() if k in planejamento_keys},
            motivo=f"resultado de {tarefa_id}: {'sucesso' if sucesso else 'falha'}",
        )
        self._sincronizar_decisoes()
        return plano.tarefas

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

    def decisões_guardadas(self, tarefas: Iterable[NoTarefa], custo: float, tempo: float, *, motivo: str = "otimização sob restrições atuais") -> None:
        self.decisoes.append({"tarefas": [t.id for t in tarefas], "custo": custo, "tempo": tempo, "motivo": motivo})

    def _sincronizar_decisoes(self) -> None:
        self.decisoes = [{"tarefas": e.get("tarefas", []), "custo": e.get("custo", 0.0), "tempo": e.get("tempo", 0.0), "motivo": e.get("motivo", "")} for e in self.agendador.historico if e.get("evento") in {"PLANEJAMENTO", "REPLANEJAMENTO"}]
