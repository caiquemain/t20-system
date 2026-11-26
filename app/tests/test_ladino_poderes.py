"""Ladino — testes de poderes de classe e cobertura completa do catálogo (T20 JdA p.72-74)."""
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Habilidade
from src.dados_habilidades_classe import DADOS_HABILIDADES_CLASSE
from src.regras import atualizar_ficha


def _ladino(nivel=7, des=4, inte=3, poderes=None, condicoes=None):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Drikka", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Ladino", nivel=nivel, primaria=True)]
    f.atributos_base = Atributos(destreza=des, inteligencia=inte, constituicao=1)
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
            fonte="Poder de Ladino",
        ))
    return f


def test_mente_criminosa_sombra_e_gatuno():
    f_base = _ladino(nivel=4, des=4, inte=3)
    atualizar_ficha(f_base)

    f_pod = _ladino(nivel=4, des=4, inte=3, poderes=[
        "LADINO_MENTE_CRIMINOSA",
        "LADINO_SOMBRA",
        "LADINO_GATUNO",
    ])
    atualizar_ficha(f_pod)
    # Mente Criminosa: +Int(3) em Ladinagem e Furtividade; Sombra: +2 Furtividade; Gatuno: +2 Atletismo
    assert f_pod.pericias["Ladinagem"].total == f_base.pericias["Ladinagem"].total + 3
    assert f_pod.pericias["Furtividade"].total == f_base.pericias["Furtividade"].total + 5
    assert f_pod.pericias["Atletismo"].total == f_base.pericias["Atletismo"].total + 2


def test_assassinar_e_roubo_de_mana():
    f = _ladino(nivel=7, poderes=["LADINO_ASSASSINAR", "LADINO_ROUBO_MANA"])
    atualizar_ficha(f)
    af = f.combate.ataque_furtivo_calc
    assert af["formula"] == "4d6"
    assert af["assassinar_formula"] == "8d6"
    assert af["roubo_mana_pm"] == 4


def test_fuga_formidavel_deslocamento_e_pericias():
    f_sem = _ladino(nivel=4, poderes=["LADINO_FUGA_FORMIDAVEL"], condicoes=[])
    atualizar_ficha(f_sem)

    f_com = _ladino(nivel=4, poderes=["LADINO_FUGA_FORMIDAVEL"], condicoes=["fuga_formidavel"])
    atualizar_ficha(f_com)
    assert f_com.status.deslocamento == f_sem.status.deslocamento + 3
    assert f_com.pericias["Acrobacia"].total == f_sem.pericias["Acrobacia"].total + 5
    assert f_com.pericias["Atletismo"].total == f_sem.pericias["Atletismo"].total + 5


FIXAS_ESPERADAS = {
    "Ataque Furtivo": 1,
    "Especialista": 1,
    "Evasão": 2,
    "Esquiva Sobrenatural": 4,
    "Olhos nas Costas": 8,
    "Evasão Aprimorada": 10,
    "A Pessoa Certa para o Trabalho": 20,
}

PODERES_ESPERADOS = {
    "Assassinar",
    "Aumento de Atributo",
    "Contatos no Submundo",
    "Emboscar",
    "Escapista",
    "Fuga Formidável",
    "Gatuno",
    "Ladrão Arcano",
    "Mão na Boca",
    "Mãos Rápidas",
    "Mente Criminosa",
    "Oportunismo",
    "Rolamento Defensivo",
    "Roubo de Mana",
    "Saqueador de Tumbas",
    "Sombra",
    "Truque Mágico",
    "Velocidade Ladina",
    "Veneno Persistente",
    "Veneno Potente",
}


def test_catalogo_ladino_completo_27_entradas():
    entries = [v for v in DADOS_HABILIDADES_CLASSE.values() if v.get("classe") == "Ladino"]
    fixas = {v["nome"]: v.get("nivel") for v in entries if v.get("tipo") == "Habilidade de Classe"}
    poderes = {v["nome"] for v in entries if v.get("tipo") == "Poder de Ladino"}

    assert fixas == FIXAS_ESPERADAS
    assert poderes == PODERES_ESPERADOS
    assert len(entries) == 27
    assert all(v.get("efeitos") for v in entries)
