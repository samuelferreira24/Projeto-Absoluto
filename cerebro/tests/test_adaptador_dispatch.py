from cerebro.adaptador_dispatch import enviar_evento
from cerebro.coleta import EventoCapturado


def test_adaptador_exige_configuracao():
    evento = EventoCapturado(
        source_type="CLAUDE",
        source_id="chat-claude-1",
        occurred_at="2026-09-17T12:00:00+00:00",
        content="Teste de integração",
    )
    try:
        enviar_evento(evento, repository=None, token=None)
    except ValueError as exc:
        assert "PA_GITHUB_REPOSITORY" in str(exc)
    else:
        raise AssertionError("o adaptador deveria exigir configuração")
