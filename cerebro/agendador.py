from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

from .aprendizado import novo_aprendizado, registrar_aprendizado
from .grafo_tarefas import EstadoTarefa, GrafoTarefas, NoTarefa


@dataclass(frozen=True)
class PerfilRecurso:
    id: str
    capacidade: float = 1.0
    custo: float = 0.0


@dataclass(frozen=True)
class PerfilExecutor:
    id: str
    capacidades: tuple[str, ...] = ()
    ferramentas: tuple[str, ...] = ()
    modelos: tuple[str, ...] = ()
    confiabilidade: float = 1.0
    fator_tempo: float = 1.0
    custo_multiplicador: float = 1.0
    combustivel_por_unidade: float = 0.0
    capacidade_concorrencia: int = 1


@dataclass(frozen=True)
class OrcamentoCombustivel:
    disponivel: float = float("inf")
    reservado: float = 0.0
    consumido: float = 0.0

    @property
    def restante(self) -> float:
        return max(0.0, self.disponivel - self.reservado - self.consumido)


@dataclass(frozen=True)
class PlanoExecucao:
    tarefas: tuple[NoTarefa, ...]
    custo_estimado: float
    valor_estimado: float
    prioridade_total: float
    risco_estimado: float
    tempo_estimado: float
    motivo: str
    estrategia: str = "equilibrio"
    modo_execucao: str = "PARALELO"
    combustivel_estimado: float = 0.0
    pontuacao: float = 0.0
    restricoes_bloqueantes: tuple[str, ...] = ()


