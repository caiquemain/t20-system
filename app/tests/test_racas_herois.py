"""Testes das 5 Novas Raças de Heróis de Arton (Cap. 1, p. 8–15)."""
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Habilidade, TamanhoEnum
from src.regras import atualizar_ficha
from src.regras.duende import gerar_duende_aleatorio, TABUS_EXEMPLOS_DUENDE
from src.dados_racas import DADOS_RACAS
from src.dados_escolhas import montar_catalogo_escolhas


def _duende_com_escolhas(
    natureza_id="Natureza_Vegetal_Duende",
    tamanho_id="Tamanho_Medio_Duende",
    dons=None,
    animal_attr=None,
    presentes=None,
    tabu_id="Tabu_Diplomacia",
    sonhos_malucos=False,
    nivel=1,
) -> Personagem:
    dons = dons or {"atributo_1": "carisma", "atributo_2": "destreza"}
    presentes = presentes or ["Lingua_Natureza_Duende", "Visao_Feerica_Duende", "Voo_Duende"]

    habs = [
        Habilidade(nome="Natureza", tipo="Racial", escolhas_aplicadas={"poder_escolha": natureza_id}),
        Habilidade(nome="Tamanho", tipo="Racial", escolhas_aplicadas={"poder_escolha": tamanho_id}),
        Habilidade(nome="Dons", tipo="Racial", escolhas_aplicadas=dons),
        Habilidade(nome="Presentes de Magia e Caos", tipo="Racial", escolhas_aplicadas={"poder_escolha": presentes}),
        Habilidade(
            nome="Limitações de Duende",
            tipo="Racial",
            escolhas_aplicadas={
                "poder_escolha": tabu_id,
                **({"sonhos_malucos": "sim"} if sonhos_malucos else {}),
            },
        ),
    ]
    if animal_attr and natureza_id == "Natureza_Animal_Duende":
        habs.append(
            Habilidade(nome="Natureza Animal", tipo="Racial", escolhas_aplicadas={"atributo": animal_attr})
        )

    f = Personagem(
        cabecalho=Cabecalho(nome="Pip, o Duende", raca="Duende"),
        classes=[ClasseInfo(nome="Bardo", nivel=nivel, primaria=True)],
        atributos_base=Atributos(forca=1, destreza=1, constituicao=1, inteligencia=1, sabedoria=1, carisma=1),
        habilidades=habs,
    )
    atualizar_ficha(f)
    return f


# =====================================================================
# 1. DUENDE (p. 8–11)
# =====================================================================

def test_duende_tamanho_sem_dupla_contagem_furtividade_e_voo_sobre_base():
    # Minúsculo: For -1, deslocamento base 6m, Furtividade +5 (SEM duplicar para +10!)
    # Com Voo (+3m sobre base): deslocamento = 6 + 3 = 9m (não 12m!)
    f_min = _duende_com_escolhas(
        tamanho_id="Tamanho_Minusculo_Duende",
        dons={"atributo_1": "carisma", "atributo_2": "inteligencia"},
        presentes=["Voo_Duende", "Lingua_Natureza_Duende", "Visao_Feerica_Duende"],
    )
    assert f_min.descricao.tamanho == TamanhoEnum.MINUSCULO
    assert f_min.atributos.forca == 0       # 1 - 1 (Minúsculo)
    assert f_min.status.deslocamento == 9.0  # 6m base + 3m Voo
    # Furtividade: Des (1) + metade nv (0) + tamanho (+5) = 6 (NUNCA 11!)
    assert f_min.pericias["Furtividade"].total == 6

    # Médio + Voo: 9m base + 3m = 12m
    f_med = _duende_com_escolhas(
        tamanho_id="Tamanho_Medio_Duende",
        dons={"atributo_1": "carisma", "atributo_2": "inteligencia"},
        presentes=["Voo_Duende", "Lingua_Natureza_Duende", "Visao_Feerica_Duende"],
    )
    assert f_med.descricao.tamanho == TamanhoEnum.MEDIO
    assert f_med.status.deslocamento == 12.0  # 9m base + 3m Voo

    # Grande: Des -1, deslocamento base 9m, Furtividade -2 (SEM duplicar para -4!)
    f_grd = _duende_com_escolhas(
        tamanho_id="Tamanho_Grande_Duende",
        dons={"atributo_1": "forca", "atributo_2": "constituicao"},
        presentes=["Lingua_Natureza_Duende", "Visao_Feerica_Duende", "Encantar_Objetos_Duende"],
    )
    assert f_grd.descricao.tamanho == TamanhoEnum.GRANDE
    assert f_grd.atributos.destreza == 0    # 1 - 1 (Grande)
    assert f_grd.status.deslocamento == 9.0
    # Furtividade: Des (0) + tamanho (-2) = -2 (NUNCA -4!)
    assert f_grd.pericias["Furtividade"].total == -2


