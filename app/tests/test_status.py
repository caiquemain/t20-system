from unittest.mock import patch
from src.regras.status import calcular_pv_pm, calcular_defesa_e_deslocamento

MOCK_CLASSES = {
    "Guerreiro": {
        "pv_inicial": 20, "pv_nivel": 5,
        "pm_inicial": 3, "pm_nivel": 3
        # Sem pm_atributo: Guerreiro NÃO soma atributo no PM
    },
    "Arcanista": {
        "pv_inicial": 8, "pv_nivel": 2,
        "pm_inicial": 6, "pm_nivel": 6,
        "pm_atributo": "int"
    }
}

@patch('src.regras.status.DADOS_CLASSES', MOCK_CLASSES)
def test_calcular_pv_pm_guerreiro_nivel_1(personagem_base):
    personagem_base.atributos.constituicao = 3
    personagem_base.atributos.sabedoria = 0
    calcular_pv_pm(personagem_base)

    assert personagem_base.status.pv.maximo == 23
    assert personagem_base.status.pm.maximo == 3

    fontes_pv = personagem_base.status.pv_calc.fontes
    assert len(fontes_pv) == 2
    assert fontes_pv[0].fonte == "Classe: Guerreiro (Inicial)"
    assert fontes_pv[0].valor == 20
    assert fontes_pv[1].fonte == "Constituição"
    assert fontes_pv[1].valor == 3


@patch('src.regras.status.DADOS_CLASSES', MOCK_CLASSES)
def test_pm_guerreiro_nao_soma_atributo(personagem_base):
    """Força alta NÃO pode entrar no PM de classe sem pm_atributo."""
    personagem_base.atributos.forca = 4
    personagem_base.atributos.constituicao = 3
    calcular_pv_pm(personagem_base)

    assert personagem_base.status.pm.maximo == 3
    assert all(f.categoria != "Atributo" for f in personagem_base.status.pm_calc.fontes)


@patch('src.regras.status.DADOS_CLASSES', MOCK_CLASSES)
def test_pm_classe_conjuradora_soma_atributo_chave(personagem_base):
    """Arcanista (pm_atributo=int) soma Inteligência no PM."""
    personagem_base.classes[0].nome = "Arcanista"
    personagem_base.atributos.inteligencia = 3
    calcular_pv_pm(personagem_base)

    assert personagem_base.status.pm.maximo == 9  # 6 inicial + 3 int
    assert any(f.fonte == "Atributo-chave: INT" and f.valor == 3
               for f in personagem_base.status.pm_calc.fontes)


@patch('src.regras.status.DADOS_CLASSES', MOCK_CLASSES)
def test_calcular_pv_pm_guerreiro_nivel_2(personagem_base):
    personagem_base.classes[0].nivel = 2
    personagem_base.cabecalho.nivel_total = 2
    personagem_base.atributos.constituicao = 3
    calcular_pv_pm(personagem_base)

    assert personagem_base.status.pv.maximo == 31
    assert personagem_base.status.pv_calc.total == 31


def test_calcular_defesa_basica(personagem_base):
    personagem_base.atributos.destreza = 4
    calcular_defesa_e_deslocamento(personagem_base)

    assert personagem_base.status.defesa.total == 14
    assert personagem_base.status.defesa_calc.total == 14
    assert personagem_base.status.defesa_calc.base == 10

    fontes_def = personagem_base.status.defesa_calc.fontes
    assert len(fontes_def) == 1
    assert fontes_def[0].fonte == "Destreza"
    assert fontes_def[0].valor == 4