# -*- coding: utf-8 -*-
"""Testes das 36 Distinções — Heróis de Arton (Cap. 2, p. 104–211)."""
from src.dados_distincoes_herois import (
    DADOS_DISTINCOES_HEROIS,
    DADOS_PODERES_DISTINCAO_HEROIS,
    REGRAS_DISTINCOES_GERAIS,
)
from src.dados_suplementos import FONTE_HEROIS
from src.models import (
    Atributos,
    Cabecalho,
    ClasseInfo,
    DistincaoPersonagem,
    Item,
    Personagem,
)
from src.regras import atualizar_ficha
from src.routers.dados import get_dados_distincoes


def _ficha(nivel: int = 7, classe: str = "Guerreiro") -> Personagem:
    return Personagem(
        cabecalho=Cabecalho(nome="Herói Distinto", raca="Humano"),
        classes=[ClasseInfo(nome=classe, nivel=nivel, primaria=True)],
        atributos_base=Atributos(
            forca=2, destreza=2, constituicao=2, inteligencia=2, sabedoria=2, carisma=2
        ),
    )


def test_catalogo_completo_36_distincoes_e_185_poderes():
    assert REGRAS_DISTINCOES_GERAIS["nivel_minimo_poderes"] == 5
    assert len(DADOS_DISTINCOES_HEROIS) == 36
    assert len(DADOS_PODERES_DISTINCAO_HEROIS) == 185

    for nome, d in DADOS_DISTINCOES_HEROIS.items():
        assert d["nome"] == nome
        assert d["fonte"] == FONTE_HEROIS
        assert d["admissao"], f"Admissão vazia em {nome}"
        assert d["marca"]["nome"], f"Marca sem nome em {nome}"
        assert d["marca"]["descricao"], f"Marca sem descrição em {nome}"
        assert d["marca"]["efeitos"], f"Marca sem efeitos em {nome}"
        assert len(d["poderes"]) >= 5, f"Menos de 5 poderes em {nome}"
        for p in d["poderes"]:
            assert p["fonte"] == FONTE_HEROIS
            assert p["tipo"] == "Poder de Distinção"
            assert p["distincao"] == nome
            assert p["efeitos"], f"Poder sem efeitos: {nome}/{p['nome']}"


def test_endpoint_dados_distincoes():
    resp = get_dados_distincoes()
    assert resp["regras"]["nivel_minimo_poderes"] == 5
    assert len(resp["distincoes"]) == 59  # 36 Heróis de Arton + 23 Deuses de Arton
    assert "Cavaleiro do Corvo" in resp["distincoes"]
    assert "Mago da Ordem do Vazio" in resp["distincoes"]
    assert "Vigarista" in resp["distincoes"]


def test_distincao_nao_admitida_nao_injeta_habilidades():
    f = _ficha()
    f.distincoes = [
        DistincaoPersonagem(nome="Cavaleiro do Corvo", admitido=False, poderes=["A Qualquer Custo"])
    ]
    f = atualizar_ficha(f)
    habs_dist = [h for h in f.habilidades if (h.fonte or "").startswith("Distinção: ")]
    assert habs_dist == []


def test_marca_amazona_defesa_sem_e_com_armadura_pesada():
    base = atualizar_ficha(_ficha())

    f_sem = _ficha()
    f_sem.distincoes = [DistincaoPersonagem(nome="Amazona", admitido=True)]
    f_sem = atualizar_ficha(f_sem)
    assert f_sem.distincoes[0].marca == "Armadura das Amazonas"
    assert f_sem.status.defesa.total == base.status.defesa.total + 2

    f_com = _ficha()
    f_com.inventario.equipamentos.append(
        Item(nome="Armadura completa", tipo="Armadura", equipado=True)
    )
    base_pesada = _ficha()
    base_pesada.inventario.equipamentos.append(
        Item(nome="Armadura completa", tipo="Armadura", equipado=True)
    )
    base_pesada = atualizar_ficha(base_pesada)

    f_com.distincoes = [DistincaoPersonagem(nome="Amazona", admitido=True)]
    f_com = atualizar_ficha(f_com)
    assert f_com.status.defesa.total == base_pesada.status.defesa.total


def test_cavaleiro_feerico_pm_por_poder_e_limpeza_ao_remover():
    base = atualizar_ficha(_ficha(nivel=7, classe="Cavaleiro"))

    f = _ficha(nivel=7, classe="Cavaleiro")
    f.distincoes = [
        DistincaoPersonagem(
            nome="Cavaleiro Feérico",
            admitido=True,
            poderes=["Arte Élfica", "Arma da Floresta"],
        )
    ]
    f = atualizar_ficha(f)
    assert f.status.pm.maximo == base.status.pm.maximo + 2
    nomes_habs = {h.nome for h in f.habilidades}
    assert {"Conexão Feérica", "Arte Élfica", "Arma da Floresta"}.issubset(nomes_habs)

    # Remover a distinção deve limpar Marca e Poderes automaticamente
    f.distincoes = []
    f = atualizar_ficha(f)
    nomes_pos = {h.nome for h in f.habilidades}
    assert "Conexão Feérica" not in nomes_pos
    assert "Arte Élfica" not in nomes_pos
    assert f.status.pm.maximo == base.status.pm.maximo


def test_marcas_chapeu_preto_corvo_e_mutagenista():
    base = atualizar_ficha(_ficha())

    f = _ficha()
    f.distincoes = [
        DistincaoPersonagem(nome="Chapéu-Preto", admitido=True),
        DistincaoPersonagem(nome="Cavaleiro do Corvo", admitido=True),
        DistincaoPersonagem(nome="Mutagenista", admitido=True),
    ]
    f = atualizar_ficha(f)

    assert f.pericias["Intimidação"].total == base.pericias["Intimidação"].total + 2
    assert f.pericias["Diplomacia"].total == base.pericias["Diplomacia"].total - 2
    assert f.pericias["Fortitude"].total == base.pericias["Fortitude"].total + 2
    assert "Medo" in f.status.imunidades
