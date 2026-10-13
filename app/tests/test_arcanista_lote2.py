"""Arcanista - Lote 2: poderes simples (T20 JdA p.37-38).

Cobre poderes com efeito direto e mensuravel:
    Poder Magico         - +1 PM por nivel de arcanista
    Arcano de Batalha    - soma atributo-chave no dano de magia
    Aumento de Atributo  - +1 atributo
    Conhecimento Magico  - +2 magias conhecidas (limite)
    Fortalecimento Arcano - +1 CD (+2 se 4o circulo)
    Magia Pungente       - +2 CD por 1 PM (ativavel)
    Especialista em Escola - +2 CD nas magias da escola escolhida
    Mestre em Escola     - -1 PM nas magias da escola escolhida
"""
import pytest
from src.models import (
    Personagem, Cabecalho, ClasseInfo, Atributos, Habilidade, Magia,
)
from src.regras import atualizar_ficha
from src.regras.magias import validar_magias_conhecidas
from src.regras.custo_magia import calcular_cd_magia, calcular_custo_magia
from src.regras.poderes_arcanista import aplicar_poderes_arcanista


def _arcanista(subclasse="Mago", nivel=1, **attrs):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Arc", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Arcanista", nivel=nivel,
                            primaria=True, subclasse=subclasse)]
    base = {"constituicao": 2, "inteligencia": 3, "carisma": 0}
    base.update(attrs)
    f.atributos_base = Atributos(**base)
    f.atributos = f.atributos_base.model_copy()
    return f


def _add_poder(f, nome, efeitos=None, escolhas=None):
    f.habilidades.append(Habilidade(
        nome=nome,
        tipo="Poder de Arcanista",
        efeitos=efeitos or {},
        escolhas_aplicadas=escolhas or {},
    ))


# ===================================================================
# 1. Poder Magico (+1 PM por nivel)
# ===================================================================

def test_poder_magico_soma_pm_por_nivel():
    """Poder Magico nivel 5 = +5 PM."""
    f = _arcanista(nivel=5)
    _add_poder(f, "Poder Mágico")
    atualizar_ficha(f)

    fontes = [fnt for fnt in f.status.pm_calc.fontes
              if "Poder Mágico" in (fnt.fonte or "")]
    assert fontes, f"Poder Magico nao somou PM. Fontes: {[x.fonte for x in f.status.pm_calc.fontes]}"
    assert fontes[0].valor == 5, f"Esperado +5 PM, obtido {fontes[0].valor}"


def test_poder_magico_retroativo_nivel_alto():
    """Poder Magico nivel 17 = +17 PM."""
    f = _arcanista(nivel=17)
    _add_poder(f, "Poder Mágico")
    atualizar_ficha(f)
    fontes = [fnt for fnt in f.status.pm_calc.fontes
              if "Poder Mágico" in (fnt.fonte or "")]
    assert fontes and fontes[0].valor == 17


# ===================================================================
# 2. Arcano de Batalha (soma atributo-chave no dano)
# ===================================================================

def test_arcano_batalha_soma_int_mago():
    """Mago com Int 3: +3 no dano de magias."""
    f = _arcanista(subclasse="Mago", nivel=1, inteligencia=3)
    _add_poder(f, "Arcano de Batalha")
    aplicar_poderes_arcanista(f)
    # O motor guarda em combate.bonus_dano_magias
    assert f.combate.bonus_dano_magias == 3, (
        f"Esperado +3, obtido {f.combate.bonus_dano_magias}"
    )


def test_arcano_batalha_soma_car_feiticeiro():
    """Feiticeiro com Car 4: +4 no dano de magias."""
    f = _arcanista(subclasse="Feiticeiro", carisma=4, inteligencia=0)
    _add_poder(f, "Arcano de Batalha")
    aplicar_poderes_arcanista(f)
    assert f.combate.bonus_dano_magias == 4, (
        f"Esperado +4, obtido {f.combate.bonus_dano_magias}"
    )


# ===================================================================
# 3. Aumento de Atributo
# ===================================================================

def test_aumento_atributo_escolha_aplica_mais_1():
    f = _arcanista(nivel=2)
    _add_poder(f, "Aumento de Atributo",
               escolhas={"atributo": "inteligencia"})
    atualizar_ficha(f)
    # inteligencia base = 3, deve virar 4
    assert f.atributos.inteligencia == 4, (
        f"Esperado Int 4 (3+1), obtido {f.atributos.inteligencia}"
    )


# ===================================================================
# 4. Conhecimento Magico (limite de magias +2)
# ===================================================================

def test_conhecimento_magico_aumenta_limite():
    """Nivel 1 Mago: 3 iniciais + 1 (Mago) + 2 (Conhecimento) = 6."""
    f = _arcanista(subclasse="Mago", nivel=1)
    _add_poder(f, "Conhecimento Mágico")
    atualizar_ficha(f)
    assert f.combate.limite_magias == 6, (
        f"Esperado 6, obtido {f.combate.limite_magias}"
    )


