from src.dados_classes import DADOS_CLASSES


def test_pv_pm_oficiais_livro_base():
    assert DADOS_CLASSES["Bárbaro"]["pv_inicial"] == 24
    assert DADOS_CLASSES["Bárbaro"]["pv_nivel"] == 6
    assert DADOS_CLASSES["Bardo"]["pm_inicial"] == 4
    assert DADOS_CLASSES["Clérigo"]["pm_inicial"] == 5
    assert DADOS_CLASSES["Arcanista"]["pv_inicial"] == 8


def test_atributo_chave_de_pm():
    assert DADOS_CLASSES["Bardo"]["pm_atributo"] == "car"
    assert DADOS_CLASSES["Clérigo"]["pm_atributo"] == "sab"
    assert DADOS_CLASSES["Druida"]["pm_atributo"] == "sab"
    assert DADOS_CLASSES["Paladino"]["pm_atributo"] == "car"
    # não-conjuradores não somam atributo no PM
    for c in ["Guerreiro", "Ladino", "Lutador", "Inventor", "Bárbaro"]:
        assert "pm_atributo" not in DADOS_CLASSES[c]


def test_proficiencias_oficiais():
    assert "Armaduras Pesadas" in DADOS_CLASSES["Cavaleiro"]["proficiencias"]
    assert "Escudos" in DADOS_CLASSES["Caçador"]["proficiencias"]
    assert DADOS_CLASSES["Inventor"]["proficiencias"] == []


def test_pv_barbaro_na_pipeline(personagem_base):
    from src.models import ClasseInfo
    from src.regras.status import calcular_pv_pm
    personagem_base.classes = [ClasseInfo(nome="Bárbaro", nivel=1, primaria=True)]
    personagem_base.atributos.constituicao = 2
    calcular_pv_pm(personagem_base)
    assert personagem_base.status.pv.maximo == 26  # 24 + Con 2
    fontes = [f.fonte for f in personagem_base.status.pv_calc.fontes]
    assert "Classe: Bárbaro (Inicial)" in fontes


def test_pm_bardo_soma_carisma(personagem_base):
    from src.models import ClasseInfo
    from src.regras.status import calcular_pv_pm
    personagem_base.classes = [ClasseInfo(nome="Bardo", nivel=1, primaria=True)]
    personagem_base.atributos.carisma = 3
    calcular_pv_pm(personagem_base)
    assert any(f.fonte == "Atributo-chave: CAR" and f.valor == 3
               for f in personagem_base.status.pm_calc.fontes)
