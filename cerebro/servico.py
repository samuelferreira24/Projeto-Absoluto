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
from .grafo_tarefas import GrafoTarefas, NoTarefa
from .agendador import AgendadorAdaptativo, PlanoExecucao
from .sinergia import DetectorSinergia, ResultadoCombinacao, SinalSinergia
from .continuidade import carregar_snapshot, gerar_prompt_retoma, salvar_prompt_retoma, salvar_snapshot
from .contexto_operacional import ContextoOperacional, construir_contexto, salvar_contexto, salvar_prompt_contexto
from .interface_chat import InterfaceChat, MensagemChat


class Cerebro:
    """Fachada operacional do Cérebro, mantendo as camadas internas substituíveis."""

    def __init__(self, dados: str | Path = "cerebro/data") -> None:
        self.repo = RepositorioJSONL(dados)
        self.estado_path = self.repo.root / "estado.json"
        self.rede_path = self.repo.root / "rede_evolutiva.json"
        self.orquestrador_path = self.repo.root / "orquestrador.json"
        self.runtime_path = self.repo.root / "runtime.json"
        self.agendador_path = self.repo.root / "agendador.json"
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
        self.grafo_tarefas = GrafoTarefas()
        self.agendador = AgendadorAdaptativo(self.grafo_tarefas, self.agendador_path)
        self.detector_sinergia = DetectorSinergia()
        self.interface_chat = InterfaceChat(self)

    def inspecionar(self, arquivo: str | Path) -> DocumentoEstruturado:
        return extrair(arquivo)

    def ingerir(self, arquivo: str | Path) -> Registro:
        documento = self.inspecionar(arquivo)
        if documento.erros:
            raise ValueError(f"Falha na ingestão: {documento.erros}")
        return registrar_fonte(self.repo, documento)

    def capturar_evento(self, evento: EventoCapturado) -> list[Registro]:
        return self.coletor.capturar(evento)

    def capturar_mensagem_chat(self, mensagem: MensagemChat) -> int:
        return self.interface_chat.capturar_mensagem(mensagem)

    def capturar_conversa_chat(self, mensagens: list[MensagemChat]) -> int:
        return self.interface_chat.capturar_conversa(mensagens)

    def contexto_para_chat(self, objetivo: str | None = None, limite: int = 20) -> list[ResultadoBusca]:
        return self.interface_chat.contexto_para_retoma(objetivo=objetivo, limite=limite)

    def contexto_operacional(self, *, objetivo: str | None = None, proximo_passo: str | None = None, contexto_da_sessao: dict[str, Any] | None = None) -> ContextoOperacional:
        """Retorna o estado operacional que qualquer chat deve conhecer antes de agir."""
        return construir_contexto(self, objetivo=objetivo, proximo_passo=proximo_passo, contexto_da_sessao=contexto_da_sessao)

    def salvar_contexto_operacional(self, *, objetivo: str | None = None, proximo_passo: str | None = None, contexto_da_sessao: dict[str, Any] | None = None, path: str | Path | None = None) -> dict[str, Any]:
        destino = path or (self.repo.root / "contexto_operacional.json")
        return salvar_contexto(self, destino, objetivo=objetivo, proximo_passo=proximo_passo, contexto_da_sessao=contexto_da_sessao)

    def preparar_contexto_para_chat(self, *, objetivo: str | None = None, proximo_passo: str | None = None, contexto_da_sessao: dict[str, Any] | None = None, path: str | Path | None = None) -> str:
        destino = path or (self.repo.root / "CONTEXTO_PARA_QUALQUER_CHAT.md")
        return salvar_prompt_contexto(self, destino, objetivo=objetivo, proximo_passo=proximo_passo, contexto_da_sessao=contexto_da_sessao)

    def registrar_memoria(self, tipo: str, titulo: str, conteudo: str, *, fonte: str | None = None, contexto: dict[str, Any] | None = None, relacoes: list[dict[str, str]] | None = None, proveniencia: dict[str, Any] | None = None, estado: str = "NOVO", metadata: dict[str, Any] | None = None) -> Registro:
        registro = novo_registro(self.repo, tipo, titulo, conteudo, source=fonte, relations=list(relacoes or []), provenance=dict(proveniencia or {}), state=estado, metadata={"contexto": dict(contexto or {}), **dict(metadata or {})})
        self.repo.salvar(registro)
        return registro

    def registrar_entendimento(self, titulo: str, conteudo: str, **kwargs: Any) -> Registro:
        return self.registrar_memoria("ENTENDIMENTO", titulo, conteudo, **kwargs)

    def registrar_descoberta(self, titulo: str, conteudo: str, **kwargs: Any) -> Registro:
        return self.registrar_memoria("DESCOBERTA", titulo, conteudo, **kwargs)

    def registrar_progresso(self, titulo: str, conteudo: str, **kwargs: Any) -> Registro:
        return self.registrar_memoria("PROGRESSO", titulo, conteudo, **kwargs)

    def adicionar_tarefa(self, tarefa: NoTarefa) -> None:
        self.grafo_tarefas.adicionar(tarefa)

    def validar_tarefas(self) -> list[str]:
        return self.grafo_tarefas.validar()

    def tarefas_prontas(self, recursos: set[str] | None = None) -> list[NoTarefa]:
        return self.grafo_tarefas.prontas(recursos)

    def lote_paralelo(self, recursos: set[str] | None = None) -> list[list[NoTarefa]]:
        return self.grafo_tarefas.lotes_paralelos(recursos)

    def planejar_tarefas(self, recursos: set[str] | None = None, *, orcamento: float | None = None, limite: int | None = None) -> PlanoExecucao:
        return self.agendador.planejar(recursos, orcamento=orcamento, limite=limite)

    def iniciar_plano(self, plano: PlanoExecucao) -> None:
        self.agendador.executar_inicio(plano)

    def concluir_tarefa(self, tarefa_id: str, sucesso: bool = True, **kwargs: Any) -> None:
        self.agendador.registrar_resultado(tarefa_id, sucesso, **kwargs)

    def replanejar_tarefas(self, recursos: set[str] | None = None, **kwargs: Any) -> PlanoExecucao:
        return self.agendador.replanejar(recursos, **kwargs)

    def registrar_resultado_combinacao(self, resultado: ResultadoCombinacao) -> None:
        self.detector_sinergia.registrar(resultado)

    def detectar_sinergias(self, *, minimo_evidencias: int = 2) -> list[SinalSinergia]:
        return self.detector_sinergia.detectar(minimo_evidencias=minimo_evidencias)

    def gerar_combinacoes_promissoras(self, capacidades: list[str], *, limite: int = 20) -> list[tuple[str, ...]]:
        return self.detector_sinergia.combinações_promissoras(capacidades, limite=limite)

    def consolidar_aprendizados(self, memoria: str | Path = "cerebro/memoria") -> dict[str, Any]:
        memoria = Path(memoria)
        return salvar_consolidado(memoria / "aprendizados_consolidados_v0_1.json", memoria / "aprendizados.jsonl", memoria / "aprendizados_fundamentais_v0_1.json")

    def checkpoint(self, *, objetivo_atual: str | None = None, proximo_passo: str | None = None, contexto_da_sessao: dict[str, Any] | None = None) -> dict[str, Any]:
        """Persiste uma fotografia portátil da sessão para continuidade em outro chat."""
        self.salvar_estado()
        self.agendador.salvar_historico()
        self.salvar_contexto_operacional(objetivo=objetivo_atual, proximo_passo=proximo_passo, contexto_da_sessao=contexto_da_sessao)
        return salvar_snapshot(self, objetivo_atual=objetivo_atual, proximo_passo=proximo_passo, contexto_da_sessao=contexto_da_sessao)

    def preparar_retoma(self, *, objetivo_atual: str | None = None, proximo_passo: str | None = None, contexto_da_sessao: dict[str, Any] | None = None) -> str:
        """Gera o prompt portátil de retomada após salvar o checkpoint."""
        self.checkpoint(objetivo_atual=objetivo_atual, proximo_passo=proximo_passo, contexto_da_sessao=contexto_da_sessao)
        return salvar_prompt_retoma(self, objetivo_atual=objetivo_atual, proximo_passo=proximo_passo, contexto_da_sessao=contexto_da_sessao)

    @staticmethod
    def carregar_continuidade(path: str | Path = "cerebro/data/continuidade.json") -> dict[str, Any]:
        return carregar_snapshot(path)

    @staticmethod
    def prompt_de_retoma(snapshot: dict[str, Any]) -> str:
        return gerar_prompt_retoma(snapshot)

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
        resultado = self.runtime.executar_ciclo(missao_id, candidatos, executor)
        self.salvar_estado()
        return resultado

    def salvar_estado(self) -> None:
        self.estado.salvar(self.estado_path)
        self.rede.salvar(str(self.rede_path))

    def diagnostico(self) -> dict[str, Any]:
        registros = self.registros()
        consolidado_path = self.repo.root.parent / "memoria" / "aprendizados_consolidados_v0_1.json"
