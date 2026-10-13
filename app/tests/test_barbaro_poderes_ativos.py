"""Bárbaro — poderes ativos e declarativos (T20 JdA p.41-42).

Contrato de dados: cada poder ativo deve expor sua mecânica em `efeitos`
de forma declarativa (VTT-ready), no mesmo padrão da Fúria
(acao_ativavel) ou chaves dedicadas (pv_temp_em_furia, em_furia, etc.).

Estes testes NAO simulam uso em combate — apenas validam que o motor
expõe a estrutura que um VTT / mod consumiria. Comportamento real sera
coberto quando o motor ganhar estado mutavel de combate.
"""
import pytest
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Habilidade
from src.regras import atualizar_ficha
from src.dados_habilidades_classe import DADOS_HABILIDADES_CLASSE


def _barbaro(nivel=1, forca=4, sabedoria=0):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Barb", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Bárbaro", nivel=nivel, primaria=True)]
    f.atributos_base = Atributos(constituicao=3, forca=forca, sabedoria=sabedoria)
    f.atributos = f.atributos_base.model_copy()
    return f


def _add(f, nome, tipo="Poder de Bárbaro", efeitos=None, escolhas=None):
    f.habilidades.append(Habilidade(
        nome=nome, tipo=tipo,
        efeitos=efeitos or {},
        escolhas_aplicadas=escolhas or {},
    ))


def _efeitos_no_catalogo(chave):
    return DADOS_HABILIDADES_CLASSE[chave].get("efeitos", {})


# ===================================================================
# Contrato de catalogo — cada poder deve ter efeitos NAO-vaZios
# ===================================================================

PODERES_ATIVOS = [
    "BARBARO_ALMA_BRONZE",
    "BARBARO_BRADO_ASSUSTADOR",
    "BARBARO_DESTRUIDOR",
    "BARBARO_ESPIRITO_INQUEBRAVEL",
    "BARBARO_FORCA_INDOMAVEL",
    "BARBARO_FRENESI",
    "BARBARO_FURIA_RAIVOSA",
    "BARBARO_GOLPE_PODEROSO",
    "BARBARO_IMPETO",
    "BARBARO_INVESTIDA_IMPRUDENTE",
    "BARBARO_SANGUE_INIMIGOS",
    "BARBARO_VIGOR_PRIMAL",
]


@pytest.mark.parametrize("chave", PODERES_ATIVOS)
def test_catalogo_tem_efeitos_declarativos(chave):
    ef = _efeitos_no_catalogo(chave)
    assert ef, f"{chave} ainda tem efeitos vazios"


# ===================================================================
# Shape de acao_ativavel (custo_pm + acao + efeito + nota/gatilho)
# ===================================================================

def _assert_acao_ativavel(ef, *, pode_ter_custo_variavel=False):
    """Valida o shape minimo do bloco acao_ativavel."""
    a = ef.get("acao_ativavel") or ef.get("habilidade_ativavel")
    assert a, "esperado acao_ativavel ou habilidade_ativavel"
    assert "custo_pm" in a or pode_ter_custo_variavel, (
        f"acao_ativavel sem custo_pm: {a}"
    )
    assert "acao" in a, f"acao_ativavel sem acao: {a}"
    assert "efeito" in a or "descricao" in a, (
        f"acao_ativavel sem efeito/descricao: {a}"
    )


def test_alma_de_bronze_pv_temp_em_furia():
    ef = _efeitos_no_catalogo("BARBARO_ALMA_BRONZE")
    pv_temp = ef.get("pv_temp_em_furia")
    assert isinstance(pv_temp, dict), f"esperado dict: {ef}"
    assert pv_temp.get("nivel") is True
    assert pv_temp.get("atributo") == "forca"


def test_brado_assustador_acao_ativavel():
    ef = _efeitos_no_catalogo("BARBARO_BRADO_ASSUSTADOR")
    _assert_acao_ativavel(ef)
    a = ef["acao_ativavel"]
    assert a["custo_pm"] == 1
    assert a["acao"] == "movimento"
    assert a["alcance"] == "curto"
    assert a.get("tipo_efeito") == "medo"


def test_destruidor_rerola_dado_dano():
    ef = _efeitos_no_catalogo("BARBARO_DESTRUIDOR")
    r = ef.get("rerola_dado_dano")
    assert isinstance(r, dict), f"esperado dict: {ef}"
    assert r.get("valores") == [1, 2]
    assert r.get("arma") == "duas_maos_corpo_a_corpo"


