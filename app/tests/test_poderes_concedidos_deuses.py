# -*- coding: utf-8 -*-
"""Testes dos Novos Poderes Concedidos — Deuses de Arton (Cap. 1, p. 42–47)."""
from src.dados_deuses import DADOS_DEUSES
from src.dados_poderes_concedidos import DADOS_PODERES_CONCEDIDOS
from src.dados_poderes_concedidos_deuses import DADOS_PODERES_CONCEDIDOS_DEUSES
from src.dados_suplementos import FONTE_DEUSES
from src.models import Atributos, Cabecalho, ClasseInfo, Habilidade, Personagem
from src.regras import atualizar_ficha
from src.regras.ativaveis import ativar_habilidade


def _ficha(nivel: int = 5) -> Personagem:
    return Personagem(
        cabecalho=Cabecalho(nome="Devoto Teste", raca="Humano"),
        classes=[ClasseInfo(nome="Frade", nivel=nivel, primaria=True)],
        atributos_base=Atributos(
            forca=1, destreza=2, constituicao=2, inteligencia=2, sabedoria=4, carisma=2
        ),
    )


def _add(f: Personagem, nome: str):
    d = DADOS_PODERES_CONCEDIDOS[nome]
    f.habilidades.append(
        Habilidade(
            nome=d["nome"],
            tipo=d["tipo"],
            descricao=d["descricao"],
            efeitos=dict(d["efeitos"]),
            fonte="Devoção",
        )
    )


def test_catalogo_poderes_concedidos_deuses_completo_nos_20_deuses():
    assert len(DADOS_PODERES_CONCEDIDOS_DEUSES) == 75
    for nome, d in DADOS_PODERES_CONCEDIDOS_DEUSES.items():
        assert nome in DADOS_PODERES_CONCEDIDOS
        assert d["fonte"] == FONTE_DEUSES
        assert d["efeitos"]
        assert d["deuses"]
        for deus in d["deuses"]:
            assert deus in DADOS_DEUSES
            assert nome in DADOS_DEUSES[deus]["poderes"]

    # Cada um dos 20 deuses maiores recebeu ao menos 4 novos poderes concedidos
    for deus_nome, deus_dados in DADOS_DEUSES.items():
        novos = [p for p in deus_dados["poderes"] if p in DADOS_PODERES_CONCEDIDOS_DEUSES]
        assert len(novos) >= 4, f"{deus_nome} tem apenas {len(novos)} novos poderes: {novos}"


def test_efeitos_passivos_e_ativaveis_poderes_concedidos_deuses():
    base = atualizar_ficha(_ficha(nivel=5))

    f = _ficha(nivel=5)
    _add(f, "Abraço da Fênix")
    _add(f, "Dom da Vontade")
    _add(f, "Perceber Farsas")
    _add(f, "Terror Profundo")
    _add(f, "Jurista Divino")
    _add(f, "Navegador Sagrado")
    _add(f, "Palavra de Poder")
    _add(f, "Pilar de Heredrimm")
    f = atualizar_ficha(f)

    assert "Fogo" in f.status.imunidades
    assert "Ilusão" in f.status.imunidades
    assert f.pericias["Vontade"].total == base.pericias["Vontade"].total + 2
    assert f.pericias["Intuição"].total == base.pericias["Intuição"].total + 5
    assert f.pericias["Intimidação"].total == base.pericias["Intimidação"].total + 2
    assert "sab" in f.pericias["Nobreza"].atributos_possiveis
    assert "sab" in f.pericias["Pilotagem"].atributos_possiveis
    assert any(m.nome == "Comando" for m in f.combate.magias)

    # Ativável: Pilar de Heredrimm (2 PM, cena, +2 Defesa / RD 5)
    pm_antes = f.status.pm.atual
    res = ativar_habilidade(f, "Pilar de Heredrimm")
    assert res["sucesso"] is True
    assert res["custo_pm"] == 2
    assert f.status.pm.atual == pm_antes - 2
    assert any(b.origem == "Pilar de Heredrimm" for b in f.status.buffs)
