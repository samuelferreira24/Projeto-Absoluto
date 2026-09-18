from __future__ import annotations

import json
import os
import shlex
import subprocess
import sys
import time
from typing import Any

from .servico import Cerebro
from .politica_execucao import Acao, NivelAutonomia, PoliticaExecucao


def executar_pedidos_pendentes(cerebro: Cerebro, comando: str, politica: PoliticaExecucao | None = None) -> list[dict[str, Any]]:
    """Processa uma leva de pedidos e retorna resultados estruturados."""
    politica = politica or PoliticaExecucao(NivelAutonomia.DELEGAR)
    acao_executor = Acao("executar_executor_externo", NivelAutonomia.DELEGAR, reversivel=False)
    comando_argv = shlex.split(comando)
    if not comando_argv:
        raise ValueError("comando do executor vazio")

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
                comando_argv,
                input=json.dumps(entrada, ensure_ascii=False),
                text=True,
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
            if not politica.autorizada(acao_executor):
                raise PermissionError("executor externo bloqueado pela política de autonomia")
            resultado = cerebro.executar_missao(pedido.missao_id, candidatos, executor)
            cerebro.despertador.concluir(pedido.id)
            resultados.append({"pedido": pedido.id, **resultado})
        except Exception as exc:
            cerebro.despertador.falhar(pedido.id, str(exc))
            resultados.append({"pedido": pedido.id, "executado": False, "erro": str(exc)})
    return resultados


def executar_continuamente(cerebro: Cerebro, comando: str, intervalo_segundos: int = 60, max_ciclos: int | None = None) -> list[list[dict[str, Any]]]:
    """Mantém o worker ativo até parada externa ou limite opcional.

    O worker é deliberadamente neutro quanto ao provedor: o comando externo
    recebe uma missão/caminho em JSON e devolve JSON. A persistência e a
    recuperação ficam no Cérebro, permitindo hospedar o processo fora do chat.
    """
    if intervalo_segundos < 0:
        raise ValueError("intervalo_segundos não pode ser negativo")
    if max_ciclos is not None and max_ciclos <= 0:
        raise ValueError("max_ciclos deve ser positivo quando informado")

    levas: list[list[dict[str, Any]]] = []
    ciclos = 0
    while max_ciclos is None or ciclos < max_ciclos:
        levas.append(executar_pedidos_pendentes(cerebro, comando))
        ciclos += 1
        if max_ciclos is not None and ciclos >= max_ciclos:
            break
        time.sleep(intervalo_segundos)
    return levas


def main() -> int:
    comando = os.environ.get("PROJETO_ABSOLUTO_EXECUTOR_CMD")
    if not comando:
        print("PROJETO_ABSOLUTO_EXECUTOR_CMD não configurado", file=sys.stderr)
        return 2
    intervalo = int(os.environ.get("PROJETO_ABSOLUTO_WORKER_INTERVALO", "60"))
    limite_raw = os.environ.get("PROJETO_ABSOLUTO_WORKER_MAX_CICLOS")
    limite = int(limite_raw) if limite_raw else None
    cerebro = Cerebro()
    resultados = executar_continuamente(cerebro, comando, intervalo, limite)
    print(json.dumps(resultados, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
