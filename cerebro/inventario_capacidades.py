from __future__ import annotations

"""Inventário técnico das capacidades do Cérebro.

Objetivo:
- separar capacidade implementada de capacidade efetivamente exposta/usa pelo Cérebro;
- mostrar dependências físicas (módulo), entrada pela fachada Cerebro e testes;
- identificar capacidades ainda parciais, planejadas ou sem persistência durável.

O inventário é deliberadamente descritivo: não transforma uma especificação
em uma capacidade implementada.
"""

from dataclasses import asdict, dataclass
from pathlib import Path
import ast
import json
from typing import Any


@dataclass(frozen=True)
class CapacidadeInventariada:
    id: str
    nome: str
    categoria: str
    modulo: str
    implementada: bool
    exposta_pelo_cerebro: bool
    usada_internamente: bool
    persistencia: str
    testes: tuple[str, ...]
    estado: str
    observacao: str = ""


MAPA_CAPACIDADES: tuple[CapacidadeInventariada, ...] = (
    CapacidadeInventariada(
        "entrada.documento", "Inspeção e ingestão de documentos", "Entrada",
        "cerebro/ingestao.py", True, True, True, "RepositorioJSONL",
        ("cerebro/tests/test_ingestao.py",), "IMPLEMENTADA",
    ),
    CapacidadeInventariada(
        "entrada.coleta", "Coleta e preservação de eventos/fontes", "Entrada",
        "cerebro/coleta.py", True, True, True, "captura bruta + repositório",
        ("cerebro/tests/test_coleta.py",), "IMPLEMENTADA",
    ),
    CapacidadeInventariada(
        "entrada.dispatch", "Despacho para adaptadores de coleta", "Entrada",
        "cerebro/adaptador_dispatch.py", True, True, True, "via captura",
        ("cerebro/tests/test_adaptador_dispatch.py",), "IMPLEMENTADA",
    ),
    CapacidadeInventariada(
        "memoria.registro", "Registro persistente de conhecimento", "Memória",
        "cerebro/nucleo.py", True, True, True, "JSONL",
        ("cerebro/tests/test_nucleo.py",), "IMPLEMENTADA",
    ),
    CapacidadeInventariada(
        "memoria.busca", "Busca híbrida e recuperação", "Memória",
        "cerebro/recuperacao.py", True, True, True, "derivada dos registros",
        ("tests/test_nucleo_recuperacao.py",), "IMPLEMENTADA",
    ),
    CapacidadeInventariada(
        "memoria.relacoes", "Expansão de relações entre registros", "Memória",
        "cerebro/recuperacao.py", True, True, True, "derivada dos registros",
        ("tests/test_nucleo_recuperacao.py",), "IMPLEMENTADA",
    ),
    CapacidadeInventariada(
        "memoria.semantica", "Unidades e relações semânticas + auditoria", "Memória",
        "cerebro/semantica.py", True, True, True, "registros",
        ("cerebro/tests/test_semantica_core.py", "cerebro/tests/test_avaliacao_semantica.py"), "IMPLEMENTADA",
    ),
    CapacidadeInventariada(
        "memoria.temporal", "Modelagem temporal do conhecimento", "Memória",
        "cerebro/temporal.py", True, False, False, "parcial",
        ("cerebro/tests/test_temporal.py",), "IMPLEMENTADA_PARCIALMENTE",
        "Existe como capacidade, mas ainda não está integrada à fachada principal.",
    ),
    CapacidadeInventariada(
        "memoria.aprendizado", "Aprendizado persistente", "Aprendizado",
        "cerebro/aprendizado.py", True, True, True, "JSONL + fundamentais",
        ("cerebro/tests/test_aprendizado.py",), "IMPLEMENTADA",
    ),
    CapacidadeInventariada(
        "memoria.consolidacao", "Consolidação do aprendizado", "Aprendizado",
        "cerebro/consolidar_aprendizados.py", True, True, True, "JSON derivado",
        ("cerebro/tests/test_consolidar_aprendizados.py", "cerebro/tests/test_integracao_aprendizados.py"), "IMPLEMENTADA",
    ),
    CapacidadeInventariada(
        "memoria.sabedoria", "Transformação de aprendizado em sabedoria", "Aprendizado",
        "cerebro/sabedoria.py", True, False, False, "parcial",
        ("cerebro/tests/test_sabedoria.py",), "IMPLEMENTADA_PARCIALMENTE",
        "Módulo existe e é testado, mas não está exposto diretamente pela fachada atual.",
    ),
    CapacidadeInventariada(
        "memoria.rede", "Rede evolutiva, relações e pontos de alavancagem", "Memória",
        "cerebro/rede_evolutiva.py", True, True, True, "rede_evolutiva.json",
        ("cerebro/tests/test_rede_evolutiva.py",), "IMPLEMENTADA",
    ),
    CapacidadeInventariada(
        "historico.reconstrucao", "Reconstrução histórica", "Histórico",
        "cerebro/reconstrucao_historica.py", True, False, False, "artefatos históricos",
        ("cerebro/tests/test_reconstrucao_historica.py",), "IMPLEMENTADA_PARCIALMENTE",
    ),
    CapacidadeInventariada(
        "contexto.operacional", "Construção e persistência de contexto operacional", "Continuidade",
        "cerebro/contexto_operacional.py", True, True, True, "JSON + prompt",
        ("cerebro/tests/test_contexto_operacional.py",), "IMPLEMENTADA",
    ),
    CapacidadeInventariada(
        "continuidade.chat", "Continuidade entre chats/sessões", "Continuidade",
        "cerebro/continuidade.py", True, True, True, "snapshot + prompt",
        ("cerebro/tests/test_continuidade.py",), "IMPLEMENTADA",
    ),
    CapacidadeInventariada(
        "interface.chat", "Captura de mensagens e conversas do chat", "Continuidade",
        "cerebro/interface_chat.py", True, True, True, "via repositório",
        (), "IMPLEMENTADA",
    ),
    CapacidadeInventariada(
        "construcao.rastreabilidade", "Mapa de elementos e relações de construção", "Construção",
        "cerebro/rastreabilidade.py", True, True, True, "em memória",
        ("cerebro/tests/test_estado_rastreabilidade.py",), "IMPLEMENTADA_PARCIALMENTE",
        "Ainda precisa de persistência durável completa.",
    ),
    CapacidadeInventariada(
        "execucao.missao", "Registro e execução de missões", "Execução",
        "cerebro/orquestrador.py + cerebro/runtime.py", True, True, True, "JSON",
        ("cerebro/tests/test_orquestrador.py", "cerebro/tests/test_runtime.py"), "IMPLEMENTADA",
    ),
    CapacidadeInventariada(
        "execucao.continua", "Runtime contínuo", "Execução",
        "cerebro/runtime.py", True, True, True, "runtime.json",
        ("cerebro/tests/test_runtime.py",), "IMPLEMENTADA",
    ),
    CapacidadeInventariada(
        "execucao.politica", "Políticas e controles de execução", "Execução",
        "cerebro/politica.py + cerebro/politica_execucao.py", True, False, False, "parcial",
        ("cerebro/tests/test_politica_execucao.py",), "IMPLEMENTADA_PARCIALMENTE",
    ),
    CapacidadeInventariada(
        "execucao.worker", "Worker de execução", "Execução",
        "cerebro/worker.py", True, False, False, "dependente do runtime",
        ("cerebro/tests/test_worker.py",), "IMPLEMENTADA_PARCIALMENTE",
    ),
    CapacidadeInventariada(
        "despertar", "Despertar por pedidos/eventos", "Execução",
        "cerebro/despertador.py", True, True, True, "despertar.json",
        ("cerebro/tests/test_despertador.py", "cerebro/tests/test_servico_despertador.py"), "IMPLEMENTADA",
    ),
    CapacidadeInventariada(
        "planejamento.grafo", "Grafo de tarefas, dependências e paralelismo", "Planejamento",
        "cerebro/grafo_tarefas.py", True, True, True, "em memória",
        ("cerebro/tests/test_grafo_tarefas.py",), "IMPLEMENTADA_PARCIALMENTE",
        "O estado do grafo ainda não é persistido.",
    ),
    CapacidadeInventariada(
        "planejamento.agendamento", "Agendamento adaptativo e replanejamento", "Planejamento",
        "cerebro/agendador.py", True, True, True, "agendador.json",
        ("cerebro/tests/test_agendador.py",), "IMPLEMENTADA",
    ),
    CapacidadeInventariada(
        "planejamento.orquestracao", "Orquestração adaptativa", "Planejamento",
        "cerebro/orquestracao_adaptativa.py", True, True, True, "parcial",
        ("cerebro/tests/test_orquestracao_adaptativa.py",), "IMPLEMENTADA_PARCIALMENTE",
        "Decisões do orquestrador ainda precisam de persistência própria.",
    ),
    CapacidadeInventariada(
        "planejamento.composicao", "Composição de capacidades", "Planejamento",
        "cerebro/composicao.py", True, False, False, "em memória",
        ("cerebro/tests/test_composicao.py",), "IMPLEMENTADA_PARCIALMENTE",
    ),
    CapacidadeInventariada(
        "planejamento.sinergia", "Detecção e exploração de sinergias", "Planejamento",
        "cerebro/sinergia.py", True, True, True, "em memória",
        ("cerebro/tests/test_sinergia.py",), "IMPLEMENTADA_PARCIALMENTE",
        "O conhecimento do detector ainda não é persistido como memória durável.",
    ),
    CapacidadeInventariada(
        "recursos", "Controle de recursos/capacidade/combustível", "Recursos",
        "cerebro/recursos.py", True, False, False, "parcial",
        ("cerebro/tests/test_recursos.py",), "IMPLEMENTADA_PARCIALMENTE",
        "Existe modelo de recursos, mas consumo quantitativo real ainda não está integrado ao ciclo.",
    ),
    CapacidadeInventariada(
        "organizacao", "Fila de organização do conhecimento", "Organização",
        "cerebro/organizacao.py", True, True, True, "organizacao.jsonl",
        ("cerebro/tests/test_organizacao.py",), "IMPLEMENTADA",
    ),
    CapacidadeInventariada(
        "auditoria", "Auditoria semântica e de integridade", "Governança",
        "cerebro/auditoria.py", True, True, False, "resultado derivado",
        ("cerebro/tests/test_avaliacao_semantica.py",), "IMPLEMENTADA",
    ),
)


