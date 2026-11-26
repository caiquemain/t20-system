"""Bardo — testes de Inspiração, Arte Mágica, Inspiração Marcial e Artista Completo (T20 JdA p.43-44)."""
import pytest
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Habilidade, Magia
from src.dados_habilidades_classe import DADOS_HABILIDADES_CLASSE
from src.regras import atualizar_ficha
from src.regras.custo_magia import calcular_cd_magia, calcular_custo_magia


def _bardo(nivel=1, car=4, poderes=None, condicoes=None):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Orfeu", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Bardo", nivel=nivel, primaria=True)]
    f.atributos_base = Atributos(carisma=car, constituicao=1)
    f.atributos = f.atributos_base.model_copy()
    if condicoes:
        f.condicoes_ativas = list(condicoes)
    for chave in (poderes or []):
        d = DADOS_HABILIDADES_CLASSE[chave]
        f.habilidades.append(Habilidade(
            nome=d["nome"],
            tipo=d["tipo"],
            descricao=d["descricao"],
            efeitos=dict(d.get("efeitos", {})),
            fonte="Poder de Bardo",
        ))
    return f


@pytest.mark.parametrize("nivel,bonus_esp,custo_esp", [
    (1, 1, 2),
    (4, 1, 2),
    (5, 2, 4),
    (8, 2, 4),
    (9, 3, 6),
    (12, 3, 6),
    (13, 4, 8),
    (16, 4, 8),
    (17, 5, 10),
    (20, 5, 10),
])
def test_inspiracao_escala_nivel(nivel, bonus_esp, custo_esp):
    f = _bardo(nivel=nivel)
    atualizar_ficha(f)
    calc = f.combate.inspiracao_calc
    assert calc is not None
    assert calc["bonus"] == bonus_esp
    assert calc["custo"] == custo_esp
    assert calc["acao"] == ("Livre" if nivel >= 20 else "Padrão")
    assert calc["reduz_custo_metade"] is (nivel >= 20)


def test_inspiracao_none_para_nao_bardo():
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Klunc", raca="Humano", nivel_total=5)
    f.classes = [ClasseInfo(nome="Bárbaro", nivel=5, primaria=True)]
    atualizar_ficha(f)
    assert f.combate.inspiracao_calc is None


def test_inspiracao_marcial_aplica_dano():
    f = _bardo(nivel=5, poderes=["BARDO_INSPIRACAO_MARCIAL"])
    atualizar_ficha(f)
    assert f.combate.inspiracao_calc["aplica_dano"] is True
    assert any("Inspiração Marcial" in e for e in f.status.efeitos_ativos)


def test_arte_magica_aumenta_cd_apenas_sob_inspiracao():
    magia = Magia(nome="Enfeitiçar", circulo=1, escola="Encantamento", atributo_chave="car")

    # Sem condição "inspiracao" ativa: CD = 10 + floor(6/2) + 4 = 17
    f_sem = _bardo(nivel=6, car=4, poderes=["BARDO_ARTE_MAGICA"], condicoes=[])
    atualizar_ficha(f_sem)
    assert f_sem.combate.inspiracao_calc["cd_bonus"] == 2
    assert f_sem.combate.inspiracao_calc["ativa"] is False
    assert calcular_cd_magia(f_sem, magia) == 17

    # Com condição "inspiracao" ativa: CD = 17 + 2 = 19
    f_com = _bardo(nivel=6, car=4, poderes=["BARDO_ARTE_MAGICA"], condicoes=["inspiracao"])
    atualizar_ficha(f_com)
    assert f_com.combate.inspiracao_calc["ativa"] is True
    assert calcular_cd_magia(f_com, magia) == 19


def test_artista_completo_reduz_custo_magia_pela_metade_sob_inspiracao():
    magia_3 = Magia(nome="Bola de Fogo", circulo=3, escola="Evocação", atributo_chave="car")

    # Nível 20 sem Inspiração ativa: 3º círculo (6 PM) + 4 PM aprimoramento = 10 PM
    f_sem = _bardo(nivel=20, condicoes=[])
    atualizar_ficha(f_sem)
    custo_sem = calcular_custo_magia(f_sem, magia_3, aprimoramentos_pm=4)
    assert custo_sem.total == 10

    # Nível 20 com Inspiração ativa: floor((6 + 4) / 2) = 5 PM
    f_com = _bardo(nivel=20, condicoes=["inspiracao"])
    atualizar_ficha(f_com)
    custo_com = calcular_custo_magia(f_com, magia_3, aprimoramentos_pm=4)
    assert custo_com.total == 5

    # Redução aplicada APÓS outras reduções: 6 PM + 3 aprim = 9 PM; -1 escola = 8 PM; /2 = 4 PM
    f_com.combate.custo_por_escola = {"Evocação": -1}
    custo_pos_red = calcular_custo_magia(f_com, magia_3, aprimoramentos_pm=3)
    assert custo_pos_red.total == 4

    # Mínimo 1 PM mesmo em magia de 1º círculo (floor(1/2) = 0 -> clamped to 1)
    magia_1 = Magia(nome="Enfeitiçar", circulo=1, escola="Encantamento", atributo_chave="car")
    assert calcular_custo_magia(f_com, magia_1).total == 1


@pytest.mark.parametrize("nivel,dados_esp", [
    (1, 1),
    (4, 1),
    (5, 2),
    (9, 3),
    (13, 4),
    (17, 5),
])
def test_golpe_elemental_escala_dados(nivel, dados_esp):
    f = _bardo(nivel=nivel, poderes=["BARDO_GOLPE_ELEMENTAL"])
    atualizar_ficha(f)
    assert f.combate.inspiracao_calc["golpe_elemental_max_dados"] == dados_esp
