from unittest.mock import patch
from src.regras.atributos import aplicar_bonus_atributos_raciais, calcular_atributos_finais
from src.models import Atributos

MOCK_RACAS = {
    "Humano": {"attrs": {"for": 1, "des": 1}, "deslocamento": 9, "tamanho": "Médio"},
    "Elfo": {"attrs": {"des": 2, "con": -1}, "deslocamento": 9, "tamanho": "Médio"},
    "Anão": {"attrs": {"con": 2, "des": -1}, "deslocamento": 6, "tamanho": "Médio"}
}

@patch('src.regras.atributos.DADOS_RACAS', MOCK_RACAS)
def test_bonus_racial_humano(personagem_base):
    personagem_base.cabecalho.raca = "Humano"
    personagem_base.atributos_base = Atributos(forca=2, destreza=2, constituicao=2, inteligencia=0, sabedoria=0, carisma=0)
    
    # 1. Aplica os bônus na pilha
    aplicar_bonus_atributos_raciais(personagem_base)
    # 2. Sincroniza a pilha com o objeto final (O que o frontend lê)
    calcular_atributos_finais(personagem_base)
    
    # Testa o valor final
    assert personagem_base.atributos.forca == 3
    assert personagem_base.atributos.destreza == 3
    assert personagem_base.modificadores_raciais["forca"] == 1
    
    # 🚀 NOVO TESTE: Verifica se a transparência (fontes) foi gravada!
    assert len(personagem_base.atributos_calc["forca"].fontes) == 1
    assert personagem_base.atributos_calc["forca"].fontes[0].fonte == "Raça: Humano"
    assert personagem_base.atributos_calc["forca"].fontes[0].valor == 1

@patch('src.regras.atributos.DADOS_RACAS', MOCK_RACAS)
def test_deslocamento_racial(personagem_base):
    personagem_base.cabecalho.raca = "Anão"
    aplicar_bonus_atributos_raciais(personagem_base)
    assert personagem_base.status.deslocamento == 6