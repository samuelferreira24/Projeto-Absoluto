from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import hashlib
import re


@dataclass(frozen=True)
class EvidenciaHistorica:
    path: str
    sha256: str
    papel_provavel: str
    confianca: str
    sinais: tuple[str, ...]
    contexto: tuple[str, ...]
    reutilizacao: str


PADROES = {
    "claude": r"\bclaude\b",
    "openhands": r"\bopenhands\b",
    "primeiro_sistema": r"\b(?:primeiro sistema|sistema antigo|app antigo|aplicativo antigo)\b",
    "construcao": r"\b(?:constru[íi]r|constru[çc][aã]o|desenvolv|implementa[çc][aã]o|cria[çc][aã]o)\b",
    "erros": r"\b(?:erro|erros|bug|bugs|falha|falhou|problema|problemas|limita[çc][aã]o)\b",
    "relatorio": r"\b(?:relat[oó]rio|diagn[oó]stico|an[aá]lise|auditoria)\b",
    "material_estudo": r"\b(?:material de estudo|material para estudo|reaproveit|não.*reutiliz|nao.*reutiliz)\b",
    "visao_limitada": r"\b(?:vis[aã]o limitada|vis[aã]o falha|vis[aã]o.*[úu]nico app|um [úu]nico app)\b",
    "conversa": r"\b(?:mensagem \d+|usu[aá]rio|ia|transcri[çc][aã]o)\b",
}


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for bloco in iter(lambda: f.read(1024 * 1024), b""):
            h.update(bloco)
    return h.hexdigest()


def _sinais(texto: str) -> list[str]:
    return [nome for nome, padrao in PADROES.items() if re.search(padrao, texto, re.I | re.S)]


def classificar_texto(texto: str, path: str = "") -> EvidenciaHistorica:
    sinais = _sinais(texto)
    tem_claude = "claude" in sinais
    tem_construcao = "construcao" in sinais
    tem_erros = "erros" in sinais
    tem_relatorio = "relatorio" in sinais
    tem_estudo = "material_estudo" in sinais
    tem_antigo = "primeiro_sistema" in sinais
    tem_limitacao = "visao_limitada" in sinais

    if tem_relatorio and tem_erros and (tem_construcao or tem_antigo):
        papel = "relatorio_pos_construcao"
        confianca = "alta"
    elif tem_claude and (tem_construcao or tem_antigo):
        papel = "evidencia_construcao_com_claude"
        confianca = "alta"
    elif tem_estudo and (tem_antigo or tem_limitacao):
        papel = "material_de_estudo_do_prototipo"
        confianca = "alta"
    elif "conversa" in sinais and (tem_claude or tem_antigo):
        papel = "transcricao_relevante"
        confianca = "media"
    elif tem_relatorio:
        papel = "relatorio_sem_vinculo_confirmado"
        confianca = "media"
    else:
        papel = "evidencia_contextual"
        confianca = "baixa"

    if tem_estudo or tem_antigo or tem_limitacao:
        reutilizacao = "somente_apos_contextualizacao"
    else:
        reutilizacao = "nao_determinado"

    contexto = []
    if tem_claude:
        contexto.append("Claude aparece explicitamente")
    if tem_antigo:
        contexto.append("há referência a sistema/app anterior")
    if tem_limitacao:
        contexto.append("há sinal de limitação da visão ou do formato inicial")
    if tem_relatorio:
        contexto.append("há caráter de relatório/análise")
    if tem_erros:
        contexto.append("há registro de erros/problemas/limitações")

    return EvidenciaHistorica(
        path=path,
        sha256="",
        papel_provavel=papel,
        confianca=confianca,
        sinais=tuple(sinais),
        contexto=tuple(contexto),
        reutilizacao=reutilizacao,
    )


def analisar_arquivo_historico(path: str | Path) -> EvidenciaHistorica:
    p = Path(path)
    texto = p.read_text(encoding="utf-8", errors="replace")
    base = classificar_texto(texto, str(p))
    return EvidenciaHistorica(**{**asdict(base), "sha256": _sha256(p)})


def analisar_lote(root: str | Path) -> list[dict]:
    raiz = Path(root)
    resultados = []
    for path in sorted(raiz.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".txt", ".md", ".html", ".htm", ".mht", ".mhtml"}:
            resultados.append(asdict(analisar_arquivo_historico(path)))
    return resultados
