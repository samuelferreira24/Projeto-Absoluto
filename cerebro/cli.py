from __future__ import annotations

import argparse
import json

from .ingestao import extrair
from .servico import Cerebro


def main() -> int:
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

    args = parser.parse_args()

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

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
