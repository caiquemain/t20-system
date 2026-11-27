# -*- coding: utf-8 -*-
"""Exportador de Ficha de Auditoria em Excel (.xlsx) — Tormenta20 JdA.

Gera uma planilha com 5 abas organizadas, visual temático T20 e fórmulas
nativas do Excel (=SUM, =IF, multiplicação de carga) para auditoria completa
de atributos, PV, PM, Defesa, CD, perícias, ataques, magias, habilidades e inventário.
"""
from io import BytesIO
from typing import Any, List, Optional, Tuple
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from .models import Personagem, StatCalculado

XLSX_MIMETYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

# ── Paleta Visual T20 ──
_FILL_BANNER = PatternFill("solid", fgColor="7B1E26")       # Vinho Tormenta
_FILL_SECTION = PatternFill("solid", fgColor="2B2B38")      # Grafite escuro
_FILL_HEADER = PatternFill("solid", fgColor="1E1E28")       # Cabeçalho tabela
_FILL_ZEBRA = PatternFill("solid", fgColor="F5F6FA")        # Linha alternada
_FILL_WHITE = PatternFill("solid", fgColor="FFFFFF")
_FILL_TOTAL = PatternFill("solid", fgColor="FFF4D6")        # Creme dourado (totais)
_FILL_WARN = PatternFill("solid", fgColor="FFEBEE")         # Alerta vermelho suave

_FONT_BANNER = Font(name="Calibri", size=15, bold=True, color="FFD700")
_FONT_SUBBANNER = Font(name="Calibri", size=10, italic=True, color="F5E6CA")
_FONT_SECTION = Font(name="Calibri", size=11, bold=True, color="FFD700")
_FONT_HEADER = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
_FONT_BODY = Font(name="Calibri", size=10, color="1F2937")
_FONT_BOLD = Font(name="Calibri", size=10, bold=True, color="111827")
_FONT_TOTAL = Font(name="Calibri", size=10, bold=True, color="7B1E26")
_FONT_MUTED = Font(name="Calibri", size=9, italic=True, color="6B7280")

_THIN = Side(style="thin", color="D1D5DB")
_MED_GOLD = Side(style="medium", color="B8860B")
_BORDER_CELL = Border(left=_THIN, right=_THIN, top=_THIN, bottom=_THIN)
_BORDER_TOTAL = Border(left=_THIN, right=_THIN, top=_MED_GOLD, bottom=_MED_GOLD)

_FMT_SIGNED = "+#,##0;-#,##0;0"
_FMT_INT = "#,##0"


def _set_banner(ws, titulo: str, subtitulo: str, max_col: int) -> int:
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=max_col)
    c1 = ws.cell(row=1, column=1, value=titulo)
    c1.font = _FONT_BANNER
    c1.fill = _FILL_BANNER
    c1.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[1].height = 28

    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=max_col)
    c2 = ws.cell(row=2, column=1, value=subtitulo)
    c2.font = _FONT_SUBBANNER
    c2.fill = _FILL_BANNER
    c2.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[2].height = 20
    return 4


def _set_section(ws, row: int, titulo: str, max_col: int) -> int:
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=max_col)
    c = ws.cell(row=row, column=1, value=titulo)
    c.font = _FONT_SECTION
    c.fill = _FILL_SECTION
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[row].height = 22
    return row + 1


def _set_headers(ws, row: int, headers: List[str], aligns: Optional[List[str]] = None) -> int:
    for idx, h in enumerate(headers, start=1):
        c = ws.cell(row=row, column=idx, value=h)
        c.font = _FONT_HEADER
        c.fill = _FILL_HEADER
        c.border = _BORDER_CELL
        h_align = (aligns[idx - 1] if aligns and idx - 1 < len(aligns) else "left")
        c.alignment = Alignment(horizontal=h_align, vertical="center", wrap_text=True)
    ws.row_dimensions[row].height = 22
    return row + 1


def _style_row(ws, row: int, ncols: int, zebra: bool = False, total: bool = False):
    fill = _FILL_TOTAL if total else (_FILL_ZEBRA if zebra else _FILL_WHITE)
    font = _FONT_TOTAL if total else _FONT_BODY
    border = _BORDER_TOTAL if total else _BORDER_CELL
    for col in range(1, ncols + 1):
        cell = ws.cell(row=row, column=col)
        cell.fill = fill
        if not cell.font or cell.font == Font():
            cell.font = font
        elif total:
            cell.font = _FONT_TOTAL
        cell.border = border


