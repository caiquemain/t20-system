"""Auditoria Lote C: estrutura de habilidades ativaveis (T20 JdA).

Nao testa UI. Valida que cada 'habilidade_ativavel' racial tem os campos
minimos que o frontend (AbilityCard + handleAtivarHabilidade) espera
para renderizar botao e aplicar buff.

Cobre:
    Dahllan   - Armadura de Allihanna  (+2 Defesa, 1 PM)
    Medusa    - Natureza Venenosa      (envenenar arma, 1 PM)
    Medusa    - Olhar Atordoante       (atordoa, 1 PM)
    Trog      - Mau Cheiro             (enjoo, 2 PM)
    Hynne     - Sorte Salvadora        (rerrolar, 1 PM)
    Kliren    - Engenhosidade          (soma INT, 2 PM)
    Silfide   - Asas de Borboleta      (voo, 1 PM)
    Sereia    - Transformacao Anfibia  (toggle pernas/cauda, 0 PM)
"""
import pytest
from src.dados_habilidades_raciais import DADOS_HABILIDADES_RACIAIS


CAMPOS_MINIMOS = {"custo", "acao", "efeito"}


CASOS = [
    ("Armadura_Allihanna_Dahllan", 1, "Movimento"),
    ("Natureza_Venenosa_Medusa",   1, "Movimento"),
    ("Olhar_Atordoante_Medusa",    1, "Movimento"),
    ("Mau_Cheiro_Trog",            2, "Padrão"),
    ("Sorte_Salvadora_Hynne",      1, "Reação"),
    ("Engenhosidade_Kliren",       2, "Livre"),
    ("Asas_Borboleta_Silfide",     1, "Livre"),
    ("Transf_Anfibia_Sereia",      0, "Livre"),
]


@pytest.mark.parametrize("chave,custo_esperado,acao_esperada", CASOS)
def test_habilidade_ativavel_estrutura_completa(chave, custo_esperado, acao_esperada):
    """Cada habilidade_ativavel precisa ter custo, acao e efeito preenchidos."""
    hab = DADOS_HABILIDADES_RACIAIS.get(chave)
    assert hab is not None, f"Chave '{chave}' ausente no catalogo"

    efeitos = hab.get("efeitos") or {}
    ativavel = efeitos.get("habilidade_ativavel")
    assert ativavel is not None, (
        f"{chave}: sem 'habilidade_ativavel' nos efeitos. Efeitos: {efeitos}"
    )

    faltando = CAMPOS_MINIMOS - set(ativavel.keys())
    assert not faltando, (
        f"{chave}: campos faltando em habilidade_ativavel: {faltando}. "
        f"Conteudo: {ativavel}"
    )

    assert ativavel["custo"] == custo_esperado, (
        f"{chave}: custo esperado {custo_esperado} PM, "
        f"obtido {ativavel['custo']}"
    )
    assert ativavel["acao"] == acao_esperada, (
        f"{chave}: acao esperada '{acao_esperada}', "
        f"obtida '{ativavel['acao']}'"
    )


# ===================================================================
# Regras especificas por habilidade
# ===================================================================

def test_dahllan_armadura_allihanna_modifica_defesa():
    """Armadura de Allihanna: +2 Defesa. Precisa ter modificador com atributo=defesa."""
    h = DADOS_HABILIDADES_RACIAIS["Armadura_Allihanna_Dahllan"]
    mods = h["efeitos"]["habilidade_ativavel"].get("modificadores") or []
    assert mods, "Armadura de Allihanna sem 'modificadores' (buff nao aplica)"
    tem_defesa = any(
        m.get("atributo") == "defesa" and m.get("valor") == 2
        for m in mods
    )
    assert tem_defesa, (
        f"Modificador de Defesa +2 ausente. Modificadores: {mods}"
    )


def test_kliren_engenhosidade_marca_acumulo():
    """Engenhosidade: nome_acumulo para stacking com Inventor."""
    h = DADOS_HABILIDADES_RACIAIS["Engenhosidade_Kliren"]
    ativavel = h["efeitos"]["habilidade_ativavel"]
    assert "nome_acumulo" in ativavel, (
        "Engenhosidade sem 'nome_acumulo' — Inventor nao vai empilhar custo."
    )
    assert ativavel.get("reducao_se_acumular") == 1, (
        f"reducao_se_acumular esperada 1, obtida {ativavel.get('reducao_se_acumular')}"
    )


