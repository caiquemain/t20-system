# -*- coding: utf-8 -*-
"""Testes dos Poderes Gerais (Combate, Destino, Magia), 64 Concedidos e 22 Tormenta (T20 JdA p.124-137)."""
import pytest
from src.dados_deuses import DADOS_DEUSES
from src.dados_habilidades import HABILIDADES_GERAIS
from src.dados_poderes_concedidos import DADOS_PODERES_CONCEDIDOS
from src.dados_poderes_tormenta import DADOS_PODERES_TORMENTA
from src.models import Personagem, ClasseInfo, Cabecalho, Atributos, Habilidade
from src.regras import atualizar_ficha


def _add(ficha: Personagem, dados: dict, fonte: str = "Poder"):
    ficha.habilidades.append(Habilidade(
        nome=dados["nome"],
        tipo=dados["tipo"],
        descricao=dados.get("descricao", ""),
        fonte=fonte,
        efeitos=dict(dados.get("efeitos") or {}),
    ))


def _ficha(nivel: int = 1, forca: int = 1, des: int = 1, con: int = 1, int_: int = 1, sab: int = 1, car: int = 3):
    return Personagem(
        cabecalho=Cabecalho(nome="Herói", raca="Humano"),
        classes=[ClasseInfo(nome="Guerreiro", nivel=nivel, primaria=True)],
        atributos_base=Atributos(
            forca=forca, destreza=des, constituicao=con,
            inteligencia=int_, sabedoria=sab, carisma=car,
        ),
    )


def test_catalogos_completos_e_todos_com_efeitos():
    assert len(DADOS_PODERES_CONCEDIDOS) == 72
    assert all(v.get("efeitos") for v in DADOS_PODERES_CONCEDIDOS.values())

    # Todo poder listado nos 20 deuses existe em DADOS_PODERES_CONCEDIDOS
    for nome_deus, dados_deus in DADOS_DEUSES.items():
        for p in dados_deus["poderes"]:
            assert p in DADOS_PODERES_CONCEDIDOS, f"Poder '{p}' de {nome_deus} ausente em DADOS_PODERES_CONCEDIDOS"

    assert len(DADOS_PODERES_TORMENTA) == 22
    assert all(v.get("efeitos") for v in DADOS_PODERES_TORMENTA.values())

    for tipo in ("Poder Geral (Combate)", "Poder Geral (Destino)", "Poder Geral (Magia)"):
        sem = [k for k, v in HABILIDADES_GERAIS.items() if v.get("tipo") == tipo and not v.get("efeitos")]
        assert sem == [], f"{tipo} com efeitos vazios: {sem}"


def test_poderes_concedidos_dom_da_esperanca_e_bencao_do_mana():
    f_sem = atualizar_ficha(_ficha(nivel=5, con=0, sab=4))
    f_com = _ficha(nivel=5, con=0, sab=4)
    _add(f_com, DADOS_PODERES_CONCEDIDOS["Dom da Esperança"], "Devoção: Marah")
    _add(f_com, DADOS_PODERES_CONCEDIDOS["Bênção do Mana"], "Devoção: Wynna")
    f_com = atualizar_ficha(f_com)

    # PV usa Sab(4) em vez de Con(0) em todos os 5 níveis -> +20 PV
    assert f_com.status.pv.maximo == f_sem.status.pv.maximo + 20
    assert {"Alquebrado", "Esmorecido", "Frustrado"}.issubset(set(f_com.status.imunidades))
    # Bênção do Mana: níveis ímpares até 5 (1, 3, 5) -> +3 PM
    assert f_com.status.pm.maximo == f_sem.status.pm.maximo + 3