def _auto_fit(ws, widths: List[int]):
    for idx, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(idx)].width = w


def _escrever_bloco_stat_calc(
    ws,
    start_row: int,
    titulo: str,
    stat: Optional[StatCalculado],
    valor_fallback: int,
    signed: bool = False,
) -> int:
    row = _set_section(ws, start_row, titulo, 5)
    row = _set_headers(ws, row, ["Fonte do Cálculo", "Categoria", "Valor", "Observação", "Status"], ["left", "center", "right", "left", "center"])
    first_data = row

    if stat is not None:
        # Base
        ws.cell(row=row, column=1, value="Valor Base").font = _FONT_BOLD
        ws.cell(row=row, column=2, value="Base").alignment = Alignment(horizontal="center")
        c_val = ws.cell(row=row, column=3, value=stat.base)
        c_val.number_format = _FMT_INT
        c_val.alignment = Alignment(horizontal="right")
        ws.cell(row=row, column=4, value="Base inicial da regra")
        ws.cell(row=row, column=5, value="Ativo").alignment = Alignment(horizontal="center")
        _style_row(ws, row, 5, zebra=False)
        row += 1

        for idx, f in enumerate(stat.fontes or []):
            ws.cell(row=row, column=1, value=f.fonte).font = _FONT_BODY
            ws.cell(row=row, column=2, value=f.categoria or "Bônus").alignment = Alignment(horizontal="center")
            cv = ws.cell(row=row, column=3, value=f.valor)
            cv.number_format = _FMT_SIGNED
            cv.alignment = Alignment(horizontal="right")
            ws.cell(row=row, column=4, value=f.descricao or "")
            ws.cell(row=row, column=5, value="Penalidade" if f.valor < 0 else "Bônus").alignment = Alignment(horizontal="center")
            _style_row(ws, row, 5, zebra=(idx % 2 == 0))
            row += 1
    else:
        ws.cell(row=row, column=1, value="Valor Calculado").font = _FONT_BOLD
        ws.cell(row=row, column=2, value="Base").alignment = Alignment(horizontal="center")
        cv = ws.cell(row=row, column=3, value=valor_fallback)
        cv.number_format = _FMT_SIGNED if signed else _FMT_INT
        cv.alignment = Alignment(horizontal="right")
        ws.cell(row=row, column=4, value="Sem detalhamento de fontes")
        ws.cell(row=row, column=5, value="Ativo").alignment = Alignment(horizontal="center")
        _style_row(ws, row, 5, zebra=False)
        row += 1

    last_data = row - 1
    ws.cell(row=row, column=1, value=f"TOTAL — {titulo}").font = _FONT_TOTAL
    ws.cell(row=row, column=2, value="Fórmula Excel").alignment = Alignment(horizontal="center")
    ct = ws.cell(row=row, column=3, value=f"=SUM(C{first_data}:C{last_data})")
    ct.number_format = _FMT_SIGNED if signed else _FMT_INT
    ct.alignment = Alignment(horizontal="right")
    ws.cell(row=row, column=4, value=f"Soma automática de C{first_data} até C{last_data}")
    ws.cell(row=row, column=5, value="Auditado").alignment = Alignment(horizontal="center")
    _style_row(ws, row, 5, total=True)
    ws.row_dimensions[row].height = 22
    return row + 2


