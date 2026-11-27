"""Testes das regras adicionais de Ameaças de Arton (p. 374–375)."""
from src.models import Cabecalho, ClasseInfo, Inventario, Item, Personagem
from src.regras import atualizar_ficha
from src.regras.ameacas import (
    TABELA_ARMAS_NATURAIS,
    aplicar_condicao_item,
    avaliar_morte_ameaca,
    calcular_ataque_ameaca_sem_pericia,
    dano_arma_natural_por_tamanho,
    dano_desarmado_ameaca,
    determinar_atributo_chave_cd_ameaca,
    reparar_item,
)


def test_tabela_armas_naturais_e_passos_tamanho():
    assert len(TABELA_ARMAS_NATURAIS) == 12
    assert TABELA_ARMAS_NATURAIS["Cascos"] == "Impacto"
    assert TABELA_ARMAS_NATURAIS["Garra"] == "Corte"
    assert TABELA_ARMAS_NATURAIS["Mordida"] == "Perfuração"

    assert dano_arma_natural_por_tamanho("Minúsculo") == "1d4"
    assert dano_arma_natural_por_tamanho("Pequeno") == "1d6"
    assert dano_arma_natural_por_tamanho("Médio") == "1d6"
    assert dano_arma_natural_por_tamanho("Grande") == "1d8"
    assert dano_arma_natural_por_tamanho("Enorme") == "1d8"
    assert dano_arma_natural_por_tamanho("Colossal") == "1d10"

    # Exemplo do livro (p. 374-375): Grande +14 -> 1d4+14
    assert dano_desarmado_ameaca("Grande", 14) == "1d4+14"
    assert dano_desarmado_ameaca("Médio", 5) == "1d3+5"


def test_ataque_sem_pericia_cd_e_morte_ameaca():
    # Exemplo do livro (p. 374): ogro caçador ND 7, Des 0 -> +3
    assert calcular_ataque_ameaca_sem_pericia(7, 0) == 3

    attrs = {"forca": 5, "destreza": 2, "constituicao": 4, "inteligencia": -1, "sabedoria": 1, "carisma": 3}
    assert determinar_atributo_chave_cd_ameaca("atletica", attrs) == ("forca", 5)
    assert determinar_atributo_chave_cd_ameaca("fisiologica", attrs) == ("constituicao", 4)
    assert determinar_atributo_chave_cd_ameaca("controle", attrs) == ("carisma", 3)
    assert determinar_atributo_chave_cd_ameaca("magia_arcana", attrs) == ("carisma", 3)

    assert avaliar_morte_ameaca("lacaio", 0) == "morto"
    assert avaliar_morte_ameaca("solo", 0) == "50%_vivo"
    assert avaliar_morte_ameaca("especial", -12) == "50%_vivo"
    assert avaliar_morte_ameaca("lacaio", 0, dano_nao_letal=True) == "inconsciente"
    assert avaliar_morte_ameaca("solo", 5) == "ativo"


def test_condicoes_itens_avariado_destruido_e_motor():
    assert aplicar_condicao_item(None, "Avariado") == "Avariado"
    assert aplicar_condicao_item("Avariado", "Avariado") == "Destruído"
    assert aplicar_condicao_item("Destruído", "Avariado") == "Destruído"
    assert reparar_item() is None

    # Armadura e arma normais
    f_ok = Personagem(
        cabecalho=Cabecalho(nome="Valeros", raca="Humano", nivel_total=1),
        classes=[ClasseInfo(nome="Guerreiro", nivel=1, primaria=True)],
        inventario=Inventario(equipamentos=[
            Item(nome="Armadura de couro", equipado=True),
            Item(nome="Espada longa", equipado=True),
        ]),
    )
    atualizar_ficha(f_ok)
    ca_normal = f_ok.status.defesa.total
    atq_normal = next(a for a in f_ok.combate.ataques if a.nome == "Espada longa")
    assert atq_normal.bonus_ataque == "+0"

    # Avariado: -5 Defesa na armadura e -5 ataque na arma
    f_av = f_ok.model_copy(deep=True)
    f_av.inventario.equipamentos[0].condicao = "Avariado"
    f_av.inventario.equipamentos[1].condicao = "Avariado"
    atualizar_ficha(f_av)
    assert f_av.status.defesa.total == ca_normal - 5
    atq_av = next(a for a in f_av.combate.ataques if a.nome == "Espada longa")
    assert atq_av.bonus_ataque == "-5"
    assert "Avariado" in atq_av.especial

    # Destruído: armadura não dá bônus de Defesa e arma não gera ataque utilizável
    f_dest = f_ok.model_copy(deep=True)
    f_dest.inventario.equipamentos[0].condicao = "Destruído"
    f_dest.inventario.equipamentos[1].condicao = "Destruído"
    atualizar_ficha(f_dest)
    assert f_dest.status.defesa.total == 10
    assert not any(a.nome == "Espada longa" for a in f_dest.combate.ataques)


