from __future__ import annotations

from dataclasses import dataclass, field
from itertools import combinations
from statistics import mean


@dataclass(frozen=True)
class ResultadoCombinacao:
    combinacao_id: str
    capacidades: tuple[str, ...]
    valor_observado: float
    custo_observado: float
    tempo_observado: float
    qualidade: float
    contexto: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class SinalSinergia:
    capacidades: tuple[str, ...]
    ganho_relativo: float
    confianca: float
    evidencias: int
    explicacao: str


class DetectorSinergia:
    """Aprende combinações úteis comparando resultados observados com bases individuais."""

    def __init__(self) -> None:
        self.resultados: list[ResultadoCombinacao] = []

    def registrar(self, resultado: ResultadoCombinacao) -> None:
        self.resultados.append(resultado)

    def detectar(self, *, minimo_evidencias: int = 2) -> list[SinalSinergia]:
        grupos: dict[tuple[str, ...], list[ResultadoCombinacao]] = {}
        for resultado in self.resultados:
            chave = tuple(sorted(set(resultado.capacidades)))
            if len(chave) >= 2:
                grupos.setdefault(chave, []).append(resultado)

        sinais: list[SinalSinergia] = []
        for capacidades, resultados in grupos.items():
            if len(resultados) < minimo_evidencias:
                continue
            ganhos: list[float] = []
            for resultado in resultados:
                base = self._melhor_base_individual(capacidades, resultado.contexto)
                if base is None or base <= 0:
                    continue
                ganhos.append((resultado.valor_observado / base) - 1.0)
            if not ganhos:
                continue
            ganho = mean(ganhos)
            confianca = min(1.0, len(ganhos) / 5.0) * min(1.0, max(0.0, 1.0 + ganho))
            sinais.append(SinalSinergia(
                capacidades=capacidades,
                ganho_relativo=ganho,
                confianca=confianca,
                evidencias=len(ganhos),
                explicacao="ganho médio da combinação sobre a melhor referência individual disponível",
            ))
        return sorted(sinais, key=lambda s: (-s.ganho_relativo, -s.confianca, s.capacidades))

    def _melhor_base_individual(self, capacidades: tuple[str, ...], contexto: dict[str, str]) -> float | None:
        valores: list[float] = []
        alvo = set(contexto.items())
        for resultado in self.resultados:
            if len(resultado.capacidades) != 1:
                continue
            if resultado.capacidades[0] not in capacidades:
                continue
            if alvo and set(resultado.contexto.items()) != alvo:
                continue
            valores.append(resultado.valor_observado)
        return max(valores) if valores else None

    def combinações_promissoras(self, capacidades: list[str], *, limite: int = 20) -> list[tuple[str, ...]]:
        """Gera candidatos não testados a partir das capacidades conhecidas."""
        existentes = {tuple(sorted(set(r.capacidades))) for r in self.resultados}
        candidatos = [c for c in combinations(sorted(set(capacidades)), 2) if c not in existentes]
        return candidatos[:limite]