def inventariar() -> list[dict[str, Any]]:
    return [asdict(item) for item in MAPA_CAPACIDADES]


def resumo() -> dict[str, Any]:
    itens = MAPA_CAPACIDADES
    return {
        "total_capacidades": len(itens),
        "implementadas": sum(i.implementada for i in itens),
        "expostas_pelo_cerebro": sum(i.exposta_pelo_cerebro for i in itens),
        "usadas_internamente": sum(i.usada_internamente for i in itens),
        "implementadas_parcialmente": sum(i.estado == "IMPLEMENTADA_PARCIALMENTE" for i in itens),
        "categorias": sorted({i.categoria for i in itens}),
        "sem_persistencia_duravel": sum(i.persistencia in {"em memória", "parcial"} for i in itens),
    }


def exportar_json(path: str | Path) -> dict[str, Any]:
    destino = Path(path)
    payload = {
        "versao": "0.1",
        "objetivo": "Fotografar capacidades do Cérebro, distinguindo existência, exposição, uso e maturidade.",
        "resumo": resumo(),
        "capacidades": inventariar(),
    }
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload


def inventariar_arquivos(cerebro_dir: str | Path = "cerebro") -> list[dict[str, str]]:
    """Complemento: mostra módulos Python existentes no diretório do Cérebro."""
    root = Path(cerebro_dir)
    encontrados: list[dict[str, str]] = []
    for path in sorted(root.glob("*.py")):
        if path.name.startswith("__"):
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
            classes = [n.name for n in tree.body if isinstance(n, ast.ClassDef)]
            funcoes = [n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        except (OSError, SyntaxError):
            classes, funcoes = [], []
        encontrados.append({
            "arquivo": str(path),
            "classes": ", ".join(classes),
            "funcoes": ", ".join(funcoes),
        })
    return encontrados


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Inventário técnico das capacidades do Cérebro.")
    parser.add_argument("--json", dest="json_path", help="exporta o inventário completo para JSON")
    parser.add_argument("--arquivos", action="store_true", help="também lista módulos/classes/funções encontrados")
    args = parser.parse_args()

    print(json.dumps({"resumo": resumo(), "capacidades": inventariar()}, ensure_ascii=False, indent=2))
    if args.arquivos:
        print(json.dumps({"arquivos": inventariar_arquivos()}, ensure_ascii=False, indent=2))
    if args.json_path:
        exportar_json(args.json_path)
