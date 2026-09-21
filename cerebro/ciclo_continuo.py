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
        return resultado
