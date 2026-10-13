"""Arcanista - Lote 3: Linhagens do Feiticeiro (T20 JdA p.39).

Cobre Linhagem Draconica e Feerica nos 3 niveis (Basica/Aprimorada/Superior).
Linhagem Rubra vem no arquivo separado (test_arcanista_lote3_rubra.py).

Regras (T20 JdA p.39):
    DRAconica (escolha tipo de dano: acido/eletricidade/fogo/frio)
        Basica: +Car nos PV iniciais + RD 5 ao tipo
        Aprimorada: magias do tipo custam -1 PM e causam +1 dano por dado
        Superior: dobro do Car nos PV + imune ao tipo

    FEERICA
        Basica: treinado em Enganacao + 1 magia 1o circ encantamento/ilusao
        Aprimorada: CD +2 em Encantamento/Ilusao; custo -1 PM nessas escolas
        Superior: +2 em Carisma
"""
import pytest
from src.models import (
    Personagem, Cabecalho, ClasseInfo, Atributos, Habilidade, Magia,
)
from src.regras import atualizar_ficha
from src.regras.custo_magia import calcular_custo_magia


def _feiticeiro(nivel=1, carisma=4, **attrs):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Feit", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Arcanista", nivel=nivel,
                            primaria=True, subclasse="Feiticeiro")]
    base = {"constituicao": 2, "inteligencia": 0, "carisma": carisma}
    base.update(attrs)
    f.atributos_base = Atributos(**base)
    f.atributos = f.atributos_base.model_copy()
    return f


def _add_linhagem(f, nome, escolhas=None):
    f.habilidades.append(Habilidade(
        nome=nome, tipo="Habilidade de Classe",
        escolhas_aplicadas=escolhas or {},
    ))


# ===================================================================
# 1. LINHAGEM DRACÔNICA — Básica
# ===================================================================

def test_draconica_basica_soma_car_em_pv_iniciais():
    """Feiticeiro Car 4: +4 PV iniciais."""
    f = _feiticeiro(nivel=1, carisma=4)
    _add_linhagem(f, "Linhagem Dracônica", escolhas={"tipo_dano": "fogo"})
    atualizar_ficha(f)

    fontes = [fnt for fnt in (f.status.pv_calc.fontes if f.status.pv_calc else [])
              if "Linhagem Dracônica" in (fnt.fonte or "")]
    assert fontes, (
        f"Dracônica Básica não somou Car em PV. Fontes: "
        f"{[x.fonte for x in (f.status.pv_calc.fontes if f.status.pv_calc else [])]}"
    )
    # +Car (4). Não é retroativo por nível.
    soma_car = sum(fnt.valor for fnt in fontes if "(básica)" in (fnt.fonte or ""))
    assert soma_car == 4, f"Esperado +4, obtido {soma_car}"


def test_draconica_basica_rd_5_ao_tipo():
    """RD 5 ao tipo de dano escolhido."""
    f = _feiticeiro()
    _add_linhagem(f, "Linhagem Dracônica", escolhas={"tipo_dano": "fogo"})
    atualizar_ficha(f)
    assert any("fogo" in rd.lower() and "5" in rd for rd in f.status.rd), (
        f"RD 5 a fogo não apareceu. RD: {f.status.rd}"
    )


def test_draconica_tipo_agua_usa_frio():
    f = _feiticeiro()
    _add_linhagem(f, "Linhagem Dracônica", escolhas={"tipo_dano": "frio"})
    atualizar_ficha(f)
    assert any("frio" in rd.lower() for rd in f.status.rd), f"RD a frio ausente: {f.status.rd}"


# ===================================================================
# 2. LINHAGEM DRACÔNICA — Aprimorada
# ===================================================================

def test_draconica_aprimorada_magias_do_tipo_custam_menos():
    """Magias de fogo custam -1 PM quando Herança Aprimorada está ativa."""
    f = _feiticeiro(nivel=6, carisma=4)
    _add_linhagem(f, "Linhagem Dracônica", escolhas={"tipo_dano": "fogo"})
    _add_linhagem(f, "Herança Aprimorada")
    atualizar_ficha(f)

    magia_fogo = Magia(nome="Bola de Fogo", circulo=2, tipo="Fogo", escola="Evocação")
    magia_frio = Magia(nome="Sopro das Uivantes", circulo=2, tipo="Frio", escola="Evocação")

    # Bola de Fogo base = 3 PM. Com redução deveria virar 2 PM.
    custo_fogo = calcular_custo_magia(f, magia_fogo).total
    custo_frio = calcular_custo_magia(f, magia_frio).total
    assert custo_fogo == custo_frio - 1, (
        f"Draconica Aprimorada deveria dar -1 PM em magias de fogo. "
        f"Custo fogo={custo_fogo}, custo frio={custo_frio}"
    )


def test_draconica_aprimorada_magias_do_tipo_causam_mais_dano():
    """Magias do tipo +1 ponto de dano por dado."""
    f = _feiticeiro(nivel=6, carisma=4)
    _add_linhagem(f, "Linhagem Dracônica", escolhas={"tipo_dano": "fogo"})
    _add_linhagem(f, "Herança Aprimorada")
    atualizar_ficha(f)

    # O motor precisa expor algum campo que diga "+1 dano/dado para fogo".
    # Como o livro não especifica um campo canônico, checamos que o mapa
    # está populado.
    assert f.combate.bonus_dano_dado_tipo, (
        f"Draconica Aprimorada não populou bonus_dano_dado_tipo. "
        f"Valor: {f.combate.bonus_dano_dado_tipo}"
    )
    assert f.combate.bonus_dano_dado_tipo.get("fogo") == 1, (
        f"Esperado +1 dano/dado de fogo, obtido "
        f"{f.combate.bonus_dano_dado_tipo.get('fogo')}"
    )


