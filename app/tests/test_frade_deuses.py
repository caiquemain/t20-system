# -*- coding: utf-8 -*-
"""Testes completos da classe Frade — Deuses de Arton (Cap. 1, p. 38–41)."""
from src.dados_classes import DADOS_CLASSES
from src.dados_frade_deuses import DADOS_HABILIDADES_FRADE, REGRAS_SACRARIOS_FRADE
from src.dados_habilidades_classe import DADOS_HABILIDADES_CLASSE
from src.dados_magias_conhecidas import REGRAS_MAGIAS_CONHECIDAS
from src.dados_progressao_magias import PROGRESSAO_CIRCULOS_POR_CLASSE
from src.dados_suplementos import FONTE_DEUSES, inferir_fonte
from src.models import Atributos, Cabecalho, ClasseInfo, Habilidade, Personagem
from src.regras import atualizar_ficha
from src.regras.ativaveis import ativar_habilidade, listar_habilidades_ativaveis
from src.regras.custo_magia import obter_atributo_chave_magia


def _frade(nivel: int = 1, sab: int = 4, con: int = 2, int_: int = 3) -> Personagem:
    return Personagem(
        cabecalho=Cabecalho(nome="Irmão Vallen", raca="Humano"),
        classes=[ClasseInfo(nome="Frade", nivel=nivel, primaria=True)],
        atributos_base=Atributos(
            forca=0, destreza=1, constituicao=con, inteligencia=int_, sabedoria=sab, carisma=2
        ),
    )


def test_catalogo_frade_completo_e_fonte_deuses():
    assert inferir_fonte("classe", "Frade", DADOS_CLASSES["Frade"]) == FONTE_DEUSES
    assert PROGRESSAO_CIRCULOS_POR_CLASSE["Frade"] == {1: 1, 5: 2, 9: 3, 13: 4, 17: 5}
    assert REGRAS_MAGIAS_CONHECIDAS["Frade"] == {"inicial": 3, "por_nivel": 1}

    entries = [v for v in DADOS_HABILIDADES_FRADE.values()]
    fixas = [v for v in entries if v["tipo"] == "Habilidade de Classe"]
    poderes = [v for v in entries if v["tipo"] == "Poder de Frade"]
    sacrarios = [v for v in poderes if v["nome"].startswith("Sacrário")]

    assert len(fixas) == 6
    assert len(poderes) == 29
    assert len(sacrarios) == 8
    assert REGRAS_SACRARIOS_FRADE["custo_pm"] == 3

    for k, v in DADOS_HABILIDADES_FRADE.items():
        assert k in DADOS_HABILIDADES_CLASSE
        assert v["fonte"] == FONTE_DEUSES
        assert v["efeitos"]

    for s in sacrarios:
        assert s["efeitos"]["sacrario"]["custo_pm"] == 3
        assert s["efeitos"]["sacrario"]["acao"] == "padrão"
        assert s["efeitos"]["sacrario"]["raio_m"] == 3


def test_frade_pv_pm_habilidades_fixas_cd_e_circulos():
    # Nível 1: PV = 12 + Con(2) = 14; PM = 6 + Sab(4) = 10
    f1 = atualizar_ficha(_frade(nivel=1, sab=4, con=2))
    assert f1.status.pv.maximo == 14
    assert f1.status.pm.maximo == 10
    assert obter_atributo_chave_magia(f1) == "sabedoria"
    assert f1.combate.circulo_maximo == 1
    assert f1.combate.cd_magias == 10 + 0 + 4  # 10 + floor(1/2) + Sab(4)
    nomes_nv1 = {h.nome for h in f1.habilidades}
    assert {"Devoto Fiel (Frade)", "Erudição", "Magias (Frade)"}.issubset(nomes_nv1)
    assert "Versiculário" not in nomes_nv1

    # Nível 5: ganha Versiculário (nv 2) + Dádiva da Fé (nv 5) + 2º círculo
    f5 = atualizar_ficha(_frade(nivel=5, sab=4, con=2))
    assert f5.status.pv.maximo == 14 + 4 * (3 + 2)  # 34
    assert f5.status.pm.maximo == 10 + 4 * 6        # 34
    assert f5.combate.circulo_maximo == 2
    assert f5.combate.cd_magias == 10 + 2 + 4       # 16
    nomes_nv5 = {h.nome for h in f5.habilidades}
    assert {"Versiculário", "Dádiva da Fé"}.issubset(nomes_nv5)

    # Nível 20: Solo Santificado + 5º círculo
    f20 = atualizar_ficha(_frade(nivel=20, sab=4, con=2))
    assert f20.combate.circulo_maximo == 5
    assert "Solo Santificado" in {h.nome for h in f20.habilidades}


def test_frade_sacrario_executavel_no_motor_ativaveis():
    f = _frade(nivel=5, sab=4)
    p = DADOS_HABILIDADES_FRADE["FRADE_SACRARIO_RESILIENCIA"]
    f.habilidades.append(Habilidade(nome=p["nome"], tipo=p["tipo"], descricao=p["descricao"], efeitos=dict(p["efeitos"])))
    f = atualizar_ficha(f)

    ativaveis = listar_habilidades_ativaveis(f)
    spec = next((a for a in ativaveis if a["nome"] == "Sacrário da Resiliência"), None)
    assert spec is not None
    assert spec["custo_pm"] == 3
    assert spec["acao"] == "padrão"
    assert spec["duracao"] == "cena"

    pm_antes = f.status.pm.atual
    res = ativar_habilidade(f, "Sacrário da Resiliência")
    assert res["sucesso"] is True
    assert f.status.pm.atual == pm_antes - 3
    assert any(b.origem == "Sacrário da Resiliência" for b in f.status.buffs)
