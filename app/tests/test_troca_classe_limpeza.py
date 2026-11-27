"""Testes de limpeza de poderes e magias ao trocar de classe (ex.: Arcanista -> Lutador)."""
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Habilidade, Magia
from src.regras import atualizar_ficha


def test_trocar_arcanista_para_lutador_remove_poderes_e_magias_de_arcanista():
    f = Personagem(
        cabecalho=Cabecalho(nome="Kord", raca="Elfo"),
        classes=[ClasseInfo(nome="Arcanista", nivel=3, primaria=True, subclasse="Mago")],
        atributos_base=Atributos(forca=2, destreza=2, constituicao=2, inteligencia=3, sabedoria=1, carisma=1),
        habilidades=[
            Habilidade(nome="Fluxo de Mana", tipo="Poder de Arcanista"),
            Habilidade(nome="Esquiva", tipo="Poder Geral (Combate)"),
        ],
    )
    f.combate.magias = [
        Magia(nome="Bola de Fogo", circulo=1, tipo="Arcana", escola="Evocação"),
        Magia(nome="Armadura Arcana", circulo=1, tipo="Arcana", escola="Abjuração"),
    ]
    atualizar_ficha(f)
    assert any(h.nome == "Fluxo de Mana" for h in f.habilidades)
    assert len(f.combate.magias) == 2

    # Troca para Lutador (não-conjurador)
    f.classes[0].nome = "Lutador"
    f.classes[0].subclasse = ""
    atualizar_ficha(f)

    # Poder de Arcanista e magias de Arcanista devem ser removidos; poder geral Esquiva mantido!
    assert not any(h.nome == "Fluxo de Mana" for h in f.habilidades)
    assert any(h.nome == "Esquiva" for h in f.habilidades)
    assert f.combate.circulo_maximo == 0
    assert len(f.combate.magias) == 0


def test_trocar_lutador_para_variante_atleta_mantem_poderes_de_lutador():
    f = Personagem(
        cabecalho=Cabecalho(nome="Kord", raca="Humano"),
        classes=[ClasseInfo(nome="Lutador", nivel=3, primaria=True)],
        atributos_base=Atributos(forca=3, destreza=2, constituicao=2),
        habilidades=[
            Habilidade(nome="Sarado", tipo="Poder de Lutador"),
        ],
    )
    atualizar_ficha(f)
    assert any(h.nome == "Sarado" for h in f.habilidades)

    # Troca para Atleta (variante de Lutador): deve manter Poder de Lutador!
    f.classes[0].nome = "Atleta"
    atualizar_ficha(f)
    assert any(h.nome == "Sarado" for h in f.habilidades)