def test_equipamentos_e_itens_magicos_ameacas():
    from src.dados_equipamentos import (
        DADOS_ARMAS, DADOS_ARMADURAS, DADOS_GERAIS, DADOS_MELHORIAS, DADOS_MATERIAIS_ESPECIAIS,
    )
    from src.dados_equipamentos_ameacas import (
        DADOS_ITENS_MAGICOS_AMEACAS,
        RECURSOS_NATURAIS_PATAMAR,
        RECURSOS_NATURAIS_UNIDADES_TAMANHO,
        REGRA_OPCIONAL_LANCINANTE_REVISADO,
    )

    # Catálogos mesclados
    for arma in ("Porrete", "Zarabatana", "Gládio", "Arcabuz", "Bacamarte", "Pistola-punhal", "Lança de fogo", "Presa de serpente", "Shuriken", "Arpão"):
        assert arma in DADOS_ARMAS
    for arm in ("Armadura de ossos", "Veste de teia de aranha", "Armadura de quitina", "Escudo de couro"):
        assert arm in DADOS_ARMADURAS
    for item in ("Caixa de voz", "Manto pesado", "Ankh solar", "Pó azul", "Peçonha anciã", "Sashimi de kraken", "Bulette"):
        assert item in DADOS_GERAIS
    assert "Multifuncional" in DADOS_MELHORIAS
    assert "Penetrante" in DADOS_MELHORIAS
    for mat in ("Casco de monstro", "Couraça de kaiju", "Lanajuste", "Prata", "Quitina razza"):
        assert mat in DADOS_MATERIAIS_ESPECIAIS
    assert len(DADOS_ITENS_MAGICOS_AMEACAS) == 8
    assert RECURSOS_NATURAIS_PATAMAR["Lenda"]["valor"] == 2500
    assert RECURSOS_NATURAIS_UNIDADES_TAMANHO["Colossal"] == 5
    assert REGRA_OPCIONAL_LANCINANTE_REVISADO["id"] == "lancinante_revisado"

    # Armadura de quitina: pesada (+7 Def), mas NÃO reduz deslocamento (fica 9m)
    f_quit = Personagem(
        cabecalho=Cabecalho(nome="Quitino", raca="Humano", nivel_total=1),
        classes=[ClasseInfo(nome="Guerreiro", nivel=1, primaria=True)],
        inventario=Inventario(equipamentos=[Item(nome="Armadura de quitina", equipado=True)]),
    )
    atualizar_ficha(f_quit)
    assert f_quit.status.defesa.total == 17
    assert f_quit.status.deslocamento == 9
    assert f_quit.regras_opcionais_ativas == []

    # Veste de teia de aranha (+4 Def, +5 Furtividade) + Fragmento de filactério (+20 PM)
    f_teia = Personagem(
        cabecalho=Cabecalho(nome="Sombra", raca="Humano", nivel_total=1),
        classes=[ClasseInfo(nome="Ladino", nivel=1, primaria=True)],
        inventario=Inventario(equipamentos=[
            Item(nome="Veste de teia de aranha", equipado=True),
            Item(nome="Fragmento de filactério", equipado=True),
        ]),
    )
    atualizar_ficha(f_teia)
    assert f_teia.status.defesa.total == 14
    assert f_teia.pericias["Furtividade"].total >= 5
    assert f_teia.status.pm.maximo == 24  # Ladino nv1 (4 PM) + Fragmento (+20 PM)

    # Armadura de ossos (+3 Def, +1 Intimidação)
    f_ossos = Personagem(
        cabecalho=Cabecalho(nome="Ossudo", raca="Humano", nivel_total=1),
        classes=[ClasseInfo(nome="Guerreiro", nivel=1, primaria=True)],
        inventario=Inventario(equipamentos=[Item(nome="Armadura de ossos", equipado=True)]),
    )
    atualizar_ficha(f_ossos)
    assert f_ossos.status.defesa.total == 13
    assert f_ossos.pericias["Intimidação"].total >= 1


def test_magias_ameacas():
    from src.dados_magias import DADOS_MAGIAS
    from src.models import Magia

    esperadas = {
        "Açoite Flamejante": (1, 1, "2d6"),
        "Dardo Gélido": (1, 1, "2d6"),
        "Invocar Fagulha Elemental": (2, 3, None),
        "Jato Corrosivo": (1, 1, "2d6"),
        "Katana Celestial": (5, 15, "12d8"),
        "Momento de Tormenta": (2, 3, "6d4"),
        "Transformação em Dragão": (4, 10, "8d6+8"),
    }
    for nome, (circ, pm, formula) in esperadas.items():
        assert nome in DADOS_MAGIAS
        m = DADOS_MAGIAS[nome]
        assert m["fonte"] == "Ameaças de Arton"
        assert m["circulo"] == circ
        assert m["custo_pm"] == pm
        if formula:
            assert m["rolagem"]["formula"] == formula

    # Aprimoramentos opcionais de Conjurar Mortos-Vivos presentes
    aprim_cmv = DADOS_MAGIAS["Conjurar Mortos-Vivos"]["aprimoramentos"]
    assert any("soterrados" in a["descricao"].lower() for a in aprim_cmv)
    assert any("fúrias de tauron" in a["descricao"].lower() for a in aprim_cmv)
    assert any("guerreiros perpétuos" in a["descricao"].lower() for a in aprim_cmv)
    assert any("zumbis peçonha" in a["descricao"].lower() for a in aprim_cmv)

    # Magia de dano de Ameaças entra automaticamente em combate.ataques
    f = Personagem(
        cabecalho=Cabecalho(nome="Arcano", raca="Humano", nivel_total=1),
        classes=[ClasseInfo(nome="Arcanista", nivel=1, primaria=True, subclasse="Mago")],
    )
    f.combate.magias.append(Magia(**DADOS_MAGIAS["Dardo Gélido"]))
    atualizar_ficha(f)
    assert any(a.nome == "Dardo Gélido" and "2d6" in a.dano for a in f.combate.ataques)
