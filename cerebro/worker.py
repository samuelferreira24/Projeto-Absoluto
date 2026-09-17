from __future__ import annotations

import json
import os
import subprocess
import sys
from typing import Any

from .servico import Cerebro


def executar_pedidos_pendentes(cerebro: Cerebro, comando: str) -> list[dict[str, Any]]:
    resultados: list[dict[str, Any]] = []
    for pedido in cerebro.despertador.pendentes():
        cerebro.despertador.iniciar(pedido.id)
        missao = cerebro.orquestrador.missoes.get(pedido.missao_id)
        if missao is None:
            cerebro.despertador.falhar(pedido.id, f"missão inexistente: {pedido.missao_id}")
            resultados.append({"pedido": pedido.id, "executado": False, "erro": "missão inexistente"})
            continue

        def candidatos(m):
            sinais = m.contexto.get("sinais") if isinstance(m.contexto, dict) else None
            return cerebro.candidatos_rede(sinais)

        def executor(m, caminho):
            entrada = {
                "missao": vars(m),
                "pedido_despertar": vars(pedido),
                "caminho": caminho,
            }
            processo = subprocess.run(
                comando,
                input=json.dumps(entrada, ensure_ascii=False),
                text=True,
                shell=True,
                capture_output=True,
                timeout=900,
                check=False,
            )
            if processo.returncode != 0:
                raise RuntimeError(processo.stderr.strip() or f"executor retornou {processo.returncode}")
            try:
                return json.loads(processo.stdout or "{}")
            except json.JSONDecodeError as exc:
                raise RuntimeError("executor deve retornar JSON em stdout") from exc

        try:
            resultado = cerebro.executar_missao(pedido.missao_id, candidatos, executor)
            cerebro.despertador.concluir(pedido.id)
            resultados.append({"pedido": pedido.id, **resultado})
        except Exception as exc:
            cerebro.despertador.falhar(pedido.id, str(exc))
            resultados.append({"pedido": pedido.id, "executado": False, "erro": str(exc)})
    return resultados


def main() -> int:
    comando = os.environ.get("PROJETO_ABSOLUTO_EXECUTOR_CMD")
    if not comando:
        print("PROJETO_ABSOLUTO_EXECUTOR_CMD não configurado", file=sys.stderr)
        return 2
    cerebro = Cerebro()
    resultados = executar_pedidos_pendentes(cerebro, comando)
    print(json.dumps(resultados, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
