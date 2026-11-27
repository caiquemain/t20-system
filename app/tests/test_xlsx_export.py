# -*- coding: utf-8 -*-
"""Testes da exportação de Ficha de Auditoria em Excel (.xlsx)."""
from io import BytesIO
from openpyxl import load_workbook

from src.models import Atributos, Cabecalho, ClasseInfo, DistincaoPersonagem, Item, Magia, Personagem
from src.regras import atualizar_ficha
from src.xlsx_export import gerar_xlsx_bytes


def test_gerar_xlsx_auditoria_5_abas_e_formulas():
    f = Personagem(
        cabecalho=Cabecalho(nome="Valen", raca="Eiradaan", origem="Acólito", deus="Tanna-Toh"),
        classes=[ClasseInfo(nome="Frade", nivel=6, primaria=True)],
        atributos_base=Atributos(forca=0, destreza=1, constituicao=2, inteligencia=2, sabedoria=4, carisma=1),
        distincoes=[DistincaoPersonagem(nome="Detetive de Tanna-Toh", admitido=True, poderes=[])],
        inventario={
            "equipamentos": [
                Item(nome="Sandálias", equipado=True, qtd=1, espaco=1),
                Item(nome="Cajado Inscrito Canônico", equipado=True, qtd=1, espaco=2),
            ]
        },
        combate={
            "magias": [
                Magia(
                    nome="Infligir Ferimentos",
                    circulo=1,
                    tipo="Divina",
                    escola="Necromancia",
                    custo_pm=1,
                    resistencia="Fortitude reduz à metade",
                )
            ]
        },
    )
    f = atualizar_ficha(f)

    data = gerar_xlsx_bytes(f)
    assert len(data) > 5000

    wb = load_workbook(BytesIO(data), data_only=False)
    assert wb.sheetnames == [
        "Resumo & Auditoria",
        "Perícias",
        "Ataques & Magias",
        "Habilidades & Poderes",
        "Inventário & Suplementos",
    ]

    # Confere fórmulas =SUM na aba Resumo & Auditoria
    ws1 = wb["Resumo & Auditoria"]
    valores_ws1 = [
        str(ws1.cell(r, c).value or "")
        for r in range(1, ws1.max_row + 1)
        for c in range(1, 6)
    ]
    assert any(v.startswith("=SUM(") for v in valores_ws1)
    assert any("Sandálias (+1 PM)" in v for v in valores_ws1)
    assert any("Canônico" in v for v in valores_ws1)
    assert any("RESUMO DE ATAQUES" in v for v in valores_ws1)
    assert any("Ataque Desarmado" in v for v in valores_ws1)

    # Confere fórmulas =SUM nas Perícias
    ws2 = wb["Perícias"]
    assert str(ws2.cell(5, 9).value).startswith("=SUM(D5:H5)")

    # Confere auditoria de Ataques (=SUM), CD e Dano em Ataques & Magias
    ws3 = wb["Ataques & Magias"]
    valores_ws3 = [
        str(ws3.cell(r, c).value or "")
        for r in range(1, ws3.max_row + 1)
        for c in range(1, 11)
    ]
    assert any(v.startswith("=SUM(C") for v in valores_ws3)
    assert any("Ataque Desarmado" in v for v in valores_ws3)
    assert any("Infligir Ferimentos" in v for v in valores_ws3)
    assert any("Base (Infligir Ferimentos)" in v for v in valores_ws3)

    # Confere fórmulas de carga (=C*D, =SUM, =IF) no Inventário
    ws5 = wb["Inventário & Suplementos"]
    valores_ws5 = [
        str(ws5.cell(r, c).value or "")
        for r in range(1, ws5.max_row + 1)
        for c in range(1, 8)
    ]
    assert any(v.startswith("=C") and "*D" in v for v in valores_ws5)
    assert any(v.startswith("=SUM(E") for v in valores_ws5)
    assert any(v.startswith("=IF(E") for v in valores_ws5)
