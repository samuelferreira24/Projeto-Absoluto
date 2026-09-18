from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable
import uuid

from .agendador import AgendadorAdaptativo, PlanoExecucao
from .controle_execucao import ControleExecucao
from .executor import ExecutorCerebro, PlanoCiclo
from .grafo_tarefas import EstadoTarefa, NoTarefa
from .politica_execucao import Acao, NivelAutonomia


@dataclass(frozen=True)
class ResultadoExecucaoTarefa:
    tarefa_id: str
    executado: bool
    estado: str
    resultado: dict[str, Any] | None = None
    erro: str | None = None
    tentativa: int | None = None


class _FonteNula:
    def candidatos_rede(self, contexto: dict[str, float] | None = None) -> list[tuple[str, float]]:
        return []


class ExecutorPlano:
    """Executa um plano já autorizado pelo scheduler, com claim, política e aprendizado."""

    def __init__(
        self,
        agendador: AgendadorAdaptativo,
        controle: ControleExecucao,
        executor: ExecutorCerebro | None = None,
    ) -> None:
        self.agendador = agendador
        self.controle = controle
        self.executor = executor or ExecutorCerebro(cerebro=_FonteNula())

    def executar(
        self,
        plano: PlanoExecucao,
        handlers: dict[str, Callable[[NoTarefa], dict[str, Any]]],
        *,
        parar_na_falha: bool = False,
        correlation_id: str | None = None,
        aprovacoes: dict[str, str] | None = None,
    ) -> list[ResultadoExecucaoTarefa]:
        correlacao = correlation_id or f"PLANO-{uuid.uuid4().hex}"
        aprovacoes = dict(aprovacoes or {})
        resultados: list[ResultadoExecucaoTarefa] = []

        for tarefa in plano.tarefas:
            if tarefa.id not in handlers:
                self.agendador.registrar_resultado(
                    tarefa.id,
                    False,
                    observacao="handler de execução inexistente",
                    contexto={"correlation_id": correlacao},
                )
                resultados.append(
                    ResultadoExecucaoTarefa(
                        tarefa.id, False, "FALHOU", erro="handler de execução inexistente"
                    )
                )
                if parar_na_falha:
                    break
                continue

            try:
                claim = self.controle.claim(tarefa.id)
            except RuntimeError as exc:
                resultados.append(ResultadoExecucaoTarefa(tarefa.id, False, "BLOQUEADO", erro=str(exc)))
                if parar_na_falha:
                    break
                continue

            nivel = NivelAutonomia(max(0, min(int(tarefa.nivel_autonomia), int(NivelAutonomia.ALTO_IMPACTO))))
            acao = Acao(
                nome=f"executar_tarefa:{tarefa.id}",
                nivel=nivel,
                reversivel=tarefa.reversivel,
                exige_autorizacao=tarefa.exige_aprovacao,
            )
            plano_ciclo = PlanoCiclo(
                acao=acao,
                alvo=tarefa.id,
                contexto={"objetivo": tarefa.objetivo},
                ferramenta=tarefa.ferramenta or (tarefa.capacidades[0] if tarefa.capacidades else acao.nome),
                recurso=tarefa.recursos[0] if tarefa.recursos else None,
                custo_estimado=tarefa.custo_estimado,
                cadeia=1,
                aprovacao_id=aprovacoes.get(tarefa.id),
                correlation_id=correlacao,
            )

            try:
                retorno = self.executor.executar(
                    plano_ciclo,
                    lambda _: handlers[tarefa.id](tarefa),
                )
                if not retorno.get("executado"):
                    motivo = str(retorno.get("motivo", "execução bloqueada"))
                    self.agendador.registrar_resultado(
                        tarefa.id,
                        False,
                        observacao=motivo,
                        contexto={"correlation_id": correlacao},
                    )
                    self.controle.falhar(tarefa.id, motivo)
                    resultados.append(ResultadoExecucaoTarefa(tarefa.id, False, "BLOQUEADO", erro=motivo, tentativa=claim.tentativa))
                    if parar_na_falha:
                        break
                    continue

                resultado = retorno.get("resultado") or {}
                self.agendador.registrar_resultado(
                    tarefa.id,
                    True,
                    observacao="tarefa executada pelo ExecutorPlano",
                    contexto={"correlation_id": correlacao},
                    aprendizado="Plano executado através da ponte entre scheduler, controle de execução e executor autorizado.",
                )
                self.controle.concluir(tarefa.id)
                resultados.append(ResultadoExecucaoTarefa(tarefa.id, True, "CONCLUIDA", resultado=resultado, tentativa=claim.tentativa))
            except Exception as exc:
                mensagem = str(exc)
                self.agendador.registrar_resultado(
                    tarefa.id,
                    False,
                    observacao=mensagem,
                    contexto={"correlation_id": correlacao},
                )
                self.controle.falhar(tarefa.id, mensagem)
                resultados.append(ResultadoExecucaoTarefa(tarefa.id, False, "FALHOU", erro=mensagem, tentativa=claim.tentativa))
                if parar_na_falha:
                    break

        return resultados
