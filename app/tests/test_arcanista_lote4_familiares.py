"""Arcanista - Lote 4: familiares arcanos (T20 JdA p.38).

Cobre os 10 familiares:
    Borboleta - +1 CD Vontade
    Cobra     - +1 CD Fortitude
    Coruja    - 1 PM: toque -> curto
    Corvo     - 1 PM: rolar 2 dados Misticismo/Vontade
    Falcão    - imune surpreendido + desprevenido
    Gato      - visão no escuro + +2 Furtividade
    Lagarto   - +1 CD Reflexos
    Morcego   - percepção às cegas (curto)
    Rato      - usa atributo-chave em Fortitude (BUG conhecido)
    Sapo      - soma atributo-chave nos PV
"""
import pytest
from src.models import (
    Personagem, Cabecalho, ClasseInfo, Atributos, Habilidade, Buff,
)
from src.regras import atualizar_ficha
from src.regras.poderes_arcanista import aplicar_poderes_arcanista


def _arcanista(nivel=5, subclasse="Mago", **attrs):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Arc", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Arcanista", nivel=nivel,
                            primaria=True, subclasse=subclasse)]
    base = {"constituicao": 2, "inteligencia": 3, "carisma": 0}
    base.update(attrs)
    f.atributos_base = Atributos(**base)
    f.atributos = f.atributos_base.model_copy()
    return f


def _com_familiar(familiar):
    f = _arcanista()
    f.habilidades.append(Habilidade(
        nome="Familiar", tipo="Poder de Arcanista",
        escolhas_aplicadas={"familiar": familiar},
    ))
    return f


def _fontes(f, pericia):
    info = f.pericias.get(pericia)
    return list(info.fontes_bonus) if info else []


# ===================================================================
# 1. Borboleta (+1 CD Vontade)
# ===================================================================

def test_borboleta_cd_vontade():
    f = _com_familiar("Borboleta")
    atualizar_ficha(f)
    assert f.combate.cd_por_resistencia.get("Vontade") == 1, (
        f"Borboleta: cd_por_resistencia[Vontade] = "
        f"{f.combate.cd_por_resistencia.get('Vontade')}"
    )


# ===================================================================
# 2. Cobra (+1 CD Fortitude)
# ===================================================================

def test_cobra_cd_fortitude():
    f = _com_familiar("Cobra")
    atualizar_ficha(f)
    assert f.combate.cd_por_resistencia.get("Fortitude") == 1


# ===================================================================
# 3. Lagarto (+1 CD Reflexos)
# ===================================================================

def test_lagarto_cd_reflexos():
    f = _com_familiar("Lagarto")
    atualizar_ficha(f)
    assert f.combate.cd_por_resistencia.get("Reflexos") == 1


# ===================================================================
# 4. Sapo (soma atributo-chave em PV)
# ===================================================================

def test_sapo_soma_attr_chave_em_pv():
    """Mago com Int 3: +3 PV temporários no maximo (cumulativo)."""
    f = _com_familiar("Sapo")
    atualizar_ficha(f)

    fontes = [fnt.fonte for fnt in (f.status.pv_calc.fontes if f.status.pv_calc else [])]
    tem_sapo = any("Familiar: Sapo" in (fonte or "") for fonte in fontes)
    assert tem_sapo, (
        f"Sapo nao somou PV. Fontes: {fontes}"
    )


def test_sapo_com_feiticeiro_usa_carisma():
    """Feiticeiro com Car 4: +4 PV."""
    f = _arcanista(subclasse="Feiticeiro", carisma=4, inteligencia=0)
    f.habilidades.append(Habilidade(
        nome="Familiar", tipo="Poder de Arcanista",
        escolhas_aplicadas={"familiar": "Sapo"},
    ))
    atualizar_ficha(f)
    fontes = [fnt for fnt in (f.status.pv_calc.fontes if f.status.pv_calc else [])
              if "Familiar: Sapo" in (fnt.fonte or "")]
    assert fontes and fontes[0].valor == 4, (
        f"Feiticeiro Sapo: esperado +4, obtido "
        f"{fontes[0].valor if fontes else 'nenhuma fonte'}"
    )


# ===================================================================
# 5. Falcão (imunidades)
# ===================================================================

def test_falcao_imunidades():
    f = _com_familiar("Falcão")
    atualizar_ficha(f)
    assert "Não pode ser surpreendido" in f.status.imunidades, (
        f"Falcao sem imunidade 'surpreendido'. Imunidades: {f.status.imunidades}"
    )
    assert "Nunca fica desprevenido" in f.status.imunidades, (
        f"Falcao sem imunidade 'desprevenido'. Imunidades: {f.status.imunidades}"
    )


