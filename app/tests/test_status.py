from unittest.mock import patch
from src.regras.status import calcular_pv_pm, calcular_defesa_e_deslocamento

MOCK_CLASSES = {
    "Guerreiro": {
        "pv_inicial": 20, "pv_nivel": 5, 
        "pm_inicial": 3, "pm_nivel": 3, "pm_atributo": "sab"
    }
}

@patch('src.regras.status.DADOS_CLASSES', MOCK_CLASSES)
def test_calcular_pv_pm_guerreiro_nivel_1(personagem_base):
    personagem_base.atributos.constituicao = 3
    personagem_base.atributos.sabedoria = 0
    calcular_pv_pm(personagem_base)
    assert personagem_base.status.pv.maximo == 23
    assert personagem_base.status.pm.maximo == 3

def test_calcular_defesa_basica(personagem_base):
    personagem_base.atributos.destreza = 4
    calcular_defesa_e_deslocamento(personagem_base)
    assert personagem_base.status.defesa.total == 14
    assert personagem_base.status.defesa.detalhes["Base"] == 10
    assert personagem_base.status.defesa.detalhes["Destreza"] == 4
