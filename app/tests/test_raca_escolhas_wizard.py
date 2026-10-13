"""Auditoria Lote B: escolhas raciais (backend consumindo escolhas_aplicadas).

Simula o que o wizard grava em 'escolhas_aplicadas' e verifica se o motor
aplica corretamente. Nao testa UI - so o fluxo escolhas -> efeito.

Cobre:
    Qareen    - Tatuagem Mistica (escolher 1 magia de 1o circulo)
    Sereia    - Cancao dos Mares (escolher 2 magias da lista)
    Silfide   - Magia das Fadas (escolher 2 magias da lista)
    Lefou     - Deformidade (escolher 2 pericias +2)
    Kliren    - Hibrido (escolher 1 pericia para treinar)
    Vanguardista (Kliren) - +2 em Oficio escolhido
    Osteon    - Memoria Postuma (pericia OU poder OU racial)
    Golem     - Fonte Elemental (espirito elemental)
"""
import pytest
from src.models import Personagem, Cabecalho, ClasseInfo, Habilidade
from src.regras import atualizar_ficha
from src.regras.habilidades import garantir_habilidades_iniciais


def _ficha(raca, classe="Guerreiro"):
    f = Personagem()
    f.cabecalho = Cabecalho(nome=f"Teste {raca}", raca=raca, nivel_total=1)
    f.classes = [ClasseInfo(nome=classe, nivel=1, primaria=True)]
    return f


def _escolher(f, nome_hab, escolhas):
    """Localiza uma habilidade racial e injeta escolhas_aplicadas."""
    hab = next((h for h in f.habilidades if h.nome == nome_hab), None)
    assert hab is not None, f"Habilidade racial '{nome_hab}' nao encontrada"
    hab.escolhas_aplicadas = dict(escolhas)


# ===================================================================
# 1. Qareen - Tatuagem Mistica
# ===================================================================

def test_qareen_tatuagem_mistica_adiciona_magia_ao_grimorio():
    f = _ficha("Qareen")
    atualizar_ficha(f)
    _escolher(f, "Tatuagem Mística", {"magia_escolhida": "Enfeitiçar"})
    atualizar_ficha(f)

    nomes = [m.nome for m in f.combate.magias]
    assert "Enfeitiçar" in nomes, (
        f"Magia escolhida nao foi para o grimorio. Magias: {nomes}"
    )


def test_qareen_tatuagem_mistica_reconhece_chave_magia_0():
    """Frontend pode usar 'magia_0' em vez de 'magia_escolhida'."""
    f = _ficha("Qareen")
    atualizar_ficha(f)
    _escolher(f, "Tatuagem Mística", {"magia_0": "Enfeitiçar"})
    atualizar_ficha(f)

    nomes = [m.nome for m in f.combate.magias]
    assert "Enfeitiçar" in nomes, (
        f"Chave 'magia_0' nao foi consumida. Magias: {nomes}"
    )


# ===================================================================
# 2. Sereia - Cancao dos Mares (2 magias)
# ===================================================================

def test_sereia_cancao_mares_adiciona_2_magias():
    f = _ficha("Sereia/Tritão")
    atualizar_ficha(f)
    _escolher(f, "Canção dos Mares", {
        "magia_0": "Amedrontar",
        "magia_1": "Sono",
    })
    atualizar_ficha(f)

    nomes = [m.nome for m in f.combate.magias]
    assert "Amedrontar" in nomes, f"Magia 1 nao entrou. Magias: {nomes}"
    assert "Sono" in nomes, f"Magia 2 nao entrou. Magias: {nomes}"


# ===================================================================
# 3. Silfide - Magia das Fadas (2 magias)
# ===================================================================

def test_silfide_magia_das_fadas_adiciona_2_magias():
    f = _ficha("Sílfide")
    atualizar_ficha(f)
    _escolher(f, "Magia das Fadas", {
        "magia_0": "Criar Ilusão",
        "magia_1": "Enfeitiçar",
    })
    atualizar_ficha(f)

    nomes = [m.nome for m in f.combate.magias]
    assert "Criar Ilusão" in nomes, f"Magia 1 nao entrou. Magias: {nomes}"
    assert "Enfeitiçar" in nomes, f"Magia 2 nao entrou. Magias: {nomes}"


# ===================================================================
# 4. Lefou - Deformidade (2 pericias +2)
# ===================================================================

def test_lefou_deformidade_aplica_2_pericias_bonus():
    f = _ficha("Lefou")
    atualizar_ficha(f)
    _escolher(f, "Deformidade", {
        "pericia_bonus_0": "Furtividade",
        "pericia_bonus_1": "Atletismo",
    })
    atualizar_ficha(f)

    for pericia in ("Furtividade", "Atletismo"):
        info = f.pericias.get(pericia)
        assert info is not None, f"Pericia {pericia} ausente"
        tem_bonus = any("Deformidade" in (linha or "")
                        for linha in info.fontes_bonus)
        assert tem_bonus, (
            f"{pericia}: sem bonus de Deformidade. "
            f"Fontes: {info.fontes_bonus}"
        )