def test_duende_dons_rejeita_duplicata_mas_acumula_com_natureza_animal():
    # Tentar colocar +2 no mesmo atributo em Dons: só conta +1!
    f_dup = _duende_com_escolhas(
        natureza_id="Natureza_Vegetal_Duende",
        dons={"atributo_1": "carisma", "atributo_2": "carisma"},
    )
    assert f_dup.atributos.carisma == 2  # 1 base + 1 (ignora duplicata em Dons)

    # Natureza Animal (+1 Car) + Dons (+1 Car, +1 Des): ACUMULA para +2 Car!
    f_ani = _duende_com_escolhas(
        natureza_id="Natureza_Animal_Duende",
        animal_attr="carisma",
        dons={"atributo_1": "carisma", "atributo_2": "destreza"},
    )
    assert f_ani.atributos.carisma == 3  # 1 base + 1 Animal + 1 Dons
    assert f_ani.atributos.destreza == 2  # 1 base + 1 Dons


def test_duende_natureza_mineral_tabu_e_sonhos_malucos():
    f_sem = _duende_com_escolhas(
        natureza_id="Natureza_Mineral_Duende",
        tabu_id="Tabu_Diplomacia",
        sonhos_malucos=False,
    )
    assert any("Corte 5" in r for r in f_sem.status.rd)
    assert any("Fogo 5" in r for r in f_sem.status.rd)
    assert any("Perfuração 5" in r for r in f_sem.status.rd)
    # Tabu (Diplomacia): -5
    assert f_sem.pericias["Diplomacia"].total == f_sem.atributos.carisma - 5

    f_sm = _duende_com_escolhas(
        natureza_id="Natureza_Mineral_Duende",
        tabu_id="Tabu_Diplomacia",
        sonhos_malucos=True,
    )
    assert f_sm.status.pm.maximo == f_sem.status.pm.maximo + 2


def test_duende_gerador_sonhos_malucos_e_catalogo_escolhas():
    res = gerar_duende_aleatorio(seed=123)
    assert res["pm_bonus"] == 2
    assert res["dons"]["atributo_1"] != res["dons"]["atributo_2"]
    assert len(res["presentes"]) == 3
    assert len({p["id"] for p in res["presentes"]}) == 3
    assert len(TABUS_EXEMPLOS_DUENDE) == 22

    cat = montar_catalogo_escolhas()
    assert "Dons" in cat["PODERES_COM_ESCOLHA"]
    assert "Natureza Animal" in cat["PODERES_COM_ESCOLHA"]
    assert "Maldição" in cat["PODERES_COM_ESCOLHA"]
    assert "Metamorfose Animal" in cat["PODERES_COM_ESCOLHA"]
    assert "Limitações de Duende" in cat["PODERES_COM_ESCOLHA"]


# =====================================================================
# 2. EIRADAAN, GALOKK, MEIO-ELFO E SÁTIRO (p. 12–15)
# =====================================================================

