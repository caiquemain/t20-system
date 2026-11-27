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
    armas_basicas = {k: v for k, v in DADOS_ARMAS.items() if not v.get("fonte")}
    assert len(armas_basicas) == 44  # 40 armas + 4 munições do T20 JdA
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


def test_tabelas_3_7_3_8_3_9_melhorias_e_materiais():
    from src.dados_equipamentos import (
        DADOS_ARMADURAS, PRECO_MELHORIAS, DADOS_MELHORIAS, DADOS_MATERIAIS_ESPECIAIS,
    )
    assert len([k for k, v in DADOS_ARMADURAS.items() if not v.get("fonte")]) == 12
    assert PRECO_MELHORIAS[1] == {"aumento_preco": 300, "aumento_cd": 5}
    assert PRECO_MELHORIAS[4] == {"aumento_preco": 18000, "aumento_cd": 20}
    assert len([k for k, v in DADOS_MELHORIAS.items() if not v.get("fonte")]) == 29
    materiais_basicos = {k for k, v in DADOS_MATERIAIS_ESPECIAIS.items() if not v.get("fonte")}
    assert materiais_basicos == {
        "Aço-Rubi", "Adamante", "Gelo Eterno", "Madeira Tollon", "Matéria Vermelha", "Mitral"
    }
    assert DADOS_MATERIAIS_ESPECIAIS["Adamante"]["precos"]["Armadura Pesada"] == 18000
    assert DADOS_MATERIAIS_ESPECIAIS["Mitral"]["precos"]["Armadura Pesada"] == 12000


def test_bonus_itens_equipados_acolchoada_simbolo_vestuario_chapeu_casaco():
    f_sem = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Mago", raca="Humano", deus="Wynna"),
        classes=[ClasseInfo(nome="Arcanista", nivel=1, primaria=True, subclasse="Mago")],
        atributos_base=Atributos(inteligencia=3, destreza=2, constituicao=1),
    ))
    f_com = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Mago", raca="Humano", deus="Wynna"),
        classes=[ClasseInfo(nome="Arcanista", nivel=1, primaria=True, subclasse="Mago")],
        atributos_base=Atributos(inteligencia=3, destreza=2, constituicao=1),
        inventario=Inventario(equipamentos=[
            Item(nome="Símbolo sagrado", equipado=True),
            Item(nome="Chapéu arcano", equipado=True),
            Item(nome="Robe místico", equipado=True),
            Item(nome="Sapatos de camurça", equipado=True),
        ]),
    ))
    # Símbolo sagrado (+1 Fort/Ref/Von)
    assert f_com.pericias["Fortitude"].total == f_sem.pericias["Fortitude"].total + 1
    assert f_com.pericias["Reflexos"].total == f_sem.pericias["Reflexos"].total + 1
    assert f_com.pericias["Vontade"].total == f_sem.pericias["Vontade"].total + 1
    # Robe místico (+1 Misticismo) e Sapatos de camurça (+1 Acrobacia)
    assert f_com.pericias["Misticismo"].total == f_sem.pericias["Misticismo"].total + 1
    assert f_com.pericias["Acrobacia"].total == f_sem.pericias["Acrobacia"].total + 1
    # Chapéu arcano (+1 PM para Arcanista)
    assert f_com.status.pm.maximo == f_sem.status.pm.maximo + 1

    # Guerreiro proficiente com Armadura acolchoada (+2 Fort) e Casaco longo (penalidade 2)
    g_sem = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Soldado", raca="Humano"),
        classes=[ClasseInfo(nome="Guerreiro", nivel=1, primaria=True)],
        atributos_base=Atributos(forca=2, destreza=2, constituicao=1),
    ))
    g_com = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Soldado", raca="Humano"),
        classes=[ClasseInfo(nome="Guerreiro", nivel=1, primaria=True)],
        atributos_base=Atributos(forca=2, destreza=2, constituicao=1),
        inventario=Inventario(equipamentos=[
            Item(nome="Armadura acolchoada", equipado=True),
            Item(nome="Casaco longo", equipado=True),
        ]),
    ))
    assert g_com.pericias["Fortitude"].total == g_sem.pericias["Fortitude"].total + 2
    assert g_com.status.penalidade_armadura == 2
    assert g_com.pericias["Acrobacia"].total == g_sem.pericias["Acrobacia"].total - 2


