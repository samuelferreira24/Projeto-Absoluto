from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from threading import Lock
from typing import Any
import json
import time


@dataclass
class NoApp:
    id: str
    nome: str
    ambiente: str = "desconhecido"
    capacidades: tuple[str, ...] = ()
    endpoint: str | None = None
    ativo: bool = True
    ultimo_sinal: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)

    def sinalizar(self) -> None:
        self.ultimo_sinal = time.time()
        self.ativo = True

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["capacidades"] = list(self.capacidades)
        return d


class RegistroNosApp:
    """Identidade e presença dos Apps conectados ao Cérebro.

    Não sincroniza tudo entre aparelhos: fornece uma identidade comum e um
    ponto central para estado, tarefas e resultados distribuídos.
    """

    def __init__(self, caminho: str | Path):
        self.caminho = Path(caminho)
        self._lock = Lock()
        self._nos: dict[str, NoApp] = {}
        self._carregar()

    def _carregar(self) -> None:
        if not self.caminho.exists():
            return
        try:
            dados = json.loads(self.caminho.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return
        for item in dados if isinstance(dados, list) else []:
            try:
                no = NoApp(
                    id=str(item["id"]),
                    nome=str(item.get("nome", item["id"])),
                    ambiente=str(item.get("ambiente", "desconhecido")),
                    capacidades=tuple(item.get("capacidades", [])),
                    endpoint=item.get("endpoint"),
                    ativo=bool(item.get("ativo", True)),
                    ultimo_sinal=float(item.get("ultimo_sinal", time.time())),
                    metadata=dict(item.get("metadata", {})),
                )
                self._nos[no.id] = no
            except (KeyError, TypeError, ValueError):
                continue

    def _salvar(self) -> None:
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.caminho.with_suffix(self.caminho.suffix + ".tmp")
        tmp.write_text(
            json.dumps([n.to_dict() for n in self._nos.values()], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        tmp.replace(self.caminho)

    def registrar(self, no: NoApp) -> NoApp:
        with self._lock:
            self._nos[no.id] = no
            self._salvar()
        return no

    def sinalizar(self, no_id: str) -> bool:
        with self._lock:
            no = self._nos.get(no_id)
            if no is None:
                return False
            no.sinalizar()
            self._salvar()
            return True

    def listar(self, *, ativos: bool | None = None) -> list[NoApp]:
        with self._lock:
            nos = list(self._nos.values())
        if ativos is None:
            return nos
        return [n for n in nos if n.ativo == ativos]

    def por_capacidade(self, capacidade: str) -> list[NoApp]:
        return [n for n in self.listar(ativos=True) if capacidade in n.capacidades]

    def remover(self, no_id: str) -> None:
        with self._lock:
            self._nos.pop(no_id, None)
            self._salvar()
