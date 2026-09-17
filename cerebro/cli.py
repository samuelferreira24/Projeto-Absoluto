from __future__ import annotations

import argparse
import json
from pathlib import Path

from .ingestao import extrair, registrar_fonte
from .nucleo import RepositorioJSONL


def main() -> int:
    parser = argparse.ArgumentParser(description="Cérebro do Projeto Absoluto — V0.1")
    sub = parser.add_subparsers(dest="comando", required=True)

    p_ingest = sub.add_parser("ingerir", help="Extrai e registra um arquivo")
    p_ingest.add_argument("arquivo")
    p_ingest.add_argument("--dados", default="cerebro/data")

    p_busca = sub.add_parser("buscar", help="Busca registros")
    p_busca.add_argument("texto")
    p_busca.add_argument("--dados", default="cerebro/data")

    p_inspect = sub.add_parser("inspecionar", help="Extrai sem registrar")
    p_inspect.add_argument("arquivo")

    args = parser.parse_args()

    if args.comando == "inspecionar":
        doc = extrair(args.arquivo)
        print(json.dumps(doc.to_dict(), ensure_ascii=False, indent=2))
        return 0 if not doc.erros else 2

    repo = RepositorioJSONL(args.dados)
    if args.comando == "ingerir":
        doc = extrair(args.arquivo)
        if doc.erros:
            print(json.dumps(doc.to_dict(), ensure_ascii=False, indent=2))
            return 2
        reg = registrar_fonte(repo, doc)
        print(reg.to_json())
        return 0

    for reg in repo.buscar(args.texto):
        print(reg.to_json())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
