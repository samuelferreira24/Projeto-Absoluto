from __future__ import annotations

from cerebro.coleta import ColetorMemoria, EventoCapturado
from cerebro.nucleo import RepositorioJSONL


def evento(**changes):
    dados = {
        "source_type": "CHATGPT",
        "source_id": "chat-001",
        "occurred_at": "2026-09-17T12:00:00+00:00",
        "content": "Descobrimos que o processo de construção também precisa ser memória.",
        "conversation_id": "conv-001",
        "event_type": "descoberta",
    }
    dados.update(changes)
    return EventoCapturado(**dados)


def test_captura_preserva_bruto_e_cria_registro(tmp_path):
    repo = RepositorioJSONL(tmp_path / "data")
    coletor = ColetorMemoria(repo)

    registros = coletor.capturar(evento())

    assert len(registros) == 1
    assert registros[0].kind == "DESCOBERTA"
    assert coletor.raw_path.exists()
    assert "construção também precisa ser memória" in coletor.raw_path.read_text(encoding="utf-8")


def test_captura_e_idempotente(tmp_path):
    repo = RepositorioJSONL(tmp_path / "data")
    coletor = ColetorMemoria(repo)
    primeiro = evento()

    assert len(coletor.capturar(primeiro)) == 1
    assert coletor.capturar(primeiro) == []
    assert len(list(repo._iter_registros())) == 1


def test_proveniencia_preserva_origem(tmp_path):
    repo = RepositorioJSONL(tmp_path / "data")
    coletor = ColetorMemoria(repo)
    registro = coletor.capturar(evento(actor="usuario"))[0]

    assert registro.provenance["source_type"] == "CHATGPT"
    assert registro.provenance["conversation_id"] == "conv-001"
    assert registro.metadata["actor"] == "usuario"
