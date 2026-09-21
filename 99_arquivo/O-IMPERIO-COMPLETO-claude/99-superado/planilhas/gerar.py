"""Gera o painel: um arquivo HTML que abre em qualquer navegador, sem instalar nada."""
import json, os, sys, glob
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extrair import ler_lancamentos, consolidar

def real(v):
    return f"R$ {v:,.2f}".replace(",", "·").replace(".", ",").replace("·", ".")

def gerar(pasta, saida="painel.html"):
    todos = []
    lidos = []
    for arq in sorted(glob.glob(os.path.join(pasta, "*.xlsx"))):
        try:
            l = ler_lancamentos(arq)
            if l:
                todos += l
                lidos.append((os.path.basename(arq), len(l)))
        except Exception as e:
            lidos.append((os.path.basename(arq), f"erro: {str(e)[:40]}"))
    if not todos:
        print("Nenhum lançamento encontrado.")
        return None

    c = consolidar(todos)
    meses = c["meses"]
    tot_r = sum(m["receita"] for m in meses.values())
    tot_c = sum(m["custo"] for m in meses.values())
    ultimo = list(meses)[-1] if meses else "—"
    um = meses.get(ultimo, {})

    # tendência: compara o último mês com a média dos anteriores
    antes = [m["resultado"] for k, m in meses.items() if k != ultimo]
    media_antes = sum(antes) / len(antes) if antes else 0
    var = ((um.get("resultado", 0) - media_antes) / abs(media_antes) * 100) if media_antes else 0

    maxr = max((m["receita"] for m in meses.values()), default=1) or 1

    linhas_mes = "".join(
        f'<tr><td>{k}</td><td class="n">{real(m["receita"])}</td>'
        f'<td class="n">{real(m["custo"])}</td>'
        f'<td class="n {"pos" if m["resultado"]>=0 else "neg"}">{real(m["resultado"])}</td>'
        f'<td class="n">{m["margem"]:.1f}%</td></tr>'
        for k, m in meses.items())

    barras = "".join(
        f'<div class="barra"><div class="rot">{k[5:]}/{k[2:4]}</div>'
        f'<div class="trilho"><div class="fill rec" style="width:{m["receita"]/maxr*100:.1f}%"></div>'
        f'<div class="fill cus" style="width:{m["custo"]/maxr*100:.1f}%"></div></div>'
        f'<div class="val {"pos" if m["resultado"]>=0 else "neg"}">{real(m["resultado"])}</div></div>'
        for k, m in meses.items())

    grupos = "".join(
        f'<tr><td>{g[:46]}</td><td class="n">{real(v)}</td>'
        f'<td class="n dim">{v/tot_c*100:.1f}%</td></tr>'
        for g, v in list(c["grupos"].items())[:12]
        if not any(p in g.lower() for p in ["particular", "convenio", "venda"]))

    fornec = "".join(
        f'<tr><td>{f[:40]}</td><td class="n">{real(v)}</td></tr>'
        for f, v in list(c["fornecedores"].items())[:10])

    fontes = "".join(f'<li>{n} — {q} lançamentos</li>' if isinstance(q, int)
                     else f'<li>{n} — {q}</li>' for n, q in lidos)

    html = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Painel Financeiro — Sorriso Maior</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
