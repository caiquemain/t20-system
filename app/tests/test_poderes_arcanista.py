from src.models import Habilidade, ClasseInfo, StatCalculado
from src.regras.poderes_arcanista import aplicar_poderes_arcanista

ATTRS = ["forca", "destreza", "constituicao", "inteligencia", "sabedoria", "carisma"]


def _ficha_arcanista(personagem_base, nivel=1, subclasse=""):
    personagem_base.classes = [ClasseInfo(nome="Arcanista", nivel=nivel, primaria=True, subclasse=subclasse)]
    personagem_base.cabecalho.nivel_total = nivel
    personagem_base.atributos_calc = {k: StatCalculado() for k in ATTRS}
    return personagem_base


def _hab(nome, escolhas=None):
    return Habilidade(nome=nome, tipo="Poder de Arcanista", descricao="", escolhas_aplicadas=escolhas or {})


def test_fortalecimento_arcano_cd_base(personagem_base):
    f = _ficha_arcanista(personagem_base)
    f.combate.circulo_maximo = 1
    f.habilidades = [_hab("Fortalecimento Arcano")]
    aplicar_poderes_arcanista(f)
    assert f.combate.cd_magias == 11


def test_fortalecimento_arcano_cd_com_4_circulo(personagem_base):
    f = _ficha_arcanista(personagem_base, nivel=13)
    f.combate.circulo_maximo = 4
    f.habilidades = [_hab("Fortalecimento Arcano")]
    aplicar_poderes_arcanista(f)
    assert f.combate.cd_magias == 12


def test_especialista_e_mestre_em_escola(personagem_base):
    f = _ficha_arcanista(personagem_base)
    f.habilidades = [
        _hab("Especialista em Escola", {"escola": "Evocação"}),
        _hab("Mestre em Escola", {"escola": "Evocação"}),
    ]
    aplicar_poderes_arcanista(f)
    assert f.combate.cd_por_escola == {"Evocação": 2}
    assert f.combate.custo_por_escola == {"Evocação": 1}


def test_alta_arcana_nivel_20(personagem_base):
    f = _ficha_arcanista(personagem_base, nivel=20)
    aplicar_poderes_arcanista(f)
    assert f.combate.custo_arcano_metade is True


def test_arcano_de_batalha_dano(personagem_base):
    f = _ficha_arcanista(personagem_base)
    f.atributos.inteligencia = 4
    f.habilidades = [_hab("Arcano de Batalha")]
    aplicar_poderes_arcanista(f)
    assert f.combate.bonus_dano_magias == 4


def test_aumento_de_atributo(personagem_base):
    f = _ficha_arcanista(personagem_base)
    f.habilidades = [_hab("Aumento de Atributo", {"atributo": "forca"})]
    aplicar_poderes_arcanista(f)
    assert f.atributos.forca == 1


def test_familiar_sapo_pv(personagem_base):
    f = _ficha_arcanista(personagem_base)
    f.atributos.inteligencia = 3
    f.habilidades = [_hab("Familiar", {"familiar": "Sapo"})]
    aplicar_poderes_arcanista(f)
    assert any(fr.fonte == "Familiar: Sapo" and fr.valor == 3 for fr in f.status.pv_calc.fontes)


def test_familiar_borboleta_cd_resistencia(personagem_base):
    f = _ficha_arcanista(personagem_base)
    f.habilidades = [_hab("Familiar", {"familiar": "Borboleta"})]
    aplicar_poderes_arcanista(f)
    assert f.combate.cd_por_resistencia == {"Vontade": 1}


def test_familiar_gato_sentidos(personagem_base):
    f = _ficha_arcanista(personagem_base)
    f.habilidades = [_hab("Familiar", {"familiar": "Gato"})]
    aplicar_poderes_arcanista(f)
    assert "Visão no Escuro" in f.status.sentidos


def test_linhagem_draconica_basica(personagem_base):
    f = _ficha_arcanista(personagem_base, subclasse="Feiticeiro")
    f.atributos.carisma = 3
    f.habilidades = [Habilidade(nome="Linhagem Dracônica", tipo="Habilidade de Classe",
                                descricao="", escolhas_aplicadas={"tipo_dano": "fogo"})]
    aplicar_poderes_arcanista(f)
    assert any(fr.fonte == "Linhagem Dracônica (básica)" for fr in f.status.pv_calc.fontes)
    assert "fogo 5" in f.status.rd


def test_linhagem_feerica_superior_carisma(personagem_base):
    f = _ficha_arcanista(personagem_base, subclasse="Feiticeiro")
    f.habilidades = [
        Habilidade(nome="Linhagem Feérica", tipo="Habilidade de Classe", descricao=""),
        _hab("Herança Aprimorada"), _hab("Herança Superior"),
    ]
    aplicar_poderes_arcanista(f)
    assert f.atributos.carisma == 2


def test_linhagem_feerica_basica_limite_magias(personagem_base):
    f = _ficha_arcanista(personagem_base, subclasse="Feiticeiro")
    f.combate.magias_calc = StatCalculado(base=3, total=3)
    f.combate.limite_magias = 3
    f.habilidades = [Habilidade(nome="Linhagem Feérica", tipo="Habilidade de Classe", descricao="")]
    aplicar_poderes_arcanista(f)
    assert f.combate.limite_magias == 4
