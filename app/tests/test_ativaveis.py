# -*- coding: utf-8 -*-
"""Testes do motor executável de Habilidades Ativáveis (regras/ativaveis.py)."""
from src.dados_habilidades import HABILIDADES_GERAIS
from src.dados_habilidades_classe import DADOS_HABILIDADES_CLASSE
from src.models import Atributos, Cabecalho, ClasseInfo, DistincaoPersonagem, Habilidade, Personagem
from src.regras import atualizar_ficha
from src.regras.ativaveis import (
    ativar_habilidade,
    extrair_especificacao_ativavel,
    listar_habilidades_ativaveis,
)


def _ficha(nivel: int = 6, classe: str = "Guerreiro") -> Personagem:
    return Personagem(
        cabecalho=Cabecalho(nome="Executor", raca="Humano"),
        classes=[ClasseInfo(nome=classe, nivel=nivel, primaria=True)],
        atributos_base=Atributos(forca=2, destreza=2, constituicao=2, inteligencia=2, sabedoria=2, carisma=2),
    )


def test_extracao_e_execucao_habilidade_ativavel_com_pm_e_buff():
    f = _ficha(nivel=6, classe="Cavaleiro")
    # Postura de Combate de Heróis de Arton (2 PM, ação movimento, duração cena)
    p = DADOS_HABILIDADES_CLASSE["HA_CAV_Postura_Quebra_Magia"]
    f.habilidades.append(Habilidade(nome=p["nome"], tipo=p["tipo"], descricao=p["descricao"], efeitos=dict(p["efeitos"])))
    f = atualizar_ficha(f)

    ativaveis = listar_habilidades_ativaveis(f)
    spec = next((a for a in ativaveis if a["nome"] == p["nome"]), None)
    assert spec is not None
    assert spec["custo_pm"] == 2
    assert spec["acao"] == "movimento"
    assert spec["duracao"] == "cena"
    assert spec["pode_ativar"] is True

    pm_antes = f.status.pm.atual
    res = ativar_habilidade(f, p["nome"])
    assert res["sucesso"] is True
    assert res["custo_pm"] == 2
    assert f.status.pm.atual == pm_antes - 2
    assert any(b.origem == p["nome"] for b in f.status.buffs)


def test_bloqueio_por_limite_pm_e_pm_insuficiente():
    f = _ficha(nivel=1, classe="Guerreiro")
    p = HABILIDADES_GERAIS["HA_Contra_Ataque"]  # 2 PM (excede limite de nível 1)
    f.habilidades.append(Habilidade(nome=p["nome"], tipo=p["tipo"], descricao=p["descricao"], efeitos=dict(p["efeitos"])))
    f = atualizar_ficha(f)

    res = ativar_habilidade(f, "Contra-Ataque")
    assert res["sucesso"] is False
    assert "limite" in res["erro"].lower()

    # Nível 5 com PM zerado -> bloqueia por PM insuficiente
    f5 = _ficha(nivel=5, classe="Guerreiro")
    f5.habilidades.append(Habilidade(nome=p["nome"], tipo=p["tipo"], descricao=p["descricao"], efeitos=dict(p["efeitos"])))
    f5 = atualizar_ficha(f5)
    f5.status.pm.atual = 1
    res5 = ativar_habilidade(f5, "Contra-Ataque")
    assert res5["sucesso"] is False
    assert "insuficiente" in res5["erro"].lower()


def test_habilidade_passiva_nao_ativa_e_distincao_ativavel_funciona():
    f = _ficha(nivel=7, classe="Guerreiro")
    f.distincoes = [
        DistincaoPersonagem(nome="Campeão de Dojo", admitido=True, poderes=["Golpe Concentrado"])
    ]
    f = atualizar_ficha(f)
    # Golpe Concentrado custa 2 PM (ação de movimento)
    res = ativar_habilidade(f, "Golpe Concentrado")
    assert res["sucesso"] is True
    assert res["custo_pm"] == 2
    assert res["acao"] == "movimento"

    passiva = Habilidade(nome="Grandão", tipo="Poder Geral (Destino)", descricao="Capacidade de carga +5 espaços.", efeitos={"carga_max_bonus": 5})
    assert extrair_especificacao_ativavel(passiva)["ativavel"] is False
