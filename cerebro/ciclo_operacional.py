from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Protocol

from .orquestrador import Missao, Orquestrador


@dataclass(frozen=True)
class DecisaoOperacional:
    """Decisão de um agente/capacidade sobre o próximo passo da missão."""

    executar: bool
    concluida: bool = False
    acao: str | None = None
    ferramenta: str | None = None
    recurso: str | None = None
    argumentos: dict[str, Any] = field(default_factory=dict)
    motivo: str = ""


@dataclass(frozen=True)
class ResultadoOperacional:
    """Evidência retornada por uma capacidade executora."""

    sucesso: bool
    observacao: str = ""
    dados: dict[str, Any] = field(default_factory=dict)
    evidencia: str | None = None
    aprendizado: str | None = None


class DecisorOperacional(Protocol):
    def decidir(self, missao: Missao) -> DecisaoOperacional: ...


class ExecutorOperacional(Protocol):
    def executar(self, missao: Missao, decisao: DecisaoOperacional) -> ResultadoOperacional: ...


class CicloOperacional:
    """Condutor de ciclos orientados a objetivo.

    O Cérebro conduz a continuidade e o estado. Inteligências, ferramentas e
    executores são capacidades injetáveis e substituíveis. A sequência concreta
    do trabalho não é codificada aqui: cada decisão pode escolher o próximo
    passo a partir do estado atual da missão.
    """

    def __init__(self, orquestrador: Orquestrador) -> None:
        self.orquestrador = orquestrador

    def executar(
        self,
        missao_id: str,
        decisor: DecisorOperacional,
        executor: ExecutorOperacional,
        *,
        limite_ciclos: int = 20,
    ) -> list[dict[str, Any]]:
        if limite_ciclos <= 0:
            raise ValueError("limite_ciclos deve ser positivo")
        if missao_id not in self.orquestrador.missoes:
            raise KeyError(missao_id)

        historico: list[dict[str, Any]] = []
        for numero in range(1, limite_ciclos + 1):
            missao = self.orquestrador.missoes[missao_id]
            if missao.estado != "ATIVA":
                break

            decisao = decisor.decidir(missao)
            self.orquestrador._registrar(
                missao_id,
                "DECISAO_OPERACIONAL",
                "CONCLUIDA",
                {"numero_ciclo": numero, **vars(decisao)},
            )

            if decisao.concluida:
                missao.atualizar(estado="CONCLUIDA", resultado={"motivo": decisao.motivo})
                self.orquestrador.salvar()
                historico.append({"ciclo": numero, "decisao": vars(decisao), "concluida": True})
                break

            if not decisao.executar:
                missao.atualizar(estado="PAUSADA", resultado={"motivo": decisao.motivo})
                self.orquestrador._registrar(
                    missao_id, "CICLO_OPERACIONAL", "PAUSADO",
                    {"numero_ciclo": numero, "motivo": decisao.motivo},
                )
                self.orquestrador.salvar()
                historico.append({"ciclo": numero, "decisao": vars(decisao), "pausada": True})
                break

            resultado = executor.executar(missao, decisao)
            payload = {
                "numero_ciclo": numero,
                "acao": decisao.acao,
                "ferramenta": decisao.ferramenta,
                "sucesso": resultado.sucesso,
                "observacao": resultado.observacao,
                "dados": resultado.dados,
                "evidencia": resultado.evidencia,
                "aprendizado": resultado.aprendizado,
            }
            self.orquestrador._registrar(
                missao_id,
                "RESULTADO_OPERACIONAL",
                "CONCLUIDO" if resultado.sucesso else "FALHOU",
                payload,
            )
            missao.contexto = {
                **missao.contexto,
                "ultimo_resultado": payload,
                "ultimo_aprendizado": resultado.aprendizado,
            }
            missao.atualizar(resultado=payload)
            self.orquestrador.salvar()
            historico.append({"ciclo": numero, "decisao": vars(decisao), "resultado": vars(resultado)})

            # A decisão seguinte recebe o resultado incorporado ao estado.
            # Falha não encerra automaticamente a missão: o decisor pode
            # escolher retry, fallback, investigação ou pausa no próximo ciclo.

        else:
            self.orquestrador._registrar(
                missao_id,
                "CICLO_OPERACIONAL",
                "LIMITE_CICLOS",
                {"limite_ciclos": limite_ciclos},
            )
            self.orquestrador.salvar()

        return historico
