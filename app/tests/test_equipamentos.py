"""Motor de equipamento (T20 JdA, Capítulo 3): catálogo, carga, ataques, defesa."""
import pytest

from src.models import Personagem, Item
from src.dados_equipamentos import DADOS_ARMAS, DADOS_ARMADURAS
from src.regras.inventario import (
    catalogo_do_item,
    sincronizar_carga,
    sincronizar_ataques_equipamento,
    calcular_penalidade_armadura,
)
from src.regras.status import calcular_defesa_e_deslocamento, calcular_modificador


def _ficha_com(*itens):
    p = Personagem()
    for it in itens:
        p.inventario.equipamentos.append(it)
    return p


def _set_des(ficha, mod):
    """atributos guardam o modificador direto (point-buy), ex.: destreza=2."""
    ficha.atributos.destreza = mod


# --- Catálogo ---

def test_catalogo_armas_completo():
    assert len(DADOS_ARMAS) >= 40
    t = DADOS_ARMAS["Tridente"]
    assert t["dano"] == "1d8"
    assert t["categoria"] == "Marcial"
    assert "versátil" in t["habilidades"]
    assert t["arremessavel"] is True


def test_catalogo_armaduras_completo():
    assert len(DADOS_ARMADURAS) == 12
    c = DADOS_ARMADURAS["Armadura completa"]
    assert c["bonus_defesa"] == 10
    assert c["penalidade_armadura"] == -5
    assert c["espacos"] == 5
    assert c["tipo_armadura"] == "Pesada"


def test_catalogo_do_item_desconhecido():
    assert catalogo_do_item("Item inexistente") is None


# --- Carga ---

def test_carga_limite_base():
    p = _ficha_com()
    sincronizar_carga(p)
    assert p.inventario.carga_maxima == 10
    assert p.inventario.carga_total == 0
    assert p.inventario.sobrecargado is False


def test_carga_soma_espacos_do_catalogo():
    p = _ficha_com(
        Item(nome="Espada longa", tipo="Arma", equipado=True),
        Item(nome="Armadura de couro", tipo="Armadura"),
    )
    sincronizar_carga(p)
    assert p.inventario.carga_total == 3  # 1 espada + 2 couro


def test_carga_multiplica_quantidade():
    p = _ficha_com(Item(nome="Adaga", tipo="Arma", qtd=3))
    sincronizar_carga(p)
    assert p.inventario.carga_total == 3


def test_sobrecarga_acima_do_limite():
    p = _ficha_com(
        Item(nome="Armadura completa", tipo="Armadura"),  # 5
        Item(nome="Montante", tipo="Arma"),               # 2
        Item(nome="Arco longo", tipo="Arma"),             # 2
        Item(nome="Besta pesada", tipo="Arma"),           # 2 = 11
    )
    sincronizar_carga(p)
    assert p.inventario.carga_total == 11
    assert p.inventario.sobrecargado is True


# --- Ataques de equipamento ---

def test_arma_empunhada_gera_ataque():
    p = _ficha_com(Item(nome="Espada longa", tipo="Arma", equipado=True))
    sincronizar_ataques_equipamento(p)
    eq = [a for a in p.combate.ataques if a.fonte == "Equipamento"]
    assert len(eq) == 1
    assert eq[0].teste == "Luta"
    assert eq[0].dano == "1d8"
    assert eq[0].tipo == "Corte"


def test_arma_guardada_nao_gera_ataque():
    p = _ficha_com(Item(nome="Espada longa", tipo="Arma", equipado=False))
    sincronizar_ataques_equipamento(p)
    assert not [a for a in p.combate.ataques if a.fonte == "Equipamento"]


def test_arma_de_distancia_usa_pontaria():
    p = _ficha_com(Item(nome="Arco curto", tipo="Arma", equipado=True))
    sincronizar_ataques_equipamento(p)
    a = [a for a in p.combate.ataques if a.fonte == "Equipamento"][0]
    assert a.teste == "Pontaria"
    assert a.alcance == "Médio"


def test_municao_nao_gera_ataque():
    p = _ficha_com(Item(nome="Flechas (20)", tipo="Munição", equipado=True))
    sincronizar_ataques_equipamento(p)
    assert not [a for a in p.combate.ataques if a.fonte == "Equipamento"]


def test_nao_proficiente_sofre_penalidade():
    p = _ficha_com(Item(nome="Espada longa", tipo="Arma", equipado=True))
    sincronizar_ataques_equipamento(p)
    a = [a for a in p.combate.ataques if a.fonte == "Equipamento"][0]
    assert "-5" in a.especial


def test_proficiente_nao_sofre_penalidade():
    p = _ficha_com(Item(nome="Adaga", tipo="Arma", equipado=True))
    p.proficiencias = ["Armas Simples"]
    sincronizar_ataques_equipamento(p)
    a = [a for a in p.combate.ataques if a.fonte == "Equipamento"][0]
    assert "-5" not in a.especial


