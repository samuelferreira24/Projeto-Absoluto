from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from .auditoria import ResultadoAuditoria, auditar_semantica
from .coleta import ColetorMemoria, EventoCapturado
from .despertador import Despertador, PedidoDespertar
from .estado import EstadoSistema
from .ingestao import DocumentoEstruturado, extrair, registrar_fonte
from .nucleo import Registro, RepositorioJSONL, novo_registro
from .orquestrador import Missao, Orquestrador
from .organizacao import FilaOrganizacao
from .recuperacao import ResultadoBusca, buscar_hibrido, expandir_relacoes
from .rastreabilidade import ElementoConstrucao, MapaConstrucao, RelacaoConstrucao
from .rede_evolutiva import ArestaRede, NoRede, RedeEvolutiva
from .runtime import RuntimeContinuo
from .semantica import RelacaoSemantica, UnidadeSemantica
from .consolidar_aprendizados import salvar_consolidado


class Cerebro:
    """Fachada operacional do Cérebro, mantendo as camadas internas substituíveis."""

    def __init__(self, dados: str | Path = "cerebro/data") -> None:
        self.repo = RepositorioJSONL(dados)
        self.estado_path = self.repo.root / "estado.json"
        self.rede_path = self.repo.root / "rede_evolutiva.json"
        self.orquestrador_path = self.repo.root / "orquestrador.json"
        self.runtime_path = self.repo.root / "runtime.json"
        self.despertador = Despertador(self.repo.root / "despertar.json")
        self.coletor = ColetorMemoria(self.repo)
        self.fila_organizacao = FilaOrganizacao(self.repo.root / "organizacao.jsonl")
        self.estado = EstadoSistema()
        if self.estado_path.exists():
            self.estado = EstadoSistema.carregar(self.estado_path)
        self.mapa = MapaConstrucao()
        self.rede = RedeEvolutiva.carregar(self.rede_path) if self.rede_path.exists() else RedeEvolutiva()
        self.orquestrador = Orquestrador(self.orquestrador_path)
        self.runtime = RuntimeContinuo(self.orquestrador, self.runtime_path)

    def inspecionar(self, arquivo: str | Path) -> DocumentoEstruturado:
        return extrair(arquivo)

    def ingerir(self, arquivo: str | Path) -> Registro:
        documento = self.inspecionar(arquivo)
        if documento.erros:
            raise ValueError(f"Falha na ingestão: {documento.erros}")
        return registrar_fonte(self.repo, documento)

    def capturar_evento(self, evento: EventoCapturado) -> list[Registro]:
        """Entrada única para eventos provenientes de chats, IAs e plataformas."""
        return self.coletor.capturar(evento)

    def registrar_memoria(
        self,
        tipo: str,
        titulo: str,
        conteudo: str,
        *,
        fonte: str | None = None,
        contexto: dict[str, Any] | None = None,
        relacoes: list[dict[str, str]] | None = None,
        proveniencia: dict[str, Any] | None = None,
        estado: str = "NOVO",
        metadata: dict[str, Any] | None = None,
    ) -> Registro:
        """Registra conhecimento produzido no próprio processo do Projeto."""
        registro = novo_registro(
            self.repo,
            tipo,
            titulo,
            conteudo,
            source=fonte,
            relations=list(relacoes or []),
            provenance=dict(proveniencia or {}),
            state=estado,
            metadata={"contexto": dict(contexto or {}), **dict(metadata or {})},
        )
        self.repo.salvar(registro)
        return registro

    def registrar_entendimento(self, titulo: str, conteudo: str, **kwargs: Any) -> Registro:
        return self.registrar_memoria("ENTENDIMENTO", titulo, conteudo, **kwargs)

    def registrar_descoberta(self, titulo: str, conteudo: str, **kwargs: Any) -> Registro:
        return self.registrar_memoria("DESCOBERTA", titulo, conteudo, **kwargs)

    def registrar_progresso(self, titulo: str, conteudo: str, **kwargs: Any) -> Registro:
        return self.registrar_memoria("PROGRESSO", titulo, conteudo, **kwargs)

    def consolidar_aprendizados(self, memoria: str | Path = "cerebro/memoria") -> dict[str, Any]:
        """Torna o aprendizado acumulado + novo uma visão consolidada do Cérebro.

        Os arquivos de origem permanecem intactos; a consolidação é uma camada derivada.
        """
        memoria = Path(memoria)
        return salvar_consolidado(
            memoria / "aprendizados_consolidados_v0_1.json",
            memoria / "aprendizados.jsonl",
            memoria / "aprendizados_fundamentais_v0_1.json",
        )

    def registros(self) -> list[Registro]:
        return list(self.repo._iter_registros())

    def buscar(self, consulta: str, limite: int = 10) -> list[ResultadoBusca]:
        return buscar_hibrido(self.registros(), consulta, limite)

    def relacionados(self, ids: list[str], profundidade: int = 1) -> list[Registro]:
        return expandir_relacoes(self.registros(), ids, profundidade)

    def auditar(self, unidades: list[UnidadeSemantica], relacoes: list[RelacaoSemantica] | None = None) -> ResultadoAuditoria:
        return auditar_semantica(unidades, relacoes)

    def adicionar_elemento_construcao(self, elemento: ElementoConstrucao) -> None:
        self.mapa.adicionar(elemento)

    def adicionar_relacao_construcao(self, relacao: RelacaoConstrucao) -> None:
        self.mapa.relacionar(relacao)

    def validar_construcao(self) -> list[str]:
        return self.mapa.validar()

    def adicionar_no_rede(self, no: NoRede) -> None:
        self.rede.adicionar_no(no)

    def adicionar_nos_rede(self, nos: list[NoRede]) -> None:
        self.rede.adicionar_nos(nos)

    def conectar_rede(self, aresta: ArestaRede) -> None:
        self.rede.conectar(aresta)

    def relacionados_rede(self, no_id: str) -> list[str]:
        return self.rede.relacionados(no_id)

    def impulso_total(self, no_id: str) -> float:
        return self.rede.impulso_total(no_id)

    def candidatos_rede(self, contexto: dict[str, float] | None = None) -> list[tuple[str, float]]:
        return self.rede.candidatos_contextuais(contexto)

    def pontos_de_alavancagem(self, limite: int = 10) -> list[tuple[str, float]]:
        return self.rede.pontos_de_alavancagem(limite)

    def validar_rede(self) -> list[str]:
        return self.rede.validar()

    def registrar_missao(self, missao: Missao) -> None:
        self.orquestrador.registrar_missao(missao)

    def solicitar_despertar(self, missao_id: str, origem: str, correlation_id: str | None = None, detalhes: dict[str, Any] | None = None) -> PedidoDespertar:
        return self.despertador.solicitar(missao_id, origem, correlation_id, detalhes)

    def despertares_pendentes(self, missao_id: str | None = None) -> list[PedidoDespertar]:
        return self.despertador.pendentes(missao_id)

    def executar_missao(self, missao_id: str, candidatos: Callable, executor: Callable) -> dict[str, Any]:
        """Executa um ciclo recuperável sem depender da conversa aberta."""
        resultado = self.runtime.executar_ciclo(missao_id, candidatos, executor)
        self.salvar_estado()
        return resultado

    def salvar_estado(self) -> None:
        self.estado.salvar(self.estado_path)
        self.rede.salvar(str(self.rede_path))

    def diagnostico(self) -> dict[str, Any]:
        registros = self.registros()
        consolidado_path = self.repo.root.parent / "memoria" / "aprendizados_consolidados_v0_1.json"
        aprendizados_consolidados = 0
        if consolidado_path.exists():
            try:
                import json
                aprendizados_consolidados = int(json.loads(consolidado_path.read_text(encoding="utf-8")).get("quantidade", 0))
            except (OSError, ValueError, TypeError, json.JSONDecodeError):
                aprendizados_consolidados = 0
        return {
            "registros": len(registros),
            "fontes": sum(1 for r in registros if r.kind == "DOCUMENTO"),
            "tipos": {kind: sum(1 for r in registros if r.kind == kind) for kind in sorted({r.kind for r in registros})},
            "estado": self.estado.status,
            "arquitetura": self.estado.architecture_version,
            "elementos_construcao": len(self.mapa.elementos),
            "relacoes_construcao": len(self.mapa.relacoes),
            "integridade_construcao": self.validar_construcao(),
            "nos_rede": len(self.rede.nos),
            "arestas_rede": len(self.rede.arestas),
            "integridade_rede": self.validar_rede(),
            "missoes": len(self.orquestrador.missoes),
            "ciclos": self.runtime.estado.ciclos,
            "runtime": self.runtime.estado.estado,
            "despertares_pendentes": len(self.despertador.pendentes()),
            "captura_bruta": str(self.coletor.raw_path),
            "organizacao_pendente": len(self.fila_organizacao.pendentes()),
            "aprendizados_consolidados": aprendizados_consolidados,
        }
