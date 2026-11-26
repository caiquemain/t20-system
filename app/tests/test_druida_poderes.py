"""Druida — testes de poderes de classe e cobertura completa do catálogo (T20 JdA p.60-63)."""
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Habilidade
from src.dados_habilidades_classe import DADOS_HABILIDADES_CLASSE
from src.regras import atualizar_ficha


def _druida(nivel=6, sab=4, poderes=None):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Lisandra", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Druida", nivel=nivel, primaria=True)]
    f.atributos_base = Atributos(sabedoria=sab, constituicao=2, destreza=2)
    f.atributos = f.atributos_base.model_copy()
    for chave in (poderes or []):
        d = DADOS_HABILIDADES_CLASSE[chave]
        f.habilidades.append(Habilidade(
            nome=d["nome"],
            tipo=d["tipo"],
            descricao=d["descricao"],
            efeitos=dict(d.get("efeitos", {})),
            fonte="Poder de Druida",
        ))
    return f


def test_segredos_da_natureza_e_aspectos_aumentam_magias_conhecidas():
    # Nível 4 base: 2 iniciais + 2 pares = 4
    f0 = _druida(nivel=4)
    atualizar_ficha(f0)
    assert f0.combate.limite_magias == 4

    # 2x Segredos da Natureza (+4) + Aspecto do Inverno (+1) + Aspecto do Verão (+1) = 10
    f1 = _druida(nivel=4, poderes=[
        "DRUIDA_SEGREDOS_NATUREZA",
        "DRUIDA_SEGREDOS_NATUREZA",
        "DRUIDA_ASPECTO_INVERNO",
        "DRUIDA_ASPECTO_VERAO",
    ])
    atualizar_ficha(f1)
    assert f1.combate.limite_magias == 10


def test_aspecto_do_inverno_concede_rd_frio_5():
    f = _druida(nivel=4, poderes=["DRUIDA_ASPECTO_INVERNO"])
    atualizar_ficha(f)
    assert "frio 5" in f.status.rd
    assert any("Aspecto do Inverno" in e for e in f.status.efeitos_ativos)


def test_poderes_de_resistencia_druida():
    f_base = _druida(nivel=6)
    atualizar_ficha(f_base)

    f_res = _druida(nivel=6, poderes=[
        "DRUIDA_FORCA_PENHASCOS",
        "DRUIDA_LIBERDADE_PRADARIA",
        "DRUIDA_TRANQUILIDADE_LAGOS",
    ])
    atualizar_ficha(f_res)
    assert f_res.pericias["Fortitude"].total == f_base.pericias["Fortitude"].total + 2
    assert f_res.pericias["Reflexos"].total == f_base.pericias["Reflexos"].total + 2
    assert f_res.pericias["Vontade"].total == f_base.pericias["Vontade"].total + 2


def test_efeitos_ativos_druida():
    f = _druida(nivel=18, poderes=[
        "DRUIDA_CORACAO_SELVA",
        "DRUIDA_MAGIA_NATURAL",
        "DRUIDA_PRESAS_AFIADAS",
        "DRUIDA_FORMA_PRIMAL",
    ])
    atualizar_ficha(f)
    txt = " | ".join(f.status.efeitos_ativos)
    assert "Coração da Selva" in txt
    assert "Magia Natural" in txt
    assert "Presas Afiadas" in txt
    assert "Forma Primal" in txt


FIXAS_ESPERADAS = {
    "Devoto Fiel (Druida)": 1,
    "Empatia Selvagem": 1,
    "Magias (Druida)": 1,
    "Caminho dos Ermos": 2,
    "Força da Natureza": 20,
}

PODERES_ESPERADOS = {
    "Aspecto do Inverno",
    "Aspecto do Outono",
    "Aspecto da Primavera",
    "Aspecto do Verão",
    "Aumento de Atributo",
    "Companheiro Animal",
    "Companheiro Animal Aprimorado",
    "Companheiro Animal Lendário",
    "Companheiro Animal Mágico",
    "Coração da Selva",
    "Espírito dos Equinócios",
    "Espírito dos Solstícios",
    "Força dos Penhascos",
    "Forma Primal",
    "Forma Selvagem",
    "Forma Selvagem Aprimorada",
    "Forma Selvagem Superior",
    "Liberdade da Pradaria",
    "Magia Natural",
    "Presas Afiadas",
    "Segredos da Natureza",
    "Tranquilidade dos Lagos",
}


def test_catalogo_druida_completo_27_entradas():
    entries = [v for v in DADOS_HABILIDADES_CLASSE.values() if v.get("classe") == "Druida"]
    fixas = {v["nome"]: v.get("nivel") for v in entries if v.get("tipo") == "Habilidade de Classe"}
    poderes = {v["nome"] for v in entries if v.get("tipo") == "Poder de Druida"}

    assert fixas == FIXAS_ESPERADAS
    assert poderes == PODERES_ESPERADOS
    assert len(entries) == 27
    assert all(v.get("efeitos") for v in entries)
