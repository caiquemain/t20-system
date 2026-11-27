"""Testes automatizados das escolhas interativas de suplementos (Ameaças + Atlas)."""
from src.dados_escolhas import montar_catalogo_escolhas
from src.models import Cabecalho, ClasseInfo, Personagem
from src.regras import atualizar_ficha


def _set_escolha(ficha: Personagem, hab_nome: str, **escolhas) -> Personagem:
    for h in ficha.habilidades:
        if h.nome == hab_nome:
            h.escolhas_aplicadas = {**(h.escolhas_aplicadas or {}), **escolhas}
    atualizar_ficha(ficha)
    return ficha


def test_catalogo_escolhas_possui_habilidades_nv1_e_suplementos():
    cat = montar_catalogo_escolhas()
    assert len(cat["HABILIDADES_CLASSE_NV1"]) >= 20
    pc = cat["PODERES_COM_ESCOLHA"]
    for chave in (
        "Origem Regional: Duplo Feérico",
        "Origem Regional: Aspirante a Herói",
        "Origem Regional: Futura Lenda",
        "Origem Regional: Cosmopolita",
        "Origem Regional: Estandarte Vivo",
        "Origem Regional: Estudante da Academia",
        "Origem Regional: De Outro Mundo",
        "Origem Regional: Tamalu",
        "Herança Dracônica",
        "Bênção de Kallyadranoch",
        "Talentos do Bando",
        "Maravilha Mecânica",
        "Terror Vivo",
        "Sapiência",
        "Esperteza Vulpina",
        "Papel Tribal",
    ):
        assert chave in pc, f"Faltando {chave} em PODERES_COM_ESCOLHA"


def test_duplo_feerico_habilidade_classe_e_excecao_magias():
    # 1) Guerreiro com Duplo Feérico escolhendo Fúria (Bárbaro)
    f = Personagem(
        cabecalho=Cabecalho(nome="Eco", raca="Humano", origem="Duplo Feérico", nivel_total=1),
        classes=[ClasseInfo(nome="Guerreiro", nivel=1, primaria=True)],
    )
    atualizar_ficha(f)
    _set_escolha(f, "Origem Regional: Duplo Feérico", habilidade_nv1="Bárbaro::Fúria")
    assert any(h.nome == "Fúria" and h.fonte == "Escolha: Origem Regional: Duplo Feérico" for h in f.habilidades)

    # 2) Troca para Magias (Arcanista) + Bola de Fogo/Seta Infalível -> +1 PM e 1 magia, remove Fúria
    _set_escolha(f, "Origem Regional: Duplo Feérico", habilidade_nv1="Arcanista::Magias", magia_1="Seta Infalível de Talude")
    nomes = [h.nome for h in f.habilidades]
    assert "Fúria" not in nomes
    assert f.status.pm.maximo == 4  # Guerreiro nv1 (3 PM) + 1 PM do Duplo Feérico (sem somar atributo)
    assert any(m.nome == "Seta Infalível de Talude" for m in f.combate.magias)


def test_outras_origens_regionais_com_escolha():
    # Aspirante a Herói (+1 em atributo escolhido)
    f_asp = Personagem(
        cabecalho=Cabecalho(nome="Aspirante", raca="Humano", origem="Aspirante a Herói", nivel_total=1),
        classes=[ClasseInfo(nome="Guerreiro", nivel=1, primaria=True)],
    )
    atualizar_ficha(f_asp)
    _set_escolha(f_asp, "Origem Regional: Aspirante a Herói", atributo="forca")
    assert f_asp.atributos.forca == 1

    # Estudante da Academia (magia arcana 1º círculo)
    f_acad = Personagem(
        cabecalho=Cabecalho(nome="Estudante", raca="Humano", origem="Estudante da Academia", nivel_total=1),
        classes=[ClasseInfo(nome="Guerreiro", nivel=1, primaria=True)],
    )
    atualizar_ficha(f_acad)
    _set_escolha(f_acad, "Origem Regional: Estudante da Academia", magia_1="Armadura Arcana")
    assert any(m.nome == "Armadura Arcana" for m in f_acad.combate.magias)

    # Tamalu (tatuagem de Defesa +1, depois troca para Magia de 1º círculo)
    f_tam = Personagem(
        cabecalho=Cabecalho(nome="Tamalu", raca="Humano", origem="Tamalu", nivel_total=1),
        classes=[ClasseInfo(nome="Nobre", nivel=1, primaria=True)],
    )
    atualizar_ficha(f_tam)
    _set_escolha(f_tam, "Origem Regional: Tamalu", tatuagem="defesa")
    assert f_tam.status.defesa.total == 11
    _set_escolha(f_tam, "Origem Regional: Tamalu", tatuagem="magia_1", magia_1="Curar Ferimentos")
    assert f_tam.status.defesa.total == 10
    assert any(m.nome == "Curar Ferimentos" for m in f_tam.combate.magias)


def test_escolhas_raciais_ameacas_kallyanach_kobolds_moreau_ceratops():
    # Kallyanach: Herança Dracônica (fogo) + Escamas Elementais (+2 Defesa, RD 10) + Armamento Kallyanach
    f_kal = Personagem(
        cabecalho=Cabecalho(nome="Kally", raca="Kallyanach", nivel_total=1),
        classes=[ClasseInfo(nome="Guerreiro", nivel=1, primaria=True)],
    )
    atualizar_ficha(f_kal)
    _set_escolha(f_kal, "Herança Dracônica", elemento="fogo")
    _set_escolha(f_kal, "Bênção de Kallyadranoch", bencao_1="Escamas Elementais", bencao_2="Armamento Kallyanach")
    assert f_kal.status.defesa.total == 12
    assert any("Armamento Kallyanach" in a.nome for a in f_kal.combate.ataques)
    heranca = next(h for h in f_kal.habilidades if h.nome == "Herança Dracônica")
    assert heranca.efeitos["rd_tipo"]["fogo"] == 10

    # Kobolds: Ex-Familiar (+2 PM)
    f_kob = Personagem(
        cabecalho=Cabecalho(nome="Bando", raca="Kobolds", nivel_total=1),
        classes=[ClasseInfo(nome="Ladino", nivel=1, primaria=True)],
    )
    atualizar_ficha(f_kob)
    _set_escolha(f_kob, "Talentos do Bando", talento_1="Ex-Familiar", talento_2="Organizadinhos")
    assert f_kob.status.pm.maximo == 6  # Ladino nv1 (4) + Ex-Familiar (+2)

    # Moreau (Raposa): Esperteza Vulpina (+2 em 2 perícias Int/Car)
    f_rap = Personagem(
        cabecalho=Cabecalho(nome="Raposa", raca="Moreau (Raposa)", nivel_total=1),
        classes=[ClasseInfo(nome="Ladino", nivel=1, primaria=True)],
    )
    atualizar_ficha(f_rap)
    _set_escolha(f_rap, "Esperteza Vulpina", pericia_bonus_1="Enganação", pericia_bonus_2="Investigação")
    assert f_rap.pericias["Enganação"].total >= 2
    assert f_rap.pericias["Investigação"].total >= 3  # +1 Int racial + 2 Esperteza Vulpina

    # Ceratops: Papel Tribal (treinado em Cura)
    f_cer = Personagem(
        cabecalho=Cabecalho(nome="Ceratops", raca="Ceratops", nivel_total=1),
        classes=[ClasseInfo(nome="Guerreiro", nivel=1, primaria=True)],
    )
    atualizar_ficha(f_cer)
    _set_escolha(f_cer, "Papel Tribal", pericia_1="Cura")
    assert f_cer.pericias["Cura"].treino > 0
