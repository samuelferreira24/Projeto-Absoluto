from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .grafo_tarefas import EstadoTarefa, GrafoTarefas, NoTarefa
from .sinergia import DetectorSinergia, ResultadoCombinacao


SCHEMA_VERSION = "0.1"


def _serializar_tarefa(tarefa: NoTarefa) -> dict[str, Any]:
    dados = asdict(tarefa)
    dados["estado"] = tarefa.estado.value
    return dados


def salvar_orquestracao(path: str | Path, grafo: GrafoTarefas, sinergia: DetectorSinergia) -> dict[str, Any]:
    """Persiste o estado estrutural da orquestração sem substituir histórico."""
    destino = Path(path)
    destino.parent.mkdir(parents=True, exist_ok=True)
    pacote = {
        "schema_version": SCHEMA_VERSION,
        "tarefas": [_serializar_tarefa(t) for t in grafo.tarefas.values()],
        "resultados_sinergia": [asdict(r) for r in sinergia.resultados],
    }
    temporario = destino.with_suffix(destino.suffix + ".tmp")
    temporario.write_text(json.dumps(pacote, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporario.replace(destino)
    return pacote


def carregar_orquestracao(path: str | Path) -> tuple[GrafoTarefas, DetectorSinergia]:
    """Reconstrói grafo e memória de sinergia a partir do snapshot persistido."""
    origem = Path(path)
    if not origem.exists():
        return GrafoTarefas(), DetectorSinergia()
    dados = json.loads(origem.read_text(encoding="utf-8"))
    if dados.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("schema de orquestração incompatível")

    grafo = GrafoTarefas()
    for item in dados.get("tarefas", []):
        item = dict(item)
        item["estado"] = EstadoTarefa(item.get("estado", EstadoTarefa.PENDENTE.value))
        for chave in ("depende_de", "recursos", "capacidades", "preferencias", "restricoes", "fallbacks"):
            if chave in item and isinstance(item[chave], list):
                item[chave] = tuple(item[chave])
        grafo.adicionar(NoTarefa(**item))

    detector = DetectorSinergia()
    for item in dados.get("resultados_sinergia", []):
        item = dict(item)
        for chave in ("capacidades",):
            if chave in item and isinstance(item[chave], list):
                item[chave] = tuple(item[chave])
        if isinstance(item.get("contexto"), dict):
            item["contexto"] = {str(k): str(v) for k, v in item["contexto"].items()}
        detector.registrar(ResultadoCombinacao(**item))
    return grafo, detector