def test_poderes_concedidos_escamas_descanso_coragem_rd_e_pericias():
    f_sem = atualizar_ficha(_ficha(nivel=6))
    f_com = _ficha(nivel=6)
    _add(f_com, DADOS_PODERES_CONCEDIDOS["Escamas Dracônicas"])
    _add(f_com, DADOS_PODERES_CONCEDIDOS["Descanso Natural"])
    _add(f_com, DADOS_PODERES_CONCEDIDOS["Coragem Total"])
    _add(f_com, DADOS_PODERES_CONCEDIDOS["Habitante do Deserto"])
    _add(f_com, DADOS_PODERES_CONCEDIDOS["Fulgor Solar"])
    _add(f_com, DADOS_PODERES_CONCEDIDOS["Astúcia da Serpente"])
    f_com = atualizar_ficha(f_com)

    assert f_com.status.defesa.total == f_sem.status.defesa.total + 2
    assert f_com.pericias["Fortitude"].total == f_sem.pericias["Fortitude"].total + 2
    assert f_com.pericias["Enganação"].total == f_sem.pericias["Enganação"].total + 2
    assert f_com.status.descanso_calc["ruim"] == 12  # Confortável = 2 * 6
    assert "Medo" in f_com.status.imunidades
    assert {"Fogo 10", "Frio 5", "Trevas 5"}.issubset(set(f_com.status.rd))


@pytest.mark.parametrize("qtd,perda_esperada,def_esperada,rd_esperada", [
    (1, 1, 1, 2),
    (2, 1, 1, 2),
    (3, 2, 2, 4),
    (4, 2, 2, 4),
    (5, 3, 3, 6),
])
def test_tormenta_perda_carisma_e_escala_oficial(qtd, perda_esperada, def_esperada, rd_esperada):
    chaves = ["Carapaca", "Pele_Corrompida", "Antenas", "Olhos_Vermelhos", "Dentes_Afiados"][:qtd]
    f_base = atualizar_ficha(_ficha(car=4))
    f = _ficha(car=4)
    for ch in chaves:
        _add(f, DADOS_PODERES_TORMENTA[ch])
    f = atualizar_ficha(f)

    assert f.atributos.carisma == 4 - perda_esperada
    assert f.status.defesa.total == f_base.status.defesa.total + def_esperada
    if qtd >= 2:
        assert f"Fogo {rd_esperada}" in f.status.rd
    if qtd >= 3:
        assert f.pericias["Percepção"].total == f_base.pericias["Percepção"].total + def_esperada


def test_afinidade_com_a_tormenta_isenta_primeiro_poder():
    f1 = _ficha(car=4)
    _add(f1, DADOS_PODERES_CONCEDIDOS["Afinidade com a Tormenta"])
    _add(f1, DADOS_PODERES_TORMENTA["Carapaca"])
    f1 = atualizar_ficha(f1)
    assert f1.atributos.carisma == 4  # 1º poder não conta!

    f2 = _ficha(car=4)
    _add(f2, DADOS_PODERES_CONCEDIDOS["Afinidade com a Tormenta"])
    _add(f2, DADOS_PODERES_TORMENTA["Carapaca"])
    _add(f2, DADOS_PODERES_TORMENTA["Antenas"])
    f2 = atualizar_ficha(f2)
    assert f2.atributos.carisma == 3  # efetivo = 1 -> -1 Car


def test_vontade_de_ferro_e_inventario_organizado():
    f_sem = atualizar_ficha(_ficha(nivel=6, int_=3))
    f_com = _ficha(nivel=6, int_=3)
    _add(f_com, HABILIDADES_GERAIS["Vontade_Ferro"])
    _add(f_com, HABILIDADES_GERAIS["Inventario_Organizado"])
    f_com = atualizar_ficha(f_com)

    assert f_com.status.pm.maximo == f_sem.status.pm.maximo + 3  # 6 // 2 = +3 PM
    assert f_com.pericias["Vontade"].total == f_sem.pericias["Vontade"].total + 2
    assert f_com.inventario.carga_maxima == f_sem.inventario.carga_maxima + 3  # +Int(3)
