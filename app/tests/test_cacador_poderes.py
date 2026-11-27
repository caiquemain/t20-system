"""Caçador — testes de poderes de classe e cobertura completa do catálogo (T20 JdA p.49-51)."""
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Habilidade, Item
from src.dados_habilidades_classe import DADOS_HABILIDADES_CLASSE
from src.regras import atualizar_ficha


def _cacador(nivel=6, des=3, sab=4, poderes=None, condicoes=None, itens=None):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Ellisa", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Caçador", nivel=nivel, primaria=True)]
    f.atributos_base = Atributos(destreza=des, sabedoria=sab, constituicao=1)
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
            fonte="Poder de Caçador",
        ))
    for nome_item in (itens or []):
        f.inventario.equipamentos.append(Item(nome=nome_item, equipado=True))
    return f


# ===================================================================
# 1. Arqueiro (+Sab dano à distância limitado pelo nível)
# ===================================================================

def test_arqueiro_soma_sabedoria_no_dano_a_distancia_limitado_pelo_nivel():
    # Nível 2 com Sab 4: limitado a +2 em Arco longo (À Distância); Espada longa não recebe.
    f = _cacador(
        nivel=2, sab=4,
        poderes=["CACADOR_ARQUEIRO"],
        itens=["Arco longo", "Espada longa"],
    )
    atualizar_ficha(f)
    por_nome = {a.nome: a for a in f.combate.ataques}
    assert por_nome["Arco longo"].dano == "1d8+2"
    assert "Arqueiro (+2 dano)" in por_nome["Arco longo"].especial
    assert por_nome["Espada longa"].dano == "1d8"


# ===================================================================
# 2. Elo com a Natureza (+Sab PM + Caminhos da Natureza)
# ===================================================================

def test_elo_com_a_natureza_soma_sab_pm_e_concede_magia():
    f = _cacador(nivel=4, sab=3, poderes=["CACADOR_ELO_NATUREZA"])
    atualizar_ficha(f)
    # PM: 4*4 = 16 + 3 (Sab) = 19
    assert f.status.pm.maximo == 19
    magia = next((m for m in f.combate.magias if m.nome == "Caminhos da Natureza"), None)
    assert magia is not None
    assert magia.atributo_chave == "sab"


# ===================================================================
# 3. Escaramuça e Escaramuça Superior
# ===================================================================

def test_escaramuca_e_superior_defesa_reflexos_e_bloqueio_armadura_pesada():
    # Escaramuça ativa (sem armadura pesada): +2 Defesa, +2 Reflexos, +1d8 dano
    f_base = _cacador(nivel=6, des=3, poderes=["CACADOR_ESCARAMUCA"], condicoes=[], itens=["Arco curto"])
    atualizar_ficha(f_base)
    f_esc = _cacador(nivel=6, des=3, poderes=["CACADOR_ESCARAMUCA"], condicoes=["escaramuca"], itens=["Arco curto"])
    atualizar_ficha(f_esc)
    assert f_esc.status.defesa.total == f_base.status.defesa.total + 2
    assert f_esc.pericias["Reflexos"].total == f_base.pericias["Reflexos"].total + 2
    assert "Escaramuça (+1d8 dano)" in f_esc.combate.ataques[0].especial

    # Escaramuça Superior substitui por +5 Defesa, +5 Reflexos, +1d12 dano
    f_sup = _cacador(
        nivel=12, des=3,
        poderes=["CACADOR_ESCARAMUCA", "CACADOR_ESCARAMUCA_SUPERIOR"],
        condicoes=["escaramuca"],
        itens=["Arco curto"],
    )
    atualizar_ficha(f_sup)
    assert f_sup.status.defesa.total == 10 + 3 + 5
    assert "Escaramuça Superior (+1d12 dano)" in f_sup.combate.ataques[0].especial

    # Armadura pesada bloqueia Escaramuça
    f_pesada = _cacador(
        nivel=6, des=3,
        poderes=["CACADOR_ESCARAMUCA"],
        condicoes=["escaramuca"],
        itens=["Armadura completa", "Arco curto"],
    )
    atualizar_ficha(f_pesada)
    assert f_pesada.status.defesa.total == 20  # 10 + 10 armadura completa (sem Des, sem Escaramuça)
    assert all("Escaramuça" not in s for s in f_pesada.pericias["Reflexos"].fontes_bonus)


# ===================================================================
# 4. Olho do Falcão, Espreitar, Ponto Fraco
# ===================================================================

def test_poderes_de_marca_da_presa():
    f = _cacador(
        nivel=9,
        poderes=["CACADOR_OLHO_FALCAO", "CACADOR_ESPREITAR", "CACADOR_PONTO_FRACO"],
    )
    atualizar_ficha(f)
    mp = f.combate.marca_presa_calc
    assert mp["alcance"] == "Longo"
    assert mp["espreitar_bonus_max"] == 3  # nv 9 -> 3 PM max
    assert mp["ponto_fraco_margem"] == 2


# ===================================================================
# 5. Integridade completa do catálogo de Caçador (5 fixas + 23 poderes)
# ===================================================================

FIXAS_ESPERADAS = {
    "Marca da Presa": 1,
    "Rastreador": 1,
    "Explorador": 3,
    "Caminho do Explorador": 5,
    "Mestre Caçador": 20,
}

PODERES_ESPERADOS = {
    "Ambidestria",
    "Armadilha: Arataca",
    "Armadilha: Espinhos",
    "Armadilha: Laço",
    "Armadilha: Rede",
    "Armadilheiro",
    "Arqueiro",
    "Aumento de Atributo",
    "Bote",
    "Camuflagem",
    "Chuva de Lâminas",
    "Companheiro Animal",
    "Elo com a Natureza",
    "Emboscar",
    "Empatia Selvagem",
    "Escaramuça",
    "Escaramuça Superior",
    "Espreitar",
    "Ervas Curativas",
    "Ímpeto",
    "Inimigo de (Criatura)",
    "Olho do Falcão",
    "Ponto Fraco",
}


def test_catalogo_cacador_completo_28_entradas():
    entries = [v for v in DADOS_HABILIDADES_CLASSE.values() if v.get("classe") == "Caçador" and v.get("fonte", "T20 JdA") == "T20 JdA"]
    fixas = {v["nome"]: v.get("nivel") for v in entries if v.get("tipo") == "Habilidade de Classe"}
    poderes = {v["nome"] for v in entries if v.get("tipo") == "Poder de Caçador"}

    assert fixas == FIXAS_ESPERADAS
    assert poderes == PODERES_ESPERADOS
    assert len(entries) == 28
    assert all(v.get("efeitos") for v in entries)


def test_armadilhas_seguem_regra_base():
    armadilhas = [
        "CACADOR_ARMADILHA_ARATACA",
        "CACADOR_ARMADILHA_ESPINHOS",
        "CACADOR_ARMADILHA_LACO",
        "CACADOR_ARMADILHA_REDE",
    ]
    for chave in armadilhas:
        a = DADOS_HABILIDADES_CLASSE[chave]["efeitos"]["armadilha"]
        assert a["acao"] == "completa"
        assert a["custo_pm"] == 3
        assert a["area"] == "3m"
