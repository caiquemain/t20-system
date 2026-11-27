"""Guerreiro — testes de poderes de classe e cobertura completa do catálogo (T20 JdA p.64-66)."""
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Habilidade, Item
from src.dados_habilidades_classe import DADOS_HABILIDADES_CLASSE
from src.regras import atualizar_ficha


def _guerreiro(nivel=12, forca=4, inte=3, sab=3, poderes=None, itens=None):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Katabrok", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Guerreiro", nivel=nivel, primaria=True)]
    f.atributos_base = Atributos(forca=forca, destreza=2, constituicao=3, inteligencia=inte, sabedoria=sab)
    f.atributos = f.atributos_base.model_copy()
    for item in (poderes or []):
        if isinstance(item, tuple):
            chave, escolhas = item
        else:
            chave, escolhas = item, {}
        d = DADOS_HABILIDADES_CLASSE[chave]
        f.habilidades.append(Habilidade(
            nome=d["nome"],
            tipo=d["tipo"],
            descricao=d["descricao"],
            efeitos=dict(d.get("efeitos", {})),
            escolhas_aplicadas=dict(escolhas),
            fonte="Poder de Guerreiro",
        ))
    for nome_item in (itens or []):
        f.inventario.equipamentos.append(Item(nome=nome_item, equipado=True))
    return f


def test_especializacao_e_mestre_em_arma():
    f = _guerreiro(
        nivel=12,
        poderes=[
            ("GUERREIRO_ESPECIALIZACAO_ARMA", {"arma": "Espada longa"}),
            ("GUERREIRO_MESTRE_ARMA", {"arma": "Espada longa"}),
        ],
        itens=["Espada longa", "Machado de batalha"],
    )
    atualizar_ficha(f)
    por_nome = {a.nome: a for a in f.combate.ataques}
    assert por_nome["Espada longa"].dano == "1d8+2"
    assert "Especialização em Arma (+2 dano)" in por_nome["Espada longa"].especial
    assert "Mestre em Arma (+1 passo de dano)" in por_nome["Espada longa"].especial
    assert por_nome["Machado de batalha"].dano == "1d8"


def test_guerreiro_arqueiro_esgrimista_solidez_e_especializacao_armadura():
    f = _guerreiro(
        nivel=12, inte=3, sab=3,
        poderes=[
            "GUERREIRO_ARQUEIRO",
            "GUERREIRO_ESGRIMISTA",
            "GUERREIRO_SOLIDEZ",
            "GUERREIRO_ESPECIALIZACAO_ARMADURA",
            "GUERREIRO_ROMPER_RESISTENCIAS",
        ],
        itens=["Arco longo", "Florete", "Armadura completa", "Escudo pesado"],
    )
    atualizar_ficha(f)
    por_nome = {a.nome: a for a in f.combate.ataques}
    assert por_nome["Arco longo"].dano == "1d8+3"
    assert por_nome["Florete"].dano == "1d6+3"
    assert "geral 5" in f.status.rd
    assert f.combate.ataque_especial_calc["romper_resistencias"] is True
    assert any("Solidez" in s for s in f.pericias["Vontade"].fontes_bonus)


def test_golpe_pessoal_tem_todos_os_17_efeitos_oficiais():
    gp = DADOS_HABILIDADES_CLASSE["GUERREIRO_GOLPE_PESSOAL"]["efeitos"]["efeitos_disponiveis"]
    assert len(gp) == 17
    assert gp["Amplo"] == 3
    assert gp["Lento"] == -2
    assert gp["Perto da Morte"] == -2
    assert gp["Sacrifício"] == -2


FIXAS_ESPERADAS = {
    "Ataque Especial": 1,
    "Durão": 3,
    "Ataque Extra": 6,
    "Campeão": 20,
}

PODERES_ESPERADOS = {
    "Ambidestria",
    "Arqueiro",
    "Ataque Reflexo",
    "Aumento de Atributo",
    "Bater e Correr",
    "Destruidor",
    "Esgrimista",
    "Especialização em Arma",
    "Especialização em Armadura",
    "Golpe de Raspão",
    "Golpe Demolidor",
    "Golpe Pessoal",
    "Ímpeto",
    "Mestre em Arma",
    "Planejamento Marcial",
    "Romper Resistências",
    "Solidez",
    "Tornado de Dor",
    "Valentão",
}


def test_catalogo_guerreiro_completo_23_entradas():
    entries = [v for v in DADOS_HABILIDADES_CLASSE.values() if v.get("classe") == "Guerreiro" and v.get("fonte", "T20 JdA") == "T20 JdA"]
    fixas = {v["nome"]: v.get("nivel") for v in entries if v.get("tipo") == "Habilidade de Classe"}
    poderes = {v["nome"] for v in entries if v.get("tipo") == "Poder de Guerreiro"}

    assert fixas == FIXAS_ESPERADAS
    assert poderes == PODERES_ESPERADOS
    assert len(entries) == 23
    assert all(v.get("efeitos") for v in entries)
