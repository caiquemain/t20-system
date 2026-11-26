"""Testes do Capítulo 8 — Recompensas & Itens Mágicos (T20 JdA, p.326–348)."""
from src.dados_recompensas import (
    TESOURO_MEDIO_POR_CENA,
    PRECO_ENCANTOS,
    ENCANTOS_ARMAS,
    ARMAS_ESPECIFICAS,
    ENCANTOS_ARMADURAS_ESCUDOS,
    ARMADURAS_ESCUDOS_ESPECIFICOS,
    POCOES_MAGICAS,
    ACESSORIOS_MAGICOS,
    ARTEFATOS,
    BARALHO_DO_CAOS_CARTAS,
)
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Inventario, Item
from src.regras import (
    atualizar_ficha,
    calcular_xp_desafio,
    calcular_fabricacao_consumivel,
    calcular_fabricacao_item_permanente,
    calcular_estatisticas_item_magico,
)


def test_catalogos_capitulo_8_completos():
    assert len(TESOURO_MEDIO_POR_CENA) == 20
    assert TESOURO_MEDIO_POR_CENA[1] == 300
    assert TESOURO_MEDIO_POR_CENA[20] == 72000
    assert len(PRECO_ENCANTOS) == 3
    assert len(ENCANTOS_ARMAS) == 28
    assert len(ARMAS_ESPECIFICAS) == 18
    assert len(ENCANTOS_ARMADURAS_ESCUDOS) == 25
    assert len(ARMADURAS_ESCUDOS_ESPECIFICOS) == 13
    assert len(POCOES_MAGICAS) == 38
    assert len(ACESSORIOS_MAGICOS) == 65
    assert len(ARTEFATOS) == 4
    assert len(BARALHO_DO_CAOS_CARTAS) == 22


def test_xp_desafios_oficiais():
    # Exemplo do livro (p.326): Ogro ND 5 para 4 aventureiros = 1.250 XP
    assert calcular_xp_desafio(nd=5, num_personagens=4) == 1250
    # XP parcial: empate (50%) e derrota (25%)
    assert calcular_xp_desafio(nd=5, num_personagens=4, resultado="empate") == 625
    assert calcular_xp_desafio(nd=5, num_personagens=4, resultado="derrota") == 312
    # Desafio irrelevante: ND <= nível do grupo - 5 -> 0 XP
    assert calcular_xp_desafio(nd=2, num_personagens=4, nivel_grupo=7) == 0
    assert calcular_xp_desafio(nd=3, num_personagens=4, nivel_grupo=7) == 750


def test_fabricacao_e_estatisticas_itens_magicos():
    # Poções / Pergaminhos (p.333)
    p1 = calcular_fabricacao_consumivel(1)
    assert p1["preco"] == 30 and p1["cd"] == 21
    p3 = calcular_fabricacao_consumivel(6)
    assert p3["preco"] == 1080 and p3["cd"] == 26

    # Itens Permanentes (exemplos p.334)
    esp_1 = calcular_fabricacao_item_permanente(preco_base=15, num_encantos=1)
    assert esp_1["preco"] == 18015
    assert esp_1["custo_fabricacao"] == 6005
    assert esp_1["cd"] == 30
    assert esp_1["sacrificio_pm"] == 1

    esp_max = calcular_fabricacao_item_permanente(preco_base=15, num_melhorias=4, num_encantos=3)
    assert esp_max["preco"] == 90015
    assert esp_max["custo_fabricacao"] == 30005
    assert esp_max["cd"] == 60
    assert esp_max["sacrificio_pm"] == 3

    # Destruindo Itens Mágicos (exemplo p.334: espada longa PV 5, RD 10, categoria Maior -> PV 45, RD 50, Res +20)
    stats = calcular_estatisticas_item_magico("Maior", pv_base=5, rd_base=10)
    assert stats["pv"] == 45
    assert stats["rd"] == 50
    assert stats["resistencia"] == 20


def test_acessorios_magicos_equipados_no_motor():
    base = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Arquimago", raca="Humano"),
        classes=[ClasseInfo(nome="Arcanista", nivel=9, primaria=True, subclasse="Mago")],
        atributos_base=Atributos(forca=1, destreza=2, constituicao=1, inteligencia=4),
    ))
    equipado = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Arquimago", raca="Humano"),
        classes=[ClasseInfo(nome="Arcanista", nivel=9, primaria=True, subclasse="Mago")],
        atributos_base=Atributos(forca=1, destreza=2, constituicao=1, inteligencia=4),
        inventario=Inventario(equipamentos=[
            Item(nome="Mochila de carga", equipado=True),
            Item(nome="Manoplas da força do ogro", equipado=True),   # +1 For
            Item(nome="Cinto da força do gigante", equipado=True),   # +2 For (substitui +1, não acumula)
            Item(nome="Anel da vitalidade", equipado=True),          # +10 PV
            Item(nome="Anel da energia", equipado=True),             # +5 PM
            Item(nome="Braceletes de ouro", equipado=True),          # +8 Defesa (sem armadura)
            Item(nome="Robe do arquimago", equipado=True),           # 9º nível (3º círculo): +8 Defesa, +4 resistências
            Item(nome="Botas velozes", equipado=True),               # +3m deslocamento
            Item(nome="Manto do morcego", equipado=True),            # +5 Furtividade
        ]),
    ))
    # Força: +2 (apenas o maior item, não +3)
    assert equipado.atributos.forca == base.atributos.forca + 2
    # Carga máxima: +4 pela Força (+2*2) +10 pela Mochila de carga = +14
    assert equipado.inventario.carga_maxima == base.inventario.carga_maxima + 14
    # PV +10, PM +5
    assert equipado.status.pv.maximo == base.status.pv.maximo + 10
    assert equipado.status.pm.maximo == base.status.pm.maximo + 5
    # Defesa: +8 (Braceletes de ouro, acumulam com itens mágicos) +8 (Robe do arquimago, 5 + 3º círculo) = +16
    assert equipado.status.defesa.total == base.status.defesa.total + 16
    # Resistências: +4 (metade do bônus na Defesa do Robe do arquimago)
    assert equipado.pericias["Fortitude"].total == base.pericias["Fortitude"].total + 4
    assert equipado.pericias["Reflexos"].total == base.pericias["Reflexos"].total + 4
    assert equipado.pericias["Vontade"].total == base.pericias["Vontade"].total + 4
    # Furtividade: +5 (Manto do morcego)
    assert equipado.pericias["Furtividade"].total == base.pericias["Furtividade"].total + 5
    # Deslocamento: +3m (Botas velozes)
    assert equipado.status.deslocamento == base.status.deslocamento + 3
