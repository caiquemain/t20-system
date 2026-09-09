from src.regras.utils import calcular_modificador, calcular_nivel_personagem
from src.models import ClasseInfo

def test_calcular_modificador_t20():
    assert calcular_modificador(3) == 3
    assert calcular_modificador(0) == 0
    assert calcular_modificador(-2) == -2

def test_calcular_nivel_personagem(personagem_base):
    assert calcular_nivel_personagem(personagem_base) == 1
    personagem_base.classes.append(ClasseInfo(nome="Mago", nivel=2))
    assert calcular_nivel_personagem(personagem_base) == 3
