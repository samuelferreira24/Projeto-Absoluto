from __future__ import annotations

from typing import Any, Callable, Iterable

from .orquestrador import Missao, Orquestrador


class CicloContinuo:
    """Executa um ciclo orientado à missão a partir de caminhos candidatos.

    O ciclo escolhe o candidato de maior pontuação e entrega somente o caminho
    escolhido ao executor. A identidade, persistência e idempotência do ciclo
    continuam pertencendo ao Orquestrador.
    """

    def __init__(self, orquestrador: Orquestrador) -> None:
        self.orquestrador = orquestrador

    def rodar(
        self,
        missao_id: str,
        candidatos: Callable[[Missao], Iterable[tuple[Any, float]]],
        executor: Callable[[Missao, Any], dict[str, Any]],
    ) -> dict[str, Any]:
        if missao_id not in self.orquestrador.missoes:
            raise KeyError(missao_id)
        missao = self.orquestrador.missoes[missao_id]
        opcoes = list(candidatos(missao))
        if not opcoes:
            raise RuntimeError(f"nenhum caminho candidato para a missão: {missao_id}")

        caminho, pontuacao = max(opcoes, key=lambda item: item[1])

        resultado = self.orquestrador.executar_um_ciclo(
            missao_id,
            lambda m: executor(m, caminho),
        )
        resultado["caminho"] = caminho
        resultado["pontuacao"] = pontuacao
        resultado["observacao"] = {
            "estado": resultado.get("resultado", {}).get("state") if isinstance(resultado.get("resultado"), dict) else None,
            "caminho": caminho,
            "pontuacao": pontuacao,
        }
        return resultado

    def reavaliar(
        self,
        missao_id: str,
        candidatos: Callable[[Missao], Iterable[tuple[Any, float]]],
        *,
        observacao: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Recompute candidate ordering from the current mission state and observation."""
        if missao_id not in self.orquestrador.missoes:
            raise KeyError(missao_id)
        missao = self.orquestrador.missoes[missao_id]
        if observacao:
            missao.contexto = {
                **missao.contexto,
                "_ultima_observacao": dict(observacao),
            }
            missao.atualizar()
            self.orquestrador.salvar()
        opcoes = list(candidatos(missao))
        if not opcoes:
            return {"reavaliado": True, "opcoes": [], "proximo": None}
        ordenadas = sorted(opcoes, key=lambda item: item[1], reverse=True)
        return {
            "reavaliado": True,
            "opcoes": [{"caminho": caminho, "pontuacao": score} for caminho, score in ordenadas],
            "proximo": ordenadas[0][0],
        }
