from pathlib import Path

from cerebro.aprendizado import novo_aprendizado, registrar_aprendizado, registrar_evento_construcao


def test_aprendizado_tem_id_deterministico():
    a = novo_aprendizado("APRENDIZADO", "Teste", "Conteúdo", "teste")
    b = novo_aprendizado("APRENDIZADO", "Teste", "Conteúdo", "teste")
    assert a.id == b.id


def test_registro_e_idempotente(tmp_path: Path):
    arquivo = tmp_path / "aprendizados.jsonl"
    a = novo_aprendizado("DESCOBERTA", "Descoberta", "Algo novo", "historico")
    assert registrar_aprendizado(a, arquivo) is True
    assert registrar_aprendizado(a, arquivo) is False
    assert len(arquivo.read_text(encoding="utf-8").splitlines()) == 1


def test_evento_de_construcao_preserva_contexto():
    e = registrar_evento_construcao(
        "Primeira capacidade histórica",
        "A construção deve registrar também o que aprendeu durante a construção.",
        "conversa",
        evidencias=("cerebro/reconstrucao_historica.py",),
        contexto=("passado informa, não determina",),
    )
    assert e.tipo == "EVENTO_DE_CONSTRUCAO"
    assert e.evidencias
    assert e.contexto
