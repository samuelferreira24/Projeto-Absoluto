from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .semantica import RelacaoSemantica, UnidadeSemantica, validar_unidades


@dataclass
class ResultadoAuditoria:
    ok: bool
    erros: list[str] = field(default_factory=list)
    avisos: list[str] = field(default_factory=list)
    metricas: dict[str, Any] = field(default_factory=dict)


def auditar_semantica(
    unidades: list[UnidadeSemantica],
    relacoes: list[RelacaoSemantica] | None = None,
) -> ResultadoAuditoria:
    relacoes = relacoes or []
    erros = validar_unidades(unidades, relacoes)
    avisos: list[str] = []

    por_tipo: dict[str, int] = {}
    derivados = 0
    sem_proveniencia = 0
    for unidade in unidades:
        por_tipo[unidade.kind] = por_tipo.get(unidade.kind, 0) + 1
        if unidade.is_derived:
            derivados += 1
        if not unidade.provenance:
            sem_proveniencia += 1

    if not unidades:
        avisos.append("Nenhuma unidade semântica foi fornecida")
    if sem_proveniencia:
        avisos.append(f"{sem_proveniencia} unidade(s) sem proveniência")
    if derivados and derivados == len(unidades):
        avisos.append("Todas as unidades são derivadas; verificar se a fonte original está preservada")

    return ResultadoAuditoria(
        ok=not erros,
        erros=erros,
        avisos=avisos,
        metricas={
            "unidades": len(unidades),
            "relacoes": len(relacoes),
            "derivadas": derivados,
            "por_tipo": por_tipo,
        },
    )
