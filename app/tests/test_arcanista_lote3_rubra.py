"""Arcanista - Lote 3B: Linhagem Rubra (T20 JdA p.39).

Regras:
    Básica: recebe 1 poder da Tormenta; pode perder outro atributo em
            vez de Carisma por poderes da Tormenta (nao testavel em motor).
    Aprimorada: escolha 1 magia para cada poder da Tormenta que possui.
                Essas magias custam -1 PM.
    Superior: +4 PM para cada poder da Tormenta que possui.
"""
import pytest
from src.models import (
    Personagem, Cabecalho, ClasseInfo, Atributos, Habilidade, Magia,
)
from src.regras import atualizar_ficha
from src.regras.custo_magia import calcular_custo_magia


def _feiticeiro(nivel=11, carisma=4, **attrs):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Feit", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Arcanista", nivel=nivel,
                            primaria=True, subclasse="Feiticeiro")]
    base = {"constituicao": 2, "inteligencia": 0, "carisma": carisma}
    base.update(attrs)
    f.atributos_base = Atributos(**base)
    f.atributos = f.atributos_base.model_copy()
    return f


def _add(f, nome, escolhas=None, tipo=None):
    f.habilidades.append(Habilidade(
        nome=nome,
        tipo=tipo or "Habilidade de Classe",
        escolhas_aplicadas=escolhas or {},
    ))


def _add_tormenta(f, nome="Anatomia Insana"):
    """Adiciona um poder da Tormenta que conta para os contadores."""
    f.habilidades.append(Habilidade(
        nome=nome, tipo="Poder da Tormenta",
    ))


# ===================================================================
# 1. Superior: +4 PM × quantidade de poderes da Tormenta
# ===================================================================

def test_rubra_superior_1_poder_tormenta():
    """1 poder da Tormenta → +4 PM."""
    f = _feiticeiro(nivel=11)
    _add(f, "Linhagem Rubra")
    _add(f, "Herança Aprimorada")
    _add(f, "Herança Superior")
    _add_tormenta(f, "Anatomia Insana")
    atualizar_ficha(f)

    fontes = [fnt for fnt in (f.status.pm_calc.fontes if f.status.pm_calc else [])
              if "Linhagem Rubra" in (fnt.fonte or "")]
    assert fontes, (
        f"Rubra Superior não somou PM. Fontes: "
        f"{[x.fonte for x in (f.status.pm_calc.fontes if f.status.pm_calc else [])]}"
    )
    soma = sum(fnt.valor for fnt in fontes)
    assert soma == 4, f"Esperado +4 PM, obtido {soma}"


def test_rubra_superior_3_poderes_tormenta():
    """3 poderes → +12 PM."""
    f = _feiticeiro(nivel=11)
    _add(f, "Linhagem Rubra")
    _add(f, "Herança Aprimorada")
    _add(f, "Herança Superior")
    _add_tormenta(f, "Anatomia Insana")
    _add_tormenta(f, "Antenas")
    _add_tormenta(f, "Carapaça")
    atualizar_ficha(f)

    fontes = [fnt for fnt in (f.status.pm_calc.fontes if f.status.pm_calc else [])
              if "Linhagem Rubra" in (fnt.fonte or "")]
    soma = sum(fnt.valor for fnt in fontes)
    assert soma == 12, f"Esperado +12 PM, obtido {soma}"


def test_rubra_superior_sem_poderes_nao_soma():
    f = _feiticeiro(nivel=11)
    _add(f, "Linhagem Rubra")
    _add(f, "Herança Aprimorada")
    _add(f, "Herança Superior")
    atualizar_ficha(f)
    fontes = [fnt for fnt in (f.status.pm_calc.fontes if f.status.pm_calc else [])
              if "Linhagem Rubra" in (fnt.fonte or "")]
    assert not fontes, f"Rubra sem poderes não deveria somar. Fontes: {[x.fonte for x in fontes]}"


def test_rubra_superior_nao_acumula_em_recalc():
    """+4 PM não pode duplicar em reprocessamentos."""
    f = _feiticeiro(nivel=11)
    _add(f, "Linhagem Rubra")
    _add(f, "Herança Aprimorada")
    _add(f, "Herança Superior")
    _add_tormenta(f, "Anatomia Insana")
    for _ in range(3):
        atualizar_ficha(f)
    fontes = [fnt for fnt in (f.status.pm_calc.fontes if f.status.pm_calc else [])
              if "Linhagem Rubra" in (fnt.fonte or "")]
    soma = sum(fnt.valor for fnt in fontes)
    assert soma == 4, f"Acumulou: {soma} (esperado 4)"


# ===================================================================
# 2. Aprimorada: magia escolhida por poder da Tormenta custa -1 PM
# ===================================================================

def test_rubra_aprimorada_magia_escolhida_custa_menos():
    """Escolher 'Bola de Fogo' para um poder da Tormenta → -1 PM nela."""
    f = _feiticeiro(nivel=6)
    _add(f, "Linhagem Rubra")
    _add(f, "Herança Aprimorada", escolhas={
        "magia_por_poder": ["Bola de Fogo"],
    })
    _add_tormenta(f, "Anatomia Insana")
    atualizar_ficha(f)

    magia_alvo = Magia(nome="Bola de Fogo", circulo=2, escola="Evocação")
    magia_outra = Magia(nome="Sopro das Uivantes", circulo=2, escola="Evocação")

    custo_alvo = calcular_custo_magia(f, magia_alvo).total
    custo_outra = calcular_custo_magia(f, magia_outra).total
    assert custo_alvo == custo_outra - 1, (
        f"Rubra Aprimorada deveria dar -1 PM em 'Bola de Fogo'. "
        f"alvo={custo_alvo}, outra={custo_outra}"
    )


def test_rubra_aprimorada_sem_escolha_nao_aplica():
    """Sem escolha de magia, nada é reduzido."""
    f = _feiticeiro(nivel=6)
    _add(f, "Linhagem Rubra")
    _add(f, "Herança Aprimorada")  # sem escolhas
    _add_tormenta(f, "Anatomia Insana")
    atualizar_ficha(f)

    magia = Magia(nome="Bola de Fogo", circulo=2, escola="Evocação")
    assert calcular_custo_magia(f, magia).total == 3, (
        "Sem escolha, custo deveria ser base 3 PM"
    )


# ===================================================================
# 3. Básica: só estrutura (a escolha do poder da Tormenta é do wizard)
# ===================================================================

def test_rubra_basica_existe_como_habilidade():
    f = _feiticeiro()
    _add(f, "Linhagem Rubra")
    atualizar_ficha(f)
    rubra = next((h for h in f.habilidades if h.nome == "Linhagem Rubra"), None)
    assert rubra is not None


# ===================================================================
# 4. Combinação Dracônica + Rubra não interfere
# ===================================================================

def test_rubra_nao_interfere_em_outras_linhagens():
    """Feiticeiro só tem 1 linhagem. Adicionar Rubra quando não há
    outra linhagem não deve somar PM se Herança Superior estiver sem
    poderes da Tormenta."""
    f = _feiticeiro(nivel=11)
    _add(f, "Linhagem Rubra")
    _add(f, "Herança Aprimorada")
    _add(f, "Herança Superior")
    # Nenhum poder da Tormenta
    atualizar_ficha(f)
    fontes = [fnt for fnt in (f.status.pm_calc.fontes if f.status.pm_calc else [])
              if "Linhagem Rubra" in (fnt.fonte or "")]
    assert not fontes
