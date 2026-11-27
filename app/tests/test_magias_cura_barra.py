# -*- coding: utf-8 -*-
"""Testes da Fase 0: Magias de Cura e PV Temporário na Barra de Ataque."""
from src.models import Atributos, Cabecalho, ClasseInfo, Habilidade, Magia, Personagem
from src.regras import atualizar_ficha


def test_curar_ferimentos_com_cura_gentil_na_barra_de_ataques():
    f = Personagem(
        cabecalho=Cabecalho(nome="Aria", raca="Humano", origem="Acólito", deus="Lena"),
        classes=[ClasseInfo(nome="Frade", nivel=1, primaria=True)],
        atributos_base=Atributos(sabedoria=4, carisma=3),
        habilidades=[
            Habilidade(nome="Cura Gentil", tipo="Poder Concedido", descricao="Soma Carisma em magias de cura.", fonte="Devoção: Lena")
        ],
        combate={
            "magias": [
                Magia(nome="Curar Ferimentos", circulo=1, tipo="Divina", escola="Evocação", custo_pm=1)
            ]
        },
    )
    f = atualizar_ficha(f)
    cura = next((a for a in f.combate.ataques if a.nome == "Curar Ferimentos"), None)
    assert cura is not None
    assert cura.tipo == "Cura"
    assert cura.bonus_ataque == "Cura"
    assert cura.dano == "2d8+2+3"
    assert any("Cura Gentil" in s for s in cura.dano_fontes)


def test_curar_ferimentos_estudante_colegio_real_e_vitalidade_fantasma():
    f = Personagem(
        cabecalho=Cabecalho(nome="Dr. Silas", raca="Humano", origem="Estudante do Colégio Real", deus=""),
        classes=[ClasseInfo(nome="Arcanista", nivel=1, subclasse="Mago", primaria=True)],
        atributos_base=Atributos(inteligencia=4),
        combate={
            "magias": [
                Magia(nome="Curar Ferimentos", circulo=1, tipo="Divina", escola="Evocação", custo_pm=1),
                Magia(nome="Vitalidade Fantasma", circulo=1, tipo="Arcana", escola="Necromancia", custo_pm=1),
            ]
        },
    )
    f = atualizar_ficha(f)

    cura = next((a for a in f.combate.ataques if a.nome == "Curar Ferimentos"), None)
    assert cura is not None
    # 2d8+2 + (2 dados * +2/dado = +4)
    assert cura.dano == "2d8+2+4"
    assert any("Estudante do Colégio Real" in s for s in cura.dano_fontes)

    pv_temp = next((a for a in f.combate.ataques if a.nome == "Vitalidade Fantasma"), None)
    assert pv_temp is not None
    assert pv_temp.tipo == "PV Temp"
    assert pv_temp.bonus_ataque == "PV Temp"
    assert pv_temp.dano == "2d10"
