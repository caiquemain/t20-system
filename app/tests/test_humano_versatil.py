"""Testes do Humano / Versátil (T20 JdA p.19).

Versátil: "Você se torna treinado em DUAS perícias à sua escolha.
Você pode trocar UMA dessas perícias por um poder geral à sua escolha."

Modelo de dados (frontend RacialAbilityRow.tsx):
- Bloco E: perícia fixa salva em 'pericia_1'
- Bloco D: slot flexível salva em 'pericia_2' (perícia) OU 'poder_geral' (poder)

Backend consome:
- pericia_1 / pericia_2 -> pericias.py, chaves_busca
- poder_geral -> habilidades.py, sincronizar_poderes_habilidades
"""
import pytest
from src.models import Personagem, Cabecalho, ClasseInfo
from src.regras import atualizar_ficha
from src.regras.habilidades import (
    garantir_habilidades_iniciais,
    sincronizar_poderes_habilidades,
)
from src.regras.pericias import inicializar_pericias


def _ficha_humano(classe="Guerreiro", nivel=1):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Humano Teste", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome=classe, nivel=nivel, primaria=True)]
    return f


def _achar_versatil(f):
    hab = next((h for h in f.habilidades if h.nome == "Versátil"), None)
    assert hab is not None, "Habilidade Versátil não foi criada por garantir_habilidades_iniciais"
    return hab


# ===================================================================
# 1. Fluxo completo (via atualizar_ficha) - o caminho real do servidor
# ===================================================================

def test_humano_duas_pericias_treinadas():
    """Humano escolhe 2 perícias -> ambas ficam treinadas.

    Nota: Furtividade e Atletismo NÃO são perícias fixas de Guerreiro,
    então o treino vem só do Versátil.
    """
    f = _ficha_humano()
    atualizar_ficha(f)
    versatil = _achar_versatil(f)
    versatil.escolhas_aplicadas = {
        "pericia_1": "Furtividade",
        "pericia_2": "Atletismo",
    }
    atualizar_ficha(f)

    assert f.pericias["Furtividade"].treino == 1, "pericia_1 não foi aplicada"
    assert f.pericias["Atletismo"].treino == 1, "pericia_2 não foi aplicada"


def test_humano_pericia_mais_poder_geral():
    """Humano troca 1 perícia por poder geral."""
    f = _ficha_humano()
    atualizar_ficha(f)
    versatil = _achar_versatil(f)
    versatil.escolhas_aplicadas = {
        "pericia_1": "Furtividade",
        "poder_geral": "Ataque Poderoso",
    }
    atualizar_ficha(f)

    assert f.pericias["Furtividade"].treino == 1
    assert f.pericias["Atletismo"].treino == 0, "pericia_2 fantasma foi treinada"

    filhas = [h for h in f.habilidades if h.fonte == "Habilidade: Versátil"]
    assert len(filhas) == 1, f"Esperava 1 habilidade filha, achei {len(filhas)}"
    assert filhas[0].nome == "Ataque Poderoso"


# ===================================================================
# 2. Testes unitários
# ===================================================================

def test_pericia_1_isolado_aplica_treino():
    f = _ficha_humano()
    garantir_habilidades_iniciais(f)
    versatil = _achar_versatil(f)
    versatil.escolhas_aplicadas = {"pericia_1": "Furtividade"}
    inicializar_pericias(f)
    assert f.pericias["Furtividade"].treino == 1
    assert f.pericias["Atletismo"].treino == 0


def test_poder_geral_isolado_cria_habilidade():
    f = _ficha_humano()
    garantir_habilidades_iniciais(f)
    versatil = _achar_versatil(f)
    versatil.escolhas_aplicadas = {"poder_geral": "Ataque Poderoso"}
    sincronizar_poderes_habilidades(f)

    filhas = [h for h in f.habilidades if h.fonte == "Habilidade: Versátil"]
    assert any(h.nome == "Ataque Poderoso" for h in filhas)


def test_escolhas_sobrevivem_a_reprocessamentos_sucessivos():
    """Escolhas não são apagadas por múltiplos atualizar_ficha."""
    f = _ficha_humano()
    atualizar_ficha(f)
    versatil = _achar_versatil(f)
    versatil.escolhas_aplicadas = {
        "pericia_1": "Furtividade",
        "pericia_2": "Atletismo",
    }
    for _ in range(3):
        atualizar_ficha(f)

    versatil_final = _achar_versatil(f)
    assert versatil_final.escolhas_aplicadas.get("pericia_1") == "Furtividade"
    assert versatil_final.escolhas_aplicadas.get("pericia_2") == "Atletismo"
    assert f.pericias["Furtividade"].treino == 1
    assert f.pericias["Atletismo"].treino == 1


def test_nao_duplica_versatil_em_varios_recalculos():
    f = _ficha_humano()
    for _ in range(5):
        atualizar_ficha(f)
    ocorrencias = [h for h in f.habilidades if h.nome == "Versátil"]
    assert len(ocorrencias) == 1, f"Versátil duplicada: {len(ocorrencias)} cópias"


# ===================================================================
# 3. Validação de "só uma troca" (limite do livro)
# ===================================================================
# O FRONTEND limita a 1 troca. O BACKEND não valida.
# Se um dia o backend ganhar validação, remova o xfail.

def test_backend_nao_cria_tres_beneficios_com_poder_e_duas_pericias():
    """Se cliente malicioso enviar pericia_1 + pericia_2 + poder_geral,
    no máximo 2 benefícios efetivos devem sobreviver.

    O livro permite apenas 2 slots (2 perícias OU 1 perícia + 1 poder).
    """
    f = _ficha_humano()
    atualizar_ficha(f)
    versatil = _achar_versatil(f)
    versatil.escolhas_aplicadas = {
        "pericia_1": "Furtividade",
        "pericia_2": "Atletismo",
        "poder_geral": "Ataque Poderoso",
    }
    atualizar_ficha(f)

    treinadas = [
        p for p in ("Furtividade", "Atletismo")
        if f.pericias[p].treino == 1
    ]
    filhas = [h for h in f.habilidades if h.fonte == "Habilidade: Versátil"]

    total_beneficios = len(treinadas) + len(filhas)
    assert total_beneficios <= 2, (
        f"Humano recebeu {total_beneficios} benefícios com 3 chaves preenchidas: "
        f"treinadas={treinadas}, filhas={[h.nome for h in filhas]}"
    )


def test_pericia_invalida_em_pericia_1_nao_cria_lixo():
    """Nome que não é perícia em pericia_1 não deve criar nada nem quebrar."""
    f = _ficha_humano()
    atualizar_ficha(f)
    versatil = _achar_versatil(f)
    versatil.escolhas_aplicadas = {
        "pericia_1": "Isso Nao Existe",
        "pericia_2": "Furtividade",
    }
    atualizar_ficha(f)
    assert f.pericias["Furtividade"].treino == 1
    filhas = [h for h in f.habilidades if h.fonte == "Habilidade: Versátil"]
    assert filhas == []
