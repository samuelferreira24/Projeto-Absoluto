from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .aprendizado import novo_aprendizado, registrar_aprendizado
from .grafo_tarefas import EstadoTarefa, NoTarefa
from .servico import Cerebro


@dataclass(frozen=True)
class ResultadoOperacao:
    entrada_id: str
    tarefas_planejadas: tuple[str, ...]
    tarefas_concluidas: tuple[str, ...]
    aprendizados_registrados: int
    consolidado: int


def operar_entrada(
    cerebro: Cerebro,
    arquivo: str | Path,
    *,
    objetivo: str | None = None,
    executor: Callable[[Cerebro, NoTarefa, str], dict[str, Any]] | None = None,
    recursos: set[str] | None = None,
) -> ResultadoOperacao:
    """Executa o menor ciclo operacional completo do Cérebro.

    A entrada é preservada pelo mecanismo de ingestão. O objetivo vira uma tarefa,
    o agendador escolhe o trabalho disponível, o executor produz um resultado,
    esse resultado vira aprendizado persistente e a memória é consolidada.
    """
    entrada = cerebro.ingerir(arquivo)
    objetivo = objetivo or f"processar entrada {entrada.id}"

    tarefa = NoTarefa(
        id=f"operacao:{entrada.id}",
        objetivo=objetivo,
        prioridade=1.0,
        valor_estimado=1.0,
        custo_estimado=1.0,
        tempo_estimado=1.0,
    )
    cerebro.adicionar_tarefa(tarefa)

    plano = cerebro.planejar_tarefas(recursos or set())
    if not plano.tarefas:
        raise RuntimeError(f"Não foi possível planejar a operação: {plano.motivo}")

    cerebro.iniciar_plano(plano)
    aprendizados = 0
    concluidas: list[str] = []

    for item in plano.tarefas:
        if executor is None:
            resultado = {
                "tipo": "RESULTADO",
                "titulo": f"Resultado da operação {item.id}",
                "conteudo": f"Tarefa executada: {item.objetivo}. Entrada preservada em {entrada.id}.",
                "qualidade": 1.0,
            }
        else:
            resultado = executor(cerebro, item, entrada.id)

        cerebro.concluir_tarefa(
            item.id,
            bool(resultado.get("sucesso", True)),
            observacao=str(resultado.get("conteudo", "")),
            custo_real=resultado.get("custo_real"),
            tempo_real=resultado.get("tempo_real"),
            qualidade=resultado.get("qualidade"),
        )

        if resultado.get("sucesso", True):
            concluidas.append(item.id)
            aprendizado = novo_aprendizado(
                "APRENDIZADO",
                str(resultado.get("titulo", f"Aprendizado da operação {item.id}")),
                str(resultado.get("conteudo", "")),
                origem=f"operacao:{item.id}",
                evidencias=(entrada.id,),
                contexto=(objetivo,),
                confianca="observada",
            )
            if registrar_aprendizado(aprendizado, cerebro.repo.root.parent / "memoria" / "aprendizados.jsonl"):
                aprendizados += 1

    consolidado = cerebro.consolidar_aprendizados().get("quantidade", 0)
    cerebro.estado.atualizar(status="OPERACIONAL", next_priority="reavaliar e melhorar o ciclo com experiência real")
    cerebro.salvar_estado()

    return ResultadoOperacao(
        entrada_id=entrada.id,
        tarefas_planejadas=tuple(t.id for t in plano.tarefas),
        tarefas_concluidas=tuple(concluidas),
        aprendizados_registrados=aprendizados,
        consolidado=int(consolidado),
    )
