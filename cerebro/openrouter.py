from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any
from urllib import request, error

from .modelos import ModeloEstruturado


@dataclass
class ModeloOpenRouter(ModeloEstruturado):
    """Adaptador OpenRouter; o Cérebro conhece apenas o contrato ModeloEstruturado."""

    nome: str
    api_key: str | None = None
    base_url: str = "https://openrouter.ai/api/v1"
    timeout: float = 60.0

    @classmethod
    def a_partir_do_ambiente(
        cls,
        modelo: str = "openrouter/free",
        *,
        timeout: float = 60.0,
    ) -> "ModeloOpenRouter":
        return cls(
            nome=modelo,
            api_key=os.getenv("OPENROUTER_API_KEY"),
            timeout=timeout,
        )

    def gerar(
        self,
        tarefa: str,
        entrada: dict[str, Any],
        schema: dict[str, Any],
    ) -> dict[str, Any]:
        if not self.api_key:
            raise RuntimeError(
                "OPENROUTER_API_KEY não configurada; conecte a chave apenas no ambiente de execução."
            )

        payload = {
            "model": self.nome,
            "messages": [
                {
                    "role": "system",
                    "content": tarefa,
                },
                {
                    "role": "user",
                    "content": json.dumps(entrada, ensure_ascii=False),
                },
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "decisao_cerebro",
                    "strict": True,
                    "schema": schema,
                },
            },
        }

        dados = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = request.Request(
            f"{self.base_url.rstrip('/')}/chat/completions",
            data=dados,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=self.timeout) as resposta:
                corpo = resposta.read().decode("utf-8")
        except error.HTTPError as exc:
            detalhe = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"OpenRouter HTTP {exc.code}: {detalhe}"
            ) from exc
        except error.URLError as exc:
            raise RuntimeError(f"Falha de conexão com OpenRouter: {exc}") from exc

        try:
            resposta_json = json.loads(corpo)
            conteudo = resposta_json["choices"][0]["message"]["content"]
            saida = json.loads(conteudo)
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            raise RuntimeError(
                "Resposta do OpenRouter não contém JSON estruturado no formato esperado."
            ) from exc

        if not isinstance(saida, dict):
            raise TypeError("OpenRouter deve retornar um objeto JSON")
        return saida