# ===================================================================
# 5. Fortalecimento Arcano (+1 CD, +2 se 4o circulo)
# ===================================================================

def test_fortalecimento_arcano_cd_bonus_nivel_baixo():
    f = _arcanista(nivel=5)
    _add_poder(f, "Fortalecimento Arcano")
    atualizar_ficha(f)
    # CD base = 10 + metade nivel (2) + Int (3) = 15
    # Fortalecimento +1 → 16
    assert f.combate.cd_magias == 16, (
        f"Esperado CD 16, obtido {f.combate.cd_magias}"
    )


def test_fortalecimento_arcano_cd_bonus_4o_circulo():
    """Se pode lancar 4o circulo (nivel 13+), bonus vira +2."""
    f = _arcanista(nivel=13)
    _add_poder(f, "Fortalecimento Arcano")
    atualizar_ficha(f)
    # CD base = 10 + 6 + 3 = 19; +2 = 21
    assert f.combate.cd_magias == 21, (
        f"Esperado CD 21, obtido {f.combate.cd_magias}"
    )


# ===================================================================
# 6. Magia Pungente (+2 CD via 1 PM ativavel)
# ===================================================================

def test_magia_pungente_adiciona_buff_quando_ativado():
    """Quando o buff 'Magia Pungente' esta nos status.buffs, soma +2 CD."""
    f = _arcanista(nivel=5)
    _add_poder(f, "Magia Pungente", efeitos={"habilidade_ativavel": {
        "custo": 1, "acao": "Livre", "efeito": "+2 CD na próxima magia",
        "modificadores": [{"atributo": "cd_magias", "valor": 2}],
    }})
    # Simula buff ativo
    from src.models import Buff
    f.status.buffs = [Buff(origem="Magia Pungente", atributo="cd_magias", valor=2)]
    atualizar_ficha(f)
    # CD base = 10 + 2 + 3 = 15; +2 Pungente = 17
    assert f.combate.cd_magias == 17, (
        f"Esperado CD 17, obtido {f.combate.cd_magias}"
    )


# ===================================================================
# 7. Especialista em Escola (+2 CD na escola)
# ===================================================================

def test_especialista_escola_aumenta_cd_da_escola():
    """Magia Evocacao: CD +2 se especialista em Evocacao."""
    f = _arcanista(nivel=5)
    _add_poder(f, "Especialista em Escola",
               escolhas={"escola": "Evocação"})
    # Adiciona magia Evocacao
    f.combate.magias = [Magia(nome="Bola de Fogo", circulo=2, escola="Evocação")]
    atualizar_ficha(f)

    cd_evocacao = f.combate.cd_por_escola.get("Evocação", 0)
    assert cd_evocacao == 2, (
        f"cd_por_escola['Evocação'] esperado 2, obtido {cd_evocacao}. "
        f"Mapa completo: {f.combate.cd_por_escola}"
    )


def test_especialista_escola_cd_por_escola_vira_bonus_efetivo():
    """O motor deve aplicar o +2 no calculo da CD da magia especifica."""
    f = _arcanista(nivel=5)
    _add_poder(f, "Especialista em Escola", escolhas={"escola": "Evocação"})
    magia_evocacao = Magia(nome="Bola de Fogo", circulo=2, escola="Evocação")
    magia_ilusionismo = Magia(nome="Invisibilidade", circulo=2, escola="Ilusão")
    atualizar_ficha(f)

    cd_evocacao = calcular_cd_magia(f, magia_evocacao)
    cd_ilusao = calcular_cd_magia(f, magia_ilusionismo)
    assert cd_evocacao == cd_ilusao + 2, (
        f"Especialista deveria dar +2 em Evocacao. "
        f"CD Evocacao={cd_evocacao}, CD Ilusao={cd_ilusao}"
    )


# ===================================================================
# 8. Mestre em Escola (-1 PM na escola)
# ===================================================================

def test_mestre_escola_reduz_custo_da_escola():
    """Magia Evocacao: custo -1 PM se mestre em Evocacao."""
    f = _arcanista(nivel=9)
    _add_poder(f, "Mestre em Escola", escolhas={"escola": "Evocação"})
    atualizar_ficha(f)  # popula combate.custo_por_escola
    magia_evocacao = Magia(nome="Bola de Fogo", circulo=2, escola="Evocação")
    magia_ilusao = Magia(nome="Invisibilidade", circulo=2, escola="Ilusão")

    custo_evocacao = calcular_custo_magia(f, magia_evocacao).total
    custo_ilusao = calcular_custo_magia(f, magia_iluso := magia_ilusao).total
    assert custo_evocacao == custo_ilusao - 1, (
        f"Mestre em Escola deveria dar -1 PM em Evocacao. "
        f"Custo Evocacao={custo_evocacao}, Custo Ilusao={custo_ilusao}"
    )
