"""Testes das regras gerais do Capítulo 4 — Magia (T20 JdA, p.170–172)."""
import pytest

from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Magia, Inventario, Item
from src.regras import (
    atualizar_ficha,
    calcular_custo_magia,
    calcular_cd_concentracao,
    verificar_armadura_magia_arcana,
    pode_usar_aprimoramento,
    pode_anular_magia,
)
from src.regras.custo_magia import (
    CUSTO_POR_CIRCULO,
    ESCOLAS_MAGIA,
    obter_atributo_chave_magia,
)


def test_tabela_4_1_e_escolas_de_magia():
    assert CUSTO_POR_CIRCULO == {1: 1, 2: 3, 3: 6, 4: 10, 5: 15}
    assert len(ESCOLAS_MAGIA) == 8
    assert ESCOLAS_MAGIA["Encantamento"]["tipo_efeito"] == "mental"
    assert ESCOLAS_MAGIA["Ilusão"]["tipo_efeito"] == "mental"
    assert ESCOLAS_MAGIA["Necromancia"]["tipo_efeito"] == "trevas"
    assert set(ESCOLAS_MAGIA["Evocação"]["energias"]) == {
        "Ácido", "Eletricidade", "Fogo", "Frio", "Luz", "Essência"
    }


def test_cd_magias_e_atributo_chave_todas_as_classes():
    # Exemplo oficial do livro (p.172): Qareen Feiticeira 8º nível com Carisma 5 -> CD 19 (10 + 4 + 5)
    samira = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Samira", raca="Humano"),
        classes=[ClasseInfo(nome="Arcanista", nivel=8, primaria=True, subclasse="Feiticeiro")],
        atributos_base=Atributos(carisma=5),
    ))
    assert obter_atributo_chave_magia(samira) == "carisma"
    assert samira.combate.cd_magias == 19

    # Mago / Bruxo -> Inteligência
    mago = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Mago", raca="Humano"),
        classes=[ClasseInfo(nome="Arcanista", nivel=6, primaria=True, subclasse="Mago")],
        atributos_base=Atributos(inteligencia=4),
    ))
    assert obter_atributo_chave_magia(mago) == "inteligencia"
    assert mago.combate.cd_magias == 10 + 3 + 4

    # Clérigo -> Sabedoria
    clerigo = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Clérigo", raca="Humano", deus="Khalmyr"),
        classes=[ClasseInfo(nome="Clérigo", nivel=4, primaria=True)],
        atributos_base=Atributos(sabedoria=4),
    ))
    assert obter_atributo_chave_magia(clerigo) == "sabedoria"
    assert clerigo.combate.cd_magias == 10 + 2 + 4

    # Druida -> Sabedoria
    druida = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Druida", raca="Humano", deus="Allihanna"),
        classes=[ClasseInfo(nome="Druida", nivel=6, primaria=True)],
        atributos_base=Atributos(sabedoria=3),
    ))
    assert obter_atributo_chave_magia(druida) == "sabedoria"
    assert druida.combate.cd_magias == 10 + 3 + 3

    # Bardo -> Carisma
    bardo = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Bardo", raca="Humano"),
        classes=[ClasseInfo(nome="Bardo", nivel=6, primaria=True)],
        atributos_base=Atributos(carisma=4),
    ))
    assert obter_atributo_chave_magia(bardo) == "carisma"
    assert bardo.combate.cd_magias == 10 + 3 + 4


def test_concentracao_cds_oficiais():
    assert calcular_cd_concentracao(custo_pm=3, situacao="ferido", dano=18) == 18
    assert calcular_cd_concentracao(custo_pm=3, situacao="ruim") == 18
    assert calcular_cd_concentracao(custo_pm=6, situacao="terrivel") == 26
    with pytest.raises(ValueError):
        calcular_cd_concentracao(custo_pm=1, situacao="desconhecida")


