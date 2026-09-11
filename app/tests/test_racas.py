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


def test_kliren_vanguardista_proficiencia_armas_de_fogo(personagem_base):
    from src.regras.habilidades import garantir_habilidades_iniciais
    from src.regras.status import calcular_proficiencias_e_extras
    f = _ficha("Kliren")
    garantir_habilidades_iniciais(f)
    calcular_proficiencias_e_extras(f)
    assert "armas de fogo" in f.status.proficiencias


def test_anao_bonus_pericia_condicional_fora_do_total(personagem_base):
    from src.regras.habilidades import garantir_habilidades_iniciais
    from src.regras.pericias import inicializar_pericias
    f = _ficha("Anão")
    garantir_habilidades_iniciais(f)
    inicializar_pericias(f)
    info = f.pericias["Percepção"]
    assert any("Conhecimento das Rochas" in linha and "situacional" in linha
               for linha in info.fontes_bonus)
    assert info.bonus_automatico == 0  # condicional NÃO infla o total


def test_lefou_resistencia_tormenta_em_efeitos(personagem_base):
    from src.regras.habilidades import garantir_habilidades_iniciais, atualizar_efeitos_ativos
    f = _ficha("Lefou")
    garantir_habilidades_iniciais(f)
    atualizar_efeitos_ativos(f)
    assert any("Tormenta" in e for e in f.status.efeitos_ativos)


def test_golem_tipo_criatura_em_efeitos(personagem_base):
    from src.regras.habilidades import garantir_habilidades_iniciais, atualizar_efeitos_ativos
    f = _ficha("Golem")
    garantir_habilidades_iniciais(f)
    atualizar_efeitos_ativos(f)
    assert any("Construto" in e for e in f.status.efeitos_ativos)


def test_sereia_bonus_dano_arma_agregado(personagem_base):
    from src.regras.habilidades import garantir_habilidades_iniciais
    from src.regras.combate import sincronizar_ataques
    f = _ficha("Sereia/Tritão")
    garantir_habilidades_iniciais(f)
    sincronizar_ataques(f)
    assert f.combate.bonus_dano_arma == {"azagaia": 2, "lança": 2, "tridente": 2}


def test_hynne_passo_dano_arremesso(personagem_base):
    from src.regras.habilidades import garantir_habilidades_iniciais
    from src.regras.combate import sincronizar_ataques
    f = _ficha("Hynne")
    garantir_habilidades_iniciais(f)
    sincronizar_ataques(f)
    assert f.combate.passo_dano_arremesso == 1


def test_condicao_ativa_soma_bonus_na_pericia(personagem_base):
    from src.regras.habilidades import garantir_habilidades_iniciais
    from src.regras.pericias import inicializar_pericias
    f = _ficha("Anão")
    garantir_habilidades_iniciais(f)
    f.condicoes_ativas = ["subterraneo"]
    inicializar_pericias(f)
    info = f.pericias["Percepção"]
    assert info.total == 2  # 0 base + 2 da condição ativa
    assert any("condição ativa" in linha for linha in info.fontes_bonus)


def test_condicao_inativa_mantem_situacional(personagem_base):
    from src.regras.habilidades import garantir_habilidades_iniciais
    from src.regras.pericias import inicializar_pericias
    f = _ficha("Anão")
    garantir_habilidades_iniciais(f)
    f.condicoes_ativas = []
    inicializar_pericias(f)
    info = f.pericias["Percepção"]
    assert info.total == 0
    assert any("situacional" in linha for linha in info.fontes_bonus)


def test_trog_sem_armadura_ativa_furtividade(personagem_base):
    from src.regras.habilidades import garantir_habilidades_iniciais
    from src.regras.pericias import inicializar_pericias
    f = _ficha("Trog")
    garantir_habilidades_iniciais(f)
    f.condicoes_ativas = ["sem_armadura"]
    inicializar_pericias(f)
    assert f.pericias["Furtividade"].total == 5
