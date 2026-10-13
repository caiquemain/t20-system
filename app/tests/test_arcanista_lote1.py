"""Arcanista - Lote 1: PV/PM, pericias, prof, progressao de circulos, caminhos.

Livro (T20 JdA p.36-37):
    PV: 8 + Con, +2 + Con por nivel
    PM: 6 por nivel (independente de nivel)
    Pericias: Misticismo, Vontade + 2 a escolha
    Proficiencias: Nenhuma
    Progressao: 1o no 1, 2o no 5, 3o no 9, 4o no 13, 5o no 17
    Atributo-chave: Bruxo/Mago = Int, Feiticeiro = Car
"""
import pytest
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos
from src.regras import atualizar_ficha
from src.regras.magias import calcular_circulo_maximo


def _arcanista(subclasse="Mago", nivel=1):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Arc", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Arcanista", nivel=nivel,
                            primaria=True, subclasse=subclasse)]
    f.atributos_base = Atributos(constituicao=2, inteligencia=3, carisma=0)
    f.atributos = f.atributos_base.model_copy()
    return f


# ===================================================================
# 1. PV / PM
# ===================================================================

def test_arcanista_pv_inicial():
    """8 base + Con 2 = 10 PV maximo no nivel 1."""
    f = _arcanista()
    atualizar_ficha(f)
    assert f.status.pv.maximo == 10, (
        f"PV esperado 8 + 2(Con) = 10, obtido {f.status.pv.maximo}"
    )


def test_arcanista_pv_por_nivel():
    """Nivel 3: 8 + 2 + (2 + 2) + (2 + 2) = 8 + 2 + 4 + 4 = 18."""
    f = _arcanista(nivel=3)
    atualizar_ficha(f)
    assert f.status.pv.maximo == 18, (
        f"PV esperado 18, obtido {f.status.pv.maximo}"
    )


def test_arcanista_pm_mago_soma_int():
    """PM: 6 inicial + Int 3 = 9 no nivel 1."""
    f = _arcanista(subclasse="Mago")
    atualizar_ficha(f)
    assert f.status.pm.maximo == 9, (
        f"PM esperado 6 + 3(Int) = 9, obtido {f.status.pm.maximo}"
    )


def test_arcanista_pm_feiticeiro_soma_car():
    """Feiticeiro: PM = 6 + Car."""
    f = _arcanista(subclasse="Feiticeiro")
    f.atributos_base = Atributos(constituicao=2, inteligencia=3, carisma=5)
    f.atributos = f.atributos_base.model_copy()
    atualizar_ficha(f)
    assert f.status.pm.maximo == 11, (
        f"Feiticeiro: PM esperado 6 + 5(Car) = 11, obtido {f.status.pm.maximo}"
    )


def test_arcanista_pm_bruxo_soma_int():
    f = _arcanista(subclasse="Bruxo")
    atualizar_ficha(f)
    assert f.status.pm.maximo == 9, (
        f"Bruxo: PM esperado 6 + 3(Int) = 9, obtido {f.status.pm.maximo}"
    )


# ===================================================================
# 2. Pericias e proficiencias
# ===================================================================

def test_arcanista_pericias_fixas():
    """Misticismo e Vontade sao treinadas automaticamente."""
    f = _arcanista()
    atualizar_ficha(f)
    assert f.pericias["Misticismo"].treino == 1
    assert f.pericias["Vontade"].treino == 1


def test_arcanista_sem_proficiencias_de_armas():
    """Arcanista comeca sem prof. marciais/pesadas/escudos."""
    f = _arcanista()
    atualizar_ficha(f)
    proibidas = {"Armas Marciais", "Armaduras Pesadas", "Escudos"}
    assert not (proibidas & set(f.status.proficiencias)), (
        f"Arcanista nao deveria ter proficiencias: {proibidas & set(f.status.proficiencias)}"
    )


# ===================================================================
# 3. Progressao de circulos
# ===================================================================

@pytest.mark.parametrize("nivel,esperado", [
    (1, 1), (4, 1), (5, 2), (8, 2), (9, 3),
    (12, 3), (13, 4), (16, 4), (17, 5), (20, 5),
])
def test_arcanista_progressao_circulos(nivel, esperado):
    assert calcular_circulo_maximo("Arcanista", nivel) == esperado, (
        f"Nivel {nivel}: circulo esperado {esperado}, "
        f"obtido {calcular_circulo_maximo('Arcanista', nivel)}"
    )


def test_arcanista_multiclasse_usa_maior_circulo():
    f = Personagem()
    f.cabecalho = Cabecalho(nome="MC", raca="Humano", nivel_total=15)
    f.classes = [
        ClasseInfo(nome="Guerreiro", nivel=10),
        ClasseInfo(nome="Arcanista", nivel=5, subclasse="Mago"),
    ]
    atualizar_ficha(f)
    assert f.combate.circulo_maximo == 2, (
        f"Multiclasse Guerreiro 10 / Arcanista 5: esperado 2, "
        f"obtido {f.combate.circulo_maximo}"
    )


# ===================================================================
# 4. Caminhos como escolha
# ===================================================================

def test_arcanista_caminho_e_escolha_subclasse():
    """A habilidade 'Caminho do Arcanista' expoe os 3 caminhos."""
    f = _arcanista()
    atualizar_ficha(f)
    caminho = next((h for h in f.habilidades if h.nome == "Caminho do Arcanista"), None)
    assert caminho is not None, "Habilidade Caminho do Arcanista ausente"
    efeitos = caminho.efeitos or {}
    assert set(efeitos.get("escolha_subclasse", [])) == {"Bruxo", "Feiticeiro", "Mago"}


def test_arcanista_pv_independe_do_caminho():
    """PV deve ser identico entre Mago, Bruxo e Feiticeiro."""
    for sub in ("Mago", "Bruxo", "Feiticeiro"):
        f = _arcanista(subclasse=sub)
        atualizar_ficha(f)
        assert f.status.pv.maximo == 10, f"{sub}: PV inesperado {f.status.pv.maximo}"
