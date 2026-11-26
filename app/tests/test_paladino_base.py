# -*- coding: utf-8 -*-
"""Testes de base do Paladino (T20 JdA p.81-84): PV/PM, perícias, habilidades fixas e mecânicas."""
import pytest
from src.models import Personagem, ClasseInfo, Cabecalho, Atributos
from src.dados_classes import DADOS_CLASSES
from src.regras import atualizar_ficha


def _paladino(nivel: int = 1, con: int = 2, car: int = 3, subclasse: str = "", condicoes=None) -> Personagem:
    ficha = Personagem(
        cabecalho=Cabecalho(nome="Lothar", raca="Humano"),
        classes=[ClasseInfo(nome="Paladino", nivel=nivel, primaria=True, subclasse=subclasse)],
        atributos_base=Atributos(forca=2, destreza=1, constituicao=con, inteligencia=0, sabedoria=1, carisma=car),
        condicoes_ativas=list(condicoes or []),
    )
    return atualizar_ficha(ficha)


def test_paladino_dados_classe_oficiais():
    dc = DADOS_CLASSES["Paladino"]
    assert dc["pv_inicial"] == 20
    assert dc["pv_nivel"] == 5
    assert dc["pm_inicial"] == 3
    assert dc["pm_nivel"] == 3
    assert dc["pm_atributo"] == "car"
    assert dc["pericias_iniciais"] == ["Luta", "Vontade"]
    assert dc["pericias_escolha"] == 2
    assert len(dc["pericias_lista"]) == 12
    assert set(dc["proficiencias"]) == {"Armas Marciais", "Armaduras Pesadas", "Escudos"}


def test_paladino_pv_pm_sem_duplicar_carisma():
    # Nível 1: PV = 20 + 2 = 22; PM = 3 + Car(3) = 6 (NÃO pode somar Car duas vezes!)
    f1 = _paladino(nivel=1, con=2, car=3)
    assert f1.status.pv.maximo == 22
    assert f1.status.pm.maximo == 6

    # Nível 5: PV = 22 + 4*(5+2) = 50; PM = 3 + 3 + 4*3 = 18
    f5 = _paladino(nivel=5, con=2, car=3)
    assert f5.status.pv.maximo == 50
    assert f5.status.pm.maximo == 18


def test_paladino_habilidades_fixas_por_nivel():
    f1 = _paladino(nivel=1)
    nomes1 = {h.nome for h in f1.habilidades}
    assert {"Abençoado", "Código do Herói", "Golpe Divino"}.issubset(nomes1)
    assert "Cura pelas Mãos" not in nomes1

    f2 = _paladino(nivel=2)
    assert "Cura pelas Mãos" in {h.nome for h in f2.habilidades}

    f3 = _paladino(nivel=3)
    assert "Aura Sagrada" in {h.nome for h in f3.habilidades}

    f5 = _paladino(nivel=5)
    assert "Bênção da Justiça" in {h.nome for h in f5.habilidades}

    f20 = _paladino(nivel=20)
    assert "Vingador Sagrado" in {h.nome for h in f20.habilidades}


@pytest.mark.parametrize("nivel,dados,custo_max", [
    (1, 1, 2),
    (4, 1, 2),
    (5, 2, 3),
    (9, 3, 4),
    (13, 4, 5),
    (17, 5, 6),
    (20, 5, 6),
])
def test_paladino_golpe_divino_escala(nivel, dados, custo_max):
    f = _paladino(nivel=nivel, car=4)
    gd = f.combate.paladino_calc["golpe_divino"]
    assert gd["dados_base"] == dados
    assert gd["dados_total"] == dados
    assert gd["tipo_dado"] == "d8"
    assert gd["formula"] == f"+{dados}d8"
    assert gd["bonus_ataque"] == 4
    assert gd["custo_base_pm"] == 2
    assert gd["custo_max_pm"] == custo_max


@pytest.mark.parametrize("nivel,degraus,formula,remove_cond", [
    (2, 1, "1d8+1", False),
    (5, 1, "1d8+1", False),
    (6, 2, "2d8+2", True),
    (10, 3, "3d8+3", True),
    (14, 4, "4d8+4", True),
    (18, 5, "5d8+5", True),
])
def test_paladino_cura_pelas_maos_escala(nivel, degraus, formula, remove_cond):
    f = _paladino(nivel=nivel, car=3)
    cm = f.combate.paladino_calc["cura_pelas_maos"]
    assert cm["degraus"] == degraus
    assert cm["formula_max"] == formula
    assert cm["alcance"] == "Corpo a corpo"
    assert cm["remove_condicoes"] is remove_cond
    assert cm["cd_mortos_vivos"] == 10 + (nivel // 2) + 3


def test_paladino_aura_sagrada_soma_carisma_nas_resistencias():
    f_off = _paladino(nivel=3, car=4, condicoes=[])
    f_on = _paladino(nivel=3, car=4, condicoes=["aura_sagrada"])

    for res in ("Fortitude", "Reflexos", "Vontade"):
        assert f_on.pericias[res].total == f_off.pericias[res].total + 4

    assert f_on.combate.paladino_calc["aura_sagrada"]["ativa"] is True
    assert f_on.combate.paladino_calc["aura_sagrada"]["raio_m"] == 9


def test_paladino_bencao_egide_sagrada_defesa_e_nivel_11():
    f_off = _paladino(nivel=5, car=4, subclasse="Égide Sagrada", condicoes=[])
    f_on = _paladino(nivel=5, car=4, subclasse="Égide Sagrada", condicoes=["egide_sagrada"])

    assert f_on.status.defesa.total == f_off.status.defesa.total + 4
    bj5 = f_on.combate.paladino_calc["bencao_justica"]
    assert bj5["escolha"] == "Égide Sagrada"
    assert bj5["egide_bonus_defesa"] == 4
    assert bj5["egide_reverter_magia"] is False

    f11 = _paladino(nivel=11, car=4, subclasse="Égide Sagrada")
    assert f11.combate.paladino_calc["bencao_justica"]["egide_reverter_magia"] is True


def test_paladino_bencao_montaria_sagrada_patamar():
    f5 = _paladino(nivel=5, car=4, subclasse="Montaria Sagrada", condicoes=["egide_sagrada"])
    f5_sem = _paladino(nivel=5, car=4, subclasse="Montaria Sagrada", condicoes=[])
    # Escolheu Montaria Sagrada -> não ganha bônus de Defesa da Égide
    assert f5.status.defesa.total == f5_sem.status.defesa.total
    assert f5.combate.paladino_calc["bencao_justica"]["montaria_patamar"] == "Veterano"

    f11 = _paladino(nivel=11, car=4, subclasse="Montaria Sagrada")
    assert f11.combate.paladino_calc["bencao_justica"]["montaria_patamar"] == "Mestre"


def test_paladino_vingador_sagrado_nv20():
    f_off = _paladino(nivel=20, car=5, condicoes=[])
    f_on = _paladino(nivel=20, car=5, condicoes=["vingador_sagrado"])

    assert "geral 20" not in f_off.status.rd
    assert "geral 20" in f_on.status.rd

    gd_on = f_on.combate.paladino_calc["golpe_divino"]
    assert gd_on["dados_base"] == 5
    assert gd_on["dados_total"] == 7
    assert gd_on["formula"] == "+7d8"
    assert gd_on["custo_base_pm"] == 1
    assert gd_on["custo_max_pm"] == 3
    assert f_on.combate.paladino_calc["vingador_sagrado"] == {"ativo": True, "voo_m": 18, "rd": 20}
