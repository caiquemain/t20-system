"""Testes automatizados das 66 Origens Regionais do Atlas de Arton (p. 470–479)."""
import pytest
from src.dados_origens import DADOS_ORIGENS
from src.dados_origens_atlas import DADOS_ORIGENS_ATLAS, DADOS_PODERES_ORIGEM_ATLAS
from src.models import Cabecalho, ClasseInfo, Personagem
from src.regras import atualizar_ficha

ORIGENS_ATLAS = sorted(DADOS_ORIGENS_ATLAS.keys())


def _ficha_origem(origem: str, nivel: int = 3) -> Personagem:
    f = Personagem(
        cabecalho=Cabecalho(nome=f"Teste {origem}", raca="Humano", origem=origem, nivel_total=nivel),
        classes=[ClasseInfo(nome="Guerreiro", nivel=nivel, primaria=True)],
    )
    atualizar_ficha(f)
    return f


def test_total_66_origens_regionais_e_metadados():
    assert len(DADOS_ORIGENS_ATLAS) == 66
    assert len(DADOS_PODERES_ORIGEM_ATLAS) == 66
    for nome in ORIGENS_ATLAS:
        assert nome in DADOS_ORIGENS
        d = DADOS_ORIGENS[nome]
        assert d["fonte"] == "Atlas de Arton"
        assert d["regional"] is True
        assert d["qtd_escolhas"] == 0
        assert d["poder_fixo"] in DADOS_PODERES_ORIGEM_ATLAS


@pytest.mark.parametrize("origem", ORIGENS_ATLAS)
def test_atualizar_ficha_todas_origens_regionais(origem: str):
    f = _ficha_origem(origem)
    poder_esperado = DADOS_ORIGENS[origem]["poder_fixo"]
    assert any(h.nome == poder_esperado for h in f.habilidades)
    for p_fixa in DADOS_ORIGENS[origem].get("pericias_fixas", []):
        if p_fixa in f.pericias:
            assert f.pericias[p_fixa].treino > 0, f"{origem} deveria treinar {p_fixa}"


def test_efeitos_mecanicos_e_troca_de_origem_regional():
    # Escudeiro da Luz: treinado em Nobreza, +2 Defesa, +3 PM
    f_luz = _ficha_origem("Escudeiro da Luz", nivel=1)
    assert f_luz.pericias["Nobreza"].treino > 0
    assert f_luz.status.defesa.total == 12
    assert f_luz.status.pm.maximo == 6  # Guerreiro nv1 (3 PM) + 3 PM

    # Cria da Favela: +1 Constituição
    f_fav = _ficha_origem("Cria da Favela", nivel=1)
    assert f_fav.atributos.constituicao == 1

    # Criado pelas Voracis: +2 Defesa, +2 Sobrevivência, +3m deslocamento
    f_vor = _ficha_origem("Criado pelas Voracis", nivel=1)
    assert f_vor.status.defesa.total == 12
    assert f_vor.status.deslocamento == 12
    assert f_vor.pericias["Sobrevivência"].total >= 2

    # Insurgente Tapistano: +1 Fort/Ref/Von, +3 PV nv1 e +1 PV/nível seguinte
    f_ins = _ficha_origem("Insurgente Tapistano", nivel=3)
    # Guerreiro nv3 base 20 + 2*5 = 30 + (2 ini + 3*1 nivel) = 35 PV
    assert f_ins.status.pv.maximo == 35
    assert f_ins.pericias["Vontade"].total >= 2  # +1 metade nível + 1 Insurgente

    # Descendente Colleniano: +2 Percepção + magia Visão Mística
    f_col = _ficha_origem("Descendente Colleniano", nivel=1)
    assert any(m.nome == "Visão Mística" for m in f_col.combate.magias)

    # Troca de origem remove o poder regional antigo automaticamente
    f_luz.cabecalho.origem = "Plebeu Arcano"
    atualizar_ficha(f_luz)
    nomes = [h.nome for h in f_luz.habilidades]
    assert "Origem Regional: Plebeu Arcano" in nomes
    assert "Origem Regional: Escudeiro da Luz" not in nomes
    assert f_luz.status.pm.maximo == 5  # Guerreiro nv1 (3) + Plebeu Arcano (+2)