def test_silfide_asas_borboleta_modifica_deslocamento():
    """Asas de Borboleta: modificador de deslocamento +3m (voo)."""
    h = DADOS_HABILIDADES_RACIAIS["Asas_Borboleta_Silfide"]
    mods = h["efeitos"]["habilidade_ativavel"].get("modificadores") or []
    assert any(
        m.get("atributo") == "deslocamento" and m.get("valor") == 3
        for m in mods
    ), f"Asas de Borboleta sem +3 deslocamento. Mods: {mods}"


def test_trog_mau_cheiro_tem_resistencia_e_imunidade_pos_teste():
    """Mau Cheiro: Fortitude (CD Con), imunidade 1 dia se passar."""
    h = DADOS_HABILIDADES_RACIAIS["Mau_Cheiro_Trog"]
    ativavel = h["efeitos"]["habilidade_ativavel"]
    assert "resistencia" in ativavel, "Mau Cheiro sem campo 'resistencia'"
    assert "Con" in ativavel["resistencia"], (
        f"CD deveria ser Con, encontrado: {ativavel['resistencia']}"
    )
    assert ativavel.get("imunidade_pos_teste") is True, (
        "Mau Cheiro sem 'imunidade_pos_teste': quem passa fica imune por 1 dia."
    )


def test_medusa_olhar_atordoante_tem_resistencia_e_limite():
    """Olhar Atordoante: Fortitude (CD Car), 1x por cena."""
    h = DADOS_HABILIDADES_RACIAIS["Olhar_Atordoante_Medusa"]
    ativavel = h["efeitos"]["habilidade_ativavel"]
    assert "resistencia" in ativavel, "Olhar Atordoante sem 'resistencia'"
    assert "Car" in ativavel["resistencia"], (
        f"CD deveria ser Car, encontrado: {ativavel['resistencia']}"
    )
    assert "limite" in ativavel, "Olhar Atordoante sem 'limite' (1x cena)"
    assert "cena" in ativavel["limite"].lower(), (
        f"Limite deveria mencionar 'cena', encontrado: {ativavel['limite']}"
    )


def test_sereia_transf_anfibia_tem_deslocamento_natacao():
    """Transformacao Anfibia: cauda fornece natacao 12m."""
    h = DADOS_HABILIDADES_RACIAIS["Transf_Anfibia_Sereia"]
    e = h["efeitos"]
    assert e.get("deslocamento_natacao") == 12, (
        f"Natacao esperada 12m, obtida {e.get('deslocamento_natacao')}"
    )
    assert e.get("respirar_agua") is True, (
        "Transformacao Anfibia sem 'respirar_agua'"
    )


# ===================================================================
# Sanidade geral
# ===================================================================

def test_todas_habilidades_ativaveis_do_livro_base_tem_efeito_legivel():
    """Cada habilidade_ativavel de RACA DO LIVRO BASE deve ter 'efeito' como
    string nao-vazia (usado pelo tooltip do card).

    Escopo: apenas habilidades com 'fonte' == 'T20 JdA'. Habilidades de
    suplemento (ex.: Duende de 'Herois de Arton') ficam de fora — ver
    Lote D / debito documentado no README.
    """
    problemas = []
    for chave, hab in DADOS_HABILIDADES_RACIAIS.items():
        if hab.get("fonte") != "T20 JdA":
            continue
        ativavel = (hab.get("efeitos") or {}).get("habilidade_ativavel")
        if not ativavel:
            continue
        efeito = ativavel.get("efeito")
        if not isinstance(efeito, str) or not efeito.strip():
            problemas.append((chave, efeito))
    assert not problemas, (
        f"Habilidades ativaveis (livro base) sem 'efeito' legivel: {problemas}"
    )


def test_habilidades_ativaveis_sem_custo_negativo():
    """Sanidade: nenhuma ativavel pode ter custo negativo."""
    problemas = []
    for chave, hab in DADOS_HABILIDADES_RACIAIS.items():
        ativavel = (hab.get("efeitos") or {}).get("habilidade_ativavel")
        if not ativavel:
            continue
        custo = ativavel.get("custo")
        if not isinstance(custo, (int, float)) or custo < 0:
            problemas.append((chave, custo))
    assert not problemas, (
        f"Habilidades ativaveis com custo invalido: {problemas}"
    )
