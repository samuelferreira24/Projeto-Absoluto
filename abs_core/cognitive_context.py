from __future__ import annotations

"""Context assembly for intelligence engines running inside ABS."""

from datetime import datetime, timezone
import os
from pathlib import Path


DEFAULT_IDENTITY = (
    "Você é o motor de inteligência operando dentro do ABS (Sistema Absoluto). "
    "O ABS é o sistema sob controle do Imperador e executa tarefas por meio de capacidades, "
    "ferramentas, memória e conhecimento. Você é um componente substituível do ABS, não o ABS inteiro. "
    "Quando o ABS fornecer um resultado externo, trate-o como contexto factual obtido pelo sistema. "
    "Não diga que uma capacidade é inexistente se o ABS acabou de executá-la."
)

DEFAULT_PROJECT_CONTEXT = (
    "Projeto Absoluto é a visão e o projeto maior. ABS é o primeiro sistema concreto sendo construído "
    "para ajudar a transformar essa visão em execução. O Imperador mantém a autoridade sobre direção, "
    "decisões e autorizações. O ABS deve evoluir de forma modular, substituível e sem dependência obrigatória "
    "de uma única IA, interface ou fornecedor."
)


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat()


def build_system_context(capabilities, external_results=None, *, project_root: str | Path | None = None) -> str:
    capability_lines = []
    for cap in capabilities:
        capability_lines.append(f"- {cap.id}: {cap.name} ({cap.kind})")
    capabilities_text = "\n".join(capability_lines) or "- nenhuma capacidade registrada"

    extra = os.getenv("ABS_SYSTEM_CONTEXT", "").strip()
    project = os.getenv("ABS_PROJECT_CONTEXT", "").strip() or DEFAULT_PROJECT_CONTEXT

    external_text = ""
    if external_results:
        external_text = (
            "\n\nRESULTADOS OBTIDOS PELO ABS NESTE PEDIDO:\n"
            + _compact_external_results(external_results)
            + "\nUse esses resultados como evidência do que o ABS realmente executou."
        )

    return (
        DEFAULT_IDENTITY
        + "\n\nCONTEXTO DO PROJETO:\n"
        + project
        + "\n\nDATA E HORA ATUAIS FORNECIDAS PELO ABS:\n"
        + _now()
        + "\n\nCAPACIDADES DISPONÍVEIS NO RUNTIME:\n"
        + capabilities_text
        + (f"\n\nCONTEXTO EXTRA:\n{extra}" if extra else "")
        + external_text
    )


def _compact_external_results(results) -> str:
    import json
    raw = json.dumps(results, ensure_ascii=False, separators=(",", ":"))
    limit = int(os.getenv("ABS_EXTERNAL_CONTEXT_MAX_CHARS", "12000"))
    if len(raw) <= limit:
        return raw
    return raw[:limit] + "... [resultado externo truncado pelo ABS]"