def test_espirito_inquebravel_em_furia():
    ef = _efeitos_no_catalogo("BARBARO_ESPIRITO_INQUEBRAVEL")
    e = ef.get("em_furia")
    assert isinstance(e, dict), f"esperado dict: {ef}"
    assert e.get("nao_inconsciente_em_0pv") is True
    assert e.get("morte_em_negativo") == "metade_pv_max"


def test_forca_indomavel_acao_ativavel():
    ef = _efeitos_no_catalogo("BARBARO_FORCA_INDOMAVEL")
    _assert_acao_ativavel(ef)
    a = ef["acao_ativavel"]
    assert a["custo_pm"] == 1
    assert a["acao"] == "livre"
    assert a["efeito"] == "soma_nivel_teste"


def test_frenesi_acao_ativavel():
    ef = _efeitos_no_catalogo("BARBARO_FRENESI")
    _assert_acao_ativavel(ef)
    a = ef["acao_ativavel"]
    assert a["custo_pm"] == 2
    assert a["acao"] == "reacao"
    assert a["efeito"] == "ataque_adicional"
    assert a.get("gatilho") == "acao_agredir_em_furia"
    assert a.get("limite") == "uma_vez_por_rodada"


def test_furia_raivosa_acao_ativavel():
    ef = _efeitos_no_catalogo("BARBARO_FURIA_RAIVOSA")
    _assert_acao_ativavel(ef)
    a = ef["acao_ativavel"]
    assert a["custo_pm"] == 1
    assert a["acao"] == "livre"
    assert a["efeito"] == "estender_furia_1_rodada"


def test_golpe_poderoso_acao_ativavel():
    ef = _efeitos_no_catalogo("BARBARO_GOLPE_PODEROSO")
    _assert_acao_ativavel(ef)
    a = ef["acao_ativavel"]
    assert a["custo_pm"] == 1
    assert a["efeito"] == "dado_extra_dano"
    assert a["dado_extra"] == 1


def test_impeto_acao_ativavel():
    ef = _efeitos_no_catalogo("BARBARO_IMPETO")
    _assert_acao_ativavel(ef)
    a = ef["acao_ativavel"]
    assert a["custo_pm"] == 1
    assert a["efeito"] == "deslocamento_bonus_temporario"
    assert a["valor"] == 6
    assert a["duracao"] == "rodada"


def test_investida_imprudente_acao_ativavel():
    ef = _efeitos_no_catalogo("BARBARO_INVESTIDA_IMPRUDENTE")
    _assert_acao_ativavel(ef, pode_ter_custo_variavel=True)
    a = ef["acao_ativavel"]
    assert a["acao"] == "livre"
    assert a["efeito"] == "trocar_defesa_por_dano"
    assert a["penalidade_defesa"] == -5
    assert a["dano_extra"] == "1d12"


def test_sangue_dos_inimigos_bonus_cumulativo():
    ef = _efeitos_no_catalogo("BARBARO_SANGUE_INIMIGOS")
    e = ef.get("em_furia", {}).get("bonus_cumulativo") or ef.get("bonus_cumulativo")
    assert isinstance(e, dict), f"esperado dict: {ef}"
    assert e.get("valor") == 1
    assert e.get("limite") == "nivel"
    assert set(e.get("gatilhos", [])) == {"acerto_critico", "reduzir_a_0_pv"}


def test_vigor_primal_acao_ativavel():
    ef = _efeitos_no_catalogo("BARBARO_VIGOR_PRIMAL")
    _assert_acao_ativavel(ef, pode_ter_custo_variavel=True)
    a = ef["acao_ativavel"]
    assert a["acao"] == "movimento"
    assert a["efeito"] == "cura"
    assert a["por_pm"] == "1d12"
    assert a["limite_pm"] == "constituicao"


def test_furia_titanica_dobra_bonus():
    ef = _efeitos_no_catalogo("BARBARO_FURIA_TITANICA")
    assert ef, "BARBARO_FURIA_TITANICA ainda tem efeitos vazios"
    a = ef.get("furia_titanica")
    assert isinstance(a, dict), f"esperado dict: {ef}"
    assert a.get("dobra_bonus_furia") is True


# ===================================================================
# Sanidade: motor aceita uma ficha com todos os poderes ativos sem quebrar
# ===================================================================

def test_barbaro_com_todos_os_poderes_ativos_atualiza_sem_quebrar():
    f = _barbaro(nivel=20, forca=4, sabedoria=3)
    for chave in PODERES_ATIVOS + ["BARBARO_FURIA_TITANICA"]:
        dados = DADOS_HABILIDADES_CLASSE[chave]
        _add(f, dados["nome"], tipo=dados.get("tipo", "Poder de Bárbaro"),
             efeitos=dados.get("efeitos", {}))
    atualizar_ficha(f)  # não deve estourar
    assert f.cabecalho.nivel_total == 20