def gerar_xlsx_bytes(ficha: Personagem) -> bytes:
    """Gera o arquivo .xlsx completo de auditoria da ficha e retorna os bytes."""
    wb = Workbook()

    cab = ficha.cabecalho
    classes_str = " / ".join(
        f"{c.nome}{f' ({c.subclasse})' if c.subclasse else ''} {c.nivel}"
        for c in (ficha.classes or [])
    ) or "Sem classe"
    subtitulo = (
        f"Raça: {cab.raca or '—'}  |  Origem: {cab.origem or '—'}  |  "
        f"Divindade: {cab.deus or 'Nenhuma'}  |  Classes: {classes_str}  |  Nível Total: {cab.nivel_total}"
    )

    # ═══════════════════════════════════════════════════════════════
    # ABA 1: RESUMO & AUDITORIA
    # ═══════════════════════════════════════════════════════════════
    ws1 = wb.active
    ws1.title = "Resumo & Auditoria"
    ws1.views.sheetView[0].showGridLines = True
    row = _set_banner(ws1, f"FICHA DE AUDITORIA T20 — {cab.nome or 'Personagem'}", subtitulo, 5)

    # Identidade e Características
    row = _set_section(ws1, row, "1. IDENTIDADE & CARACTERÍSTICAS DERIVADAS", 5)
    info_rows: List[Tuple[str, Any, str, Any]] = [
        ("Nome", cab.nome or "—", "Tamanho", getattr(ficha.status, "tamanho", None) or "Médio"),
        ("Raça", cab.raca or "—", "Deslocamento", f"{ficha.status.deslocamento}m"),
        ("Origem", cab.origem or "—", "Penalidade Armadura", ficha.status.penalidade_armadura),
        ("Divindade", cab.deus or "Nenhuma", "Círculo Máximo Magia", ficha.combate.circulo_maximo),
        ("Proficiências", ", ".join(ficha.status.proficiencias or []) or "Nenhuma", "Imunidades", ", ".join(ficha.status.imunidades or []) or "Nenhuma"),
        ("Sentidos", ", ".join(ficha.status.sentidos or []) or "Comuns", "Reduções de Dano (RD)", ", ".join(f"{k} {v}" for k, v in (ficha.status.rd or {}).items()) or "Nenhuma"),
    ]
    for idx, (k1, v1, k2, v2) in enumerate(info_rows):
        ws1.cell(row=row, column=1, value=k1).font = _FONT_BOLD
        ws1.cell(row=row, column=2, value=v1).alignment = Alignment(wrap_text=True)
        ws1.cell(row=row, column=3, value=k2).font = _FONT_BOLD
        ws1.merge_cells(start_row=row, start_column=4, end_row=row, end_column=5)
        ws1.cell(row=row, column=4, value=v2).alignment = Alignment(wrap_text=True)
        _style_row(ws1, row, 5, zebra=(idx % 2 == 1))
        row += 1
    row += 1

    # Atributos com fórmula =SUM(...)
    row = _set_section(ws1, row, "2. ATRIBUTOS (BASE + BÔNUS = TOTAL AUTOMÁTICO)", 5)
    row = _set_headers(ws1, row, ["Atributo", "Base", "Bônus (Raça/Poderes/Itens)", "Total (=SUM)", "Fontes Auditadas"], ["left", "right", "right", "right", "left"])
    atributos_lista = [
        ("Força", "forca"),
        ("Destreza", "destreza"),
        ("Constituição", "constituicao"),
        ("Inteligência", "inteligencia"),
        ("Sabedoria", "sabedoria"),
        ("Carisma", "carisma"),
    ]
    for idx, (label, key) in enumerate(atributos_lista):
        base_v = getattr(ficha.atributos_base, key, 0)
        final_v = getattr(ficha.atributos, key, 0)
        calc_obj = (ficha.atributos_calc or {}).get(key)
        bonus_v = final_v - base_v
        fontes_txt = "; ".join(f"{f.fonte} ({f.valor:+d})" for f in (calc_obj.fontes if calc_obj else [])) or "Apenas base"

        ws1.cell(row=row, column=1, value=label).font = _FONT_BOLD
        cb = ws1.cell(row=row, column=2, value=base_v)
        cb.number_format = _FMT_SIGNED
        cb.alignment = Alignment(horizontal="right")
        cbon = ws1.cell(row=row, column=3, value=bonus_v)
        cbon.number_format = _FMT_SIGNED
        cbon.alignment = Alignment(horizontal="right")
        ct = ws1.cell(row=row, column=4, value=f"=SUM(B{row}:C{row})")
        ct.number_format = _FMT_SIGNED
        ct.alignment = Alignment(horizontal="right")
        ct.font = _FONT_BOLD
        ws1.cell(row=row, column=5, value=fontes_txt).alignment = Alignment(wrap_text=True)
        _style_row(ws1, row, 5, zebra=(idx % 2 == 1))
        row += 1
    row += 1

    # Auditoria de PV, PM, Defesa e CD de Magias
    row = _escrever_bloco_stat_calc(ws1, row, "3. PONTOS DE VIDA (PV MÁXIMO)", ficha.status.pv_calc, ficha.status.pv.maximo)
    row = _escrever_bloco_stat_calc(ws1, row, "4. PONTOS DE MANA (PM MÁXIMO)", ficha.status.pm_calc, ficha.status.pm.maximo)
    row = _escrever_bloco_stat_calc(ws1, row, "5. DEFESA", ficha.status.defesa_calc, ficha.status.defesa)
    if ficha.combate.cd_magias_calc or (ficha.combate.cd_magias or 0) > 0:
        row = _escrever_bloco_stat_calc(ws1, row, "6. CD DE MAGIAS", ficha.combate.cd_magias_calc, ficha.combate.cd_magias)

    _auto_fit(ws1, [34, 22, 18, 34, 42])
    ws1.freeze_panes = "A4"

    # ═══════════════════════════════════════════════════════════════
    # ABA 2: PERÍCIAS (COM FÓRMULAS =SUM)
    # ═══════════════════════════════════════════════════════════════
    ws2 = wb.create_sheet("Perícias")
    row = _set_banner(ws2, f"PERÍCIAS AUDITADAS — {cab.nome or 'Personagem'}", "Total = Metade do Nível + Atributo + Treino + Bônus Automáticos + Outros", 10)
    row = _set_headers(
        ws2,
        row,
        ["Perícia", "Treinada", "Atributo", "½ Nível", "Mod. Atrib.", "Treino", "Bônus Auto", "Outros", "Total (=SUM)", "Auditoria / Fontes"],
        ["left", "center", "center", "right", "right", "right", "right", "right", "right", "left"],
    )

    for idx, (p_nome, per) in enumerate(sorted((ficha.pericias or {}).items(), key=lambda x: x[0])):
        fontes_list = []
        if per.calculo and per.calculo.fontes:
            for f in per.calculo.fontes:
                if f.categoria not in ("Nível", "Atributo", "Treino"):
                    fontes_list.append(f"{f.fonte} ({f.valor:+d})")
        if per.fontes_bonus:
            for fb in per.fontes_bonus:
                if fb not in fontes_list:
                    fontes_list.append(fb)

        ws2.cell(row=row, column=1, value=p_nome).font = _FONT_BOLD if per.treino else _FONT_BODY
        ws2.cell(row=row, column=2, value="Sim" if per.treino else "Não").alignment = Alignment(horizontal="center")
        ws2.cell(row=row, column=3, value=(per.atributo_selecionado or "").upper()).alignment = Alignment(horizontal="center")

        for col_i, val in [(4, per.bonus_nivel), (5, per.atributo_valor), (6, per.treino), (7, per.bonus_automatico), (8, per.outros)]:
            cell = ws2.cell(row=row, column=col_i, value=val)
            cell.number_format = _FMT_SIGNED
            cell.alignment = Alignment(horizontal="right")

        c_tot = ws2.cell(row=row, column=9, value=f"=SUM(D{row}:H{row})")
        c_tot.number_format = _FMT_SIGNED
        c_tot.alignment = Alignment(horizontal="right")
        c_tot.font = _FONT_BOLD

        ws2.cell(row=row, column=10, value="; ".join(fontes_list) or "—").alignment = Alignment(wrap_text=True)
        _style_row(ws2, row, 10, zebra=(idx % 2 == 1))
        row += 1

    _auto_fit(ws2, [22, 10, 10, 10, 11, 10, 11, 10, 13, 52])
    ws2.freeze_panes = "A5"

    # ═══════════════════════════════════════════════════════════════
    # ABA 3: ATAQUES & MAGIAS
    # ═══════════════════════════════════════════════════════════════
    ws3 = wb.create_sheet("Ataques & Magias")
    row = _set_banner(ws3, f"ATAQUES & MAGIAS — {cab.nome or 'Personagem'}", "Auditoria completa de CD, dados de dano, bônus e grimório", 9)

    row = _set_section(ws3, row, "1. ATAQUES & MAGIAS OFENSIVAS", 9)
    row = _set_headers(
        ws3,
        row,
        ["Arma / Magia", "Bônus / CD", "Dano", "Crítico", "Tipo", "Alcance", "Teste", "Auditoria CD / Ataque", "Auditoria Dano / Efeitos"],
        ["left", "center", "center", "center", "center", "center", "center", "left", "left"],
    )
    for idx, atq in enumerate(ficha.combate.ataques or []):
        ws3.cell(row=row, column=1, value=atq.nome).font = _FONT_BOLD
        ws3.cell(row=row, column=2, value=atq.bonus_ataque).alignment = Alignment(horizontal="center")
        ws3.cell(row=row, column=3, value=atq.dano).alignment = Alignment(horizontal="center")
        ws3.cell(row=row, column=4, value=atq.critico).alignment = Alignment(horizontal="center")
        ws3.cell(row=row, column=5, value=atq.tipo).alignment = Alignment(horizontal="center")
        ws3.cell(row=row, column=6, value=atq.alcance).alignment = Alignment(horizontal="center")
        ws3.cell(row=row, column=7, value=atq.teste).alignment = Alignment(horizontal="center")
        ws3.cell(row=row, column=8, value=" | ".join(atq.cd_fontes or []) or (atq.especial or "—")).alignment = Alignment(wrap_text=True)
        ws3.cell(row=row, column=9, value=" | ".join(atq.dano_fontes or []) or (atq.especial or "—")).alignment = Alignment(wrap_text=True)
        _style_row(ws3, row, 9, zebra=(idx % 2 == 1))
        row += 1
    row += 2

    row = _set_section(ws3, row, f"2. GRIMÓRIO — MAGIAS CONHECIDAS ({len(ficha.combate.magias or [])})", 9)
    row = _set_headers(
        ws3,
        row,
        ["Magia", "Círculo", "Escola", "Tipo", "Custo PM", "Execução", "Alcance", "Resistência", "Descrição"],
        ["left", "center", "center", "center", "right", "center", "center", "center", "left"],
    )
    for idx, m in enumerate(ficha.combate.magias or []):
        ws3.cell(row=row, column=1, value=m.nome).font = _FONT_BOLD
        ws3.cell(row=row, column=2, value=f"{m.circulo}º").alignment = Alignment(horizontal="center")
        ws3.cell(row=row, column=3, value=m.escola or "—").alignment = Alignment(horizontal="center")
        ws3.cell(row=row, column=4, value=m.tipo or "—").alignment = Alignment(horizontal="center")
        cpm = ws3.cell(row=row, column=5, value=m.custo_pm)
        cpm.number_format = _FMT_INT
        cpm.alignment = Alignment(horizontal="right")
        ws3.cell(row=row, column=6, value=m.execucao or "—").alignment = Alignment(horizontal="center")
        ws3.cell(row=row, column=7, value=m.alcance or "—").alignment = Alignment(horizontal="center")
        ws3.cell(row=row, column=8, value=m.resistencia or "Nenhuma").alignment = Alignment(horizontal="center")
        ws3.cell(row=row, column=9, value=(m.descricao or "")[:400]).alignment = Alignment(wrap_text=True)
        _style_row(ws3, row, 9, zebra=(idx % 2 == 1))
        row += 1

    _auto_fit(ws3, [24, 12, 14, 10, 13, 12, 13, 36, 48])
    ws3.freeze_panes = "A5"

    # ═══════════════════════════════════════════════════════════════
    # ABA 4: HABILIDADES & PODERES
    # ═══════════════════════════════════════════════════════════════
    ws4 = wb.create_sheet("Habilidades & Poderes")
    row = _set_banner(ws4, f"HABILIDADES & PODERES — {cab.nome or 'Personagem'}", f"Total de {len(ficha.habilidades or [])} habilidades, poderes e traços com origem auditada", 6)
    row = _set_headers(
        ws4,
        row,
        ["Nome", "Tipo", "Origem / Fonte", "Custo PM", "Descrição", "Efeitos Mecânicos"],
        ["left", "center", "left", "center", "left", "left"],
    )
    for idx, h in enumerate(ficha.habilidades or []):
        ef = h.efeitos or {}
        custo_pm = ef.get("custo_pm", "—")
        ef_resumo = ", ".join(f"{k}={v}" for k, v in ef.items() if k != "nota") or "Passivo / Narrativo"
        ws4.cell(row=row, column=1, value=h.nome).font = _FONT_BOLD
        ws4.cell(row=row, column=2, value=h.tipo or "—").alignment = Alignment(horizontal="center")
        ws4.cell(row=row, column=3, value=h.fonte or "—")
        ws4.cell(row=row, column=4, value=f"{custo_pm} PM" if isinstance(custo_pm, (int, float)) else "—").alignment = Alignment(horizontal="center")
        ws4.cell(row=row, column=5, value=(h.descricao or "")[:500]).alignment = Alignment(wrap_text=True)
        ws4.cell(row=row, column=6, value=ef_resumo[:300]).alignment = Alignment(wrap_text=True)
        _style_row(ws4, row, 6, zebra=(idx % 2 == 1))
        row += 1

    _auto_fit(ws4, [26, 20, 24, 11, 56, 36])
    ws4.freeze_panes = "A5"

    # ═══════════════════════════════════════════════════════════════
    # ABA 5: INVENTÁRIO & SUPLEMENTOS
    # ═══════════════════════════════════════════════════════════════
    ws5 = wb.create_sheet("Inventário & Suplementos")
    row = _set_banner(ws5, f"INVENTÁRIO & SUPLEMENTOS — {cab.nome or 'Personagem'}", "Soma automática de carga, moedas, distinções, complicações e regras opcionais", 7)

    row = _set_section(ws5, row, "1. EQUIPAMENTOS & CARGA (COM FÓRMULAS EXCEL)", 7)
    row = _set_headers(
        ws5,
        row,
        ["Item", "Equipado", "Qtd", "Espaço Unit.", "Total Espaços (=C*D)", "Condição", "Notas / Melhorias"],
        ["left", "center", "right", "right", "right", "center", "left"],
    )
    first_item_row = row
    itens = ficha.inventario.equipamentos or []
    for idx, it in enumerate(itens):
        ws5.cell(row=row, column=1, value=it.nome).font = _FONT_BOLD if it.equipado else _FONT_BODY
        ws5.cell(row=row, column=2, value="Sim" if it.equipado else "Não").alignment = Alignment(horizontal="center")
        cq = ws5.cell(row=row, column=3, value=getattr(it, "qtd", 1))
        cq.number_format = _FMT_INT
        cq.alignment = Alignment(horizontal="right")
        ce = ws5.cell(row=row, column=4, value=getattr(it, "espaco", 0))
        ce.number_format = "0.0"
        ce.alignment = Alignment(horizontal="right")
        ctot = ws5.cell(row=row, column=5, value=f"=C{row}*D{row}")
        ctot.number_format = "0.0"
        ctot.alignment = Alignment(horizontal="right")
        ws5.cell(row=row, column=6, value=getattr(it, "condicao", None) or "Normal").alignment = Alignment(horizontal="center")
        melhorias_txt = ", ".join(getattr(it, "melhorias", None) or [])
        ws5.cell(row=row, column=7, value=melhorias_txt or (it.descricao or "—")[:180]).alignment = Alignment(wrap_text=True)
        _style_row(ws5, row, 7, zebra=(idx % 2 == 1))
        row += 1

    if not itens:
        ws5.cell(row=row, column=1, value="(Nenhum item no inventário)").font = _FONT_MUTED
        ws5.cell(row=row, column=5, value=0)
        _style_row(ws5, row, 7, zebra=False)
        row += 1

    last_item_row = row - 1
    carga_max = ficha.inventario.carga_maxima or 10
    ws5.cell(row=row, column=1, value="CARGA TOTAL").font = _FONT_TOTAL
    ws5.cell(row=row, column=4, value=f"Máx: {carga_max}").alignment = Alignment(horizontal="right")
    c_carga = ws5.cell(row=row, column=5, value=f"=SUM(E{first_item_row}:E{last_item_row})")
    c_carga.number_format = "0.0"
    c_carga.alignment = Alignment(horizontal="right")
    c_status = ws5.cell(row=row, column=6, value=f'=IF(E{row}>{carga_max},"SOBRECARGA","OK")')
    c_status.alignment = Alignment(horizontal="center")
    ws5.cell(row=row, column=7, value=f"Dinheiro: T$ {ficha.inventario.dinheiro.tp} | TO {ficha.inventario.dinheiro.to} | TC {ficha.inventario.dinheiro.tl}")
    _style_row(ws5, row, 7, total=True)
    row += 2

    # Suplementos
    row = _set_section(ws5, row, "2. DISTINÇÕES, COMPLICAÇÕES & REGRAS OPCIONAIS", 7)
    sup_rows = [
        ("Distinções", "; ".join(f"{d.nome} (Marca: {d.marca}; Poderes: {', '.join(d.poderes) or 'nenhum'})" for d in (ficha.distincoes or [])) or "Nenhuma"),
        ("Complicações", ", ".join(ficha.complicacoes or []) or "Nenhuma"),
        ("Papel no Grupo", ficha.papel_grupo or "Nenhum"),
        ("Objetivo Heroico", ficha.objetivo_heroico or "Nenhum"),
        ("Regras Opcionais Ativas", ", ".join(ficha.regras_opcionais_ativas or []) or "Nenhuma"),
    ]
    for idx, (lbl, val) in enumerate(sup_rows):
        ws5.cell(row=row, column=1, value=lbl).font = _FONT_BOLD
        ws5.merge_cells(start_row=row, start_column=2, end_row=row, end_column=7)
        ws5.cell(row=row, column=2, value=val).alignment = Alignment(wrap_text=True)
        _style_row(ws5, row, 7, zebra=(idx % 2 == 1))
        row += 1

    _auto_fit(ws5, [28, 11, 8, 13, 18, 15, 42])
    ws5.freeze_panes = "A5"

    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()