# ===================================================================
# 6. Gato (visão no escuro + +2 Furtividade)
# ===================================================================

def test_gato_visao_no_escuro():
    f = _com_familiar("Gato")
    atualizar_ficha(f)
    assert "Visão no Escuro" in f.status.sentidos, (
        f"Gato sem visao no escuro. Sentidos: {f.status.sentidos}"
    )


def test_gato_bonus_furtividade():
    f = _com_familiar("Gato")
    atualizar_ficha(f)
    info = f.pericias.get("Furtividade")
    assert info is not None, "Pericia Furtividade ausente"
    tem_fonte = any("Gato" in (linha or "") for linha in info.fontes_bonus)
    tem_bonus_auto = (info.bonus_automatico or 0) >= 2
    assert tem_fonte or tem_bonus_auto, (
        f"Gato sem +2 Furtividade. fontes={info.fontes_bonus}, "
        f"bonus_auto={info.bonus_automatico}"
    )


# ===================================================================
# 7. Morcego (percepção às cegas)
# ===================================================================

def test_morcego_percepcao_as_cegas():
    f = _com_familiar("Morcego")
    atualizar_ficha(f)
    tem = any("cegas" in s.lower() or "cegas" in s.lower()
              for s in f.status.sentidos)
    assert tem, (
        f"Morcego sem percepcao as cegas. Sentidos: {f.status.sentidos}"
    )


# ===================================================================
# 8. Coruja / Corvo (ativaveis)
# ===================================================================

def test_coruja_habilidade_ativavel_injetada():
    """Coruja adiciona habilidade_ativavel ao card do Familiar."""
    f = _com_familiar("Coruja")
    fam = next((h for h in f.habilidades if h.nome == "Familiar"), None)
    aplicar_poderes_arcanista(f)
    assert fam is not None
    ativavel = (fam.efeitos or {}).get("habilidade_ativavel")
    assert ativavel is not None, (
        f"Coruja nao injetou habilidade_ativavel. Efeitos: {fam.efeitos}"
    )
    assert ativavel.get("custo") == 1


def test_corvo_habilidade_ativavel_injetada():
    f = _com_familiar("Corvo")
    fam = next((h for h in f.habilidades if h.nome == "Familiar"), None)
    aplicar_poderes_arcanista(f)
    ativavel = (fam.efeitos or {}).get("habilidade_ativavel")
    assert ativavel is not None, (
        f"Corvo nao injetou habilidade_ativavel. Efeitos: {fam.efeitos}"
    )


# ===================================================================
# 9. Rato (usa atributo-chave em Fortitude) — BUG conhecido
# ===================================================================

def test_rato_permite_attr_chave_em_fortitude():
    """Livro: 'Você pode usar seu atributo-chave em Fortitude, no lugar
    de Constituição.' Esperado: pericia Fortitude aceita 'int'/'car'
    como atributo-chave."""
    f = _com_familiar("Rato")
    atualizar_ficha(f)
    info = f.pericias.get("Fortitude")
    assert info is not None, "Fortitude ausente"
    possiveis = set(info.atributos_possiveis or [])
    aceita_chave = "int" in possiveis or "car" in possiveis
    assert aceita_chave, (
        f"Rato nao liberou atributo-chave em Fortitude. "
        f"atributos_possiveis={possiveis}"
    )


# ===================================================================
# 10. Idempotencia
# ===================================================================

@pytest.mark.parametrize("familiar", [
    "Borboleta", "Cobra", "Lagarto", "Gato", "Morcego", "Sapo",
])
def test_familiar_nao_duplica_bonus_em_reprocessamentos(familiar):
    """Rodar atualizar_ficha 3x nao pode acumular o mesmo bonus."""
    f = _com_familiar(familiar)
    for _ in range(3):
        atualizar_ficha(f)

    if familiar == "Gato":
        fontes = _fontes(f, "Furtividade")
        ocorrencias = [x for x in fontes if "Gato" in (x or "")]
        assert len(ocorrencias) <= 1, (
            f"Gato acumulou: {ocorrencias}"
        )
    elif familiar == "Sapo":
        fontes = [fnt for fnt in (f.status.pv_calc.fontes if f.status.pv_calc else [])
                  if "Familiar: Sapo" in (fnt.fonte or "")]
        assert len(fontes) <= 1, (
            f"Sapo acumulou: {[x.fonte for x in fontes]}"
        )
    elif familiar == "Falcao" or familiar == "Falcão":
        pass
    else:
        # CDs nao podem acumular
        valores = list(f.combate.cd_por_resistencia.values())
        assert all(v <= 1 for v in valores), (
            f"{familiar} acumulou CD: {f.combate.cd_por_resistencia}"
        )
