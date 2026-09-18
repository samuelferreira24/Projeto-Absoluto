from __future__ import annotations

import json
from unittest.mock import patch

from cerebro.openrouter import ModeloOpenRouter


def test_openrouter_usa_contrato_estruturado_sem_expor_chave_no_payload():
    resposta = {
        "choices": [
            {
                "message": {
                    "content": json.dumps(
                        {
                            "executar": True,
                            "concluida": False,
                            "acao": "obter",
                            "ferramenta": "obter_arquivo_github",
                            "recurso": "documento",
                            "argumentos": {"caminho": "docs/teste.docx"},
                            "motivo": "preciso do documento",
                        }
                    )
                }
            }
        ]
    }

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            return json.dumps(resposta).encode("utf-8")

    captured = {}

    def fake_urlopen(req, timeout):
        captured["url"] = req.full_url
        captured["headers"] = dict(req.headers)
        captured["payload"] = json.loads(req.data.decode("utf-8"))
        captured["timeout"] = timeout
        return FakeResponse()

    modelo = ModeloOpenRouter("openrouter/free", api_key="secret")

    with patch("cerebro.openrouter.request.urlopen", fake_urlopen):
        saida = modelo.gerar(
            "Decida o próximo passo.",
            {"objetivo": "obter documento"},
            {
                "type": "object",
                "required": ["executar", "concluida"],
                "properties": {
                    "executar": {"type": "boolean"},
                    "concluida": {"type": "boolean"},
                },
            },
        )

    assert saida["ferramenta"] == "obter_arquivo_github"
    assert captured["url"].endswith("/chat/completions")
    assert captured["headers"]["Authorization"] == "Bearer secret"
    assert captured["payload"]["model"] == "openrouter/free"
    assert captured["payload"]["response_format"]["type"] == "json_schema"
    assert "secret" not in json.dumps(captured["payload"])


def test_openrouter_exige_chave_no_momento_da_execucao():
    modelo = ModeloOpenRouter("openrouter/free", api_key=None)

    try:
        modelo.gerar("tarefa", {}, {"type": "object"})
    except RuntimeError as exc:
        assert "OPENROUTER_API_KEY" in str(exc)
    else:
        raise AssertionError("deveria exigir OPENROUTER_API_KEY")
