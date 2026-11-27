"""Testes da classe Treinador e Melhor Amigo — Heróis de Arton (Cap. 1, p. 16–21)."""
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Habilidade
from src.regras import atualizar_ficha
from src.dados_habilidades_classe import DADOS_HABILIDADES_CLASSE
from src.dados_treinador_herois import (
    DADOS_HABILIDADES_TREINADOR,
    DADOS_MASCOTES_TREINADOR,
    DADOS_TIPOS_MELHOR_AMIGO,
    DADOS_TRUQUES_MELHOR_AMIGO,
    obter_catalogo_treinador,
)
from src.dados_escolhas import montar_catalogo_escolhas


def _treinador(nivel=1, habilidades=None, melhores_amigos=None, extra_classes=None) -> Personagem:
    classes = [ClasseInfo(nome="Treinador", nivel=nivel, primaria=True)]
    if extra_classes:
        classes.extend(extra_classes)
    f = Personagem(
        cabecalho=Cabecalho(nome="Kael, o Treinador", raca="Humano"),
        classes=classes,
        atributos_base=Atributos(forca=0, destreza=2, constituicao=2, inteligencia=1, sabedoria=1, carisma=4),
        habilidades=habilidades or [],
        melhores_amigos=melhores_amigos or [],
    )
    atualizar_ficha(f)
    return f


def test_catalogo_treinador_completo():
    assert len(DADOS_HABILIDADES_TREINADOR) == 27  # 6 fixas + 21 poderes
    assert len(DADOS_MASCOTES_TREINADOR) == 8
    assert len(DADOS_TIPOS_MELHOR_AMIGO) == 5
    assert len(DADOS_TRUQUES_MELHOR_AMIGO) == 22
    assert "TREINADOR_DIRECIONAR" in DADOS_HABILIDADES_CLASSE
    assert "TREINADOR_VETERINARIO_CAMPO" in DADOS_HABILIDADES_CLASSE
    cat = obter_catalogo_treinador()
    assert len(cat["truques"]) == 22
    esc = montar_catalogo_escolhas()
    assert "Treino Especializado" in esc["PODERES_COM_ESCOLHA"]
    assert "Mascote" in esc["PODERES_COM_ESCOLHA"]


def test_nao_treinador_tem_treinador_calc_none():
    f = Personagem(
        cabecalho=Cabecalho(nome="Guerreiro", raca="Humano"),
        classes=[ClasseInfo(nome="Guerreiro", nivel=5, primaria=True)],
        atributos_base=Atributos(forca=3, constituicao=2),
    )
    atualizar_ficha(f)
    assert f.combate.treinador_calc is None


def test_treinador_progressao_tabela_1_1_e_domar_criatura():
    f1 = _treinador(nivel=1)
    assert f1.status.pv.maximo == 14  # 12 + Con 2
    assert f1.status.pm.maximo == 4
    assert f1.pericias["Adestramento"].treino == 1
    assert f1.pericias["Vontade"].treino == 1
    tc1 = f1.combate.treinador_calc
    assert tc1["truques_disponiveis"] == 2
    assert tc1["domar_criatura"] is None

    f6 = _treinador(nivel=6)
    tc6 = f6.combate.treinador_calc
    assert tc6["truques_disponiveis"] == 3  # 2 + (6-1)//3 = 3
    assert tc6["domar_criatura"]["formula"] == "4d8"
    assert tc6["domar_criatura"]["controla_cena"] is True
    assert tc6["domar_criatura"]["controla_dia"] is False
    assert tc6["sincronia_combate"] is True

    f18 = _treinador(
        nivel=18,
        habilidades=[
            Habilidade(nome="Domador Cativante", tipo="Poder de Treinador"),
            Habilidade(nome="Domador Lendário", tipo="Poder de Treinador"),
            Habilidade(nome="Coração Grande", tipo="Poder de Treinador"),
            Habilidade(nome="Comandos Distantes", tipo="Poder de Treinador"),
        ],
    )
    tc18 = f18.combate.treinador_calc
    assert tc18["domar_criatura"]["formula"] == "10d10+4"
    assert tc18["domar_criatura"]["formula_lendaria"] == "10d12+4"
    assert tc18["domar_criatura"]["controla_dia"] is True
    assert tc18["domar_criatura"]["nd_max_dia"] == 15
    assert tc18["limite_parceiros_bonus"] == 2
    assert tc18["alcance_habilidades"] == "Médio"


