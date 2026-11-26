# -*- coding: utf-8 -*-
"""Testes dos Toques Finais (T20 JdA p.106-111): envelhecimento, raças longevas, descanso e descrição."""
from src.models import Personagem, ClasseInfo, Cabecalho, Atributos, Descricao
from src.regras import atualizar_ficha


def test_envelhecimento_humano_maduro_e_velho():
    base = Atributos(forca=3, destreza=2, constituicao=2, inteligencia=1, sabedoria=1, carisma=1)

    f_adulto = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Jovem", raca="Humano"),
        classes=[ClasseInfo(nome="Guerreiro", nivel=1, primaria=True)],
        atributos_base=base.model_copy(),
        descricao=Descricao(idade=25),
    ))
    assert f_adulto.descricao.faixa_etaria == "Adulto"
    assert f_adulto.atributos.forca == 3
    assert f_adulto.atributos.inteligencia == 1

    f_maduro = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Maduro", raca="Humano"),
        classes=[ClasseInfo(nome="Guerreiro", nivel=1, primaria=True)],
        atributos_base=base.model_copy(),
        descricao=Descricao(idade=45),
    ))
    assert f_maduro.descricao.faixa_etaria == "Maduro"
    assert f_maduro.atributos.forca == 2
    assert f_maduro.atributos.destreza == 1
    assert f_maduro.atributos.constituicao == 1
    assert f_maduro.atributos.inteligencia == 2
    assert f_maduro.atributos.sabedoria == 2
    assert f_maduro.atributos.carisma == 2

    f_velho = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Velho", raca="Humano"),
        classes=[ClasseInfo(nome="Guerreiro", nivel=1, primaria=True)],
        atributos_base=base.model_copy(),
        descricao=Descricao(idade=70),
    ))
    assert f_velho.descricao.faixa_etaria == "Velho"
    assert f_velho.atributos.forca == 0       # 3 - 3
    assert f_velho.atributos.destreza == -1   # 2 - 3
    assert f_velho.atributos.constituicao == -1
    assert f_velho.atributos.inteligencia == 3  # 1 + 2
    assert f_velho.atributos.sabedoria == 3
    assert f_velho.atributos.carisma == 3


def test_racas_longevas_multiplicador_envelhecimento():
    # Anão (x2): 80 anos ainda é Adulto; 90 é Maduro; 140 é Velho
    f_anao_80 = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Thorin", raca="Anão"),
        classes=[ClasseInfo(nome="Guerreiro", nivel=1, primaria=True)],
        descricao=Descricao(idade=80),
    ))
    assert f_anao_80.descricao.faixa_etaria == "Adulto"

    f_anao_90 = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Thorin", raca="Anão"),
        classes=[ClasseInfo(nome="Guerreiro", nivel=1, primaria=True)],
        descricao=Descricao(idade=90),
    ))
    assert f_anao_90.descricao.faixa_etaria == "Maduro"

    # Elfo (x5): 200 anos ainda é Adulto; 225 é Maduro; 350 é Velho
    f_elfo_200 = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Helior", raca="Elfo"),
        classes=[ClasseInfo(nome="Caçador", nivel=7, primaria=True)],
        descricao=Descricao(idade=200),
    ))
    assert f_elfo_200.descricao.faixa_etaria == "Adulto"

    f_elfo_350 = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Helior", raca="Elfo"),
        classes=[ClasseInfo(nome="Caçador", nivel=7, primaria=True)],
        descricao=Descricao(idade=350),
    ))
    assert f_elfo_350.descricao.faixa_etaria == "Velho"


def test_recuperacao_descanso_padrao_estoico_e_vida_rustica():
    # Exemplo do livro (p.106): Helior, 7º nível -> Ruim 3, Normal 7, Confortável 14, Luxuosa 21
    f7 = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Helior", raca="Elfo"),
        classes=[ClasseInfo(nome="Caçador", nivel=7, primaria=True)],
    ))
    assert f7.status.descanso_calc["ruim"] == 3
    assert f7.status.descanso_calc["normal"] == 7
    assert f7.status.descanso_calc["confortavel"] == 14
    assert f7.status.descanso_calc["luxuosa"] == 21

    # Estoico (Refugiado): +1 categoria (Ruim -> Normal 7, Normal -> Confortável 14, Confortável -> Luxuosa 21)
    f_est = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Refug", raca="Humano", origem="Refugiado"),
        classes=[ClasseInfo(nome="Guerreiro", nivel=7, primaria=True)],
        escolhas_origem=["Estoico"],
    ))
    assert f_est.status.descanso_calc["ruim"] == 7
    assert f_est.status.descanso_calc["normal"] == 14
    assert f_est.status.descanso_calc["confortavel"] == 21
    assert f_est.status.descanso_calc["luxuosa"] == 21

    # Vida Rústica (Selvagem): recuperação mínima = nível (Ruim sobe de 3 para 7)
    f_vr = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Selv", raca="Humano", origem="Selvagem"),
        classes=[ClasseInfo(nome="Bárbaro", nivel=7, primaria=True)],
        escolhas_origem=["Vida Rústica"],
    ))
    assert f_vr.status.descanso_calc["ruim"] == 7
    assert f_vr.status.descanso_calc["normal"] == 7


def test_descricao_alinhamento_personalidade():
    f = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Ignis Crae", raca="Golem"),
        classes=[ClasseInfo(nome="Paladino", nivel=1, primaria=True)],
        descricao=Descricao(
            alinhamento="LB",
            personalidade="Honrado e implacável contra o mal.",
            aparencia="Golem de aço dourado.",
            historia="Líder da Ordem da Redenção.",
        ),
    ))
    assert f.descricao.alinhamento == "LB"
    assert f.descricao.personalidade == "Honrado e implacável contra o mal."
