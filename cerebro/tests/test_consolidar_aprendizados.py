import json

from cerebro.consolidar_aprendizados import consolidar, salvar_consolidado


def test_consolidar_preserva_acumulado_e_eventos(tmp_path):
    jsonl = tmp_path / "aprendizados.jsonl"
    fundamentais = tmp_path / "fundamentais.json"

    jsonl.write_text(
        json.dumps({"tipo": "APRENDIZADO", "titulo": "Novo", "conteudo": "evento"}) + "\n",
        encoding="utf-8",
    )
    fundamentais.write_text(
        json.dumps(
            {"versao": "0.1", "aprendizados": [
                {"tipo": "VISAO", "titulo": "Antigo", "conteudo": "acumulado"}
            ]}
        ),
        encoding="utf-8",
    )

    resultado = consolidar(jsonl, fundamentais)

    assert resultado["quantidade"] == 2
    assert {item["titulo"] for item in resultado["aprendizados"]} == {"Antigo", "Novo"}


def test_consolidar_e_idempotente_por_conteudo(tmp_path):
    jsonl = tmp_path / "aprendizados.jsonl"
    fundamentais = tmp_path / "fundamentais.json"
    destino = tmp_path / "consolidado.json"

    item = {"tipo": "APRENDIZADO", "titulo": "Mesmo", "conteudo": "x"}
    jsonl.write_text(json.dumps(item) + "\n", encoding="utf-8")
    fundamentais.write_text(
        json.dumps({"versao": "0.1", "aprendizados": [item]}),
        encoding="utf-8",
    )

    resultado = salvar_consolidado(destino, jsonl, fundamentais)

    assert resultado["quantidade"] == 1
    assert json.loads(destino.read_text(encoding="utf-8"))["quantidade"] == 1
