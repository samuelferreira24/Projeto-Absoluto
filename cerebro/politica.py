"""Políticas portáveis de autonomia, risco e autorização."""
from dataclasses import dataclass

NIVEIS = {0: "OBSERVAR", 1: "ANALISAR", 2: "AGIR_REVERSIVEL", 3: "DELEGAR", 4: "ALTERAR_AUTORIZADO", 5: "PROPOR_ESTRATEGIA", 6: "AUTORIZACAO_HUMANA"}

@dataclass(frozen=True)
class PoliticaAcao:
    nome: str
    nivel_autonomia: int
    reversivel: bool = True
    requer_autorizacao: bool = False
    justificativa: str = ""

    def __post_init__(self):
        if not self.nome.strip():
            raise ValueError("nome obrigatório")
        if self.nivel_autonomia not in NIVEIS:
            raise ValueError("nível de autonomia inválido")
        if self.nivel_autonomia >= 6 and not self.requer_autorizacao:
            raise ValueError("ações de nível 6 exigem autorização humana")
        if self.requer_autorizacao and not self.justificativa.strip():
            raise ValueError("ação que requer autorização deve ter justificativa")

def pode_executar(acao: PoliticaAcao, nivel_concedido: int) -> bool:
    if nivel_concedido not in NIVEIS:
        raise ValueError("nível concedido inválido")
    return nivel_concedido >= acao.nivel_autonomia and not acao.requer_autorizacao
