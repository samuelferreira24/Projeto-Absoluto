from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Protocol
import hashlib
import shutil
import tempfile

from .ciclo_operacional import (
    CicloOperacional,
    DecisaoOperacional,
    DecisorOperacional,
    ExecutorOperacional,
    ResultadoOperacional,
)
from .modelos import OrquestradorModelos
from .orquestrador import Missao
from .servico import Cerebro


class Capacidade(Protocol):
    nome: str

    def executar(self, argumentos: dict[str, Any], missao: Missao) -> ResultadoOperacional:
        ...


@dataclass(frozen=True)
class RegistroCapacidade:
    nome: str
    descricao: str
    executor: Callable[[dict[str, Any], Missao], ResultadoOperacional]


class DecisorPorModelo(DecisorOperacional):
    """Transforma uma ou mais IAs em capacidade decisória substituível.

    O modelo não acessa diretamente o estado interno: recebe apenas o objetivo,
    contexto operacional e catálogo das capacidades disponíveis.
    """

    def __init__(self, modelos: OrquestradorModelos, *, papel: str = "decisor") -> None:
        self.modelos = modelos
        self.papel = papel

    def decidir(self, missao: Missao) -> DecisaoOperacional:
        entrada = {
            "objetivo": missao.objetivo,
            "estado": missao.estado,
            "contexto": missao.contexto,
            "resultado_anterior": missao.resultado,
        }
        schema = {
            "type": "object",
            "required": ["executar", "concluida"],
            "properties": {
                "executar": {"type": "boolean"},
                "concluida": {"type": "boolean"},
                "acao": {"type": ["string", "null"]},
                "ferramenta": {"type": ["string", "null"]},
                "recurso": {"type": ["string", "null"]},
                "argumentos": {"type": "object"},
                "motivo": {"type": "string"},
            },
        }
        resultado = self.modelos.executar(
            self.papel,
            "Decida o próximo passo necessário para alcançar o objetivo. "
            "Use somente capacidades apresentadas pela entrada. "
            "Não invente resultado já não observado.",
            entrada,
            schema,
        )
        saida = resultado.saida
        return DecisaoOperacional(
            executar=bool(saida.get("executar", False)),
            concluida=bool(saida.get("concluida", False)),
            acao=saida.get("acao"),
            ferramenta=saida.get("ferramenta"),
            recurso=saida.get("recurso"),
            argumentos=dict(saida.get("argumentos") or {}),
            motivo=str(saida.get("motivo") or ""),
        )


class ExecutorDeCapacidades(ExecutorOperacional):
    """Despacha a decisão para uma capacidade registrada, sem fixar o tipo de IA."""

    def __init__(self, capacidades: dict[str, RegistroCapacidade]) -> None:
        self.capacidades = capacidades

    def executar(self, missao: Missao, decisao: DecisaoOperacional) -> ResultadoOperacional:
        if not decisao.ferramenta:
            return ResultadoOperacional(False, "decisão não informou ferramenta")
        capacidade = self.capacidades.get(decisao.ferramenta)
        if capacidade is None:
            return ResultadoOperacional(False, f"capacidade inexistente: {decisao.ferramenta}")
        try:
            resultado = capacidade.executor(dict(decisao.argumentos), missao)
        except Exception as exc:
            return ResultadoOperacional(
                False,
                f"capacidade falhou: {type(exc).__name__}: {exc}",
            )
        return resultado