# ===================================================================
# 3. LINHAGEM DRACÔNICA — Superior
# ===================================================================

def test_draconica_superior_imune_ao_tipo():
    f = _feiticeiro(nivel=11, carisma=4)
    _add_linhagem(f, "Linhagem Dracônica", escolhas={"tipo_dano": "fogo"})
    _add_linhagem(f, "Herança Aprimorada")
    _add_linhagem(f, "Herança Superior")
    atualizar_ficha(f)
    assert any("fogo" in im.lower() for im in f.status.imunidades), (
        f"Dracônica Superior sem imunidade a fogo. Imunidades: {f.status.imunidades}"
    )


def test_draconica_superior_dobra_car_em_pv():
    """Básica + Superior: +2x Car nos PV (dobra). Car 4 → +8 PV."""
    f = _feiticeiro(nivel=11, carisma=4)
    _add_linhagem(f, "Linhagem Dracônica", escolhas={"tipo_dano": "fogo"})
    _add_linhagem(f, "Herança Aprimorada")
    _add_linhagem(f, "Herança Superior")
    atualizar_ficha(f)

    fontes = [fnt for fnt in (f.status.pv_calc.fontes if f.status.pv_calc else [])
              if "Linhagem Dracônica" in (fnt.fonte or "")]
    soma = sum(fnt.valor for fnt in fontes)
    assert soma == 8, (
        f"Dracônica Básica+Superior deveria dar +8 PV (2xCar 4). "
        f"Soma atual: {soma}. Fontes: {[(x.fonte, x.valor) for x in fontes]}"
    )


# ===================================================================
# 4. LINHAGEM FEÉRICA — Básica
# ===================================================================

def test_feerica_basica_treina_enganacao():
    f = _feiticeiro()
    _add_linhagem(f, "Linhagem Feérica")
    atualizar_ficha(f)
    info = f.pericias.get("Enganação")
    assert info is not None
    assert info.treino == 1, f"Enganação não treinada: treino={info.treino}"


# ===================================================================
# 5. LINHAGEM FEÉRICA — Aprimorada
# ===================================================================

def test_feerica_aprimorada_cd_encantamento():
    f = _feiticeiro(nivel=6, carisma=4)
    _add_linhagem(f, "Linhagem Feérica")
    _add_linhagem(f, "Herança Aprimorada")
    atualizar_ficha(f)
    assert f.combate.cd_por_escola.get("Encantamento") == 2, (
        f"Feérica Aprimorada deveria dar +2 CD em Encantamento. "
        f"cd_por_escola: {f.combate.cd_por_escola}"
    )


def test_feerica_aprimorada_cd_ilusao():
    f = _feiticeiro(nivel=6, carisma=4)
    _add_linhagem(f, "Linhagem Feérica")
    _add_linhagem(f, "Herança Aprimorada")
    atualizar_ficha(f)
    assert f.combate.cd_por_escola.get("Ilusão") == 2


def test_feerica_aprimorada_custo_encantamento_menos_1():
    f = _feiticeiro(nivel=6, carisma=4)
    _add_linhagem(f, "Linhagem Feérica")
    _add_linhagem(f, "Herança Aprimorada")
    atualizar_ficha(f)

    # Magias de 2o circulo: base 3 PM, sobra espaco para a reducao de -1 PM
    # (1o circulo base 1 PM seria clampado pelo minimo).
    magia_enc = Magia(nome="Marca da Obediência", circulo=2, escola="Encantamento")
    magia_evoc = Magia(nome="Bola de Fogo", circulo=2, escola="Evocação")

    custo_enc = calcular_custo_magia(f, magia_enc).total
    custo_evoc = calcular_custo_magia(f, magia_evoc).total
    assert custo_enc == custo_evoc - 1, (
        f"Feérica Aprimorada deveria dar -1 PM em Encantamento. "
        f"Encantamento={custo_enc}, Evocação={custo_evoc}"
    )


# ===================================================================
# 6. LINHAGEM FEÉRICA — Superior
# ===================================================================

def test_feerica_superior_mais_2_carisma():
    f = _feiticeiro(nivel=11, carisma=4)
    _add_linhagem(f, "Linhagem Feérica")
    _add_linhagem(f, "Herança Aprimorada")
    _add_linhagem(f, "Herança Superior")
    atualizar_ficha(f)
    assert f.atributos.carisma == 6, (
        f"Feérica Superior deveria dar +2 Car (4→6). Obtido: {f.atributos.carisma}"
    )


def test_feerica_superior_carisma_persiste_em_recalc():
    """+2 Car não pode ser apagado por reprocessamentos."""
    f = _feiticeiro(nivel=11, carisma=4)
    _add_linhagem(f, "Linhagem Feérica")
    _add_linhagem(f, "Herança Aprimorada")
    _add_linhagem(f, "Herança Superior")
    for _ in range(3):
        atualizar_ficha(f)
    assert f.atributos.carisma == 6, (
        f"Carisma fantasma em recalc: {f.atributos.carisma}"
    )


# ===================================================================
# 7. Sanidade geral
# ===================================================================

def test_feiticeiro_sem_linhagem_nao_quebra():
    f = _feiticeiro()
    atualizar_ficha(f)
    assert f.status.pv.maximo > 0


def test_draconica_sem_tipo_dano_nao_quebra():
    """Se o jogador não escolheu tipo_dano, não deve quebrar."""
    f = _feiticeiro()
    _add_linhagem(f, "Linhagem Dracônica", escolhas={})
    atualizar_ficha(f)
    assert f.status.pv.maximo > 0
