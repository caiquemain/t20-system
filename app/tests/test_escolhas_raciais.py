"""Escolhas variáveis de atributos raciais (T20 JdA: +1 por escolha)."""
from src.models import Personagem
from src.regras import atualizar_ficha


def test_humano_bonus_1_por_escolha():
    p = Personagem()
    p.cabecalho.raca = 'Humano'
    p.escolhas_atributos_raciais = ['for', 'des', 'con']
    atualizar_ficha(p)
    assert p.atributos.forca == 1
    assert p.atributos.destreza == 1
    assert p.atributos.constituicao == 1


def test_chave_curta_e_longa_equivalentes():
    for chave in ('des', 'destreza'):
        p = Personagem()
        p.cabecalho.raca = 'Humano'
        p.escolhas_atributos_raciais = [chave]
        atualizar_ficha(p)
        assert p.atributos.destreza == 1, chave


def test_lefou_mais_1_e_carisma_fixo():
    p = Personagem()
    p.cabecalho.raca = 'Lefou'
    p.escolhas_atributos_raciais = ['for', 'des', 'int']
    atualizar_ficha(p)
    assert p.atributos.forca == 1
    assert p.atributos.carisma == -1


def test_sem_residuo_no_total():
    """total == base + racial (o -1 fantasma de 'outros' não pode voltar)."""
    p = Personagem()
    p.cabecalho.raca = 'Humano'
    p.escolhas_atributos_raciais = ['for']
    atualizar_ficha(p)
    assert p.atributos.forca == p.atributos_base.forca + p.modificadores_raciais.get('forca', 0)
    fontes = [f for f in p.atributos_calc['forca'].fontes if f.categoria == 'Racial']
    assert fontes and fontes[0].valor == 1
