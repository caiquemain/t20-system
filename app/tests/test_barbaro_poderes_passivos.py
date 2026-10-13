"""Bárbaro — poderes passivos (T20 JdA p.41-42).

Cobre os poderes cujos efeitos são declarativos e mensuráveis na ficha
estática. Poderes com mecânica de combate (Alma de Bronze, Brado
Assustador, Golpe Poderoso, etc.) ficam como débito documentado.

Caso especial — Pele de Ferro/Aço: o livro diz "apenas se não estiver
usando armadura pesada". O motor precisa respeitar essa condição.
"""
import pytest
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Habilidade, Item
from src.regras import atualizar_ficha


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


def _fontes_defesa(f):
    if not f.status.defesa_calc:
        return []
    return [(x.fonte, x.valor) for x in f.status.defesa_calc.fontes]


# ===================================================================
# 1. Aumento de Atributo (mesmo padrão do Arcanista)
# ===================================================================

def test_aumento_atributo_forca():
    f = _barbaro(nivel=2, forca=4)
    _add(f, "Aumento de Atributo",
         escolhas={"atributo": "forca"})
    atualizar_ficha(f)
    assert f.atributos.forca == 5, (
        f"Esperado +1 em For (4→5), obtido {f.atributos.forca}"
    )


# ===================================================================
# 2. Esquiva Sobrenatural (imunidade "surpreendido")
# ===================================================================

def test_esquiva_sobrenatural_imunidade_surpreendido():
    f = _barbaro(nivel=2)
    _add(f, "Esquiva Sobrenatural", efeitos={"imunidade": ["surpreendido"]})
    atualizar_ficha(f)
    assert any("surpreendido" in im.lower() for im in f.status.imunidades), (
        f"Esquiva Sobrenatural não expôs imunidade. "
        f"Imunidades: {f.status.imunidades}"
    )


# ===================================================================
# 3. Pele de Ferro (+4 Defesa, só sem armadura pesada)
# ===================================================================

def test_pele_ferro_sem_armadura_pesada():
    f = _barbaro(nivel=2)
    _add(f, "Pele de Ferro", efeitos={"defesa_bonus": 4})
    atualizar_ficha(f)
    fontes = _fontes_defesa(f)
    tem = any("Pele de Ferro" in (x[0] or "") and x[1] == 4 for x in fontes)
    assert tem, (
        f"Pele de Ferro +4 Defesa ausente. Fontes: {fontes}"
    )


def test_pele_ferro_com_armadura_pesada_nao_aplica():
    f = _barbaro(nivel=2)
    _add(f, "Pele de Ferro", efeitos={"defesa_bonus": 4})
    # Adiciona armadura pesada equipada
    f.inventario.equipamentos.append(Item(
        nome="Armadura completa", qtd=1, espaco=5, equipado=True, tipo="Armadura"
    ))
    atualizar_ficha(f)
    fontes = _fontes_defesa(f)
    tem = any("Pele de Ferro" in (x[0] or "") for x in fontes)
    assert not tem, (
        f"Pele de Ferro NÃO deveria aplicar com armadura pesada. "
        f"Fontes: {fontes}"
    )


# ===================================================================
# 4. Pele de Aço (+8 Defesa, req. Pele de Ferro, nv 8)
# ===================================================================

def test_pele_aco_sem_armadura_pesada():
    f = _barbaro(nivel=8)
    _add(f, "Pele de Ferro", efeitos={"defesa_bonus": 4})
    _add(f, "Pele de Aço", efeitos={"defesa_bonus": 8})
    atualizar_ficha(f)
    fontes = _fontes_defesa(f)
    tem_ferro = any("Pele de Ferro" in (x[0] or "") for x in fontes)
    tem_aco = any("Pele de Aço" in (x[0] or "") and x[1] == 8 for x in fontes)
    assert tem_aco, (
        f"Pele de Aço +8 Defesa ausente. Fontes: {fontes}"
    )
    assert not tem_ferro, (
        f"Pele de Ferro NÃO deveria aplicar quando Pele de Aço substitui. "
        f"Fontes: {fontes}"
    )


# ===================================================================
# 5. Superstição (resistência a magia +5)
# ===================================================================

def test_supersticao_resistencia_magia():
    """Livro: 'Você recebe resistência a magia +5.' O motor precisa
    expor em algum lugar inspecionável."""
    f = _barbaro(nivel=2)
    _add(f, "Superstição", efeitos={"resistencia_magia_bonus": 5})
    atualizar_ficha(f)

    # Procura em vários lugares plausíveis
    tem = (
        any("magia" in im.lower() and "5" in im for im in f.status.imunidades)
        or getattr(f.status, "resistencia_magia", None) == 5
        or getattr(f.combate, "resistencia_magia", None) == 5
    )
    assert tem, (
        f"Superstição +5 resistência a magia não exposta. "
        f"status.imunidades={f.status.imunidades}"
    )


# ===================================================================
# 6. Totem Espiritual (SAB no PM)
# ===================================================================

def test_totem_espiritual_soma_sab_em_pm():
    f = _barbaro(nivel=4, sabedoria=3)
    _add(f, "Totem Espiritual",
         efeitos={"pm_soma_atributo": "sab", "escolha_totem": True},
         escolhas={"totem": "Lobo"})
    atualizar_ficha(f)

    # Soma SAB (3) no PM máximo
    fontes = [fnt.fonte for fnt in (f.status.pm_calc.fontes if f.status.pm_calc else [])]
    tem = any("Totem" in (x or "") for x in fontes)
    assert tem, (
        f"Totem Espiritual não somou SAB em PM. Fontes: {fontes}"
    )


# ===================================================================
# 7. Crítico Brutal (multiplicador +1)
# ===================================================================

def test_critico_brutal_exposto():
    f = _barbaro(nivel=6)
    _add(f, "Crítico Brutal", efeitos={"multiplicador_critico_bonus": 1})
    atualizar_ficha(f)
    # Procura em algum campo exposto
    tem = (
        getattr(f.combate, "multiplicador_critico_bonus", None) == 1
        or any("Crítico Brutal" in (getattr(a, "especial", "") or "")
               for a in (f.combate.ataques or []))
    )
    assert tem, (
        "Crítico Brutal +1 multiplicador não exposto em combate."
    )


# ===================================================================
# 8. Fúria da Savana (+3m deslocamento)
# ===================================================================

def test_furia_savana_deslocamento():
    f = _barbaro(nivel=2)
    desloc_base = 9
    _add(f, "Fúria da Savana", efeitos={"deslocamento_bonus": 3})
    atualizar_ficha(f)
    assert f.status.deslocamento == desloc_base + 3, (
        f"Fúria da Savana deveria dar +3m (9→12). "
        f"Obtido: {f.status.deslocamento}"
    )
