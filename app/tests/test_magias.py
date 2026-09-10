from src.models import Magia, ClasseInfo
from src.regras.magias import (
    calcular_circulo_maximo,
    calcular_circulo_maximo_ficha,
    validar_circulos_magias,
)


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
    # Bruxo/Mago/Feiticeiro são caminhos do Arcanista
    assert calcular_circulo_maximo("Bruxo", 1) == 1
    assert calcular_circulo_maximo("Bruxo", 5) == 2
    assert calcular_circulo_maximo("Mago", 9) == 3
    assert calcular_circulo_maximo("Feiticeiro", 13) == 4