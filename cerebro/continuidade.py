"""Continuidade portatil: estado, memoria, aprendizado e retomada entre chats."""
from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .contexto_operacional import construir_contexto

SCHEMA_VERSION = "0.3"


class ErroContinuidade(ValueError):
    """Falha estrutural no pacote de continuidade."""


def agora() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


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


def _estado(obj: Any) -> dict[str, Any]:
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    return asdict(obj)


def _registros(cerebro: Any) -> list[dict[str, Any]]:
    return [r.to_dict() for r in cerebro.registros()]


def criar_snapshot(
    cerebro: Any,
    *,
    objetivo_atual: str | None = None,
    proximo_passo: str | None = None,
    contexto_da_sessao: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Cria um snapshot completo e portatil para outra conversa."""
    estado = cerebro.estado.to_dict()
    tarefas = []
    for tarefa in cerebro.grafo_tarefas.tarefas.values():
        item = asdict(tarefa)
        item["estado"] = tarefa.estado.value
        tarefas.append(item)

    memoria = _registros(cerebro)
    aprendizados = [
        r for r in memoria
        if r.get("kind") in {"APRENDIZADO", "ENTENDIMENTO", "DESCOBERTA", "PROGRESSO", "ERRO", "DECISAO", "RESULTADO", "EXPERIENCIA"}
    ]
    contexto = construir_contexto(cerebro, objetivo=objetivo_atual, proximo_passo=proximo_passo, contexto_da_sessao=contexto_da_sessao).to_dict()

    return {
        "schema_version": SCHEMA_VERSION,
        "snapshot_at": agora(),
        "project_id": estado["project_id"],
        "objetivo_atual": objetivo_atual or estado.get("next_priority"),
        "proximo_passo": proximo_passo,
        "contexto_operacional": contexto,
        "contexto_da_sessao": dict(contexto_da_sessao or {}),
        "estado_sistema": estado,
        "tarefas": tarefas,
        "memoria_completa": memoria,
        "aprendizados": aprendizados,
        "rede_evolutiva": {
            "nos": [asdict(n) for n in cerebro.rede.nos.values()],
            "arestas": [asdict(a) for a in cerebro.rede.arestas.values()],
        },
        "runtime": _estado(cerebro.runtime.estado),
        "missoes": [asdict(m) for m in cerebro.orquestrador.missoes.values()],
        "regras_de_continuidade": [
            "O snapshot é uma ponte entre sessões, não uma substituição das evidências.",
            "Preservar contexto, aprendizado, progresso, decisões, erros e histórico.",
            "O passado informa a arquitetura, mas não determina a arquitetura.",
            "Uma nova instrução pode ampliar ou corrigir a rota sem apagar trabalho anterior silenciosamente.",
            "Validar o estado atual do repositório antes de continuar quando ele estiver disponível.",
            "Antes de agir, qualquer chat deve reconstruir o que está sendo feito, como, por que, estado, decisões, ações recentes, bloqueios, riscos e próximo passo.",
        ],
    }


def salvar_snapshot(
    cerebro: Any,
    path: str | Path = "cerebro/data/continuidade.json",
    **kwargs: Any,
) -> dict[str, Any]:
    destino = Path(path)
    destino.parent.mkdir(parents=True, exist_ok=True)
    snapshot = criar_snapshot(cerebro, **kwargs)
    destino.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return snapshot


def carregar_snapshot(path: str | Path = "cerebro/data/continuidade.json") -> dict[str, Any]:
    return carregar_json(path)


def gerar_prompt_retoma(snapshot: dict[str, Any]) -> str:
    """Gera instrução que pode ser colada em outro chat."""
    estado = snapshot.get("estado_sistema", {})
    tarefas = snapshot.get("tarefas", [])
    aprendizados = snapshot.get("aprendizados", [])
    contexto = snapshot.get("contexto_operacional", {})
    relevantes = [
        t for t in tarefas
        if t.get("estado") in {"PENDENTE", "PRONTA", "EXECUTANDO", "BLOQUEADA", "FALHOU"}
    ]
    return "\n".join([
        "# RETOMADA DO PROJETO ABSOLUTO",
        "",
        f"Projeto: {snapshot.get('project_id', 'PROJETO-ABSOLUTO')}",
        f"Snapshot: {snapshot.get('snapshot_at', '')}",
        f"Objetivo atual: {snapshot.get('objetivo_atual') or 'não informado'}",
        f"Próximo passo: {snapshot.get('proximo_passo') or 'determinar a partir do estado registrado'}",
        "",
        "## CONTEXTO OPERACIONAL OBRIGATÓRIO",
        json.dumps(contexto, ensure_ascii=False, indent=2),
        "",
        "## Estado do sistema",
        json.dumps(estado, ensure_ascii=False, indent=2),
        "",
        "## Tarefas relevantes",
        json.dumps(relevantes, ensure_ascii=False, indent=2),
        "",
        "## O que foi aprendido",
        json.dumps(aprendizados, ensure_ascii=False, indent=2),
        "",
        "## Contexto adicional da sessão",
        json.dumps(snapshot.get("contexto_da_sessao", {}), ensure_ascii=False, indent=2),
        "",
        "## Regra de retomada",
        "Continue de onde o trabalho parou. Não recomece do zero. Antes de executar, entenda o que está sendo feito, como está sendo feito, por que está sendo feito, o que já foi feito, quais decisões foram tomadas, quais riscos e bloqueios existem e qual é o próximo passo. Ao executar, registre ação, ferramenta, motivo, resultado e evidência. Não descarte decisões, aprendizados ou progresso registrados. Use o snapshot para reconstruir o contexto inicial e, quando o repositório estiver disponível, confira os arquivos atuais antes de modificar qualquer coisa. Registre novas descobertas, erros, decisões, mudanças de entendimento e progresso no Cérebro.",
    ])


def salvar_prompt_retoma(
    cerebro: Any,
    path: str | Path = "cerebro/data/RETOMAR_OUTRO_CHAT.md",
    **kwargs: Any,
) -> str:
    snapshot = criar_snapshot(cerebro, **kwargs)
    destino = Path(path)
    destino.parent.mkdir(parents=True, exist_ok=True)
    prompt = gerar_prompt_retoma(snapshot)
    destino.write_text(prompt + "\n", encoding="utf-8")
    return prompt