class AgendadorAdaptativo:
    """Scheduler adaptativo: planeja, seleciona executores, replaneja e aprende."""

    def __init__(
        self,
        grafo: GrafoTarefas,
        historico_path: str | Path | None = None,
        aprendizado_path: str | Path | None = None,
    ) -> None:
        self.grafo = grafo
        self.historico_path = Path(historico_path) if historico_path else None
        self.aprendizado_path = Path(aprendizado_path) if aprendizado_path else None
        self.historico: list[dict[str, object]] = []
        self.perfis: dict[str, dict[str, float]] = {}
        self.executores: dict[str, PerfilExecutor] = {}
        self.fuel = OrcamentoCombustivel()
        self.cenario: dict[str, object] = {}
        if self.historico_path:
            self._carregar_historico()

    def registrar_executor(self, executor: PerfilExecutor) -> None:
        self.executores[executor.id] = executor
        self._adicionar_historico({"evento": "EXECUTOR_REGISTRADO", "executor": executor.id})

    def atualizar_cenario(self, **mudancas: object) -> None:
        self.cenario.update(mudancas)
        self._adicionar_historico({"evento": "CENARIO_ATUALIZADO", "mudancas": dict(mudancas)})

    def definir_combustivel(self, disponivel: float, *, reservado: float = 0.0, consumido: float = 0.0) -> None:
        if min(disponivel, reservado, consumido) < 0:
            raise ValueError("combustível não pode ser negativo")
        self.fuel = OrcamentoCombustivel(disponivel, reservado, consumido)

    @staticmethod
    def pontuacao(tarefa: NoTarefa, perfil: dict[str, float] | None = None, *, objetivo: str = "equilibrio") -> float:
        perfil = perfil or {}
        valor = max(0.0, tarefa.valor_estimado if tarefa.valor_estimado > 0 else tarefa.prioridade)
        oportunidade = max(0.0, tarefa.oportunidade)
        custo = max(0.1, tarefa.custo_estimado if tarefa.custo_estimado > 0 else 1.0)
        risco = min(1.0, max(0.0, tarefa.risco))
        incerteza = min(1.0, max(0.0, tarefa.incerteza))
        confiabilidade = min(1.0, max(0.0, perfil.get("confiabilidade", 1.0)))
        fator_tempo = max(0.1, perfil.get("fator_tempo", 1.0))
        urgencia = 1.0 / max(1.0, tarefa.prazo) if tarefa.prazo is not None else 1.0
        esperado = (valor + oportunidade) * (1.0 - risco) * (1.0 - incerteza) * confiabilidade
        comunicacao = 1.0 + max(0.0, tarefa.comunicacao_estimado)
        if objetivo == "valor":
            return esperado / comunicacao
        if objetivo == "eficiencia":
            return esperado * urgencia / (custo * fator_tempo * comunicacao)
        if objetivo == "conclusao":
            return esperado * urgencia / (fator_tempo * comunicacao)
        if objetivo == "rapidez":
            return esperado / (max(0.1, tarefa.tempo_estimado * fator_tempo) * comunicacao)
        if objetivo == "aprendizado":
            return (esperado + oportunidade + incerteza) / (custo * comunicacao)
        return esperado * urgencia / (custo * fator_tempo * comunicacao)

    def selecionar_executor(self, tarefa: NoTarefa) -> PerfilExecutor | None:
        requeridas = set(tarefa.capacidades)
        candidatos: list[tuple[float, PerfilExecutor]] = []
        for executor in self.executores.values():
            capacidades = set(executor.capacidades)
            if requeridas and not requeridas.issubset(capacidades):
                continue
            compat = len(requeridas & capacidades) / len(requeridas) if requeridas else 1.0
            score = compat * executor.confiabilidade / max(0.1, executor.fator_tempo * executor.custo_multiplicador)
            candidatos.append((score, executor))
        return max(candidatos, key=lambda x: (x[0], x[1].id))[1] if candidatos else None

    def planejar(
        self,
        recursos_disponiveis: set[str] | None = None,
        *,
        orcamento: float | None = None,
        limite: int | None = None,
        objetivo: str = "equilibrio",
        capacidades_recursos: dict[str, float] | None = None,
        restricao_satisfaz: Callable[[NoTarefa], bool] | None = None,
        capacidade_de_tempo: float | None = None,
        forcar_sequencial: bool = False,
    ) -> PlanoExecucao:
        erros = self.grafo.validar()
        if erros:
            return self._registrar_plano_vazio("grafo inválido; planejamento bloqueado", erros)

        prontas = self.grafo.prontas(recursos_disponiveis)
        if not prontas:
            return self._registrar_plano_vazio("nenhuma tarefa pronta", ())

        avaliadas: list[tuple[NoTarefa, float, PerfilExecutor | None]] = []
        for tarefa in prontas:
            if restricao_satisfaz and not restricao_satisfaz(tarefa):
                continue
            executor = self.selecionar_executor(tarefa)
            perfil = dict(self.perfis.get(tarefa.id, {}))
            if executor:
                perfil["confiabilidade"] = min(perfil.get("confiabilidade", 1.0), executor.confiabilidade)
                perfil["fator_tempo"] = perfil.get("fator_tempo", 1.0) * executor.fator_tempo
            avaliadas.append((tarefa, self.pontuacao(tarefa, perfil, objetivo=objetivo), executor))

        ordenadas = sorted(avaliadas, key=lambda x: (-x[1], -x[0].prioridade, x[0].id))
        selecionadas: list[NoTarefa] = []
        uso: dict[str, float] = {}
        custo = valor = risco = prioridade = fuel = 0.0
        duracoes: list[float] = []
        bloqueios: list[str] = []
        decisoes: list[dict[str, object]] = []
        budget = float("inf") if orcamento is None else max(0.0, orcamento)

        for tarefa, score, executor in ordenadas:
            if limite is not None and len(selecionadas) >= limite:
                break
            recursos = set(tarefa.recursos)
            if any(uso.get(r, 0.0) + 1.0 > max(0.0, (capacidades_recursos or {}).get(r, 1.0)) for r in recursos):
                decisoes.append({"tarefa": tarefa.id, "aceita": False, "motivo": "capacidade_recurso", "score": score})
                continue
            custo_tarefa = max(0.0, tarefa.custo_estimado)
            if executor:
                custo_tarefa *= max(0.0, executor.custo_multiplicador)
            if custo_tarefa == 0:
                custo_tarefa = 1.0 / max(tarefa.prioridade, 0.1)
            fuel_tarefa = max(0.0, tarefa.combustivel_estimado) + (executor.combustivel_por_unidade if executor else 0.0)
            if custo + custo_tarefa > budget:
                bloqueios.append(f"{tarefa.id}: orçamento")
                continue
            if fuel + fuel_tarefa > self.fuel.restante:
                bloqueios.append(f"{tarefa.id}: combustível")
                continue
            fator_tempo = executor.fator_tempo if executor else 1.0
            tempo = max(0.0, tarefa.tempo_estimado) * max(0.1, fator_tempo)
            if tarefa.prazo is not None and tempo > tarefa.prazo:
                bloqueios.append(f"{tarefa.id}: prazo incompatível")
                continue
            if capacidade_de_tempo is not None and tempo > capacidade_de_tempo:
                bloqueios.append(f"{tarefa.id}: capacidade de tempo")
                continue

            selecionadas.append(tarefa)
            for r in recursos:
                uso[r] = uso.get(r, 0.0) + 1.0
            custo += custo_tarefa
            fuel += fuel_tarefa
            valor += max(0.0, tarefa.valor_estimado + tarefa.oportunidade)
            risco += min(1.0, max(0.0, tarefa.risco))
            prioridade += tarefa.prioridade
            duracoes.append(tempo)
            decisoes.append({
                "tarefa": tarefa.id, "aceita": True, "score": score,
                "executor": executor.id if executor else None,
                "motivo": "selecionada sob restrições atuais",
            })

        modo = self._determinar_modo(selecionadas, forcar_sequencial=forcar_sequencial)
        tempo_plano = sum(duracoes) if modo == "SEQUENCIAL" else max(duracoes, default=0.0)
        if capacidade_de_tempo is not None and tempo_plano > capacidade_de_tempo:
            bloqueios.append("lote: duração excede capacidade de tempo")
        score_total = sum(self.pontuacao(t, self.perfis.get(t.id), objetivo=objetivo) for t in selecionadas)
        plano = PlanoExecucao(
            tuple(selecionadas), custo, valor, prioridade,
            risco / len(selecionadas) if selecionadas else 0.0,
            tempo_plano,
            "valor esperado ajustado por risco, incerteza, custo, prazo, combustível, comunicação e experiência",
            objetivo, modo, fuel, score_total, tuple(bloqueios),
        )
        self._registrar_historico(plano, evento="PLANEJAMENTO", decisoes=decisoes)
        return plano

    def executar_inicio(self, plano: PlanoExecucao) -> None:
        for tarefa in plano.tarefas:
            if tarefa.estado == EstadoTarefa.PENDENTE:
                self.grafo.marcar(tarefa.id, EstadoTarefa.EXECUTANDO)
        self._adicionar_historico({"evento": "INICIO_EXECUCAO", "tarefas": [t.id for t in plano.tarefas], "modo": plano.modo_execucao})

    def registrar_resultado(self, tarefa_id: str, sucesso: bool, *, observacao: str | None = None, custo_real: float | None = None, tempo_real: float | None = None, qualidade: float | None = None, evidencia: str | None = None, contexto: dict[str, object] | None = None, aprendizado: str | None = None, fallback_tarefa_id: str | None = None, reintentar: bool = False) -> None:
        tarefa = self.grafo.tarefas[tarefa_id]
        self.grafo.marcar(tarefa_id, EstadoTarefa.CONCLUIDA if sucesso else EstadoTarefa.FALHOU)
        perfil = self.perfis.setdefault(tarefa_id, {"execucoes": 0.0, "sucessos": 0.0, "confiabilidade": 1.0, "fator_tempo": 1.0})
        perfil["execucoes"] += 1.0
        if sucesso:
            perfil["sucessos"] += 1.0
        perfil["confiabilidade"] = perfil["sucessos"] / perfil["execucoes"]
        if tempo_real is not None and tarefa.tempo_estimado > 0:
            observado = max(0.1, tempo_real / tarefa.tempo_estimado)
            n = perfil["execucoes"]
            perfil["fator_tempo"] = (perfil["fator_tempo"] * (n - 1.0) + observado) / n
        self._adicionar_historico({
            "evento": "RESULTADO", "tarefa": tarefa_id, "sucesso": sucesso,
            "observacao": observacao or "", "custo_real": custo_real, "tempo_real": tempo_real,
            "qualidade": qualidade, "evidencia": evidencia or "", "contexto": dict(contexto or {}),
            "aprendizado": aprendizado or "", "perfil_atualizado": dict(perfil),
            "fallback": fallback_tarefa_id, "retry": reintentar,
        })
        if not sucesso and fallback_tarefa_id:
            if fallback_tarefa_id not in self.grafo.tarefas:
                raise ValueError(f"fallback inexistente: {fallback_tarefa_id}")
            self.grafo.marcar(fallback_tarefa_id, EstadoTarefa.PENDENTE)
            self._adicionar_historico({"evento": "FALLBACK_ATIVADO", "tarefa_origem": tarefa_id, "tarefa_fallback": fallback_tarefa_id, "motivo": observacao or "falha"})
        if not sucesso and reintentar:
            self.grafo.marcar(tarefa_id, EstadoTarefa.PENDENTE)
            self._adicionar_historico({"evento": "RETRY", "tarefa": tarefa_id, "motivo": observacao or "nova tentativa"})
        self._registrar_aprendizado(
            titulo=f"Resultado de orquestração: {tarefa_id}",
            conteudo=aprendizado or (observacao or ("execução bem-sucedida" if sucesso else "execução falhou")),
            contexto={"tarefa": tarefa_id, "sucesso": sucesso, **dict(contexto or {})},
            evidencias=((evidencia,) if evidencia else ()),
            tipo="APRENDIZADO" if sucesso or aprendizado else "ERRO",
        )

    def retentar_tarefa(self, tarefa_id: str, *, motivo: str = "nova tentativa") -> None:
        if self.grafo.tarefas[tarefa_id].estado != EstadoTarefa.FALHOU:
            raise ValueError(f"Só é possível retentar tarefa FALHOU: {tarefa_id}")
        self.grafo.marcar(tarefa_id, EstadoTarefa.PENDENTE)
        self._adicionar_historico({"evento": "RETRY", "tarefa": tarefa_id, "motivo": motivo})

    def cancelar_tarefa(self, tarefa_id: str, *, motivo: str = "cancelamento solicitado", cancelar_dependentes: bool = False) -> list[str]:
        self.grafo.marcar(tarefa_id, EstadoTarefa.CANCELADA)
        canceladas = [tarefa_id]
        if cancelar_dependentes:
            canceladas.extend(self.grafo.cancelar_dependentes(tarefa_id))
        self._adicionar_historico({"evento": "CANCELAMENTO", "tarefa": tarefa_id, "dependentes_cancelados": canceladas[1:], "motivo": motivo})
        return canceladas

    def replanejar(self, recursos_disponiveis: set[str] | None = None, **kwargs: object) -> PlanoExecucao:
        motivo = str(kwargs.pop("motivo", "estado, resultados, recursos ou informações alterados"))
        mudancas = kwargs.pop("mudancas", {})
        plano = self.planejar(recursos_disponiveis, **kwargs)
        self._adicionar_historico({"evento": "REPLANEJAMENTO", "tarefas": [t.id for t in plano.tarefas], "motivo": motivo, "mudancas": mudancas, "estrategia": plano.estrategia})
        self._registrar_aprendizado(titulo="Mudança de estratégia de orquestração", conteudo=motivo, contexto={"plano": [t.id for t in plano.tarefas], "mudancas": mudancas}, tipo="DECISAO")
        return plano

    def planos_candidatos(self, recursos_disponiveis: set[str] | None = None, *, orcamento: float | None = None, limite: int | None = None) -> list[PlanoExecucao]:
        estrategias = ("valor", "eficiencia", "conclusao", "rapidez", "aprendizado")
        return [self.planejar(recursos_disponiveis, orcamento=orcamento, limite=limite, objetivo=e) for e in estrategias]

    def selecionar_plano(self, planos: list[PlanoExecucao], *, objetivo: str = "equilibrio") -> PlanoExecucao:
        validos = [p for p in planos if p.tarefas]
        if not validos:
            return PlanoExecucao((), 0, 0, 0, 0, 0, "nenhum plano candidato viável", objetivo)
        def score(p: PlanoExecucao) -> float:
            valor = p.valor_estimado * (1.0 - p.risco_estimado)
            if objetivo == "eficiencia":
                return valor / max(0.1, p.custo_estimado)
            if objetivo == "rapidez":
                return valor / max(0.1, p.tempo_estimado)
            return valor / max(0.1, p.custo_estimado * max(0.1, p.tempo_estimado))
        escolhido = max(validos, key=lambda p: (score(p), -p.risco_estimado, -p.custo_estimado))
        self._adicionar_historico({"evento": "SELECAO_PLANO", "objetivo": objetivo, "selecionado": [t.id for t in escolhido.tarefas], "pontuacao": score(escolhido), "alternativas": [[t.id for t in p.tarefas] for p in validos]})
        return escolhido

    def padroes_orquestracao_reutilizaveis(self, minimo_ocorrencias: int = 2) -> list[dict[str, object]]:
        contagem: dict[str, int] = {}
        for evento in self.historico:
            if evento.get("evento") == "RESULTADO" and evento.get("sucesso"):
                tarefa = str(evento.get("tarefa", ""))
                contagem[tarefa] = contagem.get(tarefa, 0) + 1
        return [{"tarefa": t, "ocorrencias": n} for t, n in contagem.items() if n >= minimo_ocorrencias]

    def perfil_tarefa(self, tarefa_id: str) -> dict[str, float]:
        return dict(self.perfis.get(tarefa_id, {}))

    def salvar_historico(self) -> None:
        if not self.historico_path:
            return
        self.historico_path.parent.mkdir(parents=True, exist_ok=True)
        self.historico_path.write_text(json.dumps({"perfis": self.perfis, "historico": self.historico, "executores": {k: e.__dict__ for k, e in self.executores.items()}, "fuel": self.fuel.__dict__, "cenario": self.cenario}, ensure_ascii=False, indent=2), encoding="utf-8")

    def _carregar_historico(self) -> None:
        if not self.historico_path or not self.historico_path.exists():
            return
        try:
            dados = json.loads(self.historico_path.read_text(encoding="utf-8"))
            self.perfis = {str(k): {str(pk): float(pv) for pk, pv in v.items()} for k, v in dados.get("perfis", {}).items()}
            self.historico = list(dados.get("historico", []))
            self.cenario = dict(dados.get("cenario", {}))
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            self.perfis, self.historico, self.cenario = {}, [], {}

    def _adicionar_historico(self, evento: dict[str, object]) -> None:
        self.historico.append(evento)
        self.salvar_historico()

    def _registrar_historico(self, plano: PlanoExecucao, *, evento: str, decisoes: list[dict[str, object]] | None = None) -> None:
        registro = {"evento": evento, "tarefas": [t.id for t in plano.tarefas], "custo": plano.custo_estimado, "valor": plano.valor_estimado, "prioridade": plano.prioridade_total, "risco": plano.risco_estimado, "tempo": plano.tempo_estimado, "combustivel": plano.combustivel_estimado, "pontuacao": plano.pontuacao, "modo": plano.modo_execucao, "motivo": plano.motivo, "estrategia": plano.estrategia, "restricoes_bloqueantes": list(plano.restricoes_bloqueantes)}
        if decisoes is not None:
            registro["decisoes"] = decisoes
        self._adicionar_historico(registro)

    def _registrar_aprendizado(self, *, titulo: str, conteudo: str, contexto: dict[str, object], evidencias: tuple[str, ...] = (), tipo: str = "APRENDIZADO") -> None:
        if not self.aprendizado_path:
            return
        aprendizado = novo_aprendizado(tipo, titulo, conteudo, origem="AgendadorAdaptativo", evidencias=evidencias, contexto=tuple(f"{k}={v}" for k, v in sorted(contexto.items())))
        registrar_aprendizado(aprendizado, self.aprendizado_path)

    def _registrar_plano_vazio(self, motivo: str, bloqueios: Iterable[str]) -> PlanoExecucao:
        plano = PlanoExecucao((), 0, 0, 0, 0, 0, motivo, restricoes_bloqueantes=tuple(bloqueios))
        self._registrar_historico(plano, evento="PLANEJAMENTO_BLOQUEADO")
        return plano

    @staticmethod
    def _determinar_modo(tarefas: list[NoTarefa], *, forcar_sequencial: bool = False) -> str:
        if not tarefas:
            return "VAZIO"
        if forcar_sequencial or len(tarefas) == 1:
            return "SEQUENCIAL"
        ids = {t.id for t in tarefas}
        if any(set(t.depende_de) & ids for t in tarefas):
            return "SEQUENCIAL"
        if any(t.comunicacao_estimado > 0.5 for t in tarefas):
            return "SEQUENCIAL"
        return "PARALELO"
