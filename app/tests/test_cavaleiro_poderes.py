"""Cavaleiro — testes de poderes de classe, posturas e cobertura do catálogo (T20 JdA p.52-55)."""
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Habilidade, Item
from src.dados_habilidades_classe import DADOS_HABILIDADES_CLASSE
from src.regras import atualizar_ficha


def _cavaleiro(nivel=10, con=3, car=3, poderes=None, condicoes=None, itens=None):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Alenn", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Cavaleiro", nivel=nivel, primaria=True)]
    f.atributos_base = Atributos(constituicao=con, forca=3, destreza=1, carisma=car)
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
            fonte="Poder de Cavaleiro",
        ))
    for nome_item in (itens or []):
        f.inventario.equipamentos.append(Item(nome=nome_item, equipado=True))
    return f


# ===================================================================
# 1. Solidez (soma bônus de Defesa do escudo nas 3 resistências)
# ===================================================================

def test_solidez_soma_bonus_escudo_em_fortitude_reflexos_e_vontade():
    f_sem = _cavaleiro(nivel=4, poderes=["CAVALEIRO_SOLIDEZ"], itens=[])
    atualizar_ficha(f_sem)

    # Escudo pesado dá +2 Defesa (e -2 penalidade de armadura, não afeta Fort/Ref/Von)
    f_com = _cavaleiro(nivel=4, poderes=["CAVALEIRO_SOLIDEZ"], itens=["Escudo pesado"])
    atualizar_ficha(f_com)

    assert f_com.pericias["Fortitude"].total == f_sem.pericias["Fortitude"].total + 2
    assert f_com.pericias["Reflexos"].total == f_sem.pericias["Reflexos"].total + 2
    assert f_com.pericias["Vontade"].total == f_sem.pericias["Vontade"].total + 2


# ===================================================================
# 2. Escudeiro, Etiqueta, Pajem, Armadura da Honra, Estandarte
# ===================================================================

def test_escudeiro_dano_e_defesa_com_armadura():
    f_sem_arm = _cavaleiro(nivel=4, poderes=["CAVALEIRO_ESCUDEIRO"], itens=[])
    atualizar_ficha(f_sem_arm)
    assert f_sem_arm.combate.bonus_dano_geral == 1
    assert f_sem_arm.status.defesa.total == 11  # 10 + Des(1), sem armadura

    f_com_arm = _cavaleiro(nivel=4, poderes=["CAVALEIRO_ESCUDEIRO"], itens=["Armadura completa"])
    atualizar_ficha(f_com_arm)
    assert f_com_arm.status.defesa.total == 21  # 10 + 10 (armadura) + 1 (Escudeiro)


def test_etiqueta_e_pajem_pericias():
    f_base = _cavaleiro(nivel=4)
    atualizar_ficha(f_base)

    f_poderes = _cavaleiro(nivel=4, poderes=["CAVALEIRO_ETIQUETA", "CAVALEIRO_PAJEM"])
    atualizar_ficha(f_poderes)
    assert f_poderes.pericias["Diplomacia"].total == f_base.pericias["Diplomacia"].total + 4
    assert f_poderes.pericias["Nobreza"].total == f_base.pericias["Nobreza"].total + 2


def test_armadura_da_honra_e_estandarte_calc():
    f = _cavaleiro(nivel=14, car=3, poderes=["CAVALEIRO_ARMADURA_HONRA", "CAVALEIRO_ESTANDARTE"])
    atualizar_ficha(f)
    assert f.combate.cavaleiro_calc["armadura_honra_pv_temp"] == 17  # 14 + 3
    assert f.combate.cavaleiro_calc["estandarte_pm_temp"] == 3


# ===================================================================
# 3. Posturas de Combate (Torre Inabalável e Muralha Intransponível)
# ===================================================================

def test_postura_torre_inabalavel_soma_con_defesa_e_zera_deslocamento():
    f_sem = _cavaleiro(nivel=6, con=4, poderes=["CAVALEIRO_POSTURA_TORRE"], condicoes=[])
    atualizar_ficha(f_sem)

    f_com = _cavaleiro(nivel=6, con=4, poderes=["CAVALEIRO_POSTURA_TORRE"], condicoes=["torre_inabalavel"])
    atualizar_ficha(f_com)
    assert f_com.status.defesa.total == f_sem.status.defesa.total + 4
    assert f_com.status.deslocamento == 0


def test_postura_muralha_intransponivel_defesa_reflexos_e_deslocamento_3m():
    f_sem = _cavaleiro(
        nivel=6, poderes=["CAVALEIRO_POSTURA_MURALHA"],
        condicoes=[], itens=["Escudo pesado"],
    )
    atualizar_ficha(f_sem)

    f_com = _cavaleiro(
        nivel=6, poderes=["CAVALEIRO_POSTURA_MURALHA"],
        condicoes=["muralha_intransponivel"], itens=["Escudo pesado"],
    )
    atualizar_ficha(f_com)
    assert f_com.status.defesa.total == f_sem.status.defesa.total + 1
    assert f_com.pericias["Reflexos"].total == f_sem.pericias["Reflexos"].total + 1
    assert f_com.status.deslocamento == 3


# ===================================================================
# 4. Integridade completa do catálogo de Cavaleiro (6 fixas + 20 poderes)
# ===================================================================

FIXAS_ESPERADAS = {
    "Código de Honra": 1,
    "Baluarte": 1,
    "Duelo": 2,
    "Caminho do Cavaleiro": 5,
    "Resoluto": 11,
    "Bravura Final": 20,
}

PODERES_ESPERADOS = {
    "Armadura da Honra",
    "Aumento de Atributo",
    "Autoridade Feudal",
    "Desprezar os Covardes",
    "Escudeiro",
    "Especialização em Armadura",
    "Estandarte",
    "Etiqueta",
    "Investida Destruidora",
    "Montaria Corajosa",
    "Pajem",
    "Postura de Combate: Aríete Implacável",
    "Postura de Combate: Castigo de Ferro",
    "Postura de Combate: Foco de Batalha",
    "Postura de Combate: Muralha Intransponível",
    "Postura de Combate: Provocação Petulante",
    "Postura de Combate: Torre Inabalável",
    "Solidez",
    "Título",
    "Torre Armada",
}


def test_catalogo_cavaleiro_completo_26_entradas():
    entries = [v for v in DADOS_HABILIDADES_CLASSE.values() if v.get("classe") == "Cavaleiro"]
    fixas = {v["nome"]: v.get("nivel") for v in entries if v.get("tipo") == "Habilidade de Classe"}
    poderes = {v["nome"] for v in entries if v.get("tipo") == "Poder de Cavaleiro"}

    assert fixas == FIXAS_ESPERADAS
    assert poderes == PODERES_ESPERADOS
    assert len(entries) == 26
    assert all(v.get("efeitos") for v in entries)


def test_posturas_de_combate_seguem_regra_base():
    posturas = [
        v for v in DADOS_HABILIDADES_CLASSE.values()
        if v.get("classe") == "Cavaleiro" and v["nome"].startswith("Postura de Combate:")
    ]
    assert len(posturas) == 6
    for p in posturas:
        pc = p["efeitos"]["postura_combate"]
        assert pc["acao"] == "movimento"
        assert pc["custo_pm"] == 2
        assert pc["duracao"] == "cena"
