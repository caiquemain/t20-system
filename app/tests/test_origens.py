# -*- coding: utf-8 -*-
"""Testes completos das 35 Origens do Livro Básico (T20 JdA p.85-95)."""
import pytest
from src.models import Personagem, ClasseInfo, Cabecalho, Atributos
from src.dados_origens import DADOS_ORIGENS
from src.dados_poderes_origem import DADOS_PODERES_ORIGEM
from src.regras import atualizar_ficha


def _ficha_origem(origem: str, escolhas=None, nivel: int = 1, forca: int = 1) -> Personagem:
    ficha = Personagem(
        cabecalho=Cabecalho(nome="Aventureiro", raca="Humano", origem=origem),
        classes=[ClasseInfo(nome="Guerreiro", nivel=nivel, primaria=True)],
        atributos_base=Atributos(forca=forca, destreza=1, constituicao=1, inteligencia=1, sabedoria=1, carisma=1),
        escolhas_origem=list(escolhas or []),
    )
    return atualizar_ficha(ficha)


def test_catalogo_35_origens_e_35_poderes_com_efeitos():
    assert len(DADOS_ORIGENS) == 35
    assert len(DADOS_PODERES_ORIGEM) == 35

    # Todos os 35 poderes exclusivos possuem efeitos declarativos
    sem_efeitos = [k for k, v in DADOS_PODERES_ORIGEM.items() if not v.get("efeitos")]
    assert sem_efeitos == []

    # Nenhuma origem do T20 JdA concede perícias fixas fora das 2 escolhas
    for nome_origem, dados in DADOS_ORIGENS.items():
        assert dados["pericias_fixas"] == [], f"{nome_origem} não deve ter pericias_fixas"
        assert dados["qtd_escolhas"] == 2


def test_todos_poderes_unicos_batem_exatamente_com_beneficios_lista():
    # Garante que não haja divergência de maiúsculas/minúsculas (ex.: Quebra-Galho vs Quebra-galho)
    nomes_beneficios = {
        b for dados in DADOS_ORIGENS.values() for b in dados["beneficios_lista"]
    }
    for chave, poder in DADOS_PODERES_ORIGEM.items():
        assert poder["nome"] in nomes_beneficios, (
            f"Poder '{poder['nome']}' ({chave}) não encontrado exatamente em DADOS_ORIGENS"
        )


def test_origens_corrigidas_beneficios_livro_base():
    assert set(DADOS_ORIGENS["Amigo dos Animais"]["beneficios_lista"]) == {
        "Adestramento", "Cavalgar", "Amigo Especial"
    }
    assert set(DADOS_ORIGENS["Assistente de Laboratório"]["beneficios_lista"]) == {
        "Ofício (alquimista)", "Misticismo", "Esse Cheiro...", "Venefício", "Poder da Tormenta (Escolha)"
    }
    assert set(DADOS_ORIGENS["Minerador"]["beneficios_lista"]) == {
        "Atletismo", "Fortitude", "Ofício (minerador)", "Ataque Poderoso", "Escavador", "Sentidos Aguçados"
    }
    assert "Ofício (cozinheiro)" in DADOS_ORIGENS["Taverneiro"]["beneficios_lista"]
    assert "Ofício (fazendeiro)" in DADOS_ORIGENS["Fazendeiro"]["beneficios_lista"]


def test_amnesico_concede_lembrancas_graduais_automaticamente():
    f = _ficha_origem("Amnésico", escolhas=["Percepção"])
    nomes = {h.nome for h in f.habilidades}
    assert "Lembranças Graduais" in nomes
    assert f.pericias["Percepção"].treino > 0


@pytest.mark.parametrize("nivel,bonus_pm", [
    (1, 3),
    (4, 3),
    (5, 6),
    (10, 6),
    (11, 9),
    (16, 9),
    (17, 12),
    (20, 12),
])
def test_coracao_heroico_pm_por_patamar(nivel, bonus_pm):
    f_sem = _ficha_origem("Herói Camponês", escolhas=["Adestramento"], nivel=nivel)
    f_com = _ficha_origem("Herói Camponês", escolhas=["Coração Heroico"], nivel=nivel)
    assert f_com.status.pm.maximo == f_sem.status.pm.maximo + bonus_pm


def test_mochileiro_aumenta_carga_maxima_em_5():
    f_sem = _ficha_origem("Nômade", escolhas=["Sobrevivência"], forca=2)
    f_com = _ficha_origem("Nômade", escolhas=["Mochileiro"], forca=2)
    assert f_sem.inventario.carga_maxima == 14  # 10 + 2*2
    assert f_com.inventario.carga_maxima == 19  # 14 + 5


def test_escavador_proficiencia_e_dano_picareta():
    f = _ficha_origem("Minerador", escolhas=["Escavador", "Ofício (minerador)"])
    assert "Picareta" in f.status.proficiencias
    assert (f.combate.bonus_dano_arma or {}).get("picareta") == 1


def test_dom_artistico_e_esse_cheiro_bonus_pericia():
    f_art_sem = _ficha_origem("Artista", escolhas=["Atuação"])
    f_art_com = _ficha_origem("Artista", escolhas=["Atuação", "Dom Artístico"])
    assert f_art_com.pericias["Atuação"].total == f_art_sem.pericias["Atuação"].total + 2

    f_lab_sem = _ficha_origem("Assistente de Laboratório", escolhas=["Misticismo"])
    f_lab_com = _ficha_origem("Assistente de Laboratório", escolhas=["Misticismo", "Esse Cheiro..."])
    assert f_lab_com.pericias["Fortitude"].total == f_lab_sem.pericias["Fortitude"].total + 2


def test_amigo_especial_adestramento_e_pericia_parceiro():
    f_sem = _ficha_origem("Amigo dos Animais", escolhas=["Adestramento"])
    f_com = _ficha_origem("Amigo dos Animais", escolhas=["Adestramento", "Amigo Especial"])
    assert f_com.pericias["Adestramento"].total == f_sem.pericias["Adestramento"].total + 5

    # Escolhendo perícia do parceiro (ex.: Percepção) -> +2; Luta/Pontaria bloqueadas
    for h in f_com.habilidades:
        if h.nome == "Amigo Especial":
            h.escolhas_aplicadas["pericia_amigo_especial"] = "Percepção"
    f_com = atualizar_ficha(f_com)
    assert f_com.pericias["Percepção"].total == f_sem.pericias["Percepção"].total + 2

    for h in f_com.habilidades:
        if h.nome == "Amigo Especial":
            h.escolhas_aplicadas["pericia_amigo_especial"] = "Luta"
    f_com = atualizar_ficha(f_com)
    assert f_com.pericias["Luta"].total == f_sem.pericias["Luta"].total


def test_vida_rustica_imunidade_itens_ingeriveis():
    f = _ficha_origem("Selvagem", escolhas=["Vida Rústica"])
    assert "Itens ingeríveis prejudiciais" in f.status.imunidades


def test_quebra_galho_resolvido_corretamente_pelo_motor():
    f = _ficha_origem("Pivete", escolhas=["Quebra-Galho"])
    hab = next(h for h in f.habilidades if h.nome == "Quebra-Galho")
    assert hab.efeitos.get("compra_mundano_desconto_pct") == 50
