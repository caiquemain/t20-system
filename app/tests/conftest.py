import pytest
from src.models import Personagem, Cabecalho, Atributos, ClasseInfo, Descricao, Status

@pytest.fixture
def personagem_base():
    return Personagem(
        cabecalho=Cabecalho(nome="Boneco de Teste", raca="Humano", nivel_total=1),
        atributos_base=Atributos(forca=1, destreza=2, constituicao=3, inteligencia=0, sabedoria=0, carisma=0),
        atributos=Atributos(forca=1, destreza=2, constituicao=3, inteligencia=0, sabedoria=0, carisma=0),
        classes=[ClasseInfo(nome="Guerreiro", nivel=1, primaria=True)],
        descricao=Descricao(),
        status=Status()
    )
