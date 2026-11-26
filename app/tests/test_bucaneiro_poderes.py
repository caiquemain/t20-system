"""Bucaneiro — testes de poderes de classe e cobertura completa do catálogo (T20 JdA p.46-48)."""
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Habilidade, Item
from src.dados_habilidades_classe import DADOS_HABILIDADES_CLASSE
from src.regras import atualizar_ficha


def _bucaneiro(nivel=6, des=3, inte=3, car=4, poderes=None, condicoes=None, itens=None):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Izzy", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Bucaneiro", nivel=nivel, primaria=True)]
    f.atributos_base = Atributos(destreza=des, inteligencia=inte, carisma=car, constituicao=1)
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
            fonte="Poder de Bucaneiro",
        ))
    for nome_item in (itens or []):
        f.inventario.equipamentos.append(Item(nome=nome_item, equipado=True))
    return f


# ===================================================================
# 1. Esgrimista & En Garde
# ===================================================================

def test_esgrimista_soma_inteligencia_limitada_pelo_nivel_em_leves_e_ageis():
    # Nível 2 com Int 4: bônus limitado a +2 em Florete (ágil) e Machadinha (leve);
    # Espada longa (uma mão não-ágil) e Montante (duas mãos) não recebem.
    f = _bucaneiro(
        nivel=2,
        inte=4,
        poderes=["BUCANEIRO_ESGRIMISTA"],
        itens=["Florete", "Machadinha", "Espada longa", "Montante"],
    )
    atualizar_ficha(f)
    por_nome = {a.nome: a for a in f.combate.ataques}

    assert por_nome["Florete"].dano == "1d6+2"
    assert "Esgrimista (+2 dano)" in por_nome["Florete"].especial
    assert por_nome["Machadinha"].dano == "1d6+2"
    assert por_nome["Espada longa"].dano == "1d8"
    assert por_nome["Montante"].dano == "2d6"


def test_en_garde_ativa_defesa_e_margem_ameaca():
    # Sem postura En Garde
    f_sem = _bucaneiro(nivel=4, des=2, car=0, poderes=["BUCANEIRO_EN_GARDE"], itens=["Florete"])
    atualizar_ficha(f_sem)
    # Defesa = 10 + Des(2) + Esquiva Sagaz(1) = 13
    assert f_sem.status.defesa.total == 13
    assert "En Garde" not in f_sem.combate.ataques[0].especial

    # Com postura En Garde ativa: Defesa = 13 + 2 = 15, e Florete ganha nota de +2 margem de ameaça
    f_com = _bucaneiro(
        nivel=4, des=2, car=0,
        poderes=["BUCANEIRO_EN_GARDE"],
        condicoes=["en_garde"],
        itens=["Florete"],
    )
    atualizar_ficha(f_com)
    assert f_com.status.defesa.total == 15
    assert "En Garde (+2 margem de ameaça)" in f_com.combate.ataques[0].especial


# ===================================================================
# 2. Pistoleiro
# ===================================================================

def test_pistoleiro_proficiencia_e_bonus_dano_arma_fogo():
    f = _bucaneiro(nivel=4, poderes=["BUCANEIRO_PISTOLEIRO"], itens=["Pistola"])
    atualizar_ficha(f)
    assert "Armas de Fogo" in f.status.proficiencias
    pistola = next(a for a in f.combate.ataques if a.nome == "Pistola")
    assert pistola.dano == "2d6+2"
    assert "não proficiente" not in pistola.especial
    assert "Pistoleiro (+2 dano)" in pistola.especial


# ===================================================================
# 3. Bravatas (Audaz e Imprudente)
# ===================================================================

def test_bravata_audaz_soma_2_pm_por_nivel_quando_cumprida():
    f_sem = _bucaneiro(nivel=5, poderes=["BUCANEIRO_BRAVATA_AUDAZ"])
    atualizar_ficha(f_sem)
    assert f_sem.status.pm.maximo == 15

    f_com = _bucaneiro(nivel=5, poderes=["BUCANEIRO_BRAVATA_AUDAZ"], condicoes=["bravata_audaz"])
    atualizar_ficha(f_com)
    assert f_com.status.pm.maximo == 25  # 15 + 2*5


