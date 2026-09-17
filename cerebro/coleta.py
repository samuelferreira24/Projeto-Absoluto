from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import hashlib
import json
import uuid

from .nucleo import Registro, RepositorioJSONL, novo_registro


def agora() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


TIPOS_FONTE = {"CHATGPT", "CLAUDE", "GEMINI", "GITHUB", "MCP", "API", "ARQUIVO", "HUMANO", "SISTEMA", "OUTRO"}


@dataclass(frozen=True)
class EventoCapturado:
    """Envelope neutro para qualquer fonte externa ou interna."""

    source_type: str
    source_id: str
    occurred_at: str
    content: str
    title: str = ""
    actor: str | None = None
    conversation_id: str | None = None
    session_id: str | None = None
    event_type: str = "mensagem"
    metadata: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: f"CAP-{uuid.uuid4().hex}")
    idempotency_key: str = ""

    def __post_init__(self) -> None:
        source = self.source_type.upper()
        if source not in TIPOS_FONTE:
            raise ValueError(f"source_type inválido: {self.source_type}")
        object.__setattr__(self, "source_type", source)
        if not self.source_id:
            raise ValueError("source_id é obrigatório")
        if not self.content.strip():
            raise ValueError("content não pode ser vazio")
        if not self.idempotency_key:
            base = {
                "source_type": source,
                "source_id": self.source_id,
                "occurred_at": self.occurred_at,
                "conversation_id": self.conversation_id,
                "event_type": self.event_type,
                "content": self.content,
            }
            chave = hashlib.sha256(json.dumps(base, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
            object.__setattr__(self, "idempotency_key", chave)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ColetorMemoria:
    """Recebe eventos de qualquer plataforma e transforma-os em memória rastreável.

    A coleta é separada da interpretação: o envelope bruto é preservado antes da
    criação de registros derivados. Assim, uma IA futura pode reprocessar a fonte
    sem perder o material original.
    """

    def __init__(self, repo: RepositorioJSONL, raw_path: str | Path | None = None) -> None:
        self.repo = repo
        self.raw_path = Path(raw_path) if raw_path else repo.root / "captura" / "eventos_brutos.jsonl"
        self.raw_path.parent.mkdir(parents=True, exist_ok=True)

    def _ids_capturados(self) -> set[str]:
        if not self.raw_path.exists():
            return set()
        ids: set[str] = set()
        for linha in self.raw_path.read_text(encoding="utf-8").splitlines():
            if not linha.strip():
                continue
            try:
                ids.add(json.loads(linha)["idempotency_key"])
            except (json.JSONDecodeError, KeyError, TypeError):
                continue
        return ids

    def capturar(self, evento: EventoCapturado) -> list[Registro]:
        """Preserva o bruto e cria memória derivada sem duplicar o mesmo evento."""
        if evento.idempotency_key in self._ids_capturados():
            return []

        with self.raw_path.open("a", encoding="utf-8") as arquivo:
            arquivo.write(json.dumps(evento.to_dict(), ensure_ascii=False) + "\n")

        tipo = classificar(evento)
        registro = novo_registro(
            self.repo,
            tipo,
            evento.title or f"{evento.source_type}: {evento.event_type}",
            evento.content,
            source=evento.source_id,
            provenance={
                "pipeline": "captura_automatica_v0_1",
                "event_id": evento.event_id,
                "source_type": evento.source_type,
                "conversation_id": evento.conversation_id,
                "session_id": evento.session_id,
                "occurred_at": evento.occurred_at,
                "idempotency_key": evento.idempotency_key,
            },
            metadata={
                "actor": evento.actor,
                "event_type": evento.event_type,
                **evento.metadata,
            },
        )
        self.repo.salvar(registro)
        return [registro]


def classificar(evento: EventoCapturado) -> str:
    """Classificação inicial conservadora; interpretação profunda fica para agentes."""
    tipo = evento.event_type.casefold()
    if tipo in {"pesquisa", "research"}:
        return "PESQUISA"
    if tipo in {"decisao", "decision"}:
        return "DECISAO"
    if tipo in {"descoberta", "discovery"}:
        return "DESCOBERTA"
    if tipo in {"entendimento", "understanding"}:
        return "ENTENDIMENTO"
    if tipo in {"progresso", "progress"}:
        return "PROGRESSO"
    if tipo in {"erro", "error", "failure"}:
        return "ERRO"
    if tipo in {"resultado", "result"}:
        return "RESULTADO"
    if tipo in {"experiencia", "experience"}:
        return "EXPERIENCIA"
    if tipo in {"aprendizado", "learning"}:
        return "APRENDIZADO"
    if tipo in {"planejamento", "plan", "planning"}:
        return "PLANEJAMENTO"
    return "DOCUMENTO"
