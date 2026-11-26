"""Testes do Apêndice — Lista de Condições (T20 JdA, p.394–395)."""
from src.dados_condicoes import DADOS_CONDICOES
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Magia
from src.regras import (
    atualizar_ficha,
    calcular_custo_magia,
    expandir_condicoes,
    aplicar_condicao_com_escalonamento,
    calcular_deslocamento_lento,
    calcular_efeitos_condicoes,
)


def test_catalogo_35_condicoes_e_subcondicoes():
    assert len(DADOS_CONDICOES) == 35
    # Expansão recursiva: Petrificado -> Inconsciente -> Indefeso -> Desprevenido
    assert expandir_condicoes(["Petrificado"]) == {"Petrificado", "Inconsciente", "Indefeso", "Desprevenido"}
    # Exausto -> Debilitado, Lento, Vulnerável
    assert expandir_condicoes(["Exausto"]) == {"Exausto", "Debilitado", "Lento", "Vulnerável"}
    # Fatigado -> Fraco, Vulnerável
    assert expandir_condicoes(["Fatigado"]) == {"Fatigado", "Fraco", "Vulnerável"}


def test_escalonamento_oficial_e_nao_acumulo():
    # Escalonamentos oficiais (p.394-395)
    assert aplicar_condicao_com_escalonamento(["Abalado"], "Abalado") == ["Apavorado"]
    assert aplicar_condicao_com_escalonamento(["Fatigado"], "Fatigado") == ["Exausto"]
    assert aplicar_condicao_com_escalonamento(["Exausto"], "Exausto") == ["Inconsciente"]
    assert aplicar_condicao_com_escalonamento(["Fraco"], "Fraco") == ["Debilitado"]
    assert aplicar_condicao_com_escalonamento(["Debilitado"], "Debilitado") == ["Inconsciente"]
    assert aplicar_condicao_com_escalonamento(["Frustrado"], "Frustrado") == ["Esmorecido"]

    # Exemplo oficial (p.394): Desprevenido (-5) e Vulnerável (-2) -> -5 na Defesa, não -7
    ef = calcular_efeitos_condicoes(["Desprevenido", "Vulnerável"])
    assert ef["defesa"] == -5

    # Caído é cumulativo com outras condições
    ef_caido = calcular_efeitos_condicoes(["Desprevenido", "Caído"])
    assert ef_caido["defesa"] == -5
    assert ef_caido["defesa_cac"] == -5
    assert ef_caido["defesa_dist"] == 5
    assert ef_caido["deslocamento"] == 1.5

    # Lento arredonda metade para baixo para incremento de 1,5m
    assert calcular_deslocamento_lento(9.0) == 4.5
    assert calcular_deslocamento_lento(7.5) == 3.0
    assert calcular_deslocamento_lento(6.0) == 3.0


def test_condicoes_ativas_aplicadas_na_ficha():
    base = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Herói", raca="Humano"),
        classes=[ClasseInfo(nome="Arcanista", nivel=5, primaria=True, subclasse="Mago")],
        atributos_base=Atributos(forca=2, destreza=2, constituicao=2, inteligencia=3),
    ))
    afetado = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Herói", raca="Humano"),
        classes=[ClasseInfo(nome="Arcanista", nivel=5, primaria=True, subclasse="Mago")],
        atributos_base=Atributos(forca=2, destreza=2, constituicao=2, inteligencia=3),
        condicoes_ativas=["Desprevenido", "Vulnerável", "Abalado", "Alquebrado"],
    ))
    # Defesa: -5 (Desprevenido prevalece sobre Vulnerável -2)
    assert afetado.status.defesa.total == base.status.defesa.total - 5
    # Reflexos: -5 (Desprevenido prevalece sobre Abalado -2)
    assert afetado.pericias["Reflexos"].total == base.pericias["Reflexos"].total - 5
    # Fortitude: -2 (Abalado)
    assert afetado.pericias["Fortitude"].total == base.pericias["Fortitude"].total - 2
    # Alquebrado: +1 PM no custo de magia (1º círculo 1 PM -> 2 PM)
    bola1 = Magia(nome="Seta Infalível", circulo=1, tipo="Arcana")
    assert calcular_custo_magia(afetado, bola1).total == 2
