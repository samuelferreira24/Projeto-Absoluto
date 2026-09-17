from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from .coleta import EventoCapturado
from .contexto_operacional import construir_contexto, gerar_prompt_contexto


@dataclass(frozen=True)
class MensagemChat:
    """Representação portátil de uma mensagem de qualquer interface conversacional."""

    message_id: str
    role: str
    content: str
    occurred_at: str
    conversation_id: str
    session_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)


class InterfaceChat:
    """Ponte entre uma interface conversacional e o Cérebro.

    A interface não é a memória. Ela entrega mensagens ao Cérebro, onde o bruto
    é preservado e onde registros derivados podem ser criados posteriormente.
    """

    def __init__(self, cerebro: Any, *, source_id: str = "chat-interface") -> None:
        self.cerebro = cerebro
        self.source_id = source_id

    def capturar_mensagem(self, mensagem: MensagemChat) -> int:
        evento = EventoCapturado(
            source_type="CHATGPT",
            source_id=self.source_id,
            occurred_at=mensagem.occurred_at,
            content=mensagem.content,
            title=f"Chat {mensagem.role}",
            actor=mensagem.role,
            conversation_id=mensagem.conversation_id,
            session_id=mensagem.session_id,
            event_type="mensagem",
            metadata={"message_id": mensagem.message_id, **mensagem.metadata},
            raw=mensagem.raw,
            idempotency_key=f"chat:{mensagem.conversation_id}:{mensagem.message_id}",
        )
        return len(self.cerebro.capturar_evento(evento))

    def capturar_conversa(self, mensagens: Iterable[MensagemChat]) -> int:
        """Importa uma conversa inteira preservando cada mensagem individualmente."""
        total = 0
        for mensagem in mensagens:
            total += self.capturar_mensagem(mensagem)
        return total

    def contexto_para_retoma(self, *, objetivo: str | None = None, limite: int = 20) -> list[Any]:
        """Recupera memória do Cérebro para alimentar uma nova sessão de chat."""
        consulta = objetivo or "contexto atual progresso decisões descobertas aprendizados"
        return self.cerebro.buscar(consulta, limite)

    def contexto_inicial(self, *, objetivo: str | None = None, proximo_passo: str | None = None, contexto_da_sessao: dict[str, Any] | None = None) -> dict[str, Any]:
        """Entrega o pacote estruturado que o chat deve conhecer antes de agir."""
        return construir_contexto(
            self.cerebro,
            objetivo=objetivo,
            proximo_passo=proximo_passo,
            contexto_da_sessao=contexto_da_sessao,
        ).to_dict()

    def prompt_inicial(self, *, objetivo: str | None = None, proximo_passo: str | None = None, contexto_da_sessao: dict[str, Any] | None = None) -> str:
        """Entrega a versão textual do contexto para hosts que trabalham por prompt."""
        return gerar_prompt_contexto(self.contexto_inicial(
            objetivo=objetivo,
            proximo_passo=proximo_passo,
            contexto_da_sessao=contexto_da_sessao,
        ))