html{{overflow-x:hidden}}
body{{font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
background:#F4F1EA;color:#1F2933;padding:20px;max-width:1100px;margin:0 auto;
overflow-x:hidden;overflow-wrap:break-word}}
h1{{font-size:22px;margin-bottom:4px}}
.sub{{color:#5F6B78;font-size:13px;margin-bottom:22px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px;margin-bottom:24px}}
.card{{background:#fff;border:1px solid #D8D0C2;border-radius:10px;padding:16px;
min-width:0;overflow:hidden}}
.card .lbl{{font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:#5F6B78;margin-bottom:6px}}
.card .big{{font-size:23px;font-weight:600;overflow-wrap:break-word}}
.card .pe{{font-size:12px;color:#5F6B78;margin-top:4px;overflow-wrap:break-word}}
.pos{{color:#2F7D4F}} .neg{{color:#B3402F}} .dim{{color:#7A8590}}
section{{background:#fff;border:1px solid #D8D0C2;border-radius:10px;padding:18px;margin-bottom:18px}}
h2{{font-size:14px;text-transform:uppercase;letter-spacing:.5px;color:#5F6B78;margin-bottom:14px}}
.tscroll{{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:0 -18px;padding:0 18px}}
table{{width:100%;min-width:460px;border-collapse:collapse;font-size:14px}}
th{{text-align:left;font-size:11px;text-transform:uppercase;color:#5F6B78;
padding:8px 6px;border-bottom:2px solid #E5DFD4}}
td{{padding:9px 6px;border-bottom:1px solid #EFEAE0}}
tr:last-child td{{border-bottom:none}}
.n{{text-align:right;font-variant-numeric:tabular-nums}}
.barra{{display:flex;align-items:center;gap:10px;margin-bottom:9px}}
.rot{{width:52px;font-size:12px;color:#5F6B78}}
.trilho{{flex:1;height:26px;background:#F0EBE1;border-radius:5px;position:relative;overflow:hidden}}
.fill{{position:absolute;top:0;height:100%}}
.rec{{background:#8FA98A}} .cus{{background:#C99A6E;height:100%;opacity:.92}}
.val{{width:112px;text-align:right;font-size:13px;font-variant-numeric:tabular-nums}}
.leg{{display:flex;gap:16px;font-size:12px;color:#5F6B78;margin-top:12px}}
.leg i{{display:inline-block;width:11px;height:11px;border-radius:2px;margin-right:5px}}
footer{{font-size:12px;color:#7A8590;margin-top:26px;padding-top:16px;border-top:1px solid #D8D0C2}}
footer ul{{margin:8px 0 0 18px}}
@media print{{body{{background:#fff}} section,.card{{break-inside:avoid}}}}
</style></head><body>

<h1>Painel Financeiro</h1>
<div class="sub">Sorriso Maior · consolidado de {len(meses)} meses ·
gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}</div>

<div class="cards">
  <div class="card"><div class="lbl">Receita no período</div>
    <div class="big">{real(tot_r)}</div>
    <div class="pe">média de {real(tot_r/max(len(meses),1))} por mês</div></div>
  <div class="card"><div class="lbl">Custo e despesa</div>
    <div class="big">{real(tot_c)}</div>
    <div class="pe">{tot_c/tot_r*100:.0f}% da receita</div></div>
  <div class="card"><div class="lbl">Resultado</div>
    <div class="big {'pos' if tot_r-tot_c>=0 else 'neg'}">{real(tot_r-tot_c)}</div>
    <div class="pe">margem de {(tot_r-tot_c)/tot_r*100:.1f}%</div></div>
  <div class="card"><div class="lbl">Último mês ({ultimo})</div>
    <div class="big {'pos' if um.get('resultado',0)>=0 else 'neg'}">{real(um.get('resultado',0))}</div>
    <div class="pe">{'+' if var>=0 else ''}{var:.0f}% ante a média dos anteriores</div></div>
</div>

<section><h2>Receita e custo por mês</h2>
{barras}
<div class="leg"><span><i style="background:#8FA98A"></i>receita</span>
<span><i style="background:#C99A6E"></i>custo e despesa</span></div>
</section>

<section><h2>Mês a mês</h2>
<div class="tscroll"><table><tr><th>Competência</th><th class="n">Receita</th><th class="n">Custo</th>
<th class="n">Resultado</th><th class="n">Margem</th></tr>{linhas_mes}</table></div></section>

<section><h2>Para onde vai o dinheiro</h2>
<table><tr><th>Grupo de conta</th><th class="n">Valor</th><th class="n">% do custo</th></tr>
{grupos}</table></section>

<section><h2>Maiores fornecedores</h2>
<table><tr><th>Fornecedor</th><th class="n">Valor</th></tr>{fornec}</table></section>

<footer>{c['total_lancamentos']} lançamentos consolidados de:
<ul>{fontes}</ul>
<p style="margin-top:10px">Receita identificada pelo grupo de conta.
Confira antes de usar para decisão contábil.</p></footer>
</body></html>"""

    caminho = os.path.join(pasta, saida) if os.path.isdir(pasta) else saida
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(html)
    return caminho, c

if __name__ == "__main__":
    pasta = sys.argv[1] if len(sys.argv) > 1 else "."
    r = gerar(pasta, sys.argv[2] if len(sys.argv) > 2 else "painel.html")
    if r:
        print(f"Painel gerado: {r[0]}")
        print(f"{r[1]['total_lancamentos']} lançamentos · {len(r[1]['meses'])} meses")
