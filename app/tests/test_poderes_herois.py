# -*- coding: utf-8 -*-
"""Testes dos Novos Poderes de Classe, Gerais, Raça e Grupo — Heróis de Arton (Cap. 1, p. 54–95)."""
from collections import Counter

from src.dados_habilidades import HABILIDADES_GERAIS
from src.dados_habilidades_classe import DADOS_HABILIDADES_CLASSE
from src.dados_poderes_classe_herois import (
    DADOS_PODERES_CLASSE_HEROIS,
    NOVOS_EFEITOS_GOLPE_PESSOAL_HEROIS,
)
from src.dados_poderes_gerais_herois import (
    DADOS_PODERES_GERAIS_HEROIS,
    DADOS_PODERES_TORMENTA_HEROIS,
)
from src.dados_poderes_tormenta import DADOS_PODERES_TORMENTA
from src.dados_suplementos import FONTE_HEROIS
from src.models import Atributos, Cabecalho, ClasseInfo, Habilidade, Personagem
from src.regras import atualizar_ficha
from src.routers.dados import listar_poderes_categorizados


def _ficha(classe: str = "Guerreiro", nivel: int = 5, **attrs) -> Personagem:
    base = {
        "forca": 2,
        "destreza": 2,
        "constituicao": 2,
        "inteligencia": 2,
        "sabedoria": 2,
        "carisma": 2,
    }
    alias = {
        "for": "forca",
        "des": "destreza",
        "con": "constituicao",
        "int": "inteligencia",
        "sab": "sabedoria",
        "car": "carisma",
    }
    for k, v in attrs.items():
        base[alias.get(k, k)] = v
    return Personagem(
        cabecalho=Cabecalho(nome="Herói Teste", raca="Humano"),
        classes=[ClasseInfo(nome=classe, nivel=nivel, primaria=True)],
        atributos_base=Atributos(**base),
    )


def _add_hab(ficha: Personagem, dados: dict, fonte: str = "Poder") -> None:
    ficha.habilidades.append(
        Habilidade(
            nome=dados["nome"],
            tipo=dados["tipo"],
            descricao=dados.get("descricao", ""),
            efeitos=dict(dados.get("efeitos") or {}),
            fonte=fonte,
        )
    )


def test_contagens_catalogo_poderes_gerais_herois():
    por_tipo = Counter(v["tipo"] for v in DADOS_PODERES_GERAIS_HEROIS.values())
    assert por_tipo["Poder Geral (Combate)"] == 25
    assert por_tipo["Poder Geral (Destino)"] == 13
    assert por_tipo["Poder Geral (Magia)"] == 14
    assert por_tipo["Poder Geral (Raça)"] == 77
    assert por_tipo["Poder Geral (Grupo)"] == 20
    assert len(DADOS_PODERES_TORMENTA_HEROIS) == 6

    for d in DADOS_PODERES_GERAIS_HEROIS.values():
        assert d["fonte"] == FONTE_HEROIS
        assert d["efeitos"], f"Efeitos vazios em {d['nome']}"
    for d in DADOS_PODERES_TORMENTA_HEROIS.values():
        assert d["fonte"] == FONTE_HEROIS
        assert d["efeitos"], f"Efeitos vazios em {d['nome']}"
        assert d["nome"] in {v["nome"] for v in DADOS_PODERES_TORMENTA.values()}


def test_contagens_catalogo_poderes_classe_herois():
    por_classe = Counter(v["classe"] for v in DADOS_PODERES_CLASSE_HEROIS.values())
    assert por_classe == {
        "Arcanista": 20,
        "Bárbaro": 20,
        "Bardo": 20,
        "Bucaneiro": 21,
        "Caçador": 22,
        "Cavaleiro": 20,
        "Clérigo": 20,
        "Druida": 22,
        "Guerreiro": 21,
        "Inventor": 20,
        "Ladino": 20,
        "Lutador": 20,
        "Nobre": 20,
        "Paladino": 22,
    }
    assert len(DADOS_PODERES_CLASSE_HEROIS) == 288
    assert len(NOVOS_EFEITOS_GOLPE_PESSOAL_HEROIS) == 7

    for chave, d in DADOS_PODERES_CLASSE_HEROIS.items():
        assert chave in DADOS_HABILIDADES_CLASSE
        assert d["fonte"] == FONTE_HEROIS
        assert d["efeitos"], f"Efeitos vazios em {chave}"


