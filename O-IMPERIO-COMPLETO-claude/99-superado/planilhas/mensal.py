"""
FECHAMENTO MENSAL — a base da pirâmide.

Aqui a recepção lança o dia a dia: quanto entrou, por qual forma de pagamento.
Tudo o mais se calcula: total do dia, acumulado, atingimento da meta, e o
FECHAMENTO DO MÊS que alimenta o DRE.

Segue o mecanismo que eles já usam (Total = soma das formas de pagamento,
Acumulado = anterior + hoje), só que sem digitar fórmula à mão todo mês.
"""
import openpyxl, warnings, calendar
from datetime import date
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, DataBarRule
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as XLImage
warnings.filterwarnings("ignore")

FONTE = "Calibri"
PRETO = "1A1A1A"
CINZA_L = "F5F5F5"
CINZA_B = "D9D9D9"
VERDE = "1F7A3D"
VERMELHO = "C00000"

F_TIT = Font(name=FONTE, bold=True, size=16, color=PRETO)
F_SUB = Font(name=FONTE, size=9, color="7F7F7F", italic=True)
F_CAB = Font(name=FONTE, bold=True, size=9, color="FFFFFF")
F_IN = Font(name=FONTE, size=10, color="0000FF")
F_AUTO = Font(name=FONTE, size=10, color="808080")
F_N = Font(name=FONTE, size=10, color=PRETO)
F_B = Font(name=FONTE, bold=True, size=10, color=PRETO)
F_SEC = Font(name=FONTE, bold=True, size=11, color=PRETO)

FILL_CAB = PatternFill("solid", fgColor=PRETO)
FILL_FAIXA = PatternFill("solid", fgColor=CINZA_L)
FILL_IN = PatternFill("solid", fgColor="FFF9E6")
FILL_FIM = PatternFill("solid", fgColor="E8E8E8")

BS = Side(style="thin", color=CINZA_B)
BORDA = Border(bottom=BS)
BOX = Border(left=BS, right=BS, top=BS, bottom=BS)
TOPO = Border(top=Side(style="medium", color=PRETO))

MOEDA = 'R$ #,##0.00;[RED]-R$ #,##0.00;"—"'
PCT = '0.0%'
DIA = '[$-416]DD/MM  ddd'

FORMAS = ["Crédito", "Débito", "PIX", "Financeira", "Dinheiro", "Boleto"]


