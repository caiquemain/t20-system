"""Testes das regras do Capítulo 5 — Jogando (T20 JdA, p.220–239)."""
from src.regras import (
    avaliar_teste,
    calcular_bonus_ajuda,
    pode_escolher_zero,
    calcular_cd_habilidade,
    combinar_multiplicadores,
    limitar_chance_falha,
    calcular_dano_recebido,
    calcular_limiar_morte,
    calcular_pv_objeto,
)
from src.regras.jogando import (
    TABELA_DIFICULDADES,
    TESTES_ESTENDIDOS,
    ALCANCES_PADRAO,
    TIPOS_DE_EFEITO,
    TIPOS_DE_DANO,
    MANOBRAS_COMBATE,
    SITUACOES_ESPECIAIS,
    ESTATISTICAS_OBJETOS,
)


def test_tabelas_e_constantes_capitulo_5():
    assert TABELA_DIFICULDADES["Fácil"] == 5
    assert TABELA_DIFICULDADES["Quase Impossível"] == 40
    assert TESTES_ESTENDIDOS["Baixa"]["sucessos"] == 3
    assert TESTES_ESTENDIDOS["Média"]["sucessos"] == 5
    assert TESTES_ESTENDIDOS["Alta"]["sucessos"] == 7
    assert ALCANCES_PADRAO["Curto"] == {"metros": 9, "quadrados": 6}
    assert ALCANCES_PADRAO["Médio"] == {"metros": 30, "quadrados": 20}
    assert ALCANCES_PADRAO["Longo"] == {"metros": 90, "quadrados": 60}
    assert len(TIPOS_DE_EFEITO) == 18
    assert len(TIPOS_DE_DANO) == 11
    assert len(MANOBRAS_COMBATE) == 5
    assert len(SITUACOES_ESPECIAIS["atacante"]) == 6
    assert len(SITUACOES_ESPECIAIS["alvo"]) == 7
    assert len(ESTATISTICAS_OBJETOS) == 21


def test_testes_sucesso_falha_ajudar_e_escolher_zero():
    # 20 natural sempre passa; 1 natural sempre falha
    assert avaliar_teste(20, 0, 40)["sucesso"] is True
    assert avaliar_teste(1, 50, 5)["sucesso"] is False
    assert avaliar_teste(10, 5, 15)["sucesso"] is True
    assert avaliar_teste(9, 5, 15)["sucesso"] is False

    # Ajudar (p.221): CD 10 -> +1, 20 -> +2, 30 -> +3
    assert calcular_bonus_ajuda(9) == 0
    assert calcular_bonus_ajuda(10) == 1
    assert calcular_bonus_ajuda(19) == 1
    assert calcular_bonus_ajuda(20) == 2
    assert calcular_bonus_ajuda(30) == 3

    # Escolher 0 (p.222)
    assert pode_escolher_zero(15, 15) is True
    assert pode_escolher_zero(14, 15) is False


def test_clarificacoes_ordem_dano_multiplicadores_e_chance_falha():
    # Exemplo oficial (p.226): Bola de Fogo 26 de dano, RD Fogo 10
    # Passou Ref + Durão -> 26//2=13 -> 13//2=6 -> 6-10=0
    assert calcular_dano_recebido(26, passou_resistencia_metade=True, divisores_metade=1, rd=10) == 0
    # Passou Ref sem Durão -> 13-10=3
    assert calcular_dano_recebido(26, passou_resistencia_metade=True, rd=10) == 3
    # Falhou Ref com Durão -> 13-10=3
    assert calcular_dano_recebido(26, divisores_metade=1, rd=10) == 3
    # Falhou Ref sem Durão -> 26-10=16
    assert calcular_dano_recebido(26, rd=10) == 16

    # Vulnerabilidade (exemplo p.229): 15 de frio * 1.5 = 22
    assert calcular_dano_recebido(15, vulneravel=True) == 22

    # Perda de Vida (p.228) ignora RD
    assert calcular_dano_recebido(12, rd=10, perda_de_vida=True) == 12

    # Multiplicações combinadas (p.226): x2 + x2 = x3
    assert combinar_multiplicadores([2, 2]) == 3
    assert combinar_multiplicadores([2, 3]) == 4

    # Chance de falha (p.226): nunca acima de 75%
    assert limitar_chance_falha([50, 50]) == 75
    assert limitar_chance_falha([20, 20]) == 40


def test_cd_habilidade_limiar_morte_e_objetos():
    # Exemplo oficial (p.227): Marsha Yleus, Nobre 10º nível com Car 4 -> CD 19
    assert calcular_cd_habilidade(10, 4) == 19

    # Exemplo oficial (p.236): Oberon com 12 PV morre em -10; com 30 PV morre em -15
    assert calcular_limiar_morte(12) == -10
    assert calcular_limiar_morte(30) == -15

    # Tabela 5-4 (p.239): PV por tamanho
    assert calcular_pv_objeto(10, "Reduzido") == 5
    assert calcular_pv_objeto(10, "Aumentado") == 20
    assert calcular_pv_objeto(10, "Gigante") == 50
