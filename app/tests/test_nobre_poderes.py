"""Nobre — testes de poderes de classe e cobertura completa do catálogo (T20 JdA p.78-80)."""
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Habilidade, Item
from src.dados_habilidades_classe import DADOS_HABILIDADES_CLASSE
from src.regras import atualizar_ficha


def _nobre(nivel=10, des=1, car=5, poderes=None, itens=None):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Shivara", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Nobre", nivel=nivel, primaria=True)]
    f.atributos_base = Atributos(destreza=des, carisma=car, constituicao=2)
    f.atributos = f.atributos_base.model_copy()
    for chave in (poderes or []):
        d = DADOS_HABILIDADES_CLASSE[chave]
        f.habilidades.append(Habilidade(
            nome=d["nome"],
            tipo=d["tipo"],
            descricao=d["descricao"],
            efeitos=dict(d.get("efeitos", {})),
            fonte="Poder de Nobre",
        ))
    for nome_item in (itens or []):
        f.inventario.equipamentos.append(Item(nome=nome_item, equipado=True))
    return f


def test_armadura_brilhante_soma_car_com_armadura_pesada():
    f = _nobre(nivel=8, des=1, car=5, poderes=["NOBRE_ARMADURA_BRILHANTE"], itens=["Armadura completa"])
    atualizar_ficha(f)
    assert f.status.defesa.total == 25  # 10 + 10 (armadura) + 5 (Car)


def test_grito_tiranico_e_voz_poderosa():
    f_base = _nobre(nivel=10, car=5)
    atualizar_ficha(f_base)

    f = _nobre(nivel=10, car=5, poderes=["NOBRE_GRITO_TIRANICO", "NOBRE_VOZ_PODEROSA"])
    atualizar_ficha(f)
    assert f.combate.nobre_calc["palavras_afiadas"]["formula"] == "6d8"
    assert f.combate.nobre_calc["alcance_habilidades"] == "Médio"
    assert f.pericias["Diplomacia"].total == f_base.pericias["Diplomacia"].total + 2
    assert f.pericias["Intimidação"].total == f_base.pericias["Intimidação"].total + 2


FIXAS_ESPERADAS = {
    "Autoconfiança": 1,
    "Espólio": 1,
    "Orgulho": 1,
    "Palavras Afiadas": 2,
    "Riqueza": 3,
    "Gritar Ordens": 4,
    "Presença Aristocrática": 5,
    "Realeza": 20,
}

PODERES_ESPERADOS = {
    "Armadura Brilhante",
    "Aumento de Atributo",
    "Autoridade Feudal",
    "Educação Privilegiada",
    "Estrategista",
    "Favor",
    "General",
    "Grito Tirânico",
    "Inspirar Confiança",
    "Inspirar Glória",
    "Jogo da Corte",
    "Liderar pelo Exemplo",
    "Língua de Ouro",
    "Língua de Prata",
    "Língua Rápida",
    "Presença Majestosa",
    "Título",
    "Voz Poderosa",
}


def test_catalogo_nobre_completo_26_entradas():
    entries = [v for v in DADOS_HABILIDADES_CLASSE.values() if v.get("classe") == "Nobre" and v.get("fonte", "T20 JdA") == "T20 JdA"]
    fixas = {v["nome"]: v.get("nivel") for v in entries if v.get("tipo") == "Habilidade de Classe"}
    poderes = {v["nome"] for v in entries if v.get("tipo") == "Poder de Nobre"}

    assert fixas == FIXAS_ESPERADAS
    assert poderes == PODERES_ESPERADOS
    assert len(entries) == 26
    assert all(v.get("efeitos") for v in entries)
