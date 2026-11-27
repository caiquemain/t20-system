"""Testes automatizados das 40 raças/heranças/variantes jogáveis de Ameaças de Arton."""
import pytest
from src.dados_habilidades_raciais import DADOS_HABILIDADES_RACIAIS
from src.dados_racas import DADOS_RACAS
from src.models import Atributos, Cabecalho, ClasseInfo, Personagem, TamanhoEnum
from src.regras import atualizar_ficha

RACAS_AMEACAS = [
    nome for nome, dados in DADOS_RACAS.items()
    if dados.get("fonte") == "Ameaças de Arton"
]


def _criar_ficha(raca: str, nivel: int = 3, **attrs) -> Personagem:
    f = Personagem(
        cabecalho=Cabecalho(nome=f"Teste {raca}", raca=raca, nivel_total=nivel),
        classes=[ClasseInfo(nome="Guerreiro", nivel=nivel, primaria=True)],
        atributos_base=Atributos(**attrs),
    )
    atualizar_ficha(f)
    return f


def test_total_racas_ameacas_e_chaves_validas():
    assert len(RACAS_AMEACAS) == 40
    for raca in RACAS_AMEACAS:
        habs = DADOS_RACAS[raca].get("habilidades") or []
        assert len(habs) >= 2, f"Raça {raca} sem habilidades cadastradas"
        for h_key in habs:
            assert h_key in DADOS_HABILIDADES_RACIAIS, f"Chave '{h_key}' ausente para raça {raca}"


@pytest.mark.parametrize("raca", RACAS_AMEACAS)
def test_atualizar_ficha_todas_racas_ameacas(raca: str):
    f = _criar_ficha(raca)
    assert f.cabecalho.raca == raca
    assert f.status.pv.maximo > 0
    assert f.status.defesa.total >= 8
    nomes_hab = [h.nome for h in f.habilidades]
    assert len(nomes_hab) >= len(DADOS_RACAS[raca]["habilidades"])


def test_mecanicas_especificas_racas_ameacas():
    # Centauro: Grande, 12m, arma natural Cascos 1d8
    cent = _criar_ficha("Centauro")
    assert cent.descricao.tamanho == TamanhoEnum.GRANDE
    assert cent.status.deslocamento == 12
    assert any("Cascos" in a.nome and "1d8" in a.dano for a in cent.combate.ataques)

    # Ceratops: Grande, +1 Defesa (Paquidérmico), Chifres 1d8
    cera = _criar_ficha("Ceratops")
    assert cera.descricao.tamanho == TamanhoEnum.GRANDE
    assert any("Chifres" in a.nome and "1d8" in a.dano for a in cera.combate.ataques)
    # Des base 0 + (-1 racial) = -1 -> Defesa base 10 - 1 + 1 (Paquidérmico) = 10
    assert cera.status.defesa.total == 10

    # Nezumi: Pequeno, deslocamento 9m (Pequeno, Mas Não Metade), +2 Intimidação, Mordida 1d6
    nez = _criar_ficha("Nezumi")
    assert nez.descricao.tamanho == TamanhoEnum.PEQUENO
    assert nez.status.deslocamento == 9
    assert any("Mordida" in a.nome and "1d6" in a.dano for a in nez.combate.ataques)

    # Orc: Vigor Brutal (+2 Fortitude + soma Força no total de PV)
    orc = _criar_ficha("Orc", nivel=1, forca=2, constituicao=0)
    # Guerreiro nv1: 20 + CON(1) + FOR(4) = 25 PV
    assert orc.atributos.forca == 4
    assert orc.status.pv.maximo == 25

    # Ogro: Grande, For +3, Con +2, Camada de Ingenuidade (-5 Intuição e Vontade)
    ogro = _criar_ficha("Ogro", nivel=1)
    assert ogro.descricao.tamanho == TamanhoEnum.GRANDE
    assert ogro.atributos.forca == 3
    assert ogro.atributos.constituicao == 2
    assert ogro.pericias["Vontade"].total <= -5

    # Kappa: Carapaça Kappa soma CON (limitado pelo nível) na Defesa sem armadura pesada + Curar Ferimentos
    kappa = _criar_ficha("Kappa", nivel=3, constituicao=2)
    # Des +2, Con 2+1=3 (min(3, nivel 3) = 3) -> 10 + 2 (DES) + 3 (CON) = 15
    assert kappa.status.defesa.total == 15
    assert any(m.nome == "Curar Ferimentos" for m in kappa.combate.magias)

    # Yidishan: Peças Metálicas (+2 Defesa, -2 penalidade de armadura)
    yidi = _criar_ficha("Yidishan", nivel=1)
    assert yidi.status.defesa.total == 12
    assert abs(yidi.status.penalidade_armadura) >= 2

    # Trog Anão: Quase Anão (+1 PV/nível, 6m)
    trog_a = _criar_ficha("Trog Anão", nivel=4, constituicao=0)
    assert trog_a.status.deslocamento == 6
    # Guerreiro nv4: 20 + 3*5 = 35 + 4*CON(2)=8 + 4*1 (Quase Anão) = 47
    assert trog_a.status.pv.maximo == 47

    # Harpia: 12m, +2 Intimidação e Sobrevivência, Garras 1d6
    harpia = _criar_ficha("Harpia", nivel=1)
    assert harpia.status.deslocamento == 12
    assert any("Garras" in a.nome and "1d6" in a.dano for a in harpia.combate.ataques)

    # Hobgoblin: Arte da Guerra (treinado em Guerra) + Táticas de Guerrilha (+2 Furtividade)
    hob = _criar_ficha("Hobgoblin", nivel=1)
    assert hob.pericias["Guerra"].treino > 0
    assert hob.pericias["Furtividade"].total >= 3  # +1 DES + 2 Táticas

    # Moreau (Urso): Grande + Mordida 1d8
    urso = _criar_ficha("Moreau (Urso)", nivel=1)
    assert urso.descricao.tamanho == TamanhoEnum.GRANDE
    assert any("Mordida" in a.nome and "1d8" in a.dano for a in urso.combate.ataques)

    # Moreau (Crocodilo): +1 Defesa + Mordida 1d6
    croc = _criar_ficha("Moreau (Crocodilo)", nivel=1)
    assert croc.status.defesa.total == 11
    assert any("Mordida" in a.nome and "1d6" in a.dano for a in croc.combate.ataques)
