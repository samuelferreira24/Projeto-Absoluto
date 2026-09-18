from __future__ import annotations

import json
import threading
import urllib.request

from cerebro.cliente_app import ClienteAppDireto
from cerebro.gateway_app import GatewayAppDireto, ServidorGatewayApp


def test_gateway_direto_http_sem_termux():
    gateway = GatewayAppDireto()
    servidor = ServidorGatewayApp(gateway, porta=0)
    # ThreadingHTTPServer escolhe uma porta livre quando porta=0.
    servidor.porta = servidor._server.server_address[1]
    servidor.iniciar()

    try:
        cliente = ClienteAppDireto(f"http://127.0.0.1:{servidor.porta}")
        assert cliente.saude()["ok"] is True

        def simular_app():
            req = urllib.request.Request(
                f"http://127.0.0.1:{servidor.porta}/v1/trabalho/proximo?timeout=2"
            )
            with urllib.request.urlopen(req, timeout=3) as resposta:
                trabalho = json.loads(resposta.read().decode())
            assert trabalho["capacidade"] == "inferencia"
            assert trabalho["payload"]["mensagem"] == "PONTE_CEREBRO_OK"

            body = json.dumps({
                "sucesso": True,
                "resultado": "PONTE_CEREBRO_OK",
            }).encode()
            req2 = urllib.request.Request(
                f"http://127.0.0.1:{servidor.porta}/v1/trabalho/{trabalho['id']}/resultado",
                data=body,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req2, timeout=3):
                pass

        app = threading.Thread(target=simular_app)
        app.start()
        resultado = cliente.executar(
            "inferencia",
            {"mensagem": "PONTE_CEREBRO_OK"},
            timeout=5,
        )
        app.join(timeout=3)

        assert resultado["sucesso"] is True
        assert resultado["resultado"] == "PONTE_CEREBRO_OK"
    finally:
        servidor.parar()


def test_gateway_expoe_que_termux_nao_e_necessario():
    gateway = GatewayAppDireto()
    servidor = ServidorGatewayApp(gateway, porta=0)
    servidor.porta = servidor._server.server_address[1]
    servidor.iniciar()
    try:
        req = urllib.request.Request(
            f"http://127.0.0.1:{servidor.porta}/v1/capacidades"
        )
        with urllib.request.urlopen(req, timeout=3) as resposta:
            dados = json.loads(resposta.read().decode())
        assert dados["termux_necessario"] is False
        assert "inferencia" in dados["capacidades"]
    finally:
        servidor.parar()


def test_gateway_rejeita_token_incorreto():
    import urllib.error
    import urllib.request

    servidor = ServidorGatewayApp(GatewayAppDireto(), porta=0, token="segredo")
    porta = servidor._server.server_address[1]
    servidor.iniciar()
    try:
        req = urllib.request.Request(f"http://127.0.0.1:{porta}/saude")
        try:
            urllib.request.urlopen(req, timeout=2)
            assert False, "deveria rejeitar"
        except urllib.error.HTTPError as exc:
            assert exc.code == 401

        req_ok = urllib.request.Request(
            f"http://127.0.0.1:{porta}/saude",
            headers={"X-Cerebro-Token": "segredo"},
        )
        with urllib.request.urlopen(req_ok, timeout=2) as resposta:
            assert json.loads(resposta.read().decode())["ok"] is True
    finally:
        servidor.parar()