def test_armaduras_e_magia_arcana_e_isencoes():
    bola = Magia(nome="Bola de Fogo", circulo=2, tipo="Arcana", escola="Evocação")
    cura = Magia(nome="Curar Ferimentos", circulo=1, tipo="Divina", escola="Evocação")
    racial = Magia(nome="Controlar Plantas", circulo=1, tipo="Arcana", fonte_origem="Racial: Amiga das Plantas", isento_armadura=True)

    mago_sem_armadura = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Mago", raca="Humano"),
        classes=[ClasseInfo(nome="Arcanista", nivel=5, primaria=True, subclasse="Mago")],
    ))
    assert verificar_armadura_magia_arcana(mago_sem_armadura, bola)["exige_teste"] is False

    mago_com_couro = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Mago", raca="Humano"),
        classes=[ClasseInfo(nome="Arcanista", nivel=5, primaria=True, subclasse="Mago")],
        inventario=Inventario(equipamentos=[Item(nome="Armadura de couro", equipado=True)]),
    ))
    res = verificar_armadura_magia_arcana(mago_com_couro, bola, custo_pm=5)
    assert res["exige_teste"] is True
    assert res["pericia"] == "Misticismo"
    assert res["cd"] == 25
    # Divina e Racial são isentas
    assert verificar_armadura_magia_arcana(mago_com_couro, cura)["exige_teste"] is False
    assert verificar_armadura_magia_arcana(mago_com_couro, racial)["exige_teste"] is False

    # Bardo com armadura leve é isento; com pesada precisa testar
    bardo_leve = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Bardo", raca="Humano"),
        classes=[ClasseInfo(nome="Bardo", nivel=5, primaria=True)],
        inventario=Inventario(equipamentos=[Item(nome="Armadura de couro", equipado=True)]),
    ))
    assert verificar_armadura_magia_arcana(bardo_leve, bola)["exige_teste"] is False

    bardo_pesada = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Bardo", raca="Humano"),
        classes=[ClasseInfo(nome="Bardo", nivel=5, primaria=True)],
        inventario=Inventario(equipamentos=[Item(nome="Cota de malha", equipado=True)]),
    ))
    assert verificar_armadura_magia_arcana(bardo_pesada, bola)["exige_teste"] is True


def test_aprimoramentos_limite_pm_truque_prerequisitos_e_contramagica():
    # Exemplo oficial (p.171): Arcanista 11º nível com Bola de Fogo (3 PM) + 8 PM de aprimoramento = 11 PM (limite 11)
    arcanista = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Mago", raca="Humano"),
        classes=[ClasseInfo(nome="Arcanista", nivel=11, primaria=True, subclasse="Mago")],
    ))
    bola = Magia(nome="Bola de Fogo", circulo=2, tipo="Arcana")
    calc = calcular_custo_magia(arcanista, bola, aprimoramentos_pm=10)
    assert calc.total == 11  # limitado ao nível 11
    # Delta negativo do limite registrado corretamente
    assert any(f.categoria == "Limite" and f.valor == -2 for f in calc.fontes)

    # Truque = 0 PM e ignora outros aprimoramentos
    calc_truque = calcular_custo_magia(arcanista, bola, aprimoramentos_pm=4, eh_truque=True)
    assert calc_truque.total == 0

    # Pré-requisitos de círculo em aprimoramentos
    assert pode_usar_aprimoramento(arcanista, bola, circulo_requerido=3) is True
    assert pode_usar_aprimoramento(arcanista, bola, circulo_requerido=4) is False
    magia_racial = Magia(nome="Luz", circulo=1, fonte_origem="Racial: Qareen", isento_armadura=True)
    assert pode_usar_aprimoramento(arcanista, magia_racial, circulo_requerido=2) is False

    # Anulando magias (Contramágica, p.172)
    luz = Magia(nome="Luz", circulo=1)
    escuridao = Magia(nome="Escuridão", circulo=1)
    dissipar = Magia(nome="Dissipar Magia", circulo=2)
    desejo = Magia(nome="Desejo", circulo=5)
    assert pode_anular_magia(bola, bola)["pode_anular"] is True
    assert pode_anular_magia(luz, escuridao)["pode_anular"] is True
    assert pode_anular_magia(bola, desejo)["pode_anular"] is False
    res_disp = pode_anular_magia(dissipar, desejo)
    assert res_disp["pode_anular"] is True
    assert res_disp["exige_teste_oposto"] is True