class CondutorCerebro:
    """Conecta decisão, capacidades e memória em um ciclo contínuo.

    O Cérebro mantém o estado, histórico e recuperação. Modelos de IA são
    capacidades substituíveis; ferramentas e executores também são injetáveis.
    Nenhum fluxo específico (GitHub, DOCX, pesquisa etc.) é codificado como
    sequência obrigatória.
    """

    def __init__(self, cerebro: Cerebro, modelos: OrquestradorModelos) -> None:
        self.cerebro = cerebro
        self.modelos = modelos
        self.capacidades: dict[str, RegistroCapacidade] = {}

    def registrar_capacidade(
        self,
        nome: str,
        executor: Callable[[dict[str, Any], Missao], ResultadoOperacional],
        *,
        descricao: str = "",
    ) -> None:
        if not nome.strip():
            raise ValueError("nome da capacidade é obrigatório")
        self.capacidades[nome] = RegistroCapacidade(nome, descricao, executor)

    def catalogo(self) -> dict[str, str]:
        return {nome: registro.descricao for nome, registro in self.capacidades.items()}

    def executar_objetivo(self, missao_id: str, *, limite_ciclos: int = 20) -> list[dict[str, Any]]:
        missao = self.cerebro.orquestrador.missoes[missao_id]
        # O catálogo é contexto de decisão, não uma regra de execução.
        missao.contexto = {**missao.contexto, "capacidades_disponiveis": self.catalogo()}
        decisor = DecisorPorModelo(self.modelos)
        executor = ExecutorDeCapacidades(self.capacidades)
        historico = CicloOperacional(self.cerebro.orquestrador).executar(
            missao_id, decisor, executor, limite_ciclos=limite_ciclos
        )
        self._registrar_experiencia(missao, historico)
        self.cerebro._salvar_orquestracao()
        return historico

    def _registrar_experiencia(self, missao: Missao, historico: list[dict[str, Any]]) -> None:
        if not historico:
            return
        self.cerebro.registrar_memoria(
            "EXPERIENCIA",
            f"Ciclo operacional: {missao.objetivo}",
            "Ciclo conduzido pelo Cérebro com capacidades substituíveis.",
            fonte=f"missao:{missao.id}",
            contexto={"ciclos": len(historico), "estado": missao.estado},
            proveniencia={"tipo": "ciclo_operacional", "missao_id": missao.id},
            metadata={"historico": historico},
        )


def capacidade_obter_arquivo(
    nome: str,
    obter: Callable[[str], bytes],
    destino_dir: str | Path,
    *,
    fonte: str = "externa",
) -> Callable[[dict[str, Any], Missao], ResultadoOperacional]:
    """Cria uma capacidade genérica de obtenção de arquivo.

    O acesso ao provedor (GitHub, API, MCP etc.) fica fora do Cérebro e entra
    por contrato. Isso permite trocar o provedor sem trocar a ingestão.
    """

    raiz = Path(destino_dir)
    raiz.mkdir(parents=True, exist_ok=True)

    def executar(argumentos: dict[str, Any], missao: Missao) -> ResultadoOperacional:
        caminho = str(argumentos.get("caminho") or nome)
        dados = obter(caminho)
        if not isinstance(dados, bytes):
            raise TypeError("provedor deve retornar bytes")
        destino = raiz / Path(caminho).name
        destino.write_bytes(dados)
        sha = hashlib.sha256(dados).hexdigest()
        return ResultadoOperacional(
            True,
            f"arquivo obtido de {fonte}",
            {"path": str(destino), "nome": Path(caminho).name, "sha256": sha},
            evidencia=f"{fonte}:{caminho}",
        )

    return executar


def capacidade_ingerir_arquivo(cerebro: Cerebro) -> Callable[[dict[str, Any], Missao], ResultadoOperacional]:
    def executar(argumentos: dict[str, Any], missao: Missao) -> ResultadoOperacional:
        caminho = argumentos.get("path")
        if not caminho:
            return ResultadoOperacional(False, "path não informado")
        registro = cerebro.ingerir(caminho)
        return ResultadoOperacional(
            True,
            "arquivo ingerido",
            {"registro_id": registro.id, "kind": registro.kind},
            evidencia=registro.source,
        )
    return executar


def capacidade_buscar(cerebro: Cerebro) -> Callable[[dict[str, Any], Missao], ResultadoOperacional]:
    def executar(argumentos: dict[str, Any], missao: Missao) -> ResultadoOperacional:
        consulta = str(argumentos.get("consulta") or missao.objetivo)
        resultados = cerebro.buscar(consulta, limite=int(argumentos.get("limite", 5)))
        dados = [
            {
                "id": r.registro.id,
                "titulo": r.registro.title,
                "score": r.score,
                "conteudo": r.registro.content,
                "fonte": r.registro.source,
            }
            for r in resultados
        ]
        return ResultadoOperacional(
            True,
            f"{len(dados)} resultado(s) recuperado(s)",
            {"resultados": dados},
        )
    return executar
