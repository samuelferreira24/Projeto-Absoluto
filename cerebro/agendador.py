from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .aprendizado import novo_aprendizado, registrar_aprendizado
from .grafo_tarefas import EstadoTarefa, GrafoTarefas, NoTarefa


@dataclass(frozen=True)
class PerfilRecurso:
    id: str
    capacidade: float = 1.0
    custo: float = 0.0


@dataclass(frozen=True)
class PlanoExecucao:
    tarefas: tuple[NoTarefa, ...]
    custo_estimado: float
    valor_estimado: float
    prioridade_total: float
    risco_estimado: float
    tempo_estimado: float
    motivo: str


class AgendadorAdaptativo:
    """Escolhe, executa, aprende e reavalia tarefas preservando a história."""

    def __init__(self, grafo: GrafoTarefas, historico_path: str | Path | None = None) -> None:
        self.grafo = grafo
        self.historico_path = Path(historico_path) if historico_path else None
        self.aprendizado_path = Path(aprendizado_path) if aprendizado_path else None
        self.historico: list[dict[str, object]] = []
        self.perfis: dict[str, dict[str, float]] = {}
        if self.historico_path:
            self._carregar_historico()

    @staticmethod
    def pontuacao(
        tarefa: NoTarefa,
        perfil: dict[str, float] | None = None,
        *,
        objetivo: str = "equilibrio",
    ) -> float:
        """Valor marginal ajustado por risco, custo, prazo e experiência observada."""
        perfil = perfil or {}
        valor = max(0.0, tarefa.valor_estimado if tarefa.valor_estimado > 0 else tarefa.prioridade)
        oportunidade = max(0.0, tarefa.oportunidade)
        custo = max(0.1, tarefa.custo_estimado if tarefa.custo_estimado > 0 else 1.0)
        risco = max(0.0, min(1.0, tarefa.risco))
        incerteza = max(0.0, min(1.0, tarefa.incerteza))
        confiabilidade_observada = max(0.0, min(1.0, perfil.get("confiabilidade", 1.0)))
        fator_tempo = max(0.1, perfil.get("fator_tempo", 1.0))
        urgencia = 1.0 / max(1.0, tarefa.prazo) if tarefa.prazo is not None else 1.0
        valor_esperado = (valor + oportunidade) * (1.0 - risco) * (1.0 - incerteza) * confiabilidade_observada
        comunicacao = 1.0 + max(0.0, tarefa.comunicacao_estimado)
        if objetivo == "valor":
            return valor_esperado / comunicacao
        if objetivo == "eficiencia":
            return valor_esperado * urgencia / (custo * fator_tempo * comunicacao)
        if objetivo == "conclusao":
            return valor_esperado * urgencia / (fator_tempo * comunicacao)
        if objetivo == "rapidez":
            return valor_esperado / (max(0.1, tarefa.tempo_estimado * fator_tempo) * comunicacao)
        if objetivo == "aprendizado":
            return (valor_esperado + oportunidade + incerteza) / (custo * comunicacao)
        return valor_esperado * urgencia / (custo * fator_tempo * comunicacao)

    def planejar(
        self,
        recursos_disponiveis: set[str] | None = None,
        *,
        orcamento: float | None = None,
        limite: int | None = None,
        objetivo: str = "equilibrio",
        capacidades_recursos: dict[str, float] | None = None,
        restricao_satisfaz: Callable[[NoTarefa], bool] | None = None,
    ) -> PlanoExecucao:
        if self.grafo.validar():
            plano = PlanoExecucao((), 0.0, 0.0, 0.0, 0.0, 0.0, "grafo inválido; planejamento bloqueado")
            self._registrar_historico(plano, evento="PLANEJAMENTO_BLOQUEADO")
            return plano

        prontas = self.grafo.prontas(recursos_disponiveis)
        if not prontas:
            plano = PlanoExecucao((), 0.0, 0.0, 0.0, 0.0, 0.0, "nenhuma tarefa pronta")
            self._registrar_historico(plano, evento="PLANEJAMENTO")
            return plano

        avaliadas = [
            (tarefa, self.pontuacao(tarefa, self.perfis.get(tarefa.id), objetivo=objetivo))
            for tarefa in prontas
            if restricao_satisfaz is None or restricao_satisfaz(tarefa)
        ]
        ordenadas = sorted(
            avaliadas,
            key=lambda item: (-item[1], -item[0].prioridade, item[0].id),
        )
        selecionadas: list[NoTarefa] = []
        usados: set[str] = set()
        custo = valor = risco = prioridade = 0.0
        tempos: list[float] = []
        decisoes: list[dict[str, object]] = []
        uso_por_recurso: dict[str, float] = {}
        bloqueios: list[str] = []

        for tarefa, score in ordenadas:
            if limite is not None and len(selecionadas) >= limite:
                break
            recursos = set(tarefa.recursos)
            if recursos & usados:
                capacidade_ok = all(uso_por_recurso.get(r, 0.0) + 1.0 <= max(0.0, (capacidades_recursos or {}).get(r, 1.0)) for r in recursos & usados)
                if not capacidade_ok:
                    decisoes.append({"tarefa": tarefa.id, "score": score, "aceita": False, "motivo": "conflito_de_recurso"})
                    continue
            custo_tarefa = max(0.0, tarefa.custo_estimado)
            if custo_tarefa == 0.0:
                custo_tarefa = 1.0 / max(tarefa.prioridade, 0.1)
            if orcamento is not None and custo + custo_tarefa > orcamento:
                bloqueios.append(f"{tarefa.id}: orçamento")
                decisoes.append({"tarefa": tarefa.id, "score": score, "aceita": False, "motivo": "orcamento"})
                continue
            perfil = self.perfis.get(tarefa.id, {})
            tempo_tarefa = max(0.0, tarefa.tempo_estimado) * perfil.get("fator_tempo", 1.0)
            if tarefa.prazo is not None and tarefa.prazo < tempo_tarefa:
                bloqueios.append(f"{tarefa.id}: prazo incompatível")
                decisoes.append({"tarefa": tarefa.id, "score": score, "aceita": False, "motivo": "prazo"})
                continue
            selecionadas.append(tarefa)
            usados.update(recursos)
            for recurso in recursos:
                uso_por_recurso[recurso] = uso_por_recurso.get(recurso, 0.0) + 1.0
            custo += custo_tarefa
            valor += max(0.0, tarefa.valor_estimado + tarefa.oportunidade)
            risco += max(0.0, min(1.0, tarefa.risco))
            tempos.append(tempo_tarefa)
            prioridade += tarefa.prioridade
            decisoes.append({"tarefa": tarefa.id, "score": score, "aceita": True, "motivo": "selecionada"})

        plano = PlanoExecucao(
            tuple(selecionadas),
            custo,
            valor,
            prioridade,
            risco / len(selecionadas) if selecionadas else 0.0,
            max(tempos, default=0.0),
            "valor esperado ajustado por risco, incerteza, custo, prazo, comunicação e experiência",
            objetivo,
            restricoes_bloqueantes=tuple(bloqueios),
        )
        self._registrar_historico(plano, evento="PLANEJAMENTO", decisoes=decisoes)
        return plano

    def executar_inicio(self, plano: PlanoExecucao) -> None:
        for tarefa in plano.tarefas:
            self.grafo.marcar(tarefa.id, EstadoTarefa.EXECUTANDO)
        self._registrar_historico(plano, evento="INICIO_EXECUCAO")

    def registrar_resultado(
        self,
        tarefa_id: str,
        sucesso: bool,
        *,
        observacao: str | None = None,
        custo_real: float | None = None,
        tempo_real: float | None = None,
        qualidade: float | None = None,
        evidencia: str | None = None,
        contexto: dict[str, object] | None = None,
        aprendizado: str | None = None,
        fallback_tarefa_id: str | None = None,
        reintentar: bool = False,
    ) -> None:
        """Registra o resultado e atualiza um perfil persistível para o próximo planejamento."""
        tarefa = self.grafo.tarefas[tarefa_id]
        self.grafo.marcar(tarefa_id, EstadoTarefa.CONCLUIDA if sucesso else EstadoTarefa.FALHOU)
        perfil = self.perfis.setdefault(tarefa_id, {"execucoes": 0.0, "sucessos": 0.0, "confiabilidade": 1.0, "fator_tempo": 1.0})
        perfil["execucoes"] += 1.0
        if sucesso:
            perfil["sucessos"] += 1.0
        perfil["confiabilidade"] = perfil["sucessos"] / perfil["execucoes"]
        if tempo_real is not None and tarefa.tempo_estimado > 0:
            observado = max(0.1, tempo_real / tarefa.tempo_estimado)
            perfil["fator_tempo"] = (perfil["fator_tempo"] * (perfil["execucoes"] - 1.0) + observado) / perfil["execucoes"]
        self._adicionar_historico({
            "evento": "RESULTADO",
            "tarefa": tarefa_id,
            "sucesso": sucesso,
            "observacao": observacao or "",
            "custo_real": custo_real,
            "tempo_real": tempo_real,
            "qualidade": qualidade,
            "evidencia": evidencia or "",
            "contexto": dict(contexto or {}),
            "aprendizado": aprendizado or "",
            "perfil_atualizado": dict(perfil),
            "fallback": fallback_tarefa_id,
            "retry": reintentar,
        })
        if fallback_tarefa_id and not sucesso:
            if fallback_tarefa_id not in self.grafo.tarefas:
                raise ValueError(f"fallback inexistente: {fallback_tarefa_id}")
            self.grafo.marcar(fallback_tarefa_id, EstadoTarefa.PENDENTE)
            self._adicionar_historico({"evento": "FALLBACK_ATIVADO", "tarefa_origem": tarefa_id, "tarefa_fallback": fallback_tarefa_id, "motivo": observacao or "falha da tarefa principal"})
        if reintentar and not sucesso:
            self.grafo.marcar(tarefa_id, EstadoTarefa.PENDENTE)
            self._adicionar_historico({"evento": "RETRY", "tarefa": tarefa_id, "motivo": observacao or "nova tentativa"})
        self._registrar_aprendizado(titulo=f"Resultado de orquestração: {tarefa_id}", conteudo=aprendizado or (observacao or ("execução bem-sucedida" if sucesso else "execução falhou")), contexto={"tarefa": tarefa_id, "sucesso": sucesso, **dict(contexto or {})}, evidencias=((evidencia,) if evidencia else ()), tipo="APRENDIZADO" if aprendizado or sucesso else "ERRO")

    def retentar_tarefa(self, tarefa_id: str, *, motivo: str = "nova tentativa") -> None:
        """Reabre uma tarefa que falhou sem apagar o registro da falha anterior."""
        tarefa = self.grafo.tarefas[tarefa_id]
        if tarefa.estado != EstadoTarefa.FALHOU:
            raise ValueError(f"Só é possível retentar tarefa FALHOU: {tarefa_id}")
        self.grafo.marcar(tarefa_id, EstadoTarefa.PENDENTE)
        self._adicionar_historico({"evento": "RETRY", "tarefa": tarefa_id, "motivo": motivo})

    def replanejar(self, recursos_disponiveis: set[str] | None = None, **kwargs: object) -> PlanoExecucao:
        """Recalcula após mudança e preserva o motivo do desvio."""
        motivo = str(kwargs.pop("motivo", "estado do grafo, resultados, experiência ou recursos alterados"))
        mudancas = kwargs.pop("mudancas", {})
        plano = self.planejar(recursos_disponiveis, **kwargs)
        self._adicionar_historico({
            "evento": "REPLANEJAMENTO",
            "tarefas": [t.id for t in plano.tarefas],
            "motivo": motivo,
            "mudancas": mudancas,
            "estrategia": plano.estrategia,
        })
        self._registrar_aprendizado(titulo="Mudança de estratégia de orquestração", conteudo=motivo, contexto={"plano": [t.id for t in plano.tarefas], "mudancas": mudancas}, tipo="DECISAO")
        return plano

    def planos_candidatos(
        self,
        recursos_disponiveis: set[str] | None = None,
        *,
        orcamento: float | None = None,
        limite: int | None = None,
    ) -> list[PlanoExecucao]:
        """Gera alternativas antes da seleção final."""
        estrategias = ("valor", "eficiencia", "conclusao", "rapidez", "aprendizado")
        planos = [
            self.planejar(
                recursos_disponiveis,
                orcamento=orcamento,
                limite=limite,
                objetivo=estrategia,
            )
            for estrategia in estrategias
        ]
        self._adicionar_historico({
            "evento": "PLANOS_CANDIDATOS",
            "estrategias": list(estrategias),
            "planos": [[t.id for t in p.tarefas] for p in planos],
        })
        return planos

    def selecionar_plano(
        self,
        planos: list[PlanoExecucao],
        *,
        objetivo: str = "equilibrio",
    ) -> PlanoExecucao:
        """Seleciona uma alternativa preservando as demais no histórico."""
        validos = [p for p in planos if p.tarefas]
        if not validos:
            return PlanoExecucao((), 0.0, 0.0, 0.0, 0.0, 0.0, "nenhum plano candidato viável")

        def score(plano: PlanoExecucao) -> float:
            valor = plano.valor_estimado * (1.0 - plano.risco_estimado)
            if objetivo == "eficiencia":
                return valor / max(0.1, plano.custo_estimado)
            if objetivo == "conclusao":
                return valor
            if objetivo == "rapidez":
                return valor / max(0.1, plano.tempo_estimado)
            return valor / (max(0.1, plano.custo_estimado) * max(0.1, plano.tempo_estimado))

        escolhido = max(validos, key=lambda p: (score(p), -p.risco_estimado, -p.custo_estimado))
        self._adicionar_historico({
            "evento": "SELECAO_PLANO",
            "objetivo": objetivo,
            "selecionado": [t.id for t in escolhido.tarefas],
            "pontuacao": score(escolhido),
            "alternativas": [[t.id for t in p.tarefas] for p in validos],
        })
        return escolhido

    def perfil_tarefa(self, tarefa_id: str) -> dict[str, float]:
        return dict(self.perfis.get(tarefa_id, {}))

    def salvar_historico(self) -> None:
        """Persiste decisões e resultados do agendador sem apagar o histórico anterior."""
        if not self.historico_path:
            return
        self.historico_path.parent.mkdir(parents=True, exist_ok=True)
        self.historico_path.write_text(json.dumps({"perfis": self.perfis, "historico": self.historico}, ensure_ascii=False, indent=2), encoding="utf-8")

    def _carregar_historico(self) -> None:
        if not self.historico_path or not self.historico_path.exists():
            return
        try:
            dados = json.loads(self.historico_path.read_text(encoding="utf-8"))
            self.perfis = {str(k): {str(pk): float(pv) for pk, pv in v.items()} for k, v in dados.get("perfis", {}).items()}
            self.historico = list(dados.get("historico", []))
        except (OSError, ValueError, TypeError):
            self.perfis = {}
            self.historico = []

    def _adicionar_historico(self, evento: dict[str, object]) -> None:
        self.historico.append(evento)
        self.salvar_historico()

    def _registrar_historico(self, plano: PlanoExecucao, *, evento: str, decisoes: list[dict[str, object]] | None = None) -> None:
        registro: dict[str, object] = {
            "evento": evento,
            "tarefas": [t.id for t in plano.tarefas],
            "custo": plano.custo_estimado,
            "valor": plano.valor_estimado,
            "prioridade": plano.prioridade_total,
            "risco": plano.risco_estimado,
            "tempo": plano.tempo_estimado,
            "motivo": plano.motivo,
            "estrategia": plano.estrategia,
        }
        if decisoes is not None:
            registro["decisoes"] = decisoes
        self._adicionar_historico(registro)

    def _registrar_aprendizado(self, *, titulo: str, conteudo: str, contexto: dict[str, object], evidencias: tuple[str, ...] = (), tipo: str = "APRENDIZADO") -> None:
        if not self.aprendizado_path:
            return
        aprendizado = novo_aprendizado(tipo, titulo, conteudo, origem="AgendadorAdaptativo", evidencias=evidencias, contexto=tuple(f"{k}={v}" for k, v in sorted(contexto.items())))
        registrar_aprendizado(aprendizado, self.aprendizado_path)
