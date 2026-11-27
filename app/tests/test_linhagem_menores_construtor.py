# -*- coding: utf-8 -*-
"""Testes: Linhagem Abençoada (Feiticeiro), Guia de Deuses Menores e Manual de Criação de Ameaças."""
from src.dados_criacao_ameacas import (
    NDS_ORDENADOS,
    TABELAS_POR_PAPEL,
    gerar_ameaca_manual,
    obter_tabelas_construtor,
)
from src.dados_deuses_menores import (
    DADOS_DEUSES_MENORES,
    DADOS_PODERES_CONCEDIDOS_MENORES,
    FONTE_DEUSES_MENORES,
)
from src.models import Atributos, Cabecalho, ClasseInfo, Habilidade, Magia, Personagem
from src.regras import atualizar_ficha
from src.regras.custo_magia import calcular_custo_magia


def test_linhagem_abencoada_basica_aprimorada_superior():
    ficha = Personagem(
        cabecalho=Cabecalho(nome="Feiticeiro Abençoado", raca="Humano"),
        classes=[ClasseInfo(nome="Arcanista", nivel=11, primaria=True, subclasse="Feiticeiro")],
        atributos_base=Atributos(sabedoria=2, carisma=4),
        habilidades=[
            Habilidade(nome="Linhagem Abençoada", tipo="Poder de Classe", descricao="Linhagem Abençoada"),
            Habilidade(nome="Herança Aprimorada", tipo="Poder de Classe", descricao="Aprimorada"),
            Habilidade(nome="Herança Superior", tipo="Poder de Classe", descricao="Superior"),
        ],
    )
    ficha = atualizar_ficha(ficha)

    # Superior concede +1 Sabedoria (2 -> 3)
    assert ficha.atributos.sabedoria == 3

    # Aprimorada reduz em -1 PM magias divinas de círculo <= Sabedoria (3)
    m_div2 = Magia(nome="Curar Ferimentos", tipo="Divina", circulo=2, custo_pm=3, escola="Evocação")
    m_div4 = Magia(nome="Guardião Divino", tipo="Divina", circulo=4, custo_pm=10, escola="Convocação")
    assert calcular_custo_magia(ficha, m_div2).total == 2  # 3 - 1
    assert calcular_custo_magia(ficha, m_div4).total == 10  # 4 > Sab(3), sem redução


def test_guia_deuses_menores_catalogo():
    assert FONTE_DEUSES_MENORES == "Guia de Deuses Menores"
    assert len(DADOS_DEUSES_MENORES) == 60
    assert len(DADOS_PODERES_CONCEDIDOS_MENORES) >= 54
    assert "A Espada-Deus" in DADOS_DEUSES_MENORES
    assert "Akok" in DADOS_DEUSES_MENORES
    assert "Sckhar" in DADOS_DEUSES_MENORES
    assert "Zakharov" in DADOS_DEUSES_MENORES
    assert DADOS_DEUSES_MENORES["Akok"]["status_divino"] == 3


def test_manual_criacao_ameacas_tabelas_e_gerador():
    tabs = obter_tabelas_construtor()
    assert len(tabs["nds"]) == 24
    for papel in ("solo", "lacaio", "especial"):
        for nd in NDS_ORDENADOS:
            assert nd in TABELAS_POR_PAPEL[papel]

    # Confere valores exatos da Tabela 2-3 A (Solo ND 10: Ataque 29, Defesa 36, PV 400, CD 30)
    solo10 = gerar_ameaca_manual(
        nome="Dragão Jovem Custom",
        nd="10",
        papel="solo",
        tipo="Monstro",
        tamanho="Grande",
        res_forte="fortitude",
        res_media="reflexos",
        res_fraca="vontade",
    )
    assert solo10.defesa == 36
    assert solo10.pontos_de_vida == 400
    assert solo10.fortitude == 22
    assert solo10.reflexos == 16
    assert solo10.vontade == 10
    assert solo10.cd_magias == 30
    assert solo10.ataques[0].bonus_ataque == 29

    # Confere Tabela 2-3 C (Especial ND 6: Defesa 25, PV 168, CD 24, PM automático)
    esp6 = gerar_ameaca_manual(nome="Lich Aprendiz", nd="6", papel="especial", tipo="Morto-vivo")
    assert esp6.defesa == 25
    assert esp6.pontos_de_vida == 168
    assert esp6.cd_magias == 24
    assert esp6.pontos_de_mana is not None and esp6.pontos_de_mana >= 18