def test_treinador_mascotes_aplicam_efeitos_no_treinador_e_no_melhor_amigo():
    f0 = _treinador(nivel=5)
    f_gekko = _treinador(
        nivel=5,
        habilidades=[
            Habilidade(nome="Mascote", tipo="Poder de Treinador", escolhas_aplicadas={"mascote": "Gekko Malhado"}),
            Habilidade(nome="Mascote", tipo="Poder de Treinador", escolhas_aplicadas={"mascote": "Ossinhos"}),
            Habilidade(nome="Mascote", tipo="Poder de Treinador", escolhas_aplicadas={"mascote": "Bicho Preguiça"}),
        ],
    )
    # No Treinador: +2 Def, +2 Reflexos, RD Corte/Frio/Perfuração 2, ataque natural Garra
    assert f_gekko.status.defesa.total == f0.status.defesa.total + 2
    assert f_gekko.pericias["Reflexos"].total == f0.pericias["Reflexos"].total + 2
    assert any("Corte 2" in r for r in f_gekko.status.rd)
    assert any("Garra (Bicho Preguiça)" in a.nome for a in f_gekko.combate.ataques)

    # No Melhor Amigo também!
    ma0 = f0.combate.treinador_calc["melhores_amigos"][0]
    ma1 = f_gekko.combate.treinador_calc["melhores_amigos"][0]
    assert ma1["defesa"] == ma0["defesa"] + 2
    assert "Corte 2" in ma1["rd"]


def test_melhor_amigo_ficha_completa_tipos_truques_e_treino_intensivo():
    f = _treinador(
        nivel=11,
        habilidades=[
            Habilidade(
                nome="Treino Especializado",
                tipo="Classe",
                escolhas_aplicadas={"treino_especializado": "Treino Intensivo"},
            ),
            Habilidade(nome="Ensinar Truque", tipo="Poder de Treinador"),
        ],
        melhores_amigos=[
            {
                "nome": "Rex",
                "tipo": "Animal",
                "tamanho": "Grande",
                "tipo_dano": "Perfuração",
                "truques": [
                    "Amigão",
                    "Amigo Feroz",
                    "Treinamento Defensivo",
                    "Treinamento Marcial",
                    "Veloz",
                    "Redução de Dano",
                    "Amigo Veterano",
                    "Amigo Mestre",
                ],
            }
        ],
    )
    tc = f.combate.treinador_calc
    # Truques: base (2 + 10//3 = 5) + Treino Intensivo nv11 (+2) + Ensinar Truque (+1) = 8
    assert tc["truques_disponiveis"] == 8
    ma = tc["melhores_amigos"][0]
    assert ma["nome"] == "Rex"
    assert ma["tamanho"] == "Enorme"  # Amigão
    assert ma["grau_parceiro"] == "Mestre"
    # Animal (+1 For, +1 Des, +1 Sab) + Amigão (+1 For) => For 3, Des 2, Con 1
    assert ma["atributos"]["forca"] == 3
    assert ma["atributos"]["destreza"] == 2
    # PV: 16 + 1 + 10*(4+1) + 4*11 (Treino Intensivo) = 17 + 50 + 44 = 111
    assert ma["pv_maximo"] == 111
    # Defesa: 10 + Des 2 + Car_tr 4 + nv 11 (Treinamento Defensivo) + 2 (Veloz) = 29
    assert ma["defesa"] == 29
    # Deslocamento: 12 + 3 (Veloz) = 15m
    assert ma["deslocamento"] == 15
    # RD: Treino Intensivo nv11 (10) + Redução de Dano (5) = geral 15
    assert "geral 15" in ma["rd"]
    # Ataque natural: 1d8 +2 passos (Amigão + Amigo Feroz) = 1d12; margem 20 - 1(Animal) - 2(Feroz) = 17
    assert ma["ataque_natural"]["dano"] == "1d12"
    assert ma["ataque_natural"]["margem_ameaca"] == 17
    # Treinamento Marcial nv11 (2 patamares acima de iniciante) = +4; +2 Amigo Feroz = +6 ataque, +4 dano
    assert ma["ataque_natural"]["bonus_ataque"] == 6
    assert ma["ataque_natural"]["bonus_dano"] == 4


def test_treinador_ecletico_e_conquistar_pelos_numeros():
    f = _treinador(
        nivel=6,
        extra_classes=[ClasseInfo(nome="Guerreiro", nivel=4)],
        habilidades=[
            Habilidade(nome="Treinador Eclético", tipo="Poder de Treinador"),
            Habilidade(
                nome="Treino Especializado",
                tipo="Classe",
                escolhas_aplicadas={"treino_especializado": "Conquistar pelos Números"},
            ),
        ],
        melhores_amigos=[
            {"nome": "Golemito", "tipo": "Construto", "truques": ["Anatomia Humanoide"]},
            {"nome": "Sombrinha", "tipo": "Morto-Vivo", "truques": []},
        ],
    )
    tc = f.combate.treinador_calc
    assert tc["max_melhores_amigos"] == 2
    assert tc["nivel_efetivo_amigo"] == 10  # 6 Treinador + 4 Guerreiro
    assert len(tc["melhores_amigos"]) == 2
    assert tc["melhores_amigos"][0]["atributos"]["inteligencia"] == -2  # Anatomia Humanoide
    assert tc["melhores_amigos"][0]["atributos"]["constituicao"] == 3   # Construto +2
    assert "Trevas" in tc["melhores_amigos"][1]["imunidades"]
