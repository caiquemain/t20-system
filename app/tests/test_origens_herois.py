"""Testes das 30 Novas Origens Especiais — Heróis de Arton (Cap. 1, p. 46–53)."""
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Habilidade
from src.regras import atualizar_ficha
from src.dados_origens import DADOS_ORIGENS
from src.dados_origens_herois import DADOS_ORIGENS_HEROIS, DADOS_PODERES_ORIGEM_HEROIS
from src.dados_suplementos import FONTE_HEROIS


def _ficha_origem(origem: str, habilidades=None) -> Personagem:
    f = Personagem(
        cabecalho=Cabecalho(nome=f"Teste {origem}", raca="Humano", origem=origem),
        classes=[ClasseInfo(nome="Guerreiro", nivel=1, primaria=True)],
        atributos_base=Atributos(forca=1, destreza=1, constituicao=1, inteligencia=1, sabedoria=1, carisma=3),
        habilidades=habilidades or [],
    )
    atualizar_ficha(f)
    return f


def test_todas_30_origens_herois_catalogadas():
    assert len(DADOS_ORIGENS_HEROIS) == 30
    assert len(DADOS_PODERES_ORIGEM_HEROIS) == 30
    for nome, dados in DADOS_ORIGENS_HEROIS.items():
        assert nome in DADOS_ORIGENS
        assert dados["fonte"] == FONTE_HEROIS
        assert dados["qtd_escolhas"] == 0
        assert dados["poder_fixo"] == f"Origem Especial: {nome}"


def test_efeitos_mecanicos_origens_herois():
    f0 = _ficha_origem("")

    # Contrabandista: Enganação + Ladinagem treinadas + +2 espaços carga
    f_con = _ficha_origem("Contrabandista")
    assert f_con.pericias["Enganação"].treino == 1
    assert f_con.pericias["Ladinagem"].treino == 1
    assert f_con.inventario.carga_maxima == f0.inventario.carga_maxima + 2

    # Insciente: Sobrevivência + resistência a magia +5
    f_ins = _ficha_origem("Insciente")
    assert f_ins.pericias["Sobrevivência"].treino == 1
    assert f_ins.status.resistencia_magia == 5

    # Mensageiro: +3m deslocamento + +2 Fort/Ref/Von
    f_men = _ficha_origem("Mensageiro")
    assert f_men.status.deslocamento == f0.status.deslocamento + 3
    assert f_men.pericias["Fortitude"].total == f0.pericias["Fortitude"].total + 2
    assert f_men.pericias["Reflexos"].total == f0.pericias["Reflexos"].total + 2
    assert f_men.pericias["Vontade"].total == f0.pericias["Vontade"].total + 2

    # Náufrago: +5 PV e +2 PM
    f_nau = _ficha_origem("Náufrago")
    assert f_nau.status.pv.maximo == f0.status.pv.maximo + 5
    assert f_nau.status.pm.maximo == f0.status.pm.maximo + 2

    # Carpinteiro de Guilda: RD Corte 2; Ladrão de Túmulos: RD Trevas 5
    f_car = _ficha_origem("Carpinteiro de Guilda")
    assert any("Corte 2" in r for r in f_car.status.rd)
    f_lad = _ficha_origem("Ladrão de Túmulos")
    assert any("Trevas 5" in r for r in f_lad.status.rd)

    # Carcereiro (+2 Eng/Fur/Int), Pedinte (+2 Eng/Fur), Pescador (+2 Ini)
    f_crc = _ficha_origem("Carcereiro")
    assert f_crc.pericias["Enganação"].total == f0.pericias["Enganação"].total + 2
    assert f_crc.pericias["Furtividade"].total == f0.pericias["Furtividade"].total + 2
    assert f_crc.pericias["Intimidação"].total == f0.pericias["Intimidação"].total + 2

    f_pes = _ficha_origem("Pescador")
    assert f_pes.pericias["Iniciativa"].total == f0.pericias["Iniciativa"].total + 2


def test_origens_com_poder_ou_escolha_escriba_menestrel_espiao():
    # Escriba: injeta Lendas e Histórias automaticamente
    f_esc = _ficha_origem("Escriba")
    assert any(h.nome == "Lendas e Histórias" for h in f_esc.habilidades)

    # Menestrel: injeta Música de bardo escolhida
    f_mst = _ficha_origem(
        "Menestrel",
        habilidades=[
            Habilidade(
                nome="Origem Especial: Menestrel",
                tipo="Origem",
                escolhas_aplicadas={"musica_bardo": "Melodia Curativa"},
            )
        ],
    )
    assert any("Melodia Curativa" in h.nome for h in f_mst.habilidades)

    # Espião: permite usar Carisma na perícia escolhida (exceto Luta/Pontaria)
    f_esp = _ficha_origem(
        "Espião",
        habilidades=[
            Habilidade(
                nome="Origem Especial: Espião",
                tipo="Origem",
                escolhas_aplicadas={"pericia_carisma": "Investigação"},
            )
        ],
    )
    assert "car" in f_esp.pericias["Investigação"].atributos_possiveis