def test_resincronizar_nao_duplica_ataques():
    p = _ficha_com(Item(nome="Espada longa", tipo="Arma", equipado=True))
    sincronizar_ataques_equipamento(p)
    sincronizar_ataques_equipamento(p)
    assert len([a for a in p.combate.ataques if a.fonte == "Equipamento"]) == 1


# --- Defesa ---

def test_defesa_com_armadura_leve():
    p = _ficha_com(Item(nome="Armadura de couro", tipo="Armadura", equipado=True))
    calcular_defesa_e_deslocamento(p)
    assert p.status.defesa_calc.total == 12
    fontes = {f.fonte: f.valor for f in p.status.defesa_calc.fontes}
    assert fontes["Equipamento: Armadura de couro"] == 2


def test_defesa_acumula_armadura_e_escudo():
    p = _ficha_com(
        Item(nome="Cota de malha", tipo="Armadura", equipado=True),
        Item(nome="Escudo pesado", tipo="Escudo", equipado=True),
    )
    calcular_defesa_e_deslocamento(p)
    assert p.status.defesa_calc.total == 18


def test_armadura_pesada_ignora_destreza():
    p = _ficha_com(Item(nome="Cota de malha", tipo="Armadura", equipado=True))
    _set_des(p, 2)
    calcular_defesa_e_deslocamento(p)
    assert not [f for f in p.status.defesa_calc.fontes if f.fonte == "Destreza"]


def test_armadura_leve_mantem_destreza():
    p = _ficha_com(Item(nome="Armadura de couro", tipo="Armadura", equipado=True))
    _set_des(p, 2)
    calcular_defesa_e_deslocamento(p)
    assert [f for f in p.status.defesa_calc.fontes if f.fonte == "Destreza"]


# --- Deslocamento ---

def test_pesada_reduz_deslocamento():
    p = _ficha_com(Item(nome="Cota de malha", tipo="Armadura", equipado=True))
    calcular_defesa_e_deslocamento(p)
    assert p.status.deslocamento_calc.total == 6


def test_sobrecarga_reduz_deslocamento():
    p = _ficha_com(
        Item(nome="Armadura completa", tipo="Armadura"),
        Item(nome="Montante", tipo="Arma"),
        Item(nome="Arco longo", tipo="Arma"),
        Item(nome="Besta pesada", tipo="Arma"),
    )
    sincronizar_carga(p)
    calcular_defesa_e_deslocamento(p)
    assert p.status.deslocamento_calc.total == 6


def test_imunidade_penalidade_mov_protege_deslocamento():
    p = _ficha_com(Item(nome="Cota de malha", tipo="Armadura", equipado=True))

    class _Hab:
        nome = "Passos Leves"
        tipo = "Poder"
        efeitos = {"imunidade_penalidade_mov": True}
        escolhas_aplicadas = {}

    p.habilidades = [_Hab()]
    calcular_defesa_e_deslocamento(p)
    assert p.status.deslocamento_calc.total == 9


# --- Penalidade de armadura ---

def test_penalidade_acumula_armadura_e_escudo():
    p = _ficha_com(
        Item(nome="Cota de malha", tipo="Armadura", equipado=True),
        Item(nome="Escudo pesado", tipo="Escudo", equipado=True),
    )
    assert calcular_penalidade_armadura(p) == 4


def test_penalidade_inclui_sobrecarga():
    p = _ficha_com(
        Item(nome="Armadura completa", tipo="Armadura", equipado=True),  # -5
        Item(nome="Montante", tipo="Arma"),
        Item(nome="Arco longo", tipo="Arma"),
        Item(nome="Besta pesada", tipo="Arma"),
    )
    sincronizar_carga(p)
    assert calcular_penalidade_armadura(p) == 10  # 5 armadura + 5 sobrecarga


def test_carga_reage_a_forca():
    """Regressão: carga máxima usava campo 'for' inexistente (modelo é 'forca')."""
    p = _ficha_com()
    p.atributos.forca = 2   # mod +2 -> limite 10 + 2*2 = 14
    sincronizar_carga(p)
    assert p.inventario.carga_maxima == 14
    p.atributos.forca = -1  # mod negativo: -1 por ponto -> 10 - 1 = 9
    sincronizar_carga(p)
    assert p.inventario.carga_maxima == 9


# --- Mestre do Tridente (Sereia/Tritão, T20 JdA) ---

def _sereia_com_tridente(empunhado=True):
    p = Personagem()
    p.cabecalho.raca = "Sereia/Tritão"
    p.proficiencias = ["Armas Simples"]

    class _Hab:
        nome = "Mestre do Tridente"
        tipo = "Racial"
        fonte = "Racial"
        descricao = ""
        efeitos = {"proficiencia_simples": ["tridente"],
                   "bonus_dano_arma": {"azagaia": 2, "lança": 2, "tridente": 2}}
        escolhas_aplicadas = {}

    p.habilidades = [_Hab()]
    p.inventario.equipamentos.append(Item(nome="Tridente", tipo="Arma", equipado=empunhado))
    return p


