from __future__ import annotations

from pathlib import Path
import json
import sys

from .coleta import ColetorMemoria, EventoCapturado
from .nucleo import RepositorioJSONL


def processar_arquivo(path: str | Path, dados: str | Path = "cerebro/data") -> int:
    origem = Path(path)
    repo = RepositorioJSONL(dados)
    coletor = ColetorMemoria(repo)
    processados = 0

    for linha in origem.read_text(encoding="utf-8").splitlines():
        if not linha.strip():
            continue
        payload = json.loads(linha)
        evento = EventoCapturado(**payload)
        processados += len(coletor.capturar(evento))
    return processados


def main() -> int:
    if len(sys.argv) != 2:
        print("uso: python -m cerebro.processar_captura EVENTOS.jsonl")
        return 2
    quantidade = processar_arquivo(sys.argv[1])
    print(json.dumps({"processados": quantidade}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
