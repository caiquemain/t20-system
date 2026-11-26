# -*- coding: utf-8 -*-
"""Testes do Capítulo 3 — Equipamento (T20 JdA p.140-151): Tabelas 3-1, 3-2, 3-3 e limites de carga."""
import pytest
from src.dados_equipamentos import DADOS_ARMAS, DINHEIRO_INICIAL_POR_NIVEL, ajustar_passo_dano
from src.models import Personagem, ClasseInfo, Cabecalho, Atributos, Item, Inventario, Dinheiro, Habilidade
from src.dados_habilidades import HABILIDADES_GERAIS
from src.regras import atualizar_ficha


def test_tabela_3_1_dinheiro_inicial():
    assert len(DINHEIRO_INICIAL_POR_NIVEL) == 20
    assert DINHEIRO_INICIAL_POR_NIVEL[1] == "4d6"
    assert DINHEIRO_INICIAL_POR_NIVEL[2] == 300
    assert DINHEIRO_INICIAL_POR_NIVEL[5] == 2000
    assert DINHEIRO_INICIAL_POR_NIVEL[10] == 13000
    assert DINHEIRO_INICIAL_POR_NIVEL[20] == 260000


@pytest.mark.parametrize("base,passos,esperado", [
    ("1d3", -2, "1"),
    ("1d4", -1, "1d3"),
    ("1d6", 1, "1d8"),
    ("1d8", 1, "1d10"),
    ("1d8", 2, "1d12"),
    ("1d8", 3, "3d6"),
    ("2d4", 1, "1d10"),
    ("2d6", 1, "3d6"),
    ("2d8", 1, "3d8"),
    ("2d8", 2, "4d8"),
    ("2d10", 1, "3d10"),
    ("4d10", 3, "4d12"),
])
def test_tabela_3_2_passos_de_dano(base, passos, esperado):
    assert ajustar_passo_dano(base, passos) == esperado


def test_tabela_3_3_armas_arremessaveis_com_alcance_curto():
    assert len(DADOS_ARMAS) == 44  # 40 armas + 4 munições
    for arma in ("Adaga", "Lança", "Machadinha", "Tridente"):
        assert DADOS_ARMAS[arma]["alcance"] == "Curto"
        assert DADOS_ARMAS[arma]["arremessavel"] is True


def test_carga_moedas_mochila_aventureiro_e_inventario_organizado():
    # For 2 -> limite base 14; Mochila de aventureiro (+2) = 16; 2500 moedas = 2 espaços
    f = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Aventureiro", raca="Humano"),
        classes=[ClasseInfo(nome="Guerreiro", nivel=1, primaria=True)],
        atributos_base=Atributos(forca=2, inteligencia=2),
        inventario=Inventario(
            dinheiro=Dinheiro(tp=2500),
            equipamentos=[
                Item(nome="Mochila de aventureiro", qtd=1, equipado=True),
                Item(nome="Ácido (frasco)", qtd=4),  # 4 * 0.5 = 2 espaços
            ],
        ),
    ))
    assert f.inventario.carga_maxima == 16
    assert f.inventario.carga_total == 4  # 2 (ácidos) + 2 (moedas)

    # Com Inventário Organizado: +Int(2) -> carga_maxima 18; 4 ácidos * 0.25 = 1 espaço -> total 3
    d_io = HABILIDADES_GERAIS["Inventario_Organizado"]
    f.habilidades.append(Habilidade(
        nome=d_io["nome"], tipo=d_io["tipo"], descricao=d_io["descricao"],
        fonte="Poder", efeitos=dict(d_io["efeitos"]),
    ))
    f = atualizar_ficha(f)
    assert f.inventario.carga_maxima == 18
    assert f.inventario.carga_total == 3
