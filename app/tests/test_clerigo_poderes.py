"""Clérigo — testes de poderes de classe, Missas, Liturgia e Símbolo Sagrado (T20 JdA p.56-58)."""
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Habilidade, Magia
from src.dados_habilidades_classe import DADOS_HABILIDADES_CLASSE
from src.regras import atualizar_ficha
from src.regras.custo_magia import calcular_cd_magia, calcular_custo_magia


def _clerigo(nivel=6, sab=4, poderes=None, condicoes=None):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Gwen", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Clérigo", nivel=nivel, primaria=True)]
    f.atributos_base = Atributos(sabedoria=sab, constituicao=2)
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
            fonte="Poder de Clérigo",
        ))
    return f


def test_conhecimento_magico_soma_2_e_acumula():
    f0 = _clerigo(nivel=4)
    atualizar_ficha(f0)
    assert f0.combate.limite_magias == 6  # 3 + 3

    f2 = _clerigo(nivel=4, poderes=["CLERIGO_CONHECIMENTO_MAGICO", "CLERIGO_CONHECIMENTO_MAGICO"])
    atualizar_ficha(f2)
    assert f2.combate.limite_magias == 10  # 6 + 4


def test_liturgia_magica_aumenta_cd_em_2():
    magia = Magia(nome="Comando", circulo=1, escola="Encantamento", atributo_chave="sab")
    f_sem = _clerigo(nivel=6, sab=4, poderes=["CLERIGO_LITURGIA_MAGICA"], condicoes=[])
    atualizar_ficha(f_sem)
    assert calcular_cd_magia(f_sem, magia) == 17  # 10 + 3 + 4

    f_com = _clerigo(nivel=6, sab=4, poderes=["CLERIGO_LITURGIA_MAGICA"], condicoes=["liturgia_magica"])
    atualizar_ficha(f_com)
    assert calcular_cd_magia(f_com, magia) == 19  # 17 + 2


def test_simbolo_sagrado_energizado_reduz_custo_magia_divina():
    magia_div = Magia(nome="Curar Ferimentos", circulo=2, tipo="Divina", atributo_chave="sab")
    f_sem = _clerigo(nivel=6, poderes=["CLERIGO_SIMBOLO_ENERGIZADO"], condicoes=[])
    atualizar_ficha(f_sem)
    assert calcular_custo_magia(f_sem, magia_div).total == 3

    f_com = _clerigo(nivel=6, poderes=["CLERIGO_SIMBOLO_ENERGIZADO"], condicoes=["simbolo_energizado"])
    atualizar_ficha(f_com)
    assert calcular_custo_magia(f_com, magia_div).total == 2

    # Magia arcana não reduz
    magia_arc = Magia(nome="Bola de Fogo", circulo=2, tipo="Arcana", atributo_chave="int")
    assert calcular_custo_magia(f_com, magia_arc).total == 3


def test_missa_escudo_divino_e_mestre_celebrante():
    f_base = _clerigo(nivel=12, sab=4, poderes=["CLERIGO_MISSA_ESCUDO"], condicoes=[])
    atualizar_ficha(f_base)
    assert f_base.combate.clerigo_calc["missa_pessoas"] == 5       # 1 + 4
    assert f_base.combate.clerigo_calc["missa_bencao_pv_temp"] == 16  # 12 + 4
    assert f_base.combate.clerigo_calc["missa_elevacao_pm_temp"] == 4

    # Missa ativa sem Mestre Celebrante: +1 Defesa e resistências
    f_missa = _clerigo(nivel=12, sab=4, poderes=["CLERIGO_MISSA_ESCUDO"], condicoes=["missa_escudo_divino"])
    atualizar_ficha(f_missa)
    assert f_missa.status.defesa.total == f_base.status.defesa.total + 1
    for res in ("Fortitude", "Reflexos", "Vontade"):
        assert f_missa.pericias[res].total == f_base.pericias[res].total + 1

    # Com Mestre Celebrante: 10x pessoas (50) e benefícios dobram (+2 Defesa/resistências, 32 PV, 8 PM)
    f_mc = _clerigo(
        nivel=12, sab=4,
        poderes=["CLERIGO_MISSA_ESCUDO", "CLERIGO_MESTRE_CELEBRANTE"],
        condicoes=["missa_escudo_divino"],
    )
    atualizar_ficha(f_mc)
    assert f_mc.combate.clerigo_calc["missa_pessoas"] == 50
    assert f_mc.combate.clerigo_calc["missa_bencao_pv_temp"] == 32
    assert f_mc.combate.clerigo_calc["missa_elevacao_pm_temp"] == 8
    assert f_mc.status.defesa.total == f_base.status.defesa.total + 2
    for res in ("Fortitude", "Reflexos", "Vontade"):
        assert f_mc.pericias[res].total == f_base.pericias[res].total + 2


def test_canalizar_energia_e_canalizar_amplo():
    f1 = _clerigo(nivel=4, poderes=["CLERIGO_CANALIZAR"])
    atualizar_ficha(f1)
    assert f1.combate.clerigo_calc["canalizar_alcance"] == "Curto"

    f2 = _clerigo(nivel=4, poderes=["CLERIGO_CANALIZAR", "CLERIGO_CANALIZAR_AMPLO"])
    atualizar_ficha(f2)
    assert f2.combate.clerigo_calc["canalizar_alcance"] == "Médio"


FIXAS_ESPERADAS = {
    "Devoto Fiel": 1,
    "Magias (Clérigo)": 1,
    "Mão da Divindade": 20,
}

PODERES_ESPERADOS = {
    "Abençoar Arma",
    "Aumento de Atributo",
    "Autoridade Eclesiástica",
    "Canalizar Energia Positiva/Negativa",
    "Canalizar Amplo",
    "Comunhão Vital",
    "Conhecimento Mágico",
    "Expulsar/Comandar Mortos-Vivos",
    "Liturgia Mágica",
    "Magia Sagrada/Profana",
    "Mestre Celebrante",
    "Missa: Bênção da Vida",
    "Missa: Chamado às Armas",
    "Missa: Elevação do Espírito",
    "Missa: Escudo Divino",
    "Missa: Superar as Limitações",
    "Prece de Combate",
    "Símbolo Sagrado Energizado",
}


def test_catalogo_clerigo_completo_21_entradas():
    entries = [v for v in DADOS_HABILIDADES_CLASSE.values() if v.get("classe") == "Clérigo" and v.get("fonte", "T20 JdA") == "T20 JdA"]
    fixas = {v["nome"]: v.get("nivel") for v in entries if v.get("tipo") == "Habilidade de Classe"}
    poderes = {v["nome"] for v in entries if v.get("tipo") == "Poder de Clérigo"}

    assert fixas == FIXAS_ESPERADAS
    assert poderes == PODERES_ESPERADOS
    assert len(entries) == 21
    assert all(v.get("efeitos") for v in entries)


def test_missas_seguem_regra_base():
    missas = [
        v for v in DADOS_HABILIDADES_CLASSE.values()
        if v.get("classe") == "Clérigo" and v["nome"].startswith("Missa:")
    ]
    assert len(missas) == 8
    for m in missas:
        dm = m["efeitos"]["missa"]
        assert dm["tempo"] == "1 hora"
        assert dm["custo_to"] == 25
        assert dm["duracao"] == "1 dia"
