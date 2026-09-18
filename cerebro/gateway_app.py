from __future__ import annotations

from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from queue import Empty, Queue
from threading import Lock
from typing import Any
import json
import os
import threading
import time
import uuid
from urllib.parse import parse_qs, urlparse


@dataclass
class TrabalhoApp:
    id: str
    capacidade: str
    payload: dict[str, Any]
    criado_em: float = field(default_factory=time.time)


class GatewayAppDireto:
    """Canal HTTP direto entre o Cérebro e o App, sem Termux.

    O App mantém uma conexão de saída/polling com o Cérebro. O Cérebro
    coloca trabalhos na fila; o App executa a capacidade usando seus
    próprios motores/configurações e devolve o resultado.
    """

    def __init__(self) -> None:
        self._fila: Queue[TrabalhoApp] = Queue()
        self._resultados: dict[str, dict[str, Any]] = {}
        self._lock = Lock()

    def enfileirar(
        self,
        capacidade: str,
        payload: dict[str, Any] | None = None,
        trabalho_id: str | None = None,
    ) -> TrabalhoApp:
        trabalho = TrabalhoApp(
            id=trabalho_id or f"app-{uuid.uuid4().hex}",
            capacidade=capacidade,
            payload=payload or {},
        )
        with self._lock:
            self._resultados.pop(trabalho.id, None)
        self._fila.put(trabalho)
        return trabalho

    def proximo(self, timeout: float = 0.0) -> TrabalhoApp | None:
        try:
            return self._fila.get(timeout=max(0.0, timeout))
        except Empty:
            return None

    def concluir(
        self,
        trabalho_id: str,
        *,
        sucesso: bool,
        resultado: Any = None,
        erro: str | None = None,
    ) -> None:
        with self._lock:
            self._resultados[trabalho_id] = {
                "id": trabalho_id,
                "sucesso": sucesso,
                "resultado": resultado,
                "erro": erro,
                "concluido_em": time.time(),
            }

    def resultado(self, trabalho_id: str) -> dict[str, Any] | None:
        with self._lock:
            return self._resultados.get(trabalho_id)


class _Handler(BaseHTTPRequestHandler):
    gateway: GatewayAppDireto
    token: str

    def log_message(self, *_args: Any) -> None:
        return

    def _autorizado(self) -> bool:
        return not self.token or self.headers.get("X-Cerebro-Token", "") == self.token

    def _responder(self, status: int, dados: dict[str, Any]) -> None:
        corpo = json.dumps(dados, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Cerebro-Token")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(corpo)

    def do_OPTIONS(self) -> None:
        self._responder(204, {})

    def do_GET(self) -> None:
        if not self._autorizado():
            self._responder(401, {"erro": "não autorizado"})
            return

        parsed = urlparse(self.path)
        caminho = parsed.path
        if caminho == "/saude":
            self._responder(200, {"ok": True, "servico": "cerebro-app-direto"})
            return

        if caminho == "/v1/capacidades":
            self._responder(
                200,
                {
                    "capacidades": ["inferencia"],
                    "modo": "polling-direto",
                    "termux_necessario": False,
                },
            )
            return

        if caminho == "/v1/trabalho/proximo":
            valores = parse_qs(parsed.query)
            try:
                timeout = min(float(valores.get("timeout", ["0"])[0]), 30.0)
            except ValueError:
                timeout = 0.0
            trabalho = self.gateway.proximo(timeout)
            if trabalho is None:
                self._responder(204, {})
                return
            self._responder(
                200,
                {
                    "id": trabalho.id,
                    "capacidade": trabalho.capacidade,
                    "payload": trabalho.payload,
                    "criado_em": trabalho.criado_em,
                },
            )
            return

        if caminho.startswith("/v1/trabalho/") and caminho.endswith("/resultado"):
            trabalho_id = caminho.split("/")[3]
            resultado = self.gateway.resultado(trabalho_id)
            if resultado is None:
                self._responder(404, {"erro": "resultado ainda não disponível"})
            else:
                self._responder(200, resultado)
            return

        self._responder(404, {"erro": "rota não encontrada"})

    def do_POST(self) -> None:
        if not self._autorizado():
            self._responder(401, {"erro": "não autorizado"})
            return

        parsed = urlparse(self.path)
        try:
            tamanho = int(self.headers.get("Content-Length", "0"))
            dados = json.loads(self.rfile.read(tamanho) or b"{}")
        except (ValueError, json.JSONDecodeError) as exc:
            self._responder(400, {"erro": f"json inválido: {exc}"})
            return

        if parsed.path == "/v1/trabalho":
            capacidade = str(dados.get("capacidade", "")).strip()
            if not capacidade:
                self._responder(400, {"erro": "capacidade obrigatória"})
                return
            trabalho = self.gateway.enfileirar(
                capacidade,
                dados.get("payload") or {},
                dados.get("id"),
            )
            self._responder(
                202,
                {
                    "id": trabalho.id,
                    "estado": "aguardando_app",
                    "capacidade": trabalho.capacidade,
                },
            )
            return

        if parsed.path.startswith("/v1/trabalho/") and parsed.path.endswith("/resultado"):
            trabalho_id = parsed.path.split("/")[3]
            self.gateway.concluir(
                trabalho_id,
                sucesso=bool(dados.get("sucesso")),
                resultado=dados.get("resultado"),
                erro=dados.get("erro"),
            )
            self._responder(200, {"ok": True, "id": trabalho_id})
            return

        self._responder(404, {"erro": "rota não encontrada"})


class ServidorGatewayApp:
    """Servidor opcional e independente do Cérebro.

    Por padrão fica somente em localhost. Para uso remoto, configure host
    explicitamente e um token em CEREBRO_APP_TOKEN.
    """

    def __init__(
        self,
        gateway: GatewayAppDireto | None = None,
        *,
        host: str = "127.0.0.1",
        porta: int = 8787,
        token: str | None = None,
    ) -> None:
        self.gateway = gateway or GatewayAppDireto()
        self.host = host
        self.porta = porta
        self.token = token if token is not None else os.environ.get("CEREBRO_APP_TOKEN", "")
        handler = type(
            "GatewayHandler",
            (_Handler,),
            {"gateway": self.gateway, "token": self.token},
        )
        self._server = ThreadingHTTPServer((host, porta), handler)
        self._thread: threading.Thread | None = None

    def iniciar(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(
            target=self._server.serve_forever,
            name="cerebro-app-gateway",
            daemon=True,
        )
        self._thread.start()

    def parar(self) -> None:
        self._server.shutdown()
        self._server.server_close()
        if self._thread:
            self._thread.join(timeout=2)
            self._thread = None
