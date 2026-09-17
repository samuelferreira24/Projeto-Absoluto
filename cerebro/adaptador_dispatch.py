from __future__ import annotations

import json
import os
from urllib import request

from .coleta import EventoCapturado


def enviar_evento(evento: EventoCapturado, repository: str | None = None, token: str | None = None) -> None:
    """Envia um envelope para o barramento do Projeto via repository_dispatch.

    O adaptador é propositalmente pequeno: a plataforma de origem só precisa
    converter seus dados para EventoCapturado. O restante fica centralizado no
    Projeto.
    """
    repository = repository or os.environ.get("PA_GITHUB_REPOSITORY")
    token = token or os.environ.get("PA_GITHUB_TOKEN")
    if not repository or not token:
        raise ValueError("PA_GITHUB_REPOSITORY e PA_GITHUB_TOKEN são obrigatórios")

    body = json.dumps(
        {
            "event_type": "memory_capture",
            "client_payload": evento.to_dict(),
        },
        ensure_ascii=False,
    ).encode("utf-8")
    req = request.Request(
        f"https://api.github.com/repos/{repository}/dispatches",
        data=body,
        method="POST",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2026-03-10",
            "Content-Type": "application/json",
        },
    )
    with request.urlopen(req, timeout=30) as response:
        if response.status not in {200, 201, 202, 204}:
            raise RuntimeError(f"repository_dispatch retornou HTTP {response.status}")
