from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .orquestrador import Missao, Orquestrador


@dataclass(frozen=True)
class DecisaoCiclo:
    executar: bool
    caminho: str | None = None
    motivo: str = ""


class CicloContinuo:
    """Executa ciclos recuperáveis sem transformar a rede em fila fixa."""

    def __init__(self, orquestrador: Orquestrador) -> None:
        self.orquestrador = orquestrador

    def decidir(
        self,
        missao: Missao,
        candidatos: Callable[[Missao], list[tuple[str, float]]],
    ) -> DecisaoCiclo:
        opcoes = candidatos(missao)
        if not opcoes:
            return DecisaoCiclo(False, motivo="nenhum caminho contextual disponível")
        caminho, sinal = max(opcoes, key=lambda item: item[1])
        return DecisaoCiclo(True, caminho=caminho, motivo=f"sinal contextual={sinal:.4f}")

    def rodar(
        self,
        missao_id: str,
        candidatos: Callable[[Missao], list[tuple[str, float]]],
        executor: Callable[[Missao, str], dict[str, Any]],
    ) -> dict[str, Any]:
        missao = self.orquestrador.missoes[missao_id]
        decisao = self.decidir(missao, candidatos)
        self.orquestrador._registrar(missao_id, "DECISAO", "CONCLUIDA", vars(decisao))
        if not decisao.executar or decisao.caminho is None:
            self.orquestrador.salvar()
            return {"executado": False, "motivo": decisao.motivo}
        return self.orquestrador.executar_um_ciclo(
            missao_id,
            lambda m: executor(m, decisao.caminho),
        )