def construir_mes(ano, mes, clinica, meta_mensal, saida, logo=None, dias_uteis=None):
    wb = openpyxl.Workbook()
    ndias = calendar.monthrange(ano, mes)[1]
    nome_mes = ["", "JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO",
                "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"][mes]

    # ═══════ ABA 1 — DIA A DIA ═══════
    ws = wb.active
    ws.title = "Dia a Dia"

    if logo:
        try:
            img = XLImage(logo); img.width, img.height = 105, 76; img.anchor = "A1"
            ws.add_image(img)
        except Exception:
            pass

    ws.merge_cells("C1:J1")
    ws["C1"] = f"{clinica.upper()} · {nome_mes} {ano}"
    ws["C1"].font = F_TIT
    ws.merge_cells("C2:J2")
    ws["C2"] = ("Lance o caixa do dia nas colunas azuis. Total, acumulado e "
                "atingimento se calculam sozinhos.")
    ws["C2"].font = F_SUB
    ws.row_dimensions[1].height = 24
    ws.row_dimensions[2].height = 16
    ws.row_dimensions[3].height = 22

    # ── Meta do mês: muda aqui, a meta diária se recalcula ──
    ws["C4"] = "Meta do mês"
    ws["C4"].font = F_B
    ws["D4"] = meta_mensal
    ws["D4"].font = Font(name=FONTE, bold=True, size=11, color="0000FF")
    ws["D4"].fill = FILL_IN
    ws["D4"].number_format = MOEDA
    ws["D4"].border = BOX
    ws["E4"] = "Dias úteis"
    ws["E4"].font = F_B
    ws["E4"].alignment = Alignment(horizontal="right")
    ws["F4"] = dias_uteis or sum(
        1 for d in range(1, ndias + 1) if date(ano, mes, d).weekday() < 5)
    ws["F4"].font = Font(name=FONTE, bold=True, size=11, color="0000FF")
    ws["F4"].fill = FILL_IN
    ws["F4"].border = BOX
    ws["F4"].alignment = Alignment(horizontal="center")
    ws.merge_cells("G4:H4")
    ws["G4"] = "Meta por dia útil"
    ws["G4"].font = F_B
    ws["G4"].alignment = Alignment(horizontal="right")
    ws["I4"] = "=IFERROR($D$4/$F$4,0)"
    ws["I4"].font = Font(name=FONTE, bold=True, size=11, color=PRETO)
    ws["I4"].number_format = MOEDA

    CAB = 6
    cabs = ["Data", "Meta do dia"] + FORMAS + ["Total do dia", "Acumulado", "% da meta"]
    for j, c in enumerate(cabs, 3):
        cel = ws.cell(CAB, j, c)
        cel.font = F_CAB
        cel.fill = FILL_CAB
        cel.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cel.border = BOX
    ws.row_dimensions[CAB].height = 30

    L0 = CAB + 1
    col_forma0 = 5                      # E = primeira forma de pagamento
    col_forma1 = col_forma0 + len(FORMAS) - 1   # J = última
    cTOT = col_forma1 + 1               # K
    cACU = cTOT + 1                     # L
    cPCT = cACU + 1                     # M

    for i in range(ndias):
        r = L0 + i
        d = date(ano, mes, i + 1)
        fim_semana = d.weekday() >= 5

        ws.cell(r, 3, d).font = F_N
        ws.cell(r, 3).number_format = DIA
        ws.cell(r, 3).alignment = Alignment(horizontal="left")

        # Meta do dia: zero no fim de semana, senão a meta diária
        ws.cell(r, 4, f'=IF(WEEKDAY(C{r},2)>5,0,$I$4)')
        ws.cell(r, 4).font = F_AUTO
        ws.cell(r, 4).number_format = MOEDA

        # Formas de pagamento: é o que a recepção digita
        for k in range(len(FORMAS)):
            c = ws.cell(r, col_forma0 + k)
            c.font = F_IN
            c.number_format = MOEDA
            c.fill = FILL_FIM if fim_semana else FILL_IN

        L = get_column_letter
        ws.cell(r, cTOT, f'=SUM({L(col_forma0)}{r}:{L(col_forma1)}{r})')
        ws.cell(r, cACU, f'={L(cTOT)}{r}' if i == 0 else f'={L(cACU)}{r-1}+{L(cTOT)}{r}')
        ws.cell(r, cPCT, f'=IFERROR({L(cTOT)}{r}/D{r},"")')
        for col in (cTOT, cACU):
            ws.cell(r, col).font = F_B if col == cTOT else F_AUTO
            ws.cell(r, col).number_format = MOEDA
        ws.cell(r, cPCT).font = F_AUTO
        ws.cell(r, cPCT).number_format = PCT

        for col in range(3, cPCT + 1):
            ws.cell(r, col).border = BORDA
            if fim_semana and col in (3, 4, cTOT, cACU, cPCT):
                ws.cell(r, col).fill = FILL_FIM

    FIM = L0 + ndias - 1

    # ── Linha de fechamento: é ela que alimenta o DRE ──
    rF = FIM + 1
    ws.cell(rF, 3, "TOTAL DO MÊS").font = Font(name=FONTE, bold=True, size=11, color=PRETO)
    ws.cell(rF, 4, f"=SUM(D{L0}:D{FIM})").number_format = MOEDA
    ws.cell(rF, 4).font = F_B
    for k in range(len(FORMAS)):
        col = col_forma0 + k
        L = get_column_letter(col)
        c = ws.cell(rF, col, f"=SUM({L}{L0}:{L}{FIM})")
        c.font = F_B
        c.number_format = MOEDA
    L = get_column_letter
    ws.cell(rF, cTOT, f"=SUM({L(cTOT)}{L0}:{L(cTOT)}{FIM})").font = Font(
        name=FONTE, bold=True, size=11, color=PRETO)
    ws.cell(rF, cTOT).number_format = MOEDA
    ws.cell(rF, cACU, f"={L(cACU)}{FIM}").font = F_B
    ws.cell(rF, cACU).number_format = MOEDA
    ws.cell(rF, cPCT, f"=IFERROR({L(cTOT)}{rF}/$D$4,0)").font = F_B
    ws.cell(rF, cPCT).number_format = PCT
    for col in range(3, cPCT + 1):
        ws.cell(rF, col).border = TOPO

    # Verde quando bate a meta, vermelho quando não
    ws.conditional_formatting.add(f"{L(cPCT)}{L0}:{L(cPCT)}{rF}", CellIsRule(
        operator="greaterThanOrEqual", formula=["1"], font=Font(name=FONTE, bold=True, color=VERDE)))
    ws.conditional_formatting.add(f"{L(cPCT)}{L0}:{L(cPCT)}{rF}", CellIsRule(
        operator="lessThan", formula=["0.8"], font=Font(name=FONTE, color=VERMELHO)))
    ws.conditional_formatting.add(f"{L(cTOT)}{L0}:{L(cTOT)}{FIM}",
                                  DataBarRule(start_type="num", start_value=0,
                                              end_type="max", color="C9C9C9"))

    ws.auto_filter.ref = f"C{CAB}:{L(cPCT)}{FIM}"
    ws.freeze_panes = f"E{L0}"
    larguras = {1: 16, 2: 2, 3: 14, 4: 13}
    for k in range(len(FORMAS)):
        larguras[col_forma0 + k] = 12
    larguras[cTOT] = 14
    larguras[cACU] = 14
    larguras[cPCT] = 11
    for j, w in larguras.items():
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.sheet_view.showGridLines = False

    # ═══════ ABA 2 — DESPESAS DO MÊS ═══════
    dp = wb.create_sheet("Despesas")
    if logo:
        try:
            img2 = XLImage(logo); img2.width, img2.height = 105, 76; img2.anchor = "A1"
            dp.add_image(img2)
        except Exception:
            pass
    dp.merge_cells("C1:G1")
    dp["C1"] = f"DESPESAS · {nome_mes} {ano}"
    dp["C1"].font = F_TIT
    dp.merge_cells("C2:G2")
    dp["C2"] = "Cada saída de dinheiro, uma linha. É isto que vira o custo no DRE."
    dp["C2"].font = F_SUB
    dp.row_dimensions[1].height = 24
    dp.row_dimensions[3].height = 22

    CATEGORIAS = ["0. Custos Diretos", "1. Administrativa", "2.Financeira", "3.Ocupação",
                  "4.Despesas com Marketing", "5.Despesa com Utilidades",
                  "6.Despesa com Pessoal", "7.Despesas Comerciais",
                  "9. Administração Pinheiro", "10.Tributos",
                  "Deduções da Receita Bruta", "Despesas Empreendedor"]

    cd = wb.create_sheet("Listas")
    for i, c in enumerate(CATEGORIAS, 1):
        cd.cell(i, 1, c)
    cd.sheet_state = "hidden"

    CABD = 5
    for j, c in enumerate(["Data", "Categoria", "Fornecedor / Descrição", "Valor", "Status"], 3):
        cel = dp.cell(CABD, j, c)
        cel.font = F_CAB
        cel.fill = FILL_CAB
        cel.alignment = Alignment(horizontal="center", vertical="center")
        cel.border = BOX
    dp.row_dimensions[CABD].height = 22

    D0 = CABD + 1
    DFIM = D0 + 149
    for r in range(D0, DFIM + 1):
        for col in range(3, 8):
            dp.cell(r, col).fill = FILL_IN
            dp.cell(r, col).font = F_IN
            dp.cell(r, col).border = BORDA
        dp.cell(r, 3).number_format = 'DD/MM/YYYY'
        dp.cell(r, 6).number_format = MOEDA

    dvc = DataValidation(type="list", formula1=f"=Listas!$A$1:$A${len(CATEGORIAS)}",
                         allow_blank=True, showDropDown=False)
    dvc.error = "Escolha uma categoria da lista."
    dp.add_data_validation(dvc)
    dvc.add(f"D{D0}:D{DFIM}")

    dvs = DataValidation(type="list", formula1='"Pago,Pendente"', allow_blank=True,
                         showDropDown=False)
    dp.add_data_validation(dvs)
    dvs.add(f"G{D0}:G{DFIM}")

    rT = DFIM + 1
    dp.cell(rT, 3, "TOTAL DE DESPESAS").font = Font(name=FONTE, bold=True, size=11, color=PRETO)
    dp.cell(rT, 6, f"=SUM(F{D0}:F{DFIM})").font = Font(name=FONTE, bold=True, size=11, color=PRETO)
    dp.cell(rT, 6).number_format = MOEDA
    for col in range(3, 8):
        dp.cell(rT, col).border = TOPO

    dp.auto_filter.ref = f"C{CABD}:G{DFIM}"
    dp.freeze_panes = f"C{D0}"
    for j, w in [(1, 16), (2, 2), (3, 13), (4, 28), (5, 34), (6, 15), (7, 12)]:
        dp.column_dimensions[get_column_letter(j)].width = w
    dp.sheet_view.showGridLines = False

    # ═══════ ABA 3 — FECHAMENTO (o que sobe pro DRE) ═══════
    fc = wb.create_sheet("Fechamento")
    if logo:
        try:
            img3 = XLImage(logo); img3.width, img3.height = 105, 76; img3.anchor = "A1"
            fc.add_image(img3)
        except Exception:
            pass
    fc.merge_cells("C1:F1")
    fc["C1"] = f"FECHAMENTO · {nome_mes} {ano}"
    fc["C1"].font = F_TIT
    fc.merge_cells("C2:F2")
    fc["C2"] = "Nada se digita aqui. É esta linha que você leva para o DRE consolidado."
    fc["C2"].font = F_SUB
    fc.row_dimensions[1].height = 24
    fc.row_dimensions[3].height = 22

    L = get_column_letter
    linhas = [
        ("RECEITA", None, None),
        ("Meta do mês", "='Dia a Dia'!$D$4", MOEDA),
        ("Realizado", f"='Dia a Dia'!{L(cTOT)}{rF}", MOEDA),
        ("Atingimento", "=IFERROR(D6/D5,0)", PCT),
        ("", None, None),
        ("POR FORMA DE PAGAMENTO", None, None),
    ]
    r = 4
    for rot, f, fmt in linhas:
        if rot:
            fc.cell(r, 3, rot).font = F_SEC if f is None else F_N
        if f:
            c = fc.cell(r, 4, f)
            c.number_format = fmt
            c.font = F_B if rot in ("Realizado", "Atingimento") else F_N
            c.alignment = Alignment(horizontal="right")
            fc.cell(r, 3).border = BORDA
            c.border = BORDA
        r += 1

    for k, forma in enumerate(FORMAS):
        rr = r + k
        fc.cell(rr, 3, forma).font = F_N
        fc.cell(rr, 4, f"='Dia a Dia'!{L(col_forma0+k)}{rF}")
        fc.cell(rr, 4).number_format = MOEDA
        fc.cell(rr, 4).alignment = Alignment(horizontal="right")
        fc.cell(rr, 5, f"=IFERROR(D{rr}/$D$6,0)")
        fc.cell(rr, 5).number_format = PCT
        fc.cell(rr, 5).font = F_AUTO
        for col in (3, 4, 5):
            fc.cell(rr, col).border = BORDA

    rD = r + len(FORMAS) + 1
    fc.cell(rD, 3, "DESPESAS").font = F_SEC
    fc.cell(rD + 1, 3, "Total de despesas").font = F_N
    fc.cell(rD + 1, 4, f"=Despesas!F{rT}")
    fc.cell(rD + 1, 4).number_format = MOEDA
    fc.cell(rD + 1, 4).alignment = Alignment(horizontal="right")

    for k, cat in enumerate(CATEGORIAS):
        rr = rD + 2 + k
        fc.cell(rr, 3, cat).font = F_N
        fc.cell(rr, 4, f'=SUMIFS(Despesas!$F:$F,Despesas!$D:$D,$C{rr})')
        fc.cell(rr, 4).number_format = MOEDA
        fc.cell(rr, 4).alignment = Alignment(horizontal="right")
        fc.cell(rr, 5, f"=IFERROR(D{rr}/$D${rD+1},0)")
        fc.cell(rr, 5).number_format = PCT
        fc.cell(rr, 5).font = F_AUTO
        for col in (3, 4, 5):
            fc.cell(rr, col).border = BORDA

    rR = rD + 2 + len(CATEGORIAS) + 1
    fc.cell(rR, 3, "RESULTADO DO MÊS").font = Font(name=FONTE, bold=True, size=12, color=PRETO)
    fc.cell(rR, 4, f"=D6-D{rD+1}")
    fc.cell(rR, 4).number_format = MOEDA
    fc.cell(rR, 4).font = Font(name=FONTE, bold=True, size=12, color=PRETO)
    fc.cell(rR, 4).alignment = Alignment(horizontal="right")
    fc.cell(rR + 1, 3, "Margem").font = F_B
    fc.cell(rR + 1, 4, f"=IFERROR(D{rR}/D6,0)")
    fc.cell(rR + 1, 4).number_format = PCT
    fc.cell(rR + 1, 4).font = F_B
    fc.cell(rR + 1, 4).alignment = Alignment(horizontal="right")
    for col in (3, 4):
        fc.cell(rR, col).border = TOPO

    fc.conditional_formatting.add(f"D{rR}", CellIsRule(
        operator="lessThan", formula=["0"],
        font=Font(name=FONTE, bold=True, size=12, color=VERMELHO)))
    fc.conditional_formatting.add(f"D{rR}", CellIsRule(
        operator="greaterThanOrEqual", formula=["0"],
        font=Font(name=FONTE, bold=True, size=12, color=VERDE)))

    for j, w in [(1, 16), (2, 2), (3, 30), (4, 17), (5, 12)]:
        fc.column_dimensions[get_column_letter(j)].width = w
    fc.sheet_view.showGridLines = False

    wb.active = 0
    wb.save(saida)
    return ndias, rF


if __name__ == "__main__":
    import sys
    ndias, linha = construir_mes(
        2026, 9, "Sorriso Maior", 78000.00,
        "/home/claude/clinica/FECHAMENTO_SETEMBRO.xlsx",
        logo="/home/claude/clinica/logo_pinheiro.png")
    print(f"{ndias} dias · fechamento na linha {linha}")
