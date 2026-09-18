from __future__ import annotations

from typing import Any
import json
import time
import urllib.error
import urllib.request


class ClienteAppDireto:
    """Cliente do App via HTTP, sem depender de Termux ou GitHub Actions."""

    def __init__(
        self,
        endpoint: str = "http://127.0.0.1:8787",
        *,
        token: str | None = None,
        timeout: float = 60.0,
    ) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.token = token
        self.timeout = timeout

    def _request(
        self,
        path: str,
        *,
        method: str = "GET",
        payload: dict[str, Any] | None = None,
        timeout: float | None = None,
    ) -> tuple[int, dict[str, Any]]:
        dados = json.dumps(payload or {}).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["X-Cerebro-Token"] = self.token
        req = urllib.request.Request(
            self.endpoint + path,
            data=dados if method != "GET" else None,
            headers=headers,
            method=method,
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout or self.timeout) as resposta:
                corpo = resposta.read().decode("utf-8")
                return resposta.status, json.loads(corpo or "{}")
        except urllib.error.HTTPError as exc:
            corpo = exc.read().decode("utf-8")
            try:
                dados_erro = json.loads(corpo or "{}")
            except json.JSONDecodeError:
                dados_erro = {"erro": corpo}
            return exc.code, dados_erro

    def saude(self) -> dict[str, Any]:
        status, dados = self._request("/saude")
        if status != 200:
            raise RuntimeError(dados.get("erro", f"HTTP {status}"))
        return dados

    def executar(
        self,
        capacidade: str,
        payload: dict[str, Any] | None = None,
        *,
        timeout: float | None = None,
        intervalo: float = 0.2,
    ) -> dict[str, Any]:
        status, aceito = self._request(
            "/v1/trabalho",
            method="POST",
            payload={"capacidade": capacidade, "payload": payload or {}},
        )
        if status != 202:
            raise RuntimeError(aceito.get("erro", f"HTTP {status}"))

        trabalho_id = str(aceito["id"])
        limite = time.monotonic() + (timeout or self.timeout)
        while time.monotonic() < limite:
            status, resultado = self._request(
                f"/v1/trabalho/{trabalho_id}/resultado",
                timeout=min(2.0, max(0.2, limite - time.monotonic())),
            )
            if status == 200:
                return resultado
            if status != 404:
                raise RuntimeError(resultado.get("erro", f"HTTP {status}"))
            time.sleep(intervalo)

        raise TimeoutError(f"App não concluiu o trabalho {trabalho_id} dentro do prazo")
