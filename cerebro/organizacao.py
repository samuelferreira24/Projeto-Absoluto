from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json

from .nucleo import Registro


def agora() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class TarefaOrganizacao:
    registro_id: str
    tipo: str
    estado: str = "PENDENTE"
    prioridade_sinal: float = 0.0
    contexto: dict = field(default_factory=dict)
    criada_em: str = field(default_factory=agora)
    tentativas: int = 0
    idempotency_key: str = ""

    def __post_init__(self) -> None:
        if not self.idempotency_key:
            base = f"{self.registro_id}|{self.tipo}"
            self.idempotency_key = hashlib.sha256(base.encode()).hexdigest()


class FilaOrganizacao:
    """Fila portátil para agentes organizadores, sem acoplamento a uma IA."""

    def __init__(self, path: str | Path = "cerebro/data/organizacao.jsonl") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _ler(self) -> list[TarefaOrganizacao]:
        if not self.path.exists():
            return []
        itens = []
        for linha in self.path.read_text(encoding="utf-8").splitlines():
            if linha.strip():
                itens.append(TarefaOrganizacao(**json.loads(linha)))
        return itens

    def adicionar(self, registro: Registro, sinal: float = 0.0) -> TarefaOrganizacao:
        existentes = {t.idempotency_key for t in self._ler()}
        tarefa = TarefaOrganizacao(
            registro_id=registro.id,
            tipo=registro.kind,
            prioridade_sinal=sinal,
            contexto={
                "source": registro.source,
                "provenance": registro.provenance,
                "metadata": registro.metadata,
            },
        )
        if tarefa.idempotency_key not in existentes:
            with self.path.open("a", encoding="utf-8") as arquivo:
                arquivo.write(json.dumps(asdict(tarefa), ensure_ascii=False) + "\n")
        return tarefa

    def pendentes(self, limite: int | None = None) -> list[TarefaOrganizacao]:
        tarefas = [t for t in self._ler() if t.estado == "PENDENTE"]
        tarefas.sort(key=lambda t: (t.prioridade_sinal, t.criada_em), reverse=True)
        return tarefas[:limite] if limite else tarefas

    def concluir(self, idempotency_key: str, resultado: dict | None = None) -> None:
        tarefas = self._ler()
        alterou = False
        for tarefa in tarefas:
            if tarefa.idempotency_key == idempotency_key:
                tarefa.estado = "CONCLUIDA"
                tarefa.tentativas += 1
                if resultado:
                    tarefa.contexto["resultado"] = resultado
                alterou = True
        if alterou:
            with self.path.open("w", encoding="utf-8") as arquivo:
                for tarefa in tarefas:
                    arquivo.write(json.dumps(asdict(tarefa), ensure_ascii=False) + "\n")
