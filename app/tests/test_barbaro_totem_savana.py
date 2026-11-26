"""Bárbaro — Animais Totêmicos (Totem Espiritual) e Fúria da Savana (T20 JdA p.41-42)."""
import pytest
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Habilidade
from src.regras import atualizar_ficha
from src.dados_escolhas import ANIMAIS_TOTEMICOS_MAGIAS, montar_catalogo_escolhas


def _barbaro(nivel=4, sabedoria=2):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Klunc", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Bárbaro", nivel=nivel, primaria=True)]
    f.atributos_base = Atributos(forca=4, constituicao=3, sabedoria=sabedoria)
    f.atributos = f.atributos_base.model_copy()
    return f


def test_catalogo_escolhas_expoe_totem_espiritual_com_8_animais():
    catalogo = montar_catalogo_escolhas()
    assert "Totem Espiritual" in catalogo["PODERES_COM_ESCOLHA"]
    gatilhos = catalogo["PODERES_COM_ESCOLHA"]["Totem Espiritual"]
    assert len(gatilhos) == 1
    assert gatilhos[0]["chave"] == "totem"
    opcoes = gatilhos[0]["opcoes"]
    assert len(opcoes) == 8
    valores = {o["valor"] for o in opcoes}
    assert valores == {"Coruja", "Corvo", "Falcão", "Grifo", "Lobo", "Raposa", "Tartaruga", "Urso"}


@pytest.mark.parametrize("animal,magia_esperada", list(ANIMAIS_TOTEMICOS_MAGIAS.items()))
def test_totem_espiritual_concede_magia_do_animal_com_sabedoria(animal, magia_esperada):
    f = _barbaro(nivel=4, sabedoria=2)
    f.habilidades.append(Habilidade(
        nome="Totem Espiritual",
        tipo="Poder de Bárbaro",
        efeitos={"pm_soma_atributo": "sab", "escolha_totem": True},
        escolhas_aplicadas={"totem": animal},
    ))
    atualizar_ficha(f)

    magia = next((m for m in f.combate.magias if m.nome == magia_esperada), None)
    assert magia is not None, f"Animal {animal} deveria conceder a magia {magia_esperada}"
    assert magia.atributo_chave == "sab"
    assert magia.fonte == f"Habilidade: Totem Espiritual ({animal})"
    assert "mesmo em fúria" in magia.descricao.lower()
    if animal == "Urso":
        assert "druida" in magia.descricao.lower()


def test_totem_espiritual_trocar_animal_substitui_magia():
    f = _barbaro(nivel=4, sabedoria=2)
    hab = Habilidade(
        nome="Totem Espiritual",
        tipo="Poder de Bárbaro",
        efeitos={"pm_soma_atributo": "sab", "escolha_totem": True},
        escolhas_aplicadas={"totem": "Lobo"},
    )
    f.habilidades.append(hab)
    atualizar_ficha(f)
    assert any(m.nome == "Concentração de Combate" for m in f.combate.magias)

    hab.escolhas_aplicadas["totem"] = "Coruja"
    atualizar_ficha(f)
    nomes = [m.nome for m in f.combate.magias]
    assert "Orientação" in nomes
    assert "Concentração de Combate" not in nomes


def test_furia_da_savana_aplica_furia_em_arremesso():
    f_sem = _barbaro(nivel=2)
    atualizar_ficha(f_sem)
    assert f_sem.combate.furia_calc is not None
    assert f_sem.combate.furia_calc["aplica_arremesso"] is False

    f_com = _barbaro(nivel=2)
    f_com.habilidades.append(Habilidade(
        nome="Fúria da Savana",
        tipo="Poder de Bárbaro",
        efeitos={"deslocamento_bonus": 3, "furia_arremesso": True},
    ))
    atualizar_ficha(f_com)
    assert f_com.combate.furia_calc is not None
    assert f_com.combate.furia_calc["aplica_arremesso"] is True
    assert any("arremesso" in e.lower() for e in f_com.status.efeitos_ativos)
