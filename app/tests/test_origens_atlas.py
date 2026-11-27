# -*- coding: utf-8 -*-
"""Testes das regras oficiais de Origens Regionais do Atlas de Arton (p. 470-479)."""
from src.dados_origens_atlas import DADOS_ORIGENS_ATLAS
from src.models import Atributos, Cabecalho, ClasseInfo, Item, Personagem
from src.regras import atualizar_ficha


def test_catalogo_origens_atlas_estrutura_regional():
    assert len(DADOS_ORIGENS_ATLAS) >= 60
    for nome, dados in DADOS_ORIGENS_ATLAS.items():
        assert dados["regional"] is True, nome
        assert dados["qtd_escolhas"] == 0, nome
        assert dados["beneficios_lista"] == [], nome
        assert dados["poder_fixo"] == f"Origem Regional: {nome}"


def test_anao_de_armas_beneficio_unico_e_limpa_escolhas_origem():
    f = Personagem(
        cabecalho=Cabecalho(nome="Thorek", raca="Anão", origem="Anão de Armas"),
        classes=[ClasseInfo(nome="Guerreiro", nivel=1, primaria=True)],
        atributos_base=Atributos(forca=3, destreza=1, constituicao=2),
        escolhas_origem=["Luta", "Vontade de Ferro"],  # lixo de origem básica anterior
        inventario={"equipamentos": [Item(nome="Machado de Batalha", equipado=True, qtd=1, espaco=1)]},
    )
    f = atualizar_ficha(f)

    # Origem regional limpa escolhas_origem (não escolhe 2 benefícios)
    assert f.escolhas_origem == []
    assert any(h.nome == "Origem Regional: Anão de Armas" for h in f.habilidades)
    assert f.pericias["Ofício (Armeiro)"].treino > 0
    assert (f.combate.bonus_dano_arma or {}).get("machado de batalha") == 2


def test_proficiencias_origens_atlas_escudos_e_fogo():
    f1 = Personagem(
        cabecalho=Cabecalho(nome="Kofi", raca="Humano", origem="Andarilho Ubaneri"),
        classes=[ClasseInfo(nome="Arcanista", nivel=1, primaria=True)],
    )
    f1 = atualizar_ficha(f1)
    assert "Escudos" in f1.status.proficiencias

    f2 = Personagem(
        cabecalho=Cabecalho(nome="Billy", raca="Humano", origem="Procurado: Vivo ou Morto"),
        classes=[ClasseInfo(nome="Bucaneiro", nivel=1, primaria=True)],
    )
    f2 = atualizar_ficha(f2)
    assert "Armas de Fogo" in f2.status.proficiencias


def test_recruta_arcano_soma_cd_magias():
    f_sem = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Mago A", raca="Humano", origem="Estudioso"),
        classes=[ClasseInfo(nome="Arcanista", nivel=1, subclasse="Mago", primaria=True)],
        atributos_base=Atributos(inteligencia=4),
    ))
    f_com = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Mago B", raca="Humano", origem="Recruta Arcano"),
        classes=[ClasseInfo(nome="Arcanista", nivel=1, subclasse="Mago", primaria=True)],
        atributos_base=Atributos(inteligencia=4),
    ))
    assert f_com.combate.cd_magias == f_sem.combate.cd_magias + 1