def test_eiradaan_galokk_meio_elfo_satiro():
    # Eiradaan: Sab +2, Car +1, For -1; Misticismo pode usar Sab
    f_eir = Personagem(
        cabecalho=Cabecalho(nome="Eiradaan Teste", raca="Eiradaan"),
        classes=[ClasseInfo(nome="Arcanista", nivel=1, primaria=True, subclasse="Mago")],
        atributos_base=Atributos(forca=1, sabedoria=2, carisma=1),
    )
    atualizar_ficha(f_eir)
    assert f_eir.atributos.sabedoria == 4
    assert f_eir.atributos.carisma == 2
    assert f_eir.atributos.forca == 0
    assert "sab" in f_eir.pericias["Misticismo"].atributos_possiveis

    # Magia Instintiva: ao ativar magia_instintiva_sab, CD e PM passam a usar Sabedoria (4) em vez de Inteligência (0)
    cd_int = f_eir.combate.cd_magias
    pm_int = f_eir.status.pm.maximo
    f_eir.condicoes_ativas = ["magia_instintiva_sab"]
    atualizar_ficha(f_eir)
    assert f_eir.combate.cd_magias == cd_int + 4
    assert f_eir.status.pm.maximo == pm_int + 4
    assert DADOS_RACAS["Eiradaan"]["devotos"] == ["Allihanna", "Lena", "Thyatis", "Wynna"]

    # Galokk: For +1, Con +1, Car -1, +1 escolha; Grande; Intimidação com For
    f_gal = Personagem(
        cabecalho=Cabecalho(nome="Galokk Teste", raca="Galokk"),
        classes=[ClasseInfo(nome="Guerreiro", nivel=1, primaria=True)],
        atributos_base=Atributos(forca=2, constituicao=2, carisma=1),
        escolhas_atributos_raciais=["for"],
    )
    atualizar_ficha(f_gal)
    assert f_gal.descricao.tamanho == TamanhoEnum.GRANDE
    assert f_gal.atributos.forca == 4
    assert f_gal.atributos.constituicao == 3
    assert f_gal.atributos.carisma == 0
    assert "for" in f_gal.pericias["Intimidação"].atributos_possiveis

    # Meio-Elfo: Int +1, +1 em 2 atributos EXCETO Constituição; +1 perícias Car; +1 PM/nv ímpar
    f_me = Personagem(
        cabecalho=Cabecalho(nome="Meio-Elfo Teste", raca="Meio-Elfo"),
        classes=[ClasseInfo(nome="Bardo", nivel=3, primaria=True)],
        atributos_base=Atributos(constituicao=1, inteligencia=1, carisma=1),
        escolhas_atributos_raciais=["car", "con"],  # con deve ser ignorada!
    )
    atualizar_ficha(f_me)
    assert f_me.atributos.inteligencia == 2
    assert f_me.atributos.carisma == 2
    assert f_me.atributos.constituicao == 1  # exceto Constituição respeitado!
    # Nível 3 = 2 níveis ímpares (1º e 3º) -> +2 PM de Sangue Élfico
    assert any("Sangue Élfico" in x.fonte and x.valor == 2 for x in f_me.status.pm_calc.fontes)

    # Sátiro: Car +2, Des +1, Sab -1, 12m, +2 Atuação/Fortitude, Des em Atletismo
    f_sat = Personagem(
        cabecalho=Cabecalho(nome="Sátiro Teste", raca="Sátiro"),
        classes=[ClasseInfo(nome="Bardo", nivel=1, primaria=True)],
        atributos_base=Atributos(destreza=2, sabedoria=1, carisma=2),
    )
    atualizar_ficha(f_sat)
    assert f_sat.atributos.carisma == 4
    assert f_sat.atributos.destreza == 3
    assert f_sat.atributos.sabedoria == 0
    assert f_sat.status.deslocamento == 12.0
    assert "des" in f_sat.pericias["Atletismo"].atributos_possiveis
    assert any(a.nome == "Marrada" and a.dano == "1d6" for a in f_sat.combate.ataques)
