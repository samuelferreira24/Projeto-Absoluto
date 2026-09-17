"""Validação do pacote mínimo de continuidade entre agentes e plataformas."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ErroContinuidade(ValueError):
    """Falha estrutural no pacote de continuidade."""


def carregar_json(path: str | Path) -> dict[str, Any]:
    dados = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(dados, dict):
        raise ErroContinuidade(f"manifesto inválido: {path}")
    return dados


def validar_manifesto(path: str | Path, raiz: str | Path | None = None) -> list[str]:
    """Valida estrutura e referências locais de um manifesto operacional."""
    manifesto = carregar_json(path)
    erros: list[str] = []
    obrigatorios = {"schema_version", "project", "construction", "continuity", "required_validation", "rules", "integration_boundary"}
    erros.extend(f"campo obrigatório ausente: {x}" for x in sorted(obrigatorios - manifesto.keys()))

    project = manifesto.get("project", {})
    if not isinstance(project, dict) or not project.get("id") or not project.get("name"):
        erros.append("project.id e project.name são obrigatórios")

    construction = manifesto.get("construction", {})
    if not isinstance(construction, dict):
        erros.append("construction deve ser objeto")
    else:
        if not construction.get("current_branch"):
            erros.append("construction.current_branch é obrigatório")
        if not construction.get("current_stage"):
            erros.append("construction.current_stage é obrigatório")

    continuity = manifesto.get("continuity", {})
    if not isinstance(continuity, dict):
        erros.append("continuity deve ser objeto")
    else:
        base = Path(raiz) if raiz is not None else Path(path).parent.parent.parent
        for nome, ref in continuity.items():
            if not isinstance(ref, str):
                erros.append(f"referência de continuidade inválida: {nome}")
                continue
            if not (base / ref).exists():
                erros.append(f"arquivo de continuidade ausente: {ref}")

    boundary = manifesto.get("integration_boundary", {})
    if not isinstance(boundary, dict) or not boundary.get("strategy"):
        erros.append("integration_boundary.strategy é obrigatório")

    return erros


def validar_ou_erro(path: str | Path, raiz: str | Path | None = None) -> None:
    erros = validar_manifesto(path, raiz)
    if erros:
        raise ErroContinuidade("; ".join(erros))