def test_mestre_tridente_dano_e_proficiencia():
    p = _sereia_com_tridente()
    sincronizar_ataques_equipamento(p)
    a = [x for x in p.combate.ataques if x.fonte == "Equipamento"][0]
    assert a.dano == "1d8+2"
    assert "-5" not in a.especial  # tridente conta como arma simples
    assert "Mestre do Tridente (+2 dano)" in a.especial


def test_mestre_tridente_guardado_sem_ataque():
    p = _sereia_com_tridente(empunhado=False)
    sincronizar_ataques_equipamento(p)
    assert not [x for x in p.combate.ataques if x.fonte == "Equipamento"]


def test_sem_racial_tridente_tem_penalidade():
    p = Personagem()
    p.proficiencias = []  # sem proficiência marcial nem a racial
    p.inventario.equipamentos.append(Item(nome="Tridente", tipo="Arma", equipado=True))
    sincronizar_ataques_equipamento(p)
    a = [x for x in p.combate.ataques if x.fonte == "Equipamento"][0]
    assert a.dano == "1d8"
    assert "-5" in a.especial


def test_mestre_tridente_cobre_lanca():
    p = _sereia_com_tridente()
    p.inventario.equipamentos.append(Item(nome="Lança", tipo="Arma", equipado=True))
    sincronizar_ataques_equipamento(p)
    lanca = [x for x in p.combate.ataques if x.nome == "Lança"][0]
    assert lanca.dano == "1d6+2"


def test_mestre_tridente_nao_rebaixa_proficiencia():
    """Guerreiro (marciais) já era proficiente no tridente marcial:
    a racial não pode remover essa proficiência."""
    p = _sereia_com_tridente()
    p.proficiencias = ["Armas Marciais"]
    sincronizar_ataques_equipamento(p)
    a = [x for x in p.combate.ataques if x.fonte == "Equipamento"][0]
    assert "-5" not in a.especial
    assert "conta como arma simples" not in a.especial  # não foi a racial que deu
    assert a.dano == "1d8+2"


def test_proficiente_marcial_usa_arma_marcial():
    """Regressão: 'marcial' não é substring de 'marciais' (plural do
    livro); Guerreiro tomava -5 em toda arma marcial desde sempre."""
    p = Personagem()
    p.proficiencias = ["Armas Marciais"]
    p.inventario.equipamentos.append(Item(nome="Espada longa", tipo="Arma", equipado=True))
    sincronizar_ataques_equipamento(p)
    a = [x for x in p.combate.ataques if x.fonte == "Equipamento"][0]
    assert "-5" not in a.especial


def test_proficiencias_vindas_do_sync_de_classe():
    """Fluxo real: o sync de classe grava em status.proficiencias;
    os ataques de equipamento precisam ler lá também (não só top-level)."""
    from src.regras import atualizar_ficha
    from src import models
    Classe = None
    for nome in ("ClasseInfo", "Classe", "ClassePersonagem"):
        Classe = getattr(models, nome, None)
        if Classe:
            break
    assert Classe is not None, "modelo de classe não encontrado"
    p = Personagem()
    p.classes = [Classe(nome="Guerreiro", nivel=1, primaria=True, subclasse="")]
    p.inventario.equipamentos.append(Item(nome="Espada longa", tipo="Arma", equipado=True))
    atualizar_ficha(p)
    profs = " ".join(p.status.proficiencias).lower()
    assert "marciais" in profs  # o sync de classe populou
    a = [x for x in p.combate.ataques if x.fonte == "Equipamento"][0]
    assert "-5" not in a.especial


# --- Itens gerais (T3-6) ---

def test_catalogo_gerais_completo():
    from src.dados_equipamentos import GERAIS
    for nome in ["Mochila", "Corda (15m)", "Tocha", "Símbolo sagrado (prata)", "Kit de ladrão"]:
        assert nome in GERAIS
        assert GERAIS[nome]["preco"] >= 0
        assert GERAIS[nome]["espacos"] >= 0
        assert GERAIS[nome]["subcategoria"] in ("Aventura", "Alquímico", "Símbolo", "Ferramenta")


def test_item_geral_soma_carga_sem_ataque_ou_penalidade():
    p = Personagem()
    p.inventario.equipamentos.append(Item(nome="Mochila", tipo="Geral", equipado=False))
    p.inventario.equipamentos.append(Item(nome="Tocha", tipo="Geral", equipado=False))
    sincronizar_carga(p)
    sincronizar_ataques_equipamento(p)
    esp = catalogo_do_item("Mochila")["espacos"] + catalogo_do_item("Tocha")["espacos"]
    assert p.inventario.carga_total == esp
    assert not [a for a in p.combate.ataques if a.fonte == "Equipamento"]
    assert calcular_penalidade_armadura(p) == 0


def test_geral_tem_categoria_propria():
    assert catalogo_do_item("Tocha")["_categoria"] == "Geral"
    assert catalogo_do_item("Símbolo sagrado (prata)")["_categoria"] == "Geral"
    assert catalogo_do_item("Tridente")["_categoria"] == "Arma"
