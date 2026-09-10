from src.models import Magia, ClasseInfo, Habilidade
from src.regras.magias import (
    calcular_circulo_maximo,
    calcular_circulo_maximo_ficha,
    validar_circulos_magias,
    aplicar_poderes_arcanista,
    calcular_limite_magias_conhecidas,
)
from src.regras.status import calcular_pv_pm


def test_progressao_arcanista():
    assert calcular_circulo_maximo("Arcanista", 1) == 1
    assert calcular_circulo_maximo("Arcanista", 4) == 1
    assert calcular_circulo_maximo("Arcanista", 5) == 2
    assert calcular_circulo_maximo("Arcanista", 9) == 3
    assert calcular_circulo_maximo("Arcanista", 13) == 4
    assert calcular_circulo_maximo("Arcanista", 17) == 5


def test_progressao_bardo_para_no_quarto():
    assert calcular_circulo_maximo("Bardo", 5) == 1
    assert calcular_circulo_maximo("Bardo", 6) == 2
    assert calcular_circulo_maximo("Bardo", 10) == 3
    assert calcular_circulo_maximo("Bardo", 14) == 4
    assert calcular_circulo_maximo("Bardo", 20) == 4


def test_progressao_druida():
    assert calcular_circulo_maximo("Druida", 1) == 1
    assert calcular_circulo_maximo("Druida", 6) == 2
    assert calcular_circulo_maximo("Druida", 14) == 4


def test_classe_sem_magia_circulo_zero():
    assert calcular_circulo_maximo("Guerreiro", 20) == 0


def test_validacao_remove_magia_acima_do_circulo(personagem_base):
    personagem_base.classes[0].nome = "Arcanista"
    personagem_base.classes[0].nivel = 1
    personagem_base.combate.magias = [
        Magia(nome="Mísseis Mágicos", circulo=1),
        Magia(nome="Bola de Fogo", circulo=3),
    ]
    validar_circulos_magias(personagem_base)
    nomes = [m.nome for m in personagem_base.combate.magias]
    assert "Mísseis Mágicos" in nomes
    assert "Bola de Fogo" not in nomes
    assert personagem_base.combate.circulo_maximo == 1


def test_validacao_preserva_magia_de_habilidade(personagem_base):
    personagem_base.classes[0].nome = "Guerreiro"
    personagem_base.combate.magias = [
        Magia(nome="Magia de Poder", circulo=3, fonte="Habilidade: Algum Poder"),
    ]
    validar_circulos_magias(personagem_base)
    assert len(personagem_base.combate.magias) == 1
    assert personagem_base.combate.circulo_maximo == 0


def test_multiclasse_usa_maior_circulo(personagem_base):
    personagem_base.classes = [
        ClasseInfo(nome="Guerreiro", nivel=10),
        ClasseInfo(nome="Arcanista", nivel=5),
    ]
    assert calcular_circulo_maximo_ficha(personagem_base) == 2


def test_subclasse_herda_progressao_da_classe_base():
    assert calcular_circulo_maximo("Bruxo", 1) == 1
    assert calcular_circulo_maximo("Bruxo", 5) == 2
    assert calcular_circulo_maximo("Mago", 9) == 3
    assert calcular_circulo_maximo("Feiticeiro", 13) == 4


def test_arcanista_feiticeiro_usa_carisma_no_pm(personagem_base):
    personagem_base.classes[0].nome = "Arcanista"
    personagem_base.classes[0].subclasse = "Feiticeiro"
    personagem_base.atributos.carisma = 4
    personagem_base.atributos.inteligencia = 0
    calcular_pv_pm(personagem_base)
    assert any(
        f.fonte == "Atributo-chave: CAR" and f.valor == 4
        for f in personagem_base.status.pm_calc.fontes
    )


def test_arcanista_bruxo_usa_inteligencia_no_pm(personagem_base):
    personagem_base.classes[0].nome = "Arcanista"
    personagem_base.classes[0].subclasse = "Bruxo"
    personagem_base.atributos.inteligencia = 3
    personagem_base.atributos.carisma = 5
    calcular_pv_pm(personagem_base)
    assert any(
        f.fonte == "Atributo-chave: INT" and f.valor == 3
        for f in personagem_base.status.pm_calc.fontes
    )
    assert not any(
        f.fonte.startswith("Atributo-chave: CAR")
        for f in personagem_base.status.pm_calc.fontes
    )


def test_poder_magico_adiciona_pm_por_nivel(personagem_base):
    personagem_base.classes[0].nome = "Arcanista"
    personagem_base.classes[0].nivel = 5
    personagem_base.habilidades = [
        Habilidade(nome="Poder Mágico", tipo="Poder de Arcanista", descricao=""),
    ]
    calcular_pv_pm(personagem_base)  # cria o pm_calc (ordem da pipeline)
    aplicar_poderes_arcanista(personagem_base)
    assert any(
        f.fonte == "Poder Mágico" and f.valor == 5
        for f in personagem_base.status.pm_calc.fontes
    )


def test_limite_magias_arcanista_nivel_1(personagem_base):
    personagem_base.classes[0].nome = "Arcanista"
    personagem_base.classes[0].nivel = 1
    limite, _ = calcular_limite_magias_conhecidas(personagem_base)
    assert limite == 3


def test_limite_magias_arcanista_nivel_5(personagem_base):
    personagem_base.classes[0].nome = "Arcanista"
    personagem_base.classes[0].nivel = 5
    limite, _ = calcular_limite_magias_conhecidas(personagem_base)
    assert limite == 7  # 3 iniciais + 4 (níveis 2 a 5)


def test_limite_magias_mago_nivel_5(personagem_base):
    personagem_base.classes[0].nome = "Arcanista"
    personagem_base.classes[0].subclasse = "Mago"
    personagem_base.classes[0].nivel = 5
    limite, _ = calcular_limite_magias_conhecidas(personagem_base)
    assert limite == 9  # 4 iniciais + 4 por nível + 1 pelo 2º círculo


def test_limite_magias_feiticeiro_nivel_5(personagem_base):
    personagem_base.classes[0].nome = "Arcanista"
    personagem_base.classes[0].subclasse = "Feiticeiro"
    personagem_base.classes[0].nivel = 5
    limite, _ = calcular_limite_magias_conhecidas(personagem_base)
    assert limite == 5  # 3 iniciais + níveis ímpares 3 e 5


def test_limite_magias_com_conhecimento_magico(personagem_base):
    personagem_base.classes[0].nome = "Arcanista"
    personagem_base.classes[0].nivel = 1
    personagem_base.habilidades = [
        Habilidade(nome="Conhecimento Mágico", tipo="Poder de Arcanista", descricao=""),
    ]
    limite, _ = calcular_limite_magias_conhecidas(personagem_base)
    assert limite == 5  # 3 + 2 do poder


def test_classe_sem_regra_nao_tem_limite(personagem_base):
    personagem_base.classes[0].nome = "Guerreiro"
    limite, calc = calcular_limite_magias_conhecidas(personagem_base)
    assert limite is None
    assert calc is None