def test_endpoint_poderes_inclui_magia_22_tormenta_28_raca_e_grupo():
    lista = listar_poderes_categorizados()
    por_cat = Counter(p["categoria"] for p in lista)
    assert por_cat["Magia"] == 22, f"Esperado 22 poderes de Magia (8 JdA + 14 Heróis), obtido {por_cat['Magia']}"
    assert por_cat["Tormenta"] == 28
    assert por_cat["Raça"] == 77
    assert por_cat["Grupo"] == 20

    nomes_magia = {p["nome"] for p in lista if p["categoria"] == "Magia"}
    for esperado in ("Magia Acelerada", "Foco em Magia", "Barreira Mística", "Encantar Itens Menores", "Celebrar Ritual"):
        assert esperado in nomes_magia


def test_efeitos_passivos_poderes_gerais_herois():
    base = atualizar_ficha(_ficha("Guerreiro", nivel=5, **{"for": 2, "con": 2}))

    f = _ficha("Guerreiro", nivel=5, **{"for": 2, "con": 2})
    _add_hab(f, HABILIDADES_GERAIS["HA_Grandao"])
    _add_hab(f, HABILIDADES_GERAIS["HA_Pose_Assustadora"])
    _add_hab(f, HABILIDADES_GERAIS["HA_Raca_Coracao_Pedra"])
    _add_hab(f, HABILIDADES_GERAIS["HA_Raca_Valentia_Nata"])
    f = atualizar_ficha(f)

    assert f.inventario.carga_maxima == base.inventario.carga_maxima + 5
    assert f.pericias["Intimidação"].total == base.pericias["Intimidação"].total + 2
    assert f.status.pv.maximo == base.status.pv.maximo + 5
    assert f.pericias["Iniciativa"].total == base.pericias["Iniciativa"].total + 5
    assert "Medo" in f.status.imunidades


def test_efeitos_passivos_poderes_classe_herois():
    base = atualizar_ficha(_ficha("Guerreiro", nivel=6, **{"int": 3}))

    f = _ficha("Guerreiro", nivel=6, **{"int": 3})
    _add_hab(f, DADOS_HABILIDADES_CLASSE["HA_GUE_Soldado_Infantaria"])
    _add_hab(f, DADOS_HABILIDADES_CLASSE["HA_GUE_Defesa_Estrategica"])
    f = atualizar_ficha(f)

    assert f.status.deslocamento == base.status.deslocamento + 3
    assert f.inventario.carga_maxima == base.inventario.carga_maxima + 6
    assert f.status.defesa.total == base.status.defesa.total + 3

    base_dru = atualizar_ficha(_ficha("Druida", nivel=4))
    f_dru = _ficha("Druida", nivel=4)
    _add_hab(f_dru, DADOS_HABILIDADES_CLASSE["HA_DRU_Xama_Mistico"])
    f_dru = atualizar_ficha(f_dru)
    assert f_dru.status.pm.maximo == base_dru.status.pm.maximo + 4

    base_pal = atualizar_ficha(_ficha("Paladino", nivel=5))
    f_pal = _ficha("Paladino", nivel=5)
    _add_hab(f_pal, DADOS_HABILIDADES_CLASSE["HA_PAL_Virtude_Paciencia"])
    f_pal = atualizar_ficha(f_pal)
    assert f_pal.status.pm.maximo == base_pal.status.pm.maximo + 1