def test_bravata_imprudente_aplica_bonus_quando_cumprida():
    f = _bucaneiro(
        nivel=5,
        poderes=["BUCANEIRO_BRAVATA_IMPRUDENTE"],
        condicoes=["bravata_imprudente"],
        itens=["Florete"],
    )
    atualizar_ficha(f)
    florete = next(a for a in f.combate.ataques if a.nome == "Florete")
    assert "Bravata Imprudente (+2 ataque e margem de ameaça)" in florete.especial


# ===================================================================
# 4. Flagelo dos Mares, Pernas do Mar, Presença Paralisante, Aumento de Atributo
# ===================================================================

def test_flagelo_dos_mares_concede_amedrontar_carisma():
    f = _bucaneiro(nivel=3, car=4, poderes=["BUCANEIRO_FLAGELO_DOS_MARES"])
    atualizar_ficha(f)
    amedrontar = next((m for m in f.combate.magias if m.nome == "Amedrontar"), None)
    assert amedrontar is not None
    assert amedrontar.atributo_chave == "car"


def test_pernas_do_mar_soma_acrobacia_e_atletismo():
    f_sem = _bucaneiro(nivel=4, des=3)
    atualizar_ficha(f_sem)
    acro_base = f_sem.pericias["Acrobacia"].total
    atle_base = f_sem.pericias["Atletismo"].total

    f_com = _bucaneiro(nivel=4, des=3, poderes=["BUCANEIRO_PERNAS_DO_MAR"])
    atualizar_ficha(f_com)
    assert f_com.pericias["Acrobacia"].total == acro_base + 2
    assert f_com.pericias["Atletismo"].total == atle_base + 2
    assert any("Pernas do Mar" in e for e in f_com.status.efeitos_ativos)


def test_presenca_paralisante_soma_carisma_em_iniciativa():
    f_sem = _bucaneiro(nivel=4, des=2, car=4)
    atualizar_ficha(f_sem)
    ini_base = f_sem.pericias["Iniciativa"].total

    f_com = _bucaneiro(nivel=4, des=2, car=4, poderes=["BUCANEIRO_PRESENCA_PARALISANTE"])
    atualizar_ficha(f_com)
    assert f_com.pericias["Iniciativa"].total == ini_base + 4
    assert any("Presença Paralisante" in e for e in f_com.status.efeitos_ativos)


def test_bucaneiro_aumento_atributo():
    f = _bucaneiro(nivel=4, des=3)
    d = DADOS_HABILIDADES_CLASSE["BUCANEIRO_AUMENTO_ATRIBUTO"]
    f.habilidades.append(Habilidade(
        nome=d["nome"],
        tipo=d["tipo"],
        descricao=d["descricao"],
        efeitos=dict(d["efeitos"]),
        escolhas_aplicadas={"atributo": "des"},
        fonte="Poder de Bucaneiro",
    ))
    atualizar_ficha(f)
    assert f.atributos.destreza == 4


# ===================================================================
# 5. Integridade completa do catálogo de Bucaneiro (7 fixas + 19 poderes)
# ===================================================================

FIXAS_ESPERADAS = {
    "Audácia": 1,
    "Insolência": 1,
    "Evasão": 2,
    "Esquiva Sagaz": 3,
    "Panache": 5,
    "Evasão Aprimorada": 10,
    "Sorte de Nimb": 20,
}

PODERES_ESPERADOS = {
    "Abusar dos Fracos",
    "Amigos no Porto",
    "Aparar",
    "Apostador",
    "Ataque Acrobático",
    "Aumento de Atributo",
    "Aventureiro Ávido",
    "Bravata Audaz",
    "Bravata Imprudente",
    "En Garde",
    "Esgrimista",
    "Flagelo dos Mares",
    "Folião",
    "Grudar o Cano",
    "Pernas do Mar",
    "Pistoleiro",
    "Presença Paralisante",
    "Ripostar",
    "Touché",
}


def test_catalogo_bucaneiro_completo_26_entradas():
    entries = [v for v in DADOS_HABILIDADES_CLASSE.values() if v.get("classe") == "Bucaneiro"]
    fixas = {v["nome"]: v.get("nivel") for v in entries if v.get("tipo") == "Habilidade de Classe"}
    poderes = {v["nome"] for v in entries if v.get("tipo") == "Poder de Bucaneiro"}

    assert fixas == FIXAS_ESPERADAS
    assert poderes == PODERES_ESPERADOS
    assert len(entries) == 26
    assert all(v.get("efeitos") for v in entries)
