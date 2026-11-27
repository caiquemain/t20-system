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


def test_catalogo_198_magias_tabela_4_1_e_ataques_magicos():
    from src.dados_magias import DADOS_MAGIAS
    basicas = {k: v for k, v in DADOS_MAGIAS.items() if not v.get("fonte")}
    assert len(basicas) == 198
    assert len(DADOS_MAGIAS) >= 198
    for nome, m in DADOS_MAGIAS.items():
        assert m["custo_pm"] == CUSTO_POR_CIRCULO[m["circulo"]], f"{nome}: custo_pm inválido"
    com_rolagem = [k for k, m in DADOS_MAGIAS.items() if m.get("rolagem")]
    assert len(com_rolagem) >= 46

    # Magias de dano entram automaticamente em combate.ataques; cura/utilidade não
    mago = Personagem(
        cabecalho=Cabecalho(nome="Mago", raca="Humano"),
        classes=[ClasseInfo(nome="Arcanista", nivel=5, primaria=True, subclasse="Mago")],
        atributos_base=Atributos(inteligencia=4),
    )
    mago.combate.magias.extend([
        Magia(nome="Bola de Fogo", circulo=2, tipo="Arcana", escola="Evocação", alcance="Médio", resistencia="Reflexos reduz à metade"),
        Magia(nome="Seta Infalível de Talude", circulo=1, tipo="Arcana", escola="Evocação", alcance="Médio", resistencia=""),
        Magia(nome="Curar Ferimentos", circulo=1, tipo="Divina", escola="Evocação", alcance="Toque", resistencia=""),
    ])
    mago = atualizar_ficha(mago)

    nomes_atq = {a.nome: a for a in mago.combate.ataques}
    assert "Bola de Fogo" in nomes_atq
    assert nomes_atq["Bola de Fogo"].dano == "6d6"
    assert nomes_atq["Bola de Fogo"].tipo == "Fogo"
    assert nomes_atq["Bola de Fogo"].bonus_ataque == f"CD {mago.combate.cd_magias}"
    assert nomes_atq["Bola de Fogo"].teste == "Reflexos"

    assert "Seta Infalível de Talude" in nomes_atq
    assert nomes_atq["Seta Infalível de Talude"].bonus_ataque == "Auto"
    assert nomes_atq["Seta Infalível de Talude"].dano == "2d4+2"

    # Curar Ferimentos agora entra na barra de ataques como Cura e mantém rolagem no modal
    assert "Curar Ferimentos" in nomes_atq
    assert nomes_atq["Curar Ferimentos"].tipo == "Cura"
    assert nomes_atq["Curar Ferimentos"].dano == "2d8+2"
    cura = next(m for m in mago.combate.magias if m.nome == "Curar Ferimentos")
    assert cura.rolagem == {"formula": "2d8+2", "tipo": "cura", "tipo_dano": "Luz"}

    # Idempotência ao esquecer a magia
    mago.combate.magias = [m for m in mago.combate.magias if m.nome != "Bola de Fogo"]
    mago = atualizar_ficha(mago)
    assert all(a.nome != "Bola de Fogo" for a in mago.combate.ataques)


def test_magia_ilimitada_celebrar_ritual_foco_e_itens_magicos():
    from src.models import Habilidade
    from src.regras import calcular_limite_pm_magia

    # Arcanista 3º nível com INT 4: limite padrão = 3 PM
    mago = Personagem(
        cabecalho=Cabecalho(nome="Mago", raca="Humano"),
        classes=[ClasseInfo(nome="Arcanista", nivel=3, primaria=True, subclasse="Mago")],
        atributos_base=Atributos(inteligencia=4),
    )
    mago = atualizar_ficha(mago)
    assert mago.combate.limite_pm_magia == 3
    cd_base = mago.combate.cd_magias

    # Com Magia Ilimitada: limite = 3 + 4 (INT) = 7 PM
    mago.habilidades.append(Habilidade(
        nome="Magia Ilimitada",
        tipo="Poder Geral (Magia)",
        descricao="Soma seu atributo-chave ao limite de PM.",
        efeitos={"limite_pm_soma_atributo_chave": True},
    ))
    mago = atualizar_ficha(mago)
    assert mago.combate.limite_pm_magia == 7
    bola = Magia(nome="Bola de Fogo", circulo=2, tipo="Arcana", escola="Evocação")
    # 3 PM base + 4 PM aprimoramento = 7 PM (permitido graças a Magia Ilimitada!)
    assert calcular_custo_magia(mago, bola, aprimoramentos_pm=4).total == 7

    # Com Celebrar Ritual: dobra limite em ritual -> 14 PM
    mago.habilidades.append(Habilidade(
        nome="Celebrar Ritual",
        tipo="Poder Geral (Magia)",
        descricao="Dobra limite de PM como ritual.",
        efeitos={"celebrar_ritual_dobra_limite_pm": True},
    ))
    mago = atualizar_ficha(mago)
    assert mago.combate.limite_pm_ritual == 14
    assert calcular_limite_pm_magia(mago, como_ritual=True)["limite"] == 14
    assert calcular_custo_magia(mago, bola, aprimoramentos_pm=10, como_ritual=True).total == 13

    # Com Foco em Magia (Bola de Fogo) + Cajado do poder: -2 PM em Bola de Fogo e +3 CD
    mago.habilidades.append(Habilidade(
        nome="Foco em Magia",
        tipo="Poder Geral (Magia)",
        descricao="-1 PM na magia escolhida.",
        efeitos={"foco_em_magia": True},
        escolhas_aplicadas={"magia": "Bola de Fogo"},
    ))
    mago.inventario.equipamentos.append(Item(nome="Cajado do poder", equipado=True))
    mago = atualizar_ficha(mago)
    assert mago.combate.cd_magias == cd_base + 3
    assert calcular_custo_magia(mago, bola).total == 1  # 3 - 1 (Foco) - 1 (Cajado) = 1 PM