def test_lefou_deformidade_aceita_chaves_legacy():
    """Chaves legacy 'pericia_1' e 'pericia_2' tambem devem funcionar."""
    f = _ficha("Lefou")
    atualizar_ficha(f)
    _escolher(f, "Deformidade", {
        "pericia_1": "Furtividade",
        "pericia_2": "Atletismo",
    })
    atualizar_ficha(f)

    for pericia in ("Furtividade", "Atletismo"):
        info = f.pericias.get(pericia)
        tem_bonus = any("Deformidade" in (linha or "")
                        for linha in (info.fontes_bonus if info else []))
        assert tem_bonus, f"{pericia}: legacy keys nao consumidas"


# ===================================================================
# 5. Kliren - Hibrido (1 pericia treinada)
# ===================================================================

def test_kliren_hibrido_treina_pericia_escolhida():
    f = _ficha("Kliren")
    atualizar_ficha(f)
    _escolher(f, "Híbrido", {"pericia_escolha": "Furtividade"})
    atualizar_ficha(f)

    info = f.pericias.get("Furtividade")
    assert info is not None
    assert info.treino == 1, f"Furtividade nao treinada: treino={info.treino}"


# ===================================================================
# 6. Kliren - Vanguardista (+2 em Oficio escolhido)
# ===================================================================

def test_kliren_vanguardista_bonus_em_oficio_escolhido():
    f = _ficha("Kliren")
    atualizar_ficha(f)
    _escolher(f, "Vanguardista", {"pericia_bonus_0": "Ofício (ferreiro)"})
    # Precisamos garantir que a pericia existe na ficha
    f.pericias["Ofício (ferreiro)"] = f.pericias.get(
        "Ofício (ferreiro)",
        __import__("src.models", fromlist=["PericiaInfo"]).PericiaInfo(treino=1, total=0)
    )
    atualizar_ficha(f)

    info = f.pericias.get("Ofício (ferreiro)")
    assert info is not None, "Oficio (ferreiro) nao esta na ficha"
    tem_bonus = any("Vanguardista" in (linha or "")
                    for linha in (info.fontes_bonus or []))
    # Ou bonus_automatico > 0
    assert tem_bonus or (info.bonus_automatico or 0) >= 2, (
        f"Vanguardista nao somou. Fontes: {info.fontes_bonus}, "
        f"bonus_auto={info.bonus_automatico}"
    )


# ===================================================================
# 7. Osteon - Memoria Postuma (3 modos)
# ===================================================================

def test_osteon_memoria_postuma_modo_pericia():
    f = _ficha("Osteon")
    atualizar_ficha(f)
    _escolher(f, "Memória Póstuma", {"memoria_postuma": "Furtividade"})
    atualizar_ficha(f)

    info = f.pericias.get("Furtividade")
    assert info is not None
    assert info.treino == 1, (
        f"Memoria Postuma modo pericia falhou: treino={info.treino}"
    )


def test_osteon_memoria_postuma_modo_poder():
    f = _ficha("Osteon")
    atualizar_ficha(f)
    _escolher(f, "Memória Póstuma", {"memoria_postuma": "Ataque Poderoso"})
    atualizar_ficha(f)

    filhas = [h for h in f.habilidades
              if h.fonte == "Habilidade: Memória Póstuma"]
    assert any("Ataque Poderoso" in h.nome for h in filhas), (
        f"Poder escolhido nao virou habilidade. Filhas: "
        f"{[h.nome for h in filhas]}"
    )


# ===================================================================
# 8. Golem - Fonte Elemental
# ===================================================================

def test_golem_fonte_elemental_aplica_imunidade():
    f = _ficha("Golem")
    atualizar_ficha(f)
    _escolher(f, "Fonte Elemental", {"imunidade_dano_escolha": "fogo"})
    atualizar_ficha(f)

    assert any("fogo" in im.lower() for im in f.status.imunidades), (
        f"Imunidade a fogo nao apareceu. Imunidades: {f.status.imunidades}"
    )


# ===================================================================
# 9. Idempotencia geral
# ===================================================================

@pytest.mark.parametrize("raca,hab,escolhas", [
    ("Qareen", "Tatuagem Mística", {"magia_escolhida": "Enfeitiçar"}),
    ("Sereia/Tritão", "Canção dos Mares",
     {"magia_0": "Amedrontar", "magia_1": "Sono"}),
    ("Sílfide", "Magia das Fadas",
     {"magia_0": "Criar Ilusão", "magia_1": "Enfeitiçar"}),
])
def test_escolha_de_magia_nao_duplica_em_reprocessamentos(raca, hab, escolhas):
    """Rodar atualizar_ficha 3x nao pode duplicar magias raciais."""
    f = _ficha(raca)
    atualizar_ficha(f)
    _escolher(f, hab, escolhas)
    for _ in range(3):
        atualizar_ficha(f)

    magias_unicas = {m.nome for m in f.combate.magias}
    # Conta duplicatas
    todos = [m.nome for m in f.combate.magias]
    duplicatas = [n for n in magias_unicas if todos.count(n) > 1]
    assert not duplicatas, (
        f"{raca}: magias duplicadas apos reprocessamentos: {duplicatas}. "
        f"Grimorio completo: {todos}"
    )
