"""Inventor — testes de poderes de classe, engenhocas, alquimia e cobertura (T20 JdA p.67-71)."""
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Habilidade, Item
from src.dados_habilidades_classe import DADOS_HABILIDADES_CLASSE
from src.regras import atualizar_ficha


def _inventor(nivel=10, des=1, inte=5, sab=3, poderes=None, itens=None):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Niebling", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Inventor", nivel=nivel, primaria=True)]
    f.atributos_base = Atributos(forca=0, destreza=des, constituicao=1, inteligencia=inte, sabedoria=sab)
    f.atributos = f.atributos_base.model_copy()
    for chave in (poderes or []):
        d = DADOS_HABILIDADES_CLASSE[chave]
        f.habilidades.append(Habilidade(
            nome=d["nome"],
            tipo=d["tipo"],
            descricao=d["descricao"],
            efeitos=dict(d.get("efeitos", {})),
            fonte="Poder de Inventor",
        ))
    for nome_item in (itens or []):
        f.inventario.equipamentos.append(Item(nome=nome_item, equipado=True))
    return f


def test_couraceiro_e_blindagem_defesa():
    # Couraceiro com armadura leve (Armadura de couro +2): 10 + Int(5) + 2 = 17 (troca Des 1 por Int 5)
    f_leve = _inventor(nivel=4, des=1, inte=5, poderes=["INVENTOR_COURACEIRO"], itens=["Armadura de couro"])
    atualizar_ficha(f_leve)
    assert f_leve.status.defesa.total == 17
    assert "Armaduras Pesadas" in f_leve.status.proficiencias
    assert "Escudos" in f_leve.status.proficiencias

    # Couraceiro sozinho com armadura pesada (Armadura completa +10): não soma Des nem Int -> 20
    f_pesada_sem = _inventor(nivel=8, des=1, inte=5, poderes=["INVENTOR_COURACEIRO"], itens=["Armadura completa"])
    atualizar_ficha(f_pesada_sem)
    assert f_pesada_sem.status.defesa.total == 20

    # Couraceiro + Blindagem com armadura pesada: 10 + 10 + Int(5) = 25
    f_blind = _inventor(
        nivel=8, des=1, inte=5,
        poderes=["INVENTOR_COURACEIRO", "INVENTOR_BLINDAGEM"],
        itens=["Armadura completa"],
    )
    atualizar_ficha(f_blind)
    assert f_blind.status.defesa.total == 25


def test_engenhoqueiro_e_manutencao_eficiente():
    f1 = _inventor(nivel=10, inte=5, poderes=["INVENTOR_ENGENHOQUEIRO"])
    atualizar_ficha(f1)
    assert f1.combate.inventor_calc["limite_engenhocas"] == 5
    assert f1.combate.inventor_calc["circulo_engenhoca"] == 3

    f2 = _inventor(nivel=18, inte=5, poderes=["INVENTOR_ENGENHOQUEIRO", "INVENTOR_MANUTENCAO_EFICIENTE"])
    atualizar_ficha(f2)
    assert f2.combate.inventor_calc["limite_engenhocas"] == 8  # 5 + 3
    assert f2.combate.inventor_calc["circulo_engenhoca"] == 5


def test_alquimista_iniciado_mestre_e_conhecimento_formulas():
    f1 = _inventor(nivel=6, poderes=["INVENTOR_ALQUIMISTA_INICIADO"])
    atualizar_ficha(f1)
    assert f1.combate.inventor_calc["circulo_pocao"] == 2
    assert f1.combate.inventor_calc["formulas_total"] == 8  # 3 + 5

    f2 = _inventor(nivel=14, poderes=[
        "INVENTOR_ALQUIMISTA_INICIADO",
        "INVENTOR_MESTRE_ALQUIMISTA",
        "INVENTOR_CONHECIMENTO_FORMULAS",
        "INVENTOR_CONHECIMENTO_FORMULAS",
    ])
    atualizar_ficha(f2)
    assert f2.combate.inventor_calc["circulo_pocao"] == 4
    assert f2.combate.inventor_calc["formulas_total"] == 22  # 3 + 13 + 6


def test_armeiro_e_balistica_anotam_inteligencia():
    f = _inventor(
        nivel=5, des=1, inte=5,
        poderes=["INVENTOR_ARMEIRO", "INVENTOR_BALISTICA"],
        itens=["Espada longa", "Pistola"],
    )
    atualizar_ficha(f)
    por_nome = {a.nome: a for a in f.combate.ataques}
    assert "Armeiro (Int +5 ataque/dano)" in por_nome["Espada longa"].especial
    assert "Balística (Int +5 ataque)" in por_nome["Pistola"].especial


FIXAS_ESPERADAS = {
    "Engenhosidade": 1,
    "Protótipo": 1,
    "Fabricar Item Superior": 2,
    "Comerciante": 3,
    "Encontrar Fraqueza": 7,
    "Fabricar Item Mágico": 9,
    "Olho do Dragão": 10,
    "Obra-Prima": 20,
}

PODERES_ESPERADOS = {
    "Agite Antes de Usar",
    "Ajuste de Mira",
    "Alquimista de Batalha",
    "Alquimista Iniciado",
    "Armeiro",
    "Ativação Rápida",
    "Aumento de Atributo",
    "Autômato",
    "Autômato Prototipado",
    "Balística",
    "Blindagem",
    "Cano Raiado",
    "Catalisador Instável",
    "Chutes e Palavrões",
    "Conhecimento de Fórmulas",
    "Couraceiro",
    "Engenhoqueiro",
    "Farmacêutico",
    "Ferreiro",
    "Granadeiro",
    "Homúnculo",
    "Invenção Potente",
    "Maestria em Perícia",
    "Manutenção Eficiente",
    "Mestre Alquimista",
    "Mestre Cuca",
    "Mistura Fervilhante",
    "Oficina de Campo",
    "Pedra de Amolar",
    "Síntese Rápida",
}


def test_catalogo_inventor_completo_38_entradas():
    entries = [v for v in DADOS_HABILIDADES_CLASSE.values() if v.get("classe") == "Inventor"]
    fixas = {v["nome"]: v.get("nivel") for v in entries if v.get("tipo") == "Habilidade de Classe"}
    poderes = {v["nome"] for v in entries if v.get("tipo") == "Poder de Inventor"}

    assert fixas == FIXAS_ESPERADAS
    assert poderes == PODERES_ESPERADOS
    assert len(entries) == 38
    assert all(v.get("efeitos") for v in entries)
