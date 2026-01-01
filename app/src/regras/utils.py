import logging
from ..models import Personagem

logger = logging.getLogger("RegrasT20")


def calcular_modificador(valor_atributo: int) -> int:
    return valor_atributo


def calcular_nivel_personagem(ficha: Personagem) -> int:
    total = 0
    for classe in ficha.classes:
        total += classe.nivel
    return max(total, 1)
