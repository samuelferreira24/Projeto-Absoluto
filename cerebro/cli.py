from __future__ import annotations

import argparse
import json

from .grafo_tarefas import NoTarefa
from .ingestao import extrair
from .operacao import operar_entrada
from .servico import Cerebro


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Cérebro do Projeto Absoluto — V0.1")
    sub = parser.add_subparsers(dest="comando", required=True)

    p_ingest = sub.add_parser("ingerir", help="Extrai e registra um arquivo")
    p_ingest.add_argument("arquivo")
    p_ingest.add_argument("--dados", default="cerebro/data")

    p_busca = sub.add_parser("buscar", help="Busca registros por texto")
    p_busca.add_argument("texto")
    p_busca.add_argument("--limite", type=int, default=10)
    p_busca.add_argument("--dados", default="cerebro/data")

    p_rel = sub.add_parser("relacionados", help="Expande relações a partir de um registro")
    p_rel.add_argument("id")
    p_rel.add_argument("--profundidade", type=int, default=1)
    p_rel.add_argument("--dados", default="cerebro/data")

    p_diag = sub.add_parser("diagnostico", help="Mostra o estado resumido do acervo")
    p_diag.add_argument("--dados", default="cerebro/data")

    p_inspect = sub.add_parser("inspecionar", help="Extrai sem registrar")
    p_inspect.add_argument("arquivo")

    p_learn = sub.add_parser("aprender", help="Registra aprendizado na memória do Cérebro")
    p_learn.add_argument("titulo")
    p_learn.add_argument("conteudo")
    p_learn.add_argument("--dados", default="cerebro/data")
    p_learn.add_argument("--origem", default="cli")

    p_task = sub.add_parser("tarefa", help="Adiciona uma tarefa ao grafo")
    p_task.add_argument("id")
    p_task.add_argument("objetivo")
    p_task.add_argument("--prioridade", type=float, default=1.0)
    p_task.add_argument("--valor", type=float, default=1.0)
    p_task.add_argument("--custo", type=float, default=1.0)
    p_task.add_argument("--tempo", type=float, default=1.0)
    p_task.add_argument("--dados", default="cerebro/data")

    p_plan = sub.add_parser("planejar", help="Planeja tarefas prontas")
    p_plan.add_argument("--orcamento", type=float)
    p_plan.add_argument("--dados", default="cerebro/data")

    p_run = sub.add_parser("executar", help="Executa o ciclo operacional completo sobre uma entrada")
    p_run.add_argument("arquivo")
    p_run.add_argument("--objetivo")
    p_run.add_argument("--dados", default="cerebro/data")

    args = parser.parse_args(argv)

    if args.comando == "inspecionar":
        doc = extrair(args.arquivo)
        print(json.dumps(doc.to_dict(), ensure_ascii=False, indent=2))
        return 0 if not doc.erros else 2

    cerebro = Cerebro(args.dados)

    if args.comando == "ingerir":
        reg = cerebro.ingerir(args.arquivo)
        print(reg.to_json())
        return 0

    if args.comando == "buscar":
        for resultado in cerebro.buscar(args.texto, args.limite):
            print(json.dumps({"score": resultado.score, "motivos": resultado.motivos, "registro": resultado.registro.to_dict()}, ensure_ascii=False, indent=2))
        return 0

    if args.comando == "relacionados":
        for reg in cerebro.relacionados([args.id], args.profundidade):
            print(reg.to_json())
        return 0

    if args.comando == "diagnostico":
        print(json.dumps(cerebro.diagnostico(), ensure_ascii=False, indent=2))
        return 0

    if args.comando == "aprender":
        reg = cerebro.registrar_memoria("APRENDIZADO", args.titulo, args.conteudo, fonte=args.origem)
        print(reg.to_json())
        return 0

    if args.comando == "tarefa":
        cerebro.adicionar_tarefa(NoTarefa(
            args.id, args.objetivo,
            prioridade=args.prioridade,
            valor_estimado=args.valor,
            custo_estimado=args.custo,
            tempo_estimado=args.tempo,
        ))
        print(json.dumps({"adicionada": args.id, "integridade": cerebro.validar_tarefas()}, ensure_ascii=False, indent=2))
        return 0

    if args.comando == "planejar":
        plano = cerebro.planejar_tarefas(orcamento=args.orcamento)
        print(json.dumps({
            "tarefas": [t.id for t in plano.tarefas],
            "custo": plano.custo_estimado,
            "valor": plano.valor_estimado,
            "risco": plano.risco_estimado,
            "tempo": plano.tempo_estimado,
            "motivo": plano.motivo,
        }, ensure_ascii=False, indent=2))
        return 0

    if args.comando == "executar":
        resultado = operar_entrada(cerebro, args.arquivo, objetivo=args.objetivo)
        print(json.dumps(resultado.__dict__, ensure_ascii=False, indent=2))
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
