"""Motor de equipamento (T20 JdA, Capítulo 3): catálogo, carga, ataques, defesa."""
import pytest

from src.models import Personagem, Item
from src.dados_equipamentos import DADOS_ARMAS, DADOS_ARMADURAS
from src.regras.inventario import (
    catalogo_do_item,
    sincronizar_carga,
    sincronizar_ataques_equipamento,
    calcular_penalidade_armadura,
)
from src.regras.status import calcular_defesa_e_deslocamento, calcular_modificador


def _ficha_com(*itens):
    p = Personagem()
    for it in itens:
        p.inventario.equipamentos.append(it)
    return p


def _set_des(ficha, mod):
    """atributos guardam o modificador direto (point-buy), ex.: destreza=2."""
    ficha.atributos.destreza = mod


# --- Catálogo ---

def test_catalogo_armas_completo():
    assert len(DADOS_ARMAS) >= 40
    t = DADOS_ARMAS["Tridente"]
    assert t["dano"] == "1d8"
    assert t["categoria"] == "Marcial"
    assert "versátil" in t["habilidades"]
    assert t["arremessavel"] is True


def test_catalogo_armaduras_completo():
    assert len(DADOS_ARMADURAS) == 12
    c = DADOS_ARMADURAS["Armadura completa"]
    assert c["bonus_defesa"] == 10
    assert c["penalidade_armadura"] == -5
    assert c["espacos"] == 5
    assert c["tipo_armadura"] == "Pesada"


def test_catalogo_do_item_desconhecido():
    assert catalogo_do_item("Item inexistente") is None


# --- Carga ---

def test_carga_limite_base():
    p = _ficha_com()
    sincronizar_carga(p)
    assert p.inventario.carga_maxima == 10
    assert p.inventario.carga_total == 0
    assert p.inventario.sobrecargado is False


def test_carga_soma_espacos_do_catalogo():
    p = _ficha_com(
        Item(nome="Espada longa", tipo="Arma", equipado=True),
        Item(nome="Armadura de couro", tipo="Armadura"),
    )
    sincronizar_carga(p)
    assert p.inventario.carga_total == 3  # 1 espada + 2 couro


def test_carga_multiplica_quantidade():
    p = _ficha_com(Item(nome="Adaga", tipo="Arma", qtd=3))
    sincronizar_carga(p)
    assert p.inventario.carga_total == 3


def test_sobrecarga_acima_do_limite():
    p = _ficha_com(
        Item(nome="Armadura completa", tipo="Armadura"),  # 5
        Item(nome="Montante", tipo="Arma"),               # 2
        Item(nome="Arco longo", tipo="Arma"),             # 2
        Item(nome="Besta pesada", tipo="Arma"),           # 2 = 11
    )
    sincronizar_carga(p)
    assert p.inventario.carga_total == 11
    assert p.inventario.sobrecargado is True


# --- Ataques de equipamento ---

def test_arma_empunhada_gera_ataque():
    p = _ficha_com(Item(nome="Espada longa", tipo="Arma", equipado=True))
    sincronizar_ataques_equipamento(p)
    eq = [a for a in p.combate.ataques if a.fonte == "Equipamento"]
    assert len(eq) == 1
    assert eq[0].teste == "Luta"
    assert eq[0].dano == "1d8"
    assert eq[0].tipo == "Corte"


def test_arma_guardada_nao_gera_ataque():
    p = _ficha_com(Item(nome="Espada longa", tipo="Arma", equipado=False))
    sincronizar_ataques_equipamento(p)
    assert not [a for a in p.combate.ataques if a.fonte == "Equipamento"]


def test_arma_de_distancia_usa_pontaria():
    p = _ficha_com(Item(nome="Arco curto", tipo="Arma", equipado=True))
    sincronizar_ataques_equipamento(p)
    a = [a for a in p.combate.ataques if a.fonte == "Equipamento"][0]
    assert a.teste == "Pontaria"
    assert a.alcance == "Médio"


def test_municao_nao_gera_ataque():
    p = _ficha_com(Item(nome="Flechas (20)", tipo="Munição", equipado=True))
    sincronizar_ataques_equipamento(p)
    assert not [a for a in p.combate.ataques if a.fonte == "Equipamento"]


def test_nao_proficiente_sofre_penalidade():
    p = _ficha_com(Item(nome="Espada longa", tipo="Arma", equipado=True))
    sincronizar_ataques_equipamento(p)
    a = [a for a in p.combate.ataques if a.fonte == "Equipamento"][0]
    assert "-5" in a.especial


