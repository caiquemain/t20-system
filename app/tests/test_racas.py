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


def test_qareen_rd_escolha_aplica_tipo(personagem_base):
    from src.models import Habilidade
    from src.regras.status import calcular_reducoes_dano
    f = _ficha("Qareen")
    f.habilidades = [Habilidade(nome="Resistência Elemental", tipo="Racial", descricao="",
                                efeitos={"resistencia_rd_escolha": 10},
                                escolhas_aplicadas={"resistencia_rd_escolha": "fogo"})]
    calcular_reducoes_dano(f)
    assert "fogo 10" in f.status.rd


def test_qareen_rd_sem_escolha_nao_gera_lixo(personagem_base):
    from src.models import Habilidade
    from src.regras.status import calcular_reducoes_dano
    f = _ficha("Qareen")
    f.habilidades = [Habilidade(nome="Resistência Elemental", tipo="Racial", descricao="",
                                efeitos={"resistencia_rd_escolha": 10}, escolhas_aplicadas={})]
    calcular_reducoes_dano(f)
    assert f.status.rd == []


def test_golem_imunidade_elemento(personagem_base):
    from src.models import Habilidade
    from src.regras.status import calcular_proficiencias_e_extras
    f = _ficha("Golem")
    f.habilidades = [Habilidade(nome="Fonte Elemental", tipo="Racial", descricao="",
                                efeitos={"imunidade_dano_escolha": True},
                                escolhas_aplicadas={"imunidade_dano_escolha": "fogo"})]
    calcular_proficiencias_e_extras(f)
    assert "Imune a fogo" in f.status.imunidades


def test_osteon_memoria_postuma_cria_racial(personagem_base):
    from src.models import Habilidade
    from src.regras.habilidades import sincronizar_poderes_habilidades
    f = _ficha("Osteon")
    f.habilidades = [Habilidade(nome="Memória Póstuma", tipo="Racial", descricao="",
                                efeitos={"pericia_ou_poder_ou_raca_escolha": 1},
                                escolhas_aplicadas={"memoria_postuma": "Faro"})]
    sincronizar_poderes_habilidades(f)
    assert any(h.nome == "Faro" and h.fonte == "Habilidade: Memória Póstuma" for h in f.habilidades)


def test_vanguardista_oficio_bonus_mais_dois(personagem_base):
    from src.models import Habilidade, PericiaInfo
    from src.regras.pericias import inicializar_pericias
    f = _ficha("Kliren")
    f.habilidades = [Habilidade(nome="Vanguardista", tipo="Racial", descricao="",
                                efeitos={"pericia_bonus_escolha": {"Ofício": 2}},
                                escolhas_aplicadas={"pericia_bonus_0": "Ofício (ferreiro)"})]
    f.pericias["Ofício (ferreiro)"] = PericiaInfo(treino=1, total=0)
    inicializar_pericias(f)
    assert f.pericias["Ofício (ferreiro)"].bonus_automatico == 2


def test_descricao_do_card_mostra_escolha_elemental(personagem_base):
    from src.models import Habilidade
    from src.regras.habilidades import limpar_habilidades_fixas, garantir_habilidades_iniciais
    f = _ficha("Qareen")
    f.habilidades = [Habilidade(
        nome="Resistência Elemental", tipo="Racial", descricao="base",
        efeitos={"resistencia_rd_escolha": 10},
        escolhas_aplicadas={"resistencia_rd_escolha": "fogo"})]
    mem = limpar_habilidades_fixas(f)
    garantir_habilidades_iniciais(f, mem)
    hab = next(h for h in f.habilidades if h.nome == "Resistência Elemental")
    assert "Ascendência: fogo" in hab.descricao


def test_chip_exibicao_ascendencia_qareen(personagem_base):
    from src.models import Habilidade
    from src.regras.habilidades import limpar_habilidades_fixas, garantir_habilidades_iniciais
    f = _ficha("Qareen")
    f.habilidades = [Habilidade(
        nome="Resistência Elemental", tipo="Racial", descricao="x",
        efeitos={"resistencia_rd_escolha": 10},
        escolhas_aplicadas={"resistencia_rd_escolha": "fogo"})]
    mem = limpar_habilidades_fixas(f)
    garantir_habilidades_iniciais(f, mem)
    hab = next(h for h in f.habilidades if h.nome == "Resistência Elemental")
    assert hab.escolhas_aplicadas.get("ascendencia_elemental") == "fogo"


def test_oficio_permite_trocar_atributo_chave(personagem_base):
    from src.models import PericiaInfo
    from src.regras.pericias import inicializar_pericias
    f = _ficha("Kliren")
    f.pericias["Ofício (ferreiro)"] = PericiaInfo(treino=1, total=0)
    inicializar_pericias(f)
    assert set(f.pericias["Ofício (ferreiro)"].atributos_possiveis) == {
        'for', 'des', 'con', 'int', 'sab', 'car'}


def test_chip_oficio_vanguardista_kliren(personagem_base):
    from src.models import Habilidade
    from src.regras.habilidades import limpar_habilidades_fixas, garantir_habilidades_iniciais
    f = _ficha("Kliren")
    f.habilidades = [Habilidade(
        nome="Vanguardista", tipo="Racial", descricao="x",
        efeitos={"pericia_bonus_escolha": {"Ofício": 2}},
        escolhas_aplicadas={"pericia_bonus_0": "Ofício (ferreiro)"})]
    mem = limpar_habilidades_fixas(f)
    garantir_habilidades_iniciais(f, mem)
    hab = next(h for h in f.habilidades if h.nome == "Vanguardista")
    # Chip único: pericia_bonus_0 não é gatilho do catálogo, então não precisa de espelho
    assert hab.escolhas_aplicadas.get("pericia_bonus_0") == "Ofício (ferreiro)"
    assert "oficio_vanguardista" not in hab.escolhas_aplicadas


def test_catalogo_vanguardista_usa_chave_do_consumidor(personagem_base):
    from src.dados_habilidades_raciais import DADOS_HABILIDADES_RACIAIS
    v = DADOS_HABILIDADES_RACIAIS["Vanguardista_Kliren"]
    assert "pericia_bonus_escolha" in v["efeitos"]
    assert isinstance(v["efeitos"]["pericia_bonus_escolha"], dict)
