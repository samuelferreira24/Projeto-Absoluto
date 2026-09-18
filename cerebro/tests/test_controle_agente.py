from pathlib import Path

from cerebro.controle_agente import AutorizacaoAgente, ControleAgente, EventoTelemetria, TelemetriaAgente
from cerebro.identidade import identidade_agente


def _controle(tmp_path: Path, *, requer_aprovacao: bool = False) -> ControleAgente:
    autorizacao = AutorizacaoAgente(
        identidade=identidade_agente(),
        ferramentas_permitidas=("pesquisa",),
        recursos_permitidos=("web",),
        nivel_maximo_autonomia=2,
        custo_maximo=10.0,
        cadeia_maxima=3,
        requer_aprovacao=requer_aprovacao,
    )
    return ControleAgente(autorizacao, TelemetriaAgente(tmp_path / "telemetria.jsonl"))


def test_bloqueia_ferramenta_nao_permitida(tmp_path: Path):
    controle = _controle(tmp_path)
    permitido, motivo = controle.verificar(operacao="buscar", ferramenta="shell", recurso="web")
    assert not permitido
    assert "não permitida" in motivo
    assert controle.telemetria.resumo()["bloqueios"] == 1


def test_bloqueia_custo_e_cadeia(tmp_path: Path):
    controle = _controle(tmp_path)
    permitido, _ = controle.verificar(operacao="buscar", ferramenta="pesquisa", recurso="web", custo_estimado=11)
    assert not permitido
    permitido, _ = controle.verificar(operacao="buscar", ferramenta="pesquisa", recurso="web", custo_estimado=1, cadeia=4)
    assert not permitido


def test_aprovacao_explicita(tmp_path: Path):
    controle = _controle(tmp_path, requer_aprovacao=True)
    permitido, motivo = controle.verificar(operacao="sensivel", ferramenta="pesquisa", recurso="web")
    assert not permitido
    assert "aprovação" in motivo
    permitido, motivo = controle.verificar(operacao="sensivel", ferramenta="pesquisa", recurso="web", aprovacao=True)
    assert permitido
    assert motivo == "OK"


def test_telemetria_preserva_eventos(tmp_path: Path):
    telemetry = TelemetriaAgente(tmp_path / "telemetria.jsonl")
    evento = EventoTelemetria(tipo="agent.execution", agente_id="PA-AGENTE-TESTE", operacao="teste", estado="CONCLUIDO")
    telemetry.registrar(evento)
    telemetry.registrar(evento)
    assert len(telemetry.listar()) == 2
    assert telemetry.listar()[0]["evento_id"] == evento.evento_id
