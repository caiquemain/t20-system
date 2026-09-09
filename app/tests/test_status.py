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
    
    # Testa compatibilidade (campo antigo)
    assert personagem_base.status.pv.maximo == 23
    assert personagem_base.status.pm.maximo == 3
    
    # 🚀 Testa a transparência (nova pilha)
    assert personagem_base.status.pv_calc is not None
    assert personagem_base.status.pv_calc.total == 23
    assert personagem_base.status.pv_calc.base == 0
    
    # Verifica fontes do PV: Classe (20) + CON (3)
    fontes_pv = personagem_base.status.pv_calc.fontes
    assert len(fontes_pv) == 2
    assert fontes_pv[0].fonte == "Classe: Guerreiro (Inicial)"
    assert fontes_pv[0].valor == 20
    assert fontes_pv[1].fonte == "Constituição"
    assert fontes_pv[1].valor == 3


@patch('src.regras.status.DADOS_CLASSES', MOCK_CLASSES)
def test_calcular_pv_pm_guerreiro_nivel_2(personagem_base):
    personagem_base.classes[0].nivel = 2
    personagem_base.cabecalho.nivel_total = 2
    personagem_base.atributos.constituicao = 3
    calcular_pv_pm(personagem_base)
    
    # PV: 20 (ini) + 3 (con) + 1*(5+3) = 31
    assert personagem_base.status.pv.maximo == 31
    assert personagem_base.status.pv_calc.total == 31


def test_calcular_defesa_basica(personagem_base):
    personagem_base.atributos.destreza = 4
    calcular_defesa_e_deslocamento(personagem_base)
    
    # Testa compatibilidade (campo antigo)
    assert personagem_base.status.defesa.total == 14
    
    # 🚀 Testa a transparência (nova pilha)
    assert personagem_base.status.defesa_calc is not None
    assert personagem_base.status.defesa_calc.total == 14
    assert personagem_base.status.defesa_calc.base == 10
    
    # Verifica fontes: Base (10) + DES (4)
    fontes_def = personagem_base.status.defesa_calc.fontes
    assert len(fontes_def) == 1
    assert fontes_def[0].fonte == "Destreza"
    assert fontes_def[0].valor == 4