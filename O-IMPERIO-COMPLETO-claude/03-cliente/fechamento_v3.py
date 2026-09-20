"""
FECHAMENTO — versão construída sobre as respostas da Lary.

O que ela disse, e o que mudou por causa disso:

"temos que digitar todas as vezes pois não é automatizado"
  → UMA origem. Lança uma vez, tudo puxa. É a dor principal.

"depende... tem clínica que sim outras não. feriado não trabalha"
  → Dias trabalhados configuráveis. Sábado por clínica, feriado marcado à mão.

"=F10/1*21 ... acumulado / dia trabalhado * total de dias que vamos trabalhar"
  → A fórmula de tendência é a deles, não a que eu tinha imaginado.

"ATENDE [convênio]"
  → Convênio entra como forma de recebimento.

"são muitas páginas e ainda tem que TIRAR PRINT E COLOCAR NO POWER POINT"
  → Aba Apresentação: já sai pronta para print, uma tela só.
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
F_TIT2 = Font(name=FONTE, bold=True, size=22, color=PRETO)
F_SUB = Font(name=FONTE, size=9, color="7F7F7F", italic=True)
F_CAB = Font(name=FONTE, bold=True, size=9, color="FFFFFF")
F_IN = Font(name=FONTE, size=10, color="0000FF")
F_AUTO = Font(name=FONTE, size=10, color="808080")
F_N = Font(name=FONTE, size=10, color=PRETO)
F_B = Font(name=FONTE, bold=True, size=10, color=PRETO)
F_SEC = Font(name=FONTE, bold=True, size=11, color=PRETO)
F_BIG = Font(name=FONTE, bold=True, size=18, color=PRETO)

FILL_CAB = PatternFill("solid", fgColor=PRETO)
FILL_SUB = PatternFill("solid", fgColor="4A4A4A")
FILL_FAIXA = PatternFill("solid", fgColor=CINZA_L)
FILL_IN = PatternFill("solid", fgColor="FFF9E6")
FILL_OFF = PatternFill("solid", fgColor="E8E8E8")

BS = Side(style="thin", color=CINZA_B)
BORDA = Border(bottom=BS)
BOX = Border(left=BS, right=BS, top=BS, bottom=BS)
TOPO = Border(top=Side(style="medium", color=PRETO))

MOEDA = 'R$ #,##0.00;[RED]-R$ #,##0.00;"—"'
MOEDA0 = 'R$ #,##0;[RED]-R$ #,##0;"—"'
INT = '#,##0;[RED]-#,##0;"—"'
PCT = '0.0%'
DIA = '[$-416]DD/MM  ddd'

# Confirmados pela Lary
PROCEDIMENTOS = ["Clínico", "Ortodontia", "Prótese", "Implante", "Estética", "Avaliação"]
FORMAS = ["Crédito", "Débito", "PIX", "Financeira", "Dinheiro", "Boleto", "Convênio"]
CATEGORIAS = ["0. Custos Diretos", "1. Administrativa", "2.Financeira", "3.Ocupação",
              "4.Despesas com Marketing", "5.Despesa com Utilidades",
              "6.Despesa com Pessoal", "7.Despesas Comerciais",
              "9. Administração Pinheiro", "10.Tributos",
              "Deduções da Receita Bruta", "Despesas Empreendedor"]
MESES = ["", "JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO",
         "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]

# Onde os lançamentos vivem — o resto da planilha conta com isto
V0, VFIM = 8, 407      # vendas
D0, DFIM = 8, 207      # despesas


def logo_em(ws, logo, alt=76):
    if logo:
        try:
            img = XLImage(logo)
            img.width, img.height = int(alt * 1.38), alt
            img.anchor = "A1"
            ws.add_image(img)
        except Exception:
            pass


def construir(ano, mes, clinica, meta, saida, logo=None, trabalha_sabado=True):
    wb = openpyxl.Workbook()
    L = get_column_letter
    ndias = calendar.monthrange(ano, mes)[1]

    # ═══ LISTAS (oculta) ═══
    li = wb.active
    li.title = "Listas"
    for i, c in enumerate(CATEGORIAS, 1):
        li.cell(i, 1, c)
    for i, p in enumerate(PROCEDIMENTOS, 1):
        li.cell(i, 2, p)
    for i, f in enumerate(FORMAS, 1):
        li.cell(i, 3, f)
    li.cell(1, 4, "Sim"); li.cell(2, 4, "Não")
    li.sheet_state = "hidden"

    # ═══ ABA 1 — CALENDÁRIO ═══
    # A Lary disse que depende da clínica e que feriado não trabalha.
    # Então o calendário é configurável, e é ele que define a meta diária.
    cal = wb.create_sheet("Calendário")
    logo_em(cal, logo)
    cal.merge_cells("C1:H1")
    cal["C1"] = f"CALENDÁRIO · {MESES[mes]} {ano}"
    cal["C1"].font = F_TIT
    cal.merge_cells("C2:H2")
    cal["C2"] = ("Marque Não nos dias que a clínica não abre — feriado, folga, o que for. "
                 "A meta se redistribui sozinha entre os dias que sobram.")
    cal["C2"].font = F_SUB
    cal.row_dimensions[1].height = 24
    cal.row_dimensions[2].height = 16

    cal["C4"] = "Meta do mês"
    cal["C4"].font = F_B
    cal["D4"] = meta
    cal["D4"].font = Font(name=FONTE, bold=True, size=12, color="0000FF")
    cal["D4"].fill = FILL_IN
    cal["D4"].number_format = MOEDA
    cal["D4"].border = BOX

    C0 = 7
    for j, t in enumerate(["Data", "Trabalha?", "Meta do dia"], 3):
        c = cal.cell(C0 - 1, j, t)
        c.font = F_CAB
        c.fill = FILL_CAB
        c.alignment = Alignment(horizontal="center")
        c.border = BOX

    for i in range(ndias):
        r = C0 + i
        d = date(ano, mes, i + 1)
        dom = d.weekday() == 6
        sab = d.weekday() == 5
        padrao = "Não" if dom or (sab and not trabalha_sabado) else "Sim"
        cal.cell(r, 3, d).font = F_N
        cal.cell(r, 3).number_format = DIA
        c = cal.cell(r, 4, padrao)
        c.font = F_IN
        c.fill = FILL_IN
        c.alignment = Alignment(horizontal="center")
        # Meta do dia = meta do mês ÷ dias marcados como Sim
        cal.cell(r, 5, f'=IF($D{r}="Sim",IFERROR($D$4/$E$4,0),0)')
        cal.cell(r, 5).font = F_AUTO
        cal.cell(r, 5).number_format = MOEDA
        for col in range(3, 6):
            cal.cell(r, col).border = BORDA
            if padrao == "Não":
                cal.cell(r, col).fill = FILL_OFF

    CFIM = C0 + ndias - 1
    cal["E4"] = f'=COUNTIF(D{C0}:D{CFIM},"Sim")'
    cal["E4"].font = Font(name=FONTE, bold=True, size=12, color=PRETO)
    cal["E4"].alignment = Alignment(horizontal="center")
    cal["E4"].border = BOX
    cal["F4"] = "dias que a clínica abre"
    cal["F4"].font = F_SUB

    dvt = DataValidation(type="list", formula1="=Listas!$D$1:$D$2", allow_blank=False,
                         showDropDown=False)
    cal.add_data_validation(dvt)
    dvt.add(f"D{C0}:D{CFIM}")

    for j, w in [(1, 16), (2, 2), (3, 15), (4, 12), (5, 15), (6, 26)]:
        cal.column_dimensions[L(j)].width = w
    cal.sheet_view.showGridLines = False
    cal.freeze_panes = f"A{C0}"

    # ═══ ABA 2 — MOVIMENTO (a única origem) ═══
    mv = wb.create_sheet("Movimento")
    logo_em(mv, logo)
    mv.merge_cells("C1:J1")
    mv["C1"] = f"{clinica.upper()} · {MESES[mes]} {ano}"
    mv["C1"].font = F_TIT
    mv.merge_cells("C2:J2")
    mv["C2"] = ("Cada venda, uma linha, uma vez só. Procedimento e forma de pagamento "
                "na mesma linha — todo o resto da planilha lê daqui.")
    mv["C2"].font = F_SUB
    mv.row_dimensions[1].height = 24
    mv.row_dimensions[2].height = 16

    for j, rot, f in [(3, "Vendido até agora", f'=SUM($F${V0}:$F${VFIM})'),
                      (5, "Meta do mês", "=Calendário!$D$4"),
                      (7, "Atingimento", "=IFERROR($D$4/$F$4,0)")]:
        mv.cell(4, j, rot).font = F_B
        c = mv.cell(4, j + 1, f)
        c.font = Font(name=FONTE, bold=True, size=11, color=PRETO)
        c.number_format = PCT if "Ating" in rot else MOEDA
    mv["I4"] = "Tendência"
    mv["I4"].font = F_B
    # A fórmula da Lary: acumulado ÷ dias trabalhados × total de dias do mês
    mv["J4"] = ('=IFERROR($D$4/MAX(1,COUNTIFS(Calendário!$D$7:$D$37,"Sim",'
                'Calendário!$C$7:$C$37,"<="&TODAY()))*Calendário!$E$4,0)')
    mv["J4"].font = Font(name=FONTE, bold=True, size=11, color=PRETO)
    mv["J4"].number_format = MOEDA

    CAB = 7
    for j, c in enumerate(["Data", "Procedimento", "Forma de recebimento", "Valor",
                           "Paciente / Obs."], 3):
        cel = mv.cell(CAB, j, c)
        cel.font = F_CAB
        cel.fill = FILL_CAB
        cel.alignment = Alignment(horizontal="center", vertical="center")
        cel.border = BOX
    mv.row_dimensions[CAB].height = 22

    for r in range(V0, VFIM + 1):
        for col in range(3, 8):
            mv.cell(r, col).fill = FILL_IN
            mv.cell(r, col).font = F_IN
            mv.cell(r, col).border = BORDA
        mv.cell(r, 3).number_format = 'DD/MM'
        mv.cell(r, 6).number_format = MOEDA

    dvp = DataValidation(type="list", formula1=f"=Listas!$B$1:$B${len(PROCEDIMENTOS)}",
                         allow_blank=True, showDropDown=False)
    dvp.error = "Escolha um procedimento da lista."
    mv.add_data_validation(dvp); dvp.add(f"D{V0}:D{VFIM}")
    dvf = DataValidation(type="list", formula1=f"=Listas!$C$1:$C${len(FORMAS)}",
                         allow_blank=True, showDropDown=False)
    dvf.error = "Escolha uma forma de recebimento da lista."
    mv.add_data_validation(dvf); dvf.add(f"E{V0}:E{VFIM}")

    mv.auto_filter.ref = f"C{CAB}:G{VFIM}"
    mv.freeze_panes = f"C{V0}"
    for j, w in [(1, 16), (2, 2), (3, 11), (4, 17), (5, 21), (6, 15), (7, 28),
                 (8, 2), (9, 13), (10, 15)]:
        mv.column_dimensions[L(j)].width = w
    mv.sheet_view.showGridLines = False

    # ═══ ABA 3 — DESPESAS ═══
    dp = wb.create_sheet("Despesas")
    logo_em(dp, logo)
    dp.merge_cells("C1:G1")
    dp["C1"] = f"DESPESAS · {MESES[mes]} {ano}"
    dp["C1"].font = F_TIT
    dp.merge_cells("C2:G2")
    dp["C2"] = "Cada saída, uma linha. Vira custo no Resumo e no DRE."
    dp["C2"].font = F_SUB
    dp.row_dimensions[1].height = 24

    dp.cell(5, 3, "Total no mês").font = F_B
    dp.cell(5, 4, f'=SUM($F${D0}:$F${DFIM})').font = Font(name=FONTE, bold=True, size=11)
    dp.cell(5, 4).number_format = MOEDA

    for j, c in enumerate(["Data", "Categoria", "Fornecedor / Descrição", "Valor", "Status"], 3):
        cel = dp.cell(7, j, c)
        cel.font = F_CAB
        cel.fill = FILL_CAB
        cel.alignment = Alignment(horizontal="center", vertical="center")
        cel.border = BOX
    dp.row_dimensions[7].height = 22

    for r in range(D0, DFIM + 1):
        for col in range(3, 8):
            dp.cell(r, col).fill = FILL_IN
            dp.cell(r, col).font = F_IN
            dp.cell(r, col).border = BORDA
        dp.cell(r, 3).number_format = 'DD/MM'
        dp.cell(r, 6).number_format = MOEDA

    dvc = DataValidation(type="list", formula1=f"=Listas!$A$1:$A${len(CATEGORIAS)}",
                         allow_blank=True, showDropDown=False)
    dvc.error = "Escolha uma categoria da lista."
    dp.add_data_validation(dvc); dvc.add(f"D{D0}:D{DFIM}")
    dvs = DataValidation(type="list", formula1='"Pago,Pendente"', allow_blank=True,
                         showDropDown=False)
    dp.add_data_validation(dvs); dvs.add(f"G{D0}:G{DFIM}")

    dp.auto_filter.ref = f"C7:G{DFIM}"
    dp.freeze_panes = f"C{D0}"
    for j, w in [(1, 16), (2, 2), (3, 11), (4, 28), (5, 34), (6, 15), (7, 12)]:
        dp.column_dimensions[L(j)].width = w
    dp.sheet_view.showGridLines = False

    # ═══ ABA 4 — DIA A DIA ═══
    # Substitui FLUXO FINANCEIRO, CATEG RESUMO e DIARIO DE ADESÃO.
    # Nada se digita: tudo lê do Movimento.
    dd = wb.create_sheet("Dia a Dia")
    logo_em(dd, logo)
    dd.merge_cells("C1:K1")
    dd["C1"] = f"DIA A DIA · {MESES[mes]} {ano}"
    dd["C1"].font = F_TIT
    dd.merge_cells("C2:K2")
    dd["C2"] = "Nada se digita aqui. Cada linha lê do Movimento e do Calendário."
    dd["C2"].font = F_SUB
    dd.row_dimensions[1].height = 24

    DCAB = 6
    for j, t in enumerate(["Data", "Trabalha", "Meta do dia", "Vendido", "% da meta",
                           "Bateu?", "Acumulado", "Meta acum.", "Dif. acum."], 3):
        c = dd.cell(DCAB, j, t)
        c.font = F_CAB
        c.fill = FILL_CAB
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BOX
    dd.row_dimensions[DCAB].height = 26

    DD0 = DCAB + 1
    for i in range(ndias):
        r = DD0 + i
        rc = C0 + i     # linha correspondente no Calendário
        dd.cell(r, 3, f"=Calendário!C{rc}").number_format = DIA
        dd.cell(r, 4, f"=Calendário!D{rc}").alignment = Alignment(horizontal="center")
        dd.cell(r, 5, f"=Calendário!E{rc}").number_format = MOEDA
        dd.cell(r, 6, f'=SUMPRODUCT((Movimento!$C${V0}:$C${VFIM}<>"")*'
                      f'(TEXT(Movimento!$C${V0}:$C${VFIM},"yyyy-mm-dd")='
                      f'TEXT($C{r},"yyyy-mm-dd"))*Movimento!$F${V0}:$F${VFIM})')
        dd.cell(r, 6).number_format = MOEDA
        dd.cell(r, 7, f'=IF($E{r}=0,"",IFERROR($F{r}/$E{r},0))')
        dd.cell(r, 7).number_format = PCT
        # "conta o dia que bateu" — resposta 14 da Lary
        dd.cell(r, 8, f'=IF(AND($E{r}>0,$F{r}>=$E{r}),1,0)')
        dd.cell(r, 8).number_format = INT
        dd.cell(r, 8).alignment = Alignment(horizontal="center")
        dd.cell(r, 9, f"=$F{r}" if i == 0 else f"=I{r-1}+$F{r}")
        dd.cell(r, 9).number_format = MOEDA
        dd.cell(r, 10, f"=$E{r}" if i == 0 else f"=J{r-1}+$E{r}")
        dd.cell(r, 10).number_format = MOEDA
        dd.cell(r, 11, f"=I{r}-J{r}")
        dd.cell(r, 11).number_format = MOEDA
        for col in range(3, 12):
            dd.cell(r, col).border = BORDA
            dd.cell(r, col).font = F_AUTO if col not in (6, 9) else F_B

    DDFIM = DD0 + ndias - 1
    rT = DDFIM + 1
    dd.cell(rT, 3, "TOTAL").font = Font(name=FONTE, bold=True, size=11)
    dd.cell(rT, 5, f"=SUM(E{DD0}:E{DDFIM})").number_format = MOEDA
    dd.cell(rT, 6, f"=SUM(F{DD0}:F{DDFIM})").number_format = MOEDA
    dd.cell(rT, 7, f"=IFERROR(F{rT}/E{rT},0)").number_format = PCT
    dd.cell(rT, 8, f"=SUM(H{DD0}:H{DDFIM})").number_format = INT
    dd.cell(rT, 8).alignment = Alignment(horizontal="center")
    dd.cell(rT, 9, f"=I{DDFIM}").number_format = MOEDA
    dd.cell(rT, 11, f"=I{rT}-E{rT}").number_format = MOEDA
    for col in range(3, 12):
        dd.cell(rT, col).font = Font(name=FONTE, bold=True, size=11)
        dd.cell(rT, col).border = TOPO

    dd.conditional_formatting.add(f"G{DD0}:G{rT}", CellIsRule(
        operator="greaterThanOrEqual", formula=["1"], font=Font(name=FONTE, bold=True, color=VERDE)))
    dd.conditional_formatting.add(f"G{DD0}:G{rT}", CellIsRule(
        operator="lessThan", formula=["0.8"], font=Font(name=FONTE, color=VERMELHO)))
    dd.conditional_formatting.add(f"K{DD0}:K{rT}", CellIsRule(
        operator="lessThan", formula=["0"], font=Font(name=FONTE, color=VERMELHO)))
    dd.conditional_formatting.add(f"F{DD0}:F{DDFIM}",
                                  DataBarRule(start_type="num", start_value=0,
                                              end_type="max", color="C9C9C9"))

    dd.freeze_panes = f"D{DD0}"
    for j, w in [(1, 16), (2, 2), (3, 14), (4, 10), (5, 13), (6, 14), (7, 11),
                 (8, 9), (9, 14), (10, 14), (11, 14)]:
        dd.column_dimensions[L(j)].width = w
    dd.sheet_view.showGridLines = False

    # ═══ ABA 5 — APRESENTAÇÃO ═══
    # Resposta 13: "tem que TIRAR PRINT E COLOCAR NO POWER POINT".
    # Esta aba já sai pronta para o print — uma tela, sem rolar.
    ap = wb.create_sheet("Apresentação")
    logo_em(ap, logo, alt=64)
    ap.merge_cells("C1:I1")
    ap["C1"] = f"{clinica.upper()}"
    ap["C1"].font = F_TIT2
    ap.merge_cells("C2:I2")
    ap["C2"] = f"{MESES[mes]} / {ano}"
    ap["C2"].font = Font(name=FONTE, size=12, color="7F7F7F")
    ap.row_dimensions[1].height = 30
    ap.row_dimensions[2].height = 20

    # Os quatro números que importam, grandes
    quatro = [("META", "=Calendário!$D$4", MOEDA0),
              ("VENDIDO", "=Movimento!$D$4", MOEDA0),
              ("TENDÊNCIA", "=Movimento!$J$4", MOEDA0),
              ("ATINGIMENTO", "=IFERROR(Movimento!$D$4/Calendário!$D$4,0)", PCT)]
    for i, (rot, f, fmt) in enumerate(quatro):
        col = 3 + i * 2
        ap.merge_cells(start_row=4, start_column=col, end_row=4, end_column=col + 1)
        c = ap.cell(4, col, rot)
        c.font = Font(name=FONTE, bold=True, size=9, color="FFFFFF")
        c.fill = FILL_CAB
        c.alignment = Alignment(horizontal="center")
        ap.merge_cells(start_row=5, start_column=col, end_row=5, end_column=col + 1)
        v = ap.cell(5, col, f)
        v.font = F_BIG
        v.number_format = fmt
        v.alignment = Alignment(horizontal="center", vertical="center")
        v.border = BOX
    ap.row_dimensions[5].height = 34

    ap.cell(7, 3, "DIAS QUE BATERAM A META").font = F_SEC
    ap.merge_cells("C8:E8")
    ap.cell(8, 3, f'=\'Dia a Dia\'!H{rT}&" de "&Calendário!$E$4&" dias trabalhados"')
    ap.cell(8, 3).font = Font(name=FONTE, bold=True, size=14, color=PRETO)

    # Receita por procedimento
    ap.cell(10, 3, "POR PROCEDIMENTO").font = F_SEC
    for j, t in enumerate(["Procedimento", "Valor", "%"], 3):
        c = ap.cell(11, j, t)
        c.font = F_CAB
        c.fill = FILL_CAB
        c.alignment = Alignment(horizontal="center")
    for i, p in enumerate(PROCEDIMENTOS):
        r = 12 + i
        ap.cell(r, 3, p).font = F_N
        ap.cell(r, 4, f'=SUMIFS(Movimento!$F${V0}:$F${VFIM},'
                      f'Movimento!$D${V0}:$D${VFIM},$C{r})')
        ap.cell(r, 4).number_format = MOEDA
        ap.cell(r, 5, f"=IFERROR(D{r}/Movimento!$D$4,0)")
        ap.cell(r, 5).number_format = PCT
        ap.cell(r, 5).font = F_AUTO
        for col in range(3, 6):
            ap.cell(r, col).border = BORDA

    # Receita por forma
    ap.cell(10, 7, "POR RECEBIMENTO").font = F_SEC
    for j, t in enumerate(["Forma", "Valor", "%"], 7):
        c = ap.cell(11, j, t)
        c.font = F_CAB
        c.fill = FILL_CAB
        c.alignment = Alignment(horizontal="center")
    for i, f in enumerate(FORMAS):
        r = 12 + i
        ap.cell(r, 7, f).font = F_N
        ap.cell(r, 8, f'=SUMIFS(Movimento!$F${V0}:$F${VFIM},'
                      f'Movimento!$E${V0}:$E${VFIM},$G{r})')
        ap.cell(r, 8).number_format = MOEDA
        ap.cell(r, 9, f"=IFERROR(H{r}/Movimento!$D$4,0)")
        ap.cell(r, 9).number_format = PCT
        ap.cell(r, 9).font = F_AUTO
        for col in range(7, 10):
            ap.cell(r, col).border = BORDA

    # Resultado
    rR = 12 + max(len(PROCEDIMENTOS), len(FORMAS)) + 1
    ap.cell(rR, 3, "RESULTADO DO MÊS").font = F_SEC
    ap.cell(rR + 1, 3, "Receita").font = F_N
    ap.cell(rR + 1, 4, "=Movimento!$D$4").number_format = MOEDA
    ap.cell(rR + 2, 3, "Despesas").font = F_N
    ap.cell(rR + 2, 4, "=Despesas!$D$5").number_format = MOEDA
    ap.cell(rR + 3, 3, "Resultado").font = F_B
    ap.cell(rR + 3, 4, f"=D{rR+1}-D{rR+2}").number_format = MOEDA
    ap.cell(rR + 3, 4).font = Font(name=FONTE, bold=True, size=12)
    ap.cell(rR + 4, 3, "Margem").font = F_B
    ap.cell(rR + 4, 4, f"=IFERROR(D{rR+3}/D{rR+1},0)").number_format = PCT
    ap.cell(rR + 4, 4).font = F_B
    for i in range(1, 5):
        ap.cell(rR + i, 3).border = BORDA
        ap.cell(rR + i, 4).border = BORDA

    ap.conditional_formatting.add(f"D{rR+3}", CellIsRule(
        operator="lessThan", formula=["0"], font=Font(name=FONTE, bold=True, size=12, color=VERMELHO)))
    ap.conditional_formatting.add(f"D{rR+3}", CellIsRule(
        operator="greaterThanOrEqual", formula=["0"], font=Font(name=FONTE, bold=True, size=12, color=VERDE)))

    for j, w in [(1, 13), (2, 2), (3, 20), (4, 15), (5, 9), (6, 4),
                 (7, 16), (8, 15), (9, 9)]:
        ap.column_dimensions[L(j)].width = w
    ap.sheet_view.showGridLines = False
    ap.page_setup.orientation = "landscape"
    ap.page_setup.fitToWidth = 1
    ap.sheet_properties.pageSetUpPr.fitToPage = True

    wb.active = 2   # abre no Movimento, onde se digita
    wb.save(saida)
    return {"dias": ndias, "linha_total_dia": rT, "vendas": (V0, VFIM)}


if __name__ == "__main__":
    info = construir(2026, 9, "Sorriso Maior", 78000.00,
                     "/home/claude/clinica/FECHAMENTO_V3.xlsx",
                     logo="/home/claude/clinica/logo_pinheiro.png",
                     trabalha_sabado=True)
    print("gerado:", info)
