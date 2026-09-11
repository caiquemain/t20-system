"""Testes das raças do Livro Básico — Lote R1 (críticos numéricos)."""
import pytest
from src.models import Personagem, Cabecalho, ClasseInfo
from src.regras.atributos import aplicar_bonus_atributos_raciais
from src.regras.status import calcular_pv_pm, calcular_proficiencias_e_extras
from src.regras.pericias import inicializar_pericias
from src.regras.habilidades import garantir_habilidades_iniciais


def _ficha(raca, classe="Guerreiro", nivel=1):
    f = Personagem()
    f.cabecalho = Cabecalho(nome=f"Teste {raca}", raca=raca, nivel_total=nivel)
    f.classes = [ClasseInfo(nome=classe, nivel=nivel, primaria=True)]
    return f


def test_elfo_graca_glorienn_nome():
    """A habilidade do Elfo chama-se 'Graça de Glórienn' (não Glanna)."""
    from src.dados_habilidades_raciais import DADOS_HABILIDADES_RACIAIS
    nomes = [d["nome"] for d in DADOS_HABILIDADES_RACIAIS.values()]
    assert "Graça de Glórienn" in nomes
    assert "Graça de Glanna" not in nomes


def test_minotauro_faro_aparece_em_sentidos():
    f = _ficha("Minotauro")
    garantir_habilidades_iniciais(f)
    aplicar_bonus_atributos_raciais(f)
    calcular_proficiencias_e_extras(f)
    assert "Faro" in f.status.sentidos


def test_hynne_atletismo_pode_usar_destreza():
    """Hynne (Pequeno e Rechonchudo) pode usar Des no lugar de For em Atletismo."""
    f = _ficha("Hynne")
    garantir_habilidades_iniciais(f)
    aplicar_bonus_atributos_raciais(f)
    inicializar_pericias(f)
    info = f.pericias.get("Atletismo")
    assert info is not None
    assert "des" in info.atributos_possiveis


def test_satiro_atletismo_pode_usar_destreza():
    f = _ficha("Sátiro")
    garantir_habilidades_iniciais(f)
    aplicar_bonus_atributos_raciais(f)
    inicializar_pericias(f)
    info = f.pericias.get("Atletismo")
    assert info is not None
    assert "des" in info.atributos_possiveis


def test_kliren_ossos_frageis_vulnerabilidade():
    """Kliren recebe +1 dano por dado de impacto (Ossos Frágeis)."""
    f = _ficha("Kliren")
    garantir_habilidades_iniciais(f)
    aplicar_bonus_atributos_raciais(f)
    calcular_proficiencias_e_extras(f)
    assert any("Impacto" in v for v in f.status.vulnerabilidades)


def test_trog_sangue_frio_vulnerabilidade():
    """Trog recebe +1 dano por dado de frio (Sangue Frio)."""
    f = _ficha("Trog")
    garantir_habilidades_iniciais(f)
    aplicar_bonus_atributos_raciais(f)
    calcular_proficiencias_e_extras(f)
    assert any("Frio" in v for v in f.status.vulnerabilidades)


def test_requisito_de_classe_persiste(personagem_base):
    """Guerreiro: escolher Luta no banner deve persistir após recálculo."""
    from src.models import ClasseInfo, PericiaInfo
    from src.regras.pericias import inicializar_pericias
    personagem_base.classes = [ClasseInfo(nome="Guerreiro", nivel=1, primaria=True)]
    personagem_base.pericias["Luta"] = PericiaInfo(treino=1, total=0)
    inicializar_pericias(personagem_base)
    assert personagem_base.pericias["Luta"].treino == 1


def test_desmarcar_pericia_remove_treino(personagem_base):
    """Desmarcar no frontend (treino=0) continua removendo o treino."""
    from src.models import ClasseInfo, PericiaInfo
    from src.regras.pericias import inicializar_pericias
    personagem_base.classes = [ClasseInfo(nome="Guerreiro", nivel=1, primaria=True)]
    personagem_base.pericias["Luta"] = PericiaInfo(treino=1, total=0)
    inicializar_pericias(personagem_base)
    personagem_base.pericias["Luta"].treino = 0
    inicializar_pericias(personagem_base)
    assert personagem_base.pericias["Luta"].treino == 0
