"""Testes das 14 Classes Variantes — Heróis de Arton (Cap. 1, p. 22–45)."""
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Habilidade
from src.regras import atualizar_ficha
from src.dados_classes import DADOS_CLASSES
from src.dados_progressao_magias import PROGRESSAO_CIRCULOS_POR_CLASSE
from src.dados_suplementos import FONTE_HEROIS, inferir_fonte
from src.dados_variantes_herois import (
    MAPA_VARIANTE_PARA_BASE,
    DADOS_CLASSES_VARIANTES,
    DADOS_HABILIDADES_VARIANTES,
    validar_multiclasse_variante,
)
from src.dados_escolhas import montar_catalogo_escolhas


def _ficha(classe: str, nivel: int = 1, habilidades=None, attrs=None) -> Personagem:
    f = Personagem(
        cabecalho=Cabecalho(nome=f"Teste {classe}", raca="Humano"),
        classes=[ClasseInfo(nome=classe, nivel=nivel, primaria=True)],
        atributos_base=attrs or Atributos(forca=2, destreza=2, constituicao=2, inteligencia=2, sabedoria=2, carisma=2),
        habilidades=habilidades or [],
    )
    atualizar_ficha(f)
    return f


def test_todas_14_variantes_catalogadas_e_fonte_herois():
    assert len(MAPA_VARIANTE_PARA_BASE) == 14
    assert len(DADOS_CLASSES_VARIANTES) == 14
    for v_nome, base_nome in MAPA_VARIANTE_PARA_BASE.items():
        assert v_nome in DADOS_CLASSES
        assert DADOS_CLASSES[v_nome]["classe_base"] == base_nome
        assert inferir_fonte("classe", v_nome, DADOS_CLASSES[v_nome]) == FONTE_HEROIS

    # Progressão de círculos das 5 variantes conjuradoras
    for conj_5 in ("Necromante", "Usurpador"):
        assert PROGRESSAO_CIRCULOS_POR_CLASSE[conj_5][17] == 5
    for conj_4 in ("Magimarcialista", "Ermitão", "Ventanista"):
        assert PROGRESSAO_CIRCULOS_POR_CLASSE[conj_4][14] == 4

    esc = montar_catalogo_escolhas()
    assert "Escola de Duelo" in esc["PODERES_COM_ESCOLHA"]
    assert "Sítio Sagrado" in esc["PODERES_COM_ESCOLHA"]
    assert "Lorde" in esc["PODERES_COM_ESCOLHA"]


def test_regra_multiclasse_variante_bloqueia_mesma_classe():
    assert validar_multiclasse_variante(["Guerreiro", "Inovador"])["valido"] is False
    assert validar_multiclasse_variante(["Arcanista", "Necromante"])["valido"] is False
    assert validar_multiclasse_variante(["Guerreiro", "Necromante"])["valido"] is True
    assert validar_multiclasse_variante(["Duelista", "Ventanista"])["valido"] is True


def test_atributos_e_habilidades_passivas_variantes():
    # Magimarcialista: 16 PV + Con (4/nv), não 12
    f_mag = _ficha("Magimarcialista", nivel=1)
    assert f_mag.status.pv.maximo == 18  # 16 + Con 2
    assert f_mag.status.pm.maximo == 6   # 4 + Car 2

    # Burguês: 12 PV + Con (3/nv), sem proficiências
    f_bur = _ficha("Burguês", nivel=1)
    assert f_bur.status.pv.maximo == 14  # 12 + Con 2
    assert f_bur.status.proficiencias == []

    # Santo: 4 PM/nv + Car
    f_san = _ficha("Santo", nivel=3)
    assert f_san.status.pm.maximo == 14  # 4*3 + Car 2

    # Usurpador: Car nos PM, Discrição Divina (+1 nv3, +2 nv9, +3 nv15)
    f_usu = _ficha("Usurpador", nivel=9, attrs=Atributos(sabedoria=0, carisma=4, destreza=1, constituicao=1))
    assert f_usu.status.pm.maximo == 49  # 5*9 + Car 4
    # Discrição Divina nv9 = +2 em Furtividade/Fort/Ref/Von
    assert any("Discrição Divina" in x.fonte and x.valor == 2 for x in f_usu.pericias["Furtividade"].calculo.fontes)

    # Ventanista: Car nos PM (Charme) + 4º círculo no nv 14
    f_ven = _ficha("Ventanista", nivel=14, attrs=Atributos(carisma=3, inteligencia=3, destreza=2, constituicao=1))
    assert f_ven.status.pm.maximo == 59  # 4*14 + Car 3
    assert f_ven.combate.circulo_maximo == 4

    # Machado de Pedra: Tanga de Peles (+Con na Defesa +1 nv3/+2 nv7/+3 nv11), Resiliência Primal RD 3..15
    f_mdp = _ficha("Machado de Pedra", nivel=11, attrs=Atributos(forca=3, destreza=1, constituicao=4))
    # Defesa: 10 + Des 1 + Con 4 (Tanga de Peles) + 3 (Tanga de Peles escala nv11) = 18
    assert f_mdp.status.defesa.total == 18
    # Resiliência Primal nv11: 3 + ((11-5)//3)*3 = 9
    assert "geral 9" in f_mdp.status.rd

    # Atleta nv5: Mais Alto e Mais Rápido (+3m desl -> 12m), Casca Grossa (+Con Defesa)
    f_atl = _ficha("Atleta", nivel=5, attrs=Atributos(forca=3, destreza=1, constituicao=3))
    assert f_atl.status.deslocamento == 12.0
    assert f_atl.status.defesa.total == 14  # 10 + Des 1 + Con 3

    # Necromante nv8: Necrologia (+3 Cura e Fortitude) + Ritual do Lich no catálogo
    f_nec = _ficha("Necromante", nivel=8)
    assert any("Necrologia" in x.fonte and x.valor == 3 for x in f_nec.pericias["Cura"].calculo.fontes)
    assert "NEC_RITUAL_LICH" in DADOS_HABILIDADES_VARIANTES


def test_ermitao_sitio_sagrado_e_vassalo_lorde():
    # Ermitão nv 11 com Sítio Sagrado = Deserto -> RD Fogo 5 (Temperado pelo Clima)
    f_erm = _ficha(
        "Ermitão",
        nivel=11,
        habilidades=[Habilidade(nome="Sítio Sagrado", tipo="Classe", escolhas_aplicadas={"terreno": "Deserto"})],
    )
    assert any("Fogo 5" in r for r in f_erm.status.rd)

    # Vassalo nv 13 Caminho do Soldado: Escudeiro Aprendiz (Armaduras pesadas), Visconde (+13 PV), Marquês (RD 5, +2 Def)
    f_vas = _ficha(
        "Vassalo",
        nivel=13,
        habilidades=[Habilidade(nome="Lorde", tipo="Classe", escolhas_aplicadas={"caminho_lorde": "Caminho do Soldado"})],
    )
    assert "Armaduras pesadas" in f_vas.status.proficiencias
    assert any("geral 5" in r for r in f_vas.status.rd)
    assert f_vas.status.defesa.total == 14  # 10 + Des 2 + Marquês 2
    # PV base Vassalo nv13 Con 2: 20+2 + 12*(5+2) = 22 + 84 = 106; +13 Visconde = 119
    assert f_vas.status.pv.maximo == 119