def test_proficiente_nao_sofre_penalidade():
    p = _ficha_com(Item(nome="Adaga", tipo="Arma", equipado=True))
    p.proficiencias = ["Armas Simples"]
    sincronizar_ataques_equipamento(p)
    a = [a for a in p.combate.ataques if a.fonte == "Equipamento"][0]
    assert "-5" not in a.especial


def test_resincronizar_nao_duplica_ataques():
    p = _ficha_com(Item(nome="Espada longa", tipo="Arma", equipado=True))
    sincronizar_ataques_equipamento(p)
    sincronizar_ataques_equipamento(p)
    assert len([a for a in p.combate.ataques if a.fonte == "Equipamento"]) == 1


# --- Defesa ---

def test_defesa_com_armadura_leve():
    p = _ficha_com(Item(nome="Armadura de couro", tipo="Armadura", equipado=True))
    calcular_defesa_e_deslocamento(p)
    assert p.status.defesa_calc.total == 12
    fontes = {f.fonte: f.valor for f in p.status.defesa_calc.fontes}
    assert fontes["Equipamento: Armadura de couro"] == 2


def test_defesa_acumula_armadura_e_escudo():
    p = _ficha_com(
        Item(nome="Cota de malha", tipo="Armadura", equipado=True),
        Item(nome="Escudo pesado", tipo="Escudo", equipado=True),
    )
    calcular_defesa_e_deslocamento(p)
    assert p.status.defesa_calc.total == 18


def test_armadura_pesada_ignora_destreza():
    p = _ficha_com(Item(nome="Cota de malha", tipo="Armadura", equipado=True))
    _set_des(p, 2)
    calcular_defesa_e_deslocamento(p)
    assert not [f for f in p.status.defesa_calc.fontes if f.fonte == "Destreza"]


def test_armadura_leve_mantem_destreza():
    p = _ficha_com(Item(nome="Armadura de couro", tipo="Armadura", equipado=True))
    _set_des(p, 2)
    calcular_defesa_e_deslocamento(p)
    assert [f for f in p.status.defesa_calc.fontes if f.fonte == "Destreza"]


# --- Deslocamento ---

def test_pesada_reduz_deslocamento():
    p = _ficha_com(Item(nome="Cota de malha", tipo="Armadura", equipado=True))
    calcular_defesa_e_deslocamento(p)
    assert p.status.deslocamento_calc.total == 6


def test_sobrecarga_reduz_deslocamento():
    p = _ficha_com(
        Item(nome="Armadura completa", tipo="Armadura"),
        Item(nome="Montante", tipo="Arma"),
        Item(nome="Arco longo", tipo="Arma"),
        Item(nome="Besta pesada", tipo="Arma"),
    )
    sincronizar_carga(p)
    calcular_defesa_e_deslocamento(p)
    assert p.status.deslocamento_calc.total == 6


def test_imunidade_penalidade_mov_protege_deslocamento():
    p = _ficha_com(Item(nome="Cota de malha", tipo="Armadura", equipado=True))

    class _Hab:
        nome = "Passos Leves"
        tipo = "Poder"
        efeitos = {"imunidade_penalidade_mov": True}
        escolhas_aplicadas = {}

    p.habilidades = [_Hab()]
    calcular_defesa_e_deslocamento(p)
    assert p.status.deslocamento_calc.total == 9


# --- Penalidade de armadura ---

def test_penalidade_acumula_armadura_e_escudo():
    p = _ficha_com(
        Item(nome="Cota de malha", tipo="Armadura", equipado=True),
        Item(nome="Escudo pesado", tipo="Escudo", equipado=True),
    )
    assert calcular_penalidade_armadura(p) == 4


def test_penalidade_inclui_sobrecarga():
    p = _ficha_com(
        Item(nome="Armadura completa", tipo="Armadura", equipado=True),  # -5
        Item(nome="Montante", tipo="Arma"),
        Item(nome="Arco longo", tipo="Arma"),
        Item(nome="Besta pesada", tipo="Arma"),
    )
    sincronizar_carga(p)
    assert calcular_penalidade_armadura(p) == 10  # 5 armadura + 5 sobrecarga


def test_carga_reage_a_forca():
    """Regressão: carga máxima usava campo 'for' inexistente (modelo é 'forca')."""
    p = _ficha_com()
    p.atributos.forca = 2   # mod +2 -> limite 10 + 2*2 = 14
    sincronizar_carga(p)
    assert p.inventario.carga_maxima == 14
    p.atributos.forca = -1  # mod negativo: -1 por ponto -> 10 - 1 = 9
    sincronizar_carga(p)
    assert p.inventario.carga_maxima == 9
