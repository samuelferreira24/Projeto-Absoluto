from __future__ import annotations

from pathlib import Path
import json
from typing import Any


def _ler_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    registros: list[dict[str, Any]] = []
    for linha in path.read_text(encoding="utf-8").splitlines():
        if not linha.strip():
            continue
        try:
            valor = json.loads(linha)
        except json.JSONDecodeError:
            continue
        if isinstance(valor, dict):
            registros.append(valor)
    return registros


def _ler_fundamentais(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    valor = json.loads(path.read_text(encoding="utf-8"))
    return list(valor.get("aprendizados", []))


def consolidar(
    jsonl: str | Path,
    fundamentais: str | Path,
) -> dict[str, Any]:
    """Une aprendizado acumulado e aprendizado novo sem apagar nenhuma fonte."""
    acumulado = _ler_jsonl(Path(jsonl))
    historico = _ler_fundamentais(Path(fundamentais))

    itens: list[dict[str, Any]] = []
    chaves: set[tuple[str, str, str]] = set()

    for item in historico:
        enriquecido = dict(item)
        enriquecido.setdefault("camada", "ACUMULADO")
        enriquecido.setdefault("status", "CONSOLIDADO")
        chave = (
            str(enriquecido.get("tipo", "")),
            str(enriquecido.get("titulo", "")),
            str(enriquecido.get("conteudo", "")),
        )
        if chave not in chaves:
            chaves.add(chave)
            itens.append(enriquecido)

    for item in acumulado:
        enriquecido = dict(item)
        enriquecido.setdefault("camada", "EVENTO")
        enriquecido.setdefault("status", "REGISTRADO")
        chave = (
            str(enriquecido.get("tipo", "")),
            str(enriquecido.get("titulo", "")),
            str(enriquecido.get("conteudo", "")),
        )
        if chave not in chaves:
            chaves.add(chave)
            itens.append(enriquecido)

    return {
        "versao": "0.1",
        "principio": "O Cérebro preserva o aprendizado acumulado e o novo aprendizado; nenhum dos dois substitui silenciosamente o outro.",
        "quantidade": len(itens),
        "aprendizados": itens,
    }


def salvar_consolidado(
    destino: str | Path,
    jsonl: str | Path,
    fundamentais: str | Path,
) -> dict[str, Any]:
    resultado = consolidar(jsonl, fundamentais)
    path = Path(destino)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(resultado, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return resultado
