from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Iterable

TIPOS_NOS = {
    "OBJETIVO", "CAPACIDADE", "IDEIA", "HIPOTESE", "PESQUISA", "DECISAO",
    "EXPERIMENTO", "RESULTADO", "EXPERIENCIA", "APRENDIZADO", "SABEDORIA",
    "COMPONENTE", "RECURSO", "RISCO", "PROBLEMA", "CONCEITO", "PRINCIPIO",
}
TIPOS_RELACAO = {
    "DEPENDE_DE", "HABILITA", "IMPULSIONA", "MULTIPLICA", "MULTIPLICA_VALOR",
    "INFORMA", "VALIDA", "CONTRADIZ", "CORRIGE", "CAUSA", "RESULTA_EM",
    "CONVERGE_COM", "ALIMENTA", "SUBSTITUI", "SUPERA", "DERIVA_DE", "REUTILIZA",
    "QUESTIONA", "REVELA", "BLOQUEIA",
}


@dataclass
class NoRede:
    id: str
    tipo: str
    titulo: str
    estado: str = "ATIVO"
    potencial_multiplicador: float = 0.0
    evidencia: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.tipo = self.tipo.upper()
        if self.tipo not in TIPOS_NOS:
            raise ValueError(f"Tipo de nó inválido: {self.tipo}")
        if not self.id or not self.titulo:
            raise ValueError("id e titulo são obrigatórios")
        if self.potencial_multiplicador < 0:
            raise ValueError("potencial_multiplicador não pode ser negativo")


@dataclass
class ArestaRede:
    origem: str
    relacao: str
    destino: str
    peso: float = 1.0
    evidencia: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.relacao not in TIPOS_RELACAO:
            raise ValueError(f"Relação inválida: {self.relacao}")
        if not self.origem or not self.destino:
            raise ValueError("origem e destino são obrigatórios")
        if self.peso < 0:
            raise ValueError("peso não pode ser negativo")


@dataclass
class RedeEvolutiva:
    """Rede de caminhos; oferece sinais para decisão sem impor uma fila."""

    schema_version: str = "0.1"
    nos: dict[str, NoRede] = field(default_factory=dict)
    arestas: list[ArestaRede] = field(default_factory=list)

    def adicionar_no(self, no: NoRede) -> None:
        if no.id in self.nos:
            raise ValueError(f"Nó já existe: {no.id}")
        self.nos[no.id] = no

    def adicionar_nos(self, nos: Iterable[NoRede]) -> None:
        for no in nos:
            self.adicionar_no(no)

    def conectar(self, aresta: ArestaRede) -> None:
        if aresta.origem not in self.nos or aresta.destino not in self.nos:
            raise KeyError("Aresta referencia nó inexistente")
        if aresta.origem == aresta.destino:
            raise ValueError("uma aresta não pode apontar para o próprio nó")
        if aresta not in self.arestas:
            self.arestas.append(aresta)

    def sucessores(self, no_id: str, relacao: str | None = None) -> list[str]:
        return [a.destino for a in self.arestas if a.origem == no_id and (relacao is None or a.relacao == relacao)]

    def predecessores(self, no_id: str, relacao: str | None = None) -> list[str]:
        return [a.origem for a in self.arestas if a.destino == no_id and (relacao is None or a.relacao == relacao)]

    def relacionados(self, no_id: str) -> list[str]:
        if no_id not in self.nos:
            raise KeyError(no_id)
        return sorted({a.destino if a.origem == no_id else a.origem for a in self.arestas if a.origem == no_id or a.destino == no_id})

    def caminhos_que_convergem(self, destino_id: str) -> list[str]:
        return self.predecessores(destino_id, "CONVERGE_COM")

    def caminhos_que_impulsionam(self, destino_id: str) -> list[str]:
        return self.predecessores(destino_id, "IMPULSIONA")

    def impulso_total(self, no_id: str) -> float:
        if no_id not in self.nos:
            raise KeyError(no_id)
        total = self.nos[no_id].potencial_multiplicador
        for a in self.arestas:
            if a.destino == no_id and a.relacao in {"IMPULSIONA", "MULTIPLICA", "MULTIPLICA_VALOR", "HABILITA"}:
                total += a.peso * self.nos[a.origem].potencial_multiplicador
        return total

    def pontos_de_alavancagem(self, limite: int = 10) -> list[tuple[str, float]]:
        if limite < 1:
            raise ValueError("limite deve ser >= 1")
        return sorted(((no_id, self.impulso_total(no_id)) for no_id in self.nos), key=lambda item: item[1], reverse=True)[:limite]

    def candidatos_contextuais(self, contexto: dict[str, float] | None = None, estados_ignorados: set[str] | None = None) -> list[tuple[str, float]]:
        """Gera sinais; não cria ordem obrigatória de execução."""
        contexto = contexto or {}
        estados_ignorados = estados_ignorados or {"ABANDONADO", "SUBSTITUIDO"}

        def sinal(no_id: str) -> float:
            no = self.nos[no_id]
            return (0.40 * no.potencial_multiplicador + 0.25 * float(contexto.get(no_id, 0.0)) + 0.10 * min(len(self.relacionados(no_id)) / 10.0, 1.0) + 0.25 * self.impulso_total(no_id))

        return sorted(((no_id, sinal(no_id)) for no_id, no in self.nos.items() if no.estado not in estados_ignorados), key=lambda item: item[1], reverse=True)

    def validar(self) -> list[str]:
        erros: list[str] = []
        ids = set(self.nos)
        for a in self.arestas:
            if a.origem not in ids:
                erros.append(f"origem inexistente: {a.origem}")
            if a.destino not in ids:
                erros.append(f"destino inexistente: {a.destino}")
        return erros

    def to_dict(self) -> dict[str, Any]:
        return {"schema_version": self.schema_version, "nos": {k: asdict(v) for k, v in self.nos.items()}, "arestas": [asdict(a) for a in self.arestas]}

    @classmethod
    def from_dict(cls, dados: dict[str, Any]) -> "RedeEvolutiva":
        rede = cls(schema_version=dados.get("schema_version", "0.1"))
        rede.adicionar_nos(NoRede(**no) for no in dados.get("nos", {}).values())
        for aresta in dados.get("arestas", []):
            rede.conectar(ArestaRede(**aresta))
        return rede

    def salvar(self, path: str) -> None:
        import json
        from pathlib import Path
        destino = Path(path)
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(json.dumps(self.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    @classmethod
    def carregar(cls, path: str) -> "RedeEvolutiva":
        import json
        from pathlib import Path
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))
