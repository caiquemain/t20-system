from src.models import Habilidade, ClasseInfo, StatCalculado
from src.regras.poderes_arcanista import aplicar_poderes_arcanista

ATTRS = ["forca", "destreza", "constituicao", "inteligencia", "sabedoria", "carisma"]


def _ficha_arcanista(personagem_base, nivel=1, subclasse=""):
    personagem_base.classes = [ClasseInfo(nome="Arcanista", nivel=nivel, primaria=True, subclasse=subclasse)]
    personagem_base.cabecalho.nivel_total = nivel
    personagem_base.atributos_calc = {k: StatCalculado() for k in ATTRS}
    return personagem_base


def _hab(nome, escolhas=None):
    return Habilidade(nome=nome, tipo="Poder de Arcanista", descricao="", escolhas_aplicadas=escolhas or {})


def test_fortalecimento_arcano_cd_base(personagem_base):
    f = _ficha_arcanista(personagem_base)
    f.combate.circulo_maximo = 1
    f.habilidades = [_hab("Fortalecimento Arcano")]
    aplicar_poderes_arcanista(f)
    assert f.combate.cd_magias == 11


def test_fortalecimento_arcano_cd_com_4_circulo(personagem_base):
    f = _ficha_arcanista(personagem_base, nivel=13)
    f.combate.circulo_maximo = 4
    f.habilidades = [_hab("Fortalecimento Arcano")]
    aplicar_poderes_arcanista(f)
    assert f.combate.cd_magias == 12


def test_especialista_e_mestre_em_escola(personagem_base):
    f = _ficha_arcanista(personagem_base)
    f.habilidades = [
        _hab("Especialista em Escola", {"escola": "Evocação"}),
        _hab("Mestre em Escola", {"escola": "Evocação"}),
    ]
    aplicar_poderes_arcanista(f)
    assert f.combate.cd_por_escola == {"Evocação": 2}
    assert f.combate.custo_por_escola == {"Evocação": 1}


def test_alta_arcana_nivel_20(personagem_base):
    f = _ficha_arcanista(personagem_base, nivel=20)
    aplicar_poderes_arcanista(f)
    assert f.combate.custo_arcano_metade is True


def test_arcano_de_batalha_dano(personagem_base):
    f = _ficha_arcanista(personagem_base)
    f.atributos.inteligencia = 4
    f.habilidades = [_hab("Arcano de Batalha")]
    aplicar_poderes_arcanista(f)
    assert f.combate.bonus_dano_magias == 4


def test_aumento_de_atributo(personagem_base):
    f = _ficha_arcanista(personagem_base)
    f.habilidades = [_hab("Aumento de Atributo", {"atributo": "forca"})]
    aplicar_poderes_arcanista(f)
    assert f.atributos.forca == 1


def test_familiar_sapo_pv(personagem_base):
    f = _ficha_arcanista(personagem_base)
    f.atributos.inteligencia = 3
    f.habilidades = [_hab("Familiar", {"familiar": "Sapo"})]
    aplicar_poderes_arcanista(f)
    assert any(fr.fonte == "Familiar: Sapo" and fr.valor == 3 for fr in f.status.pv_calc.fontes)


def test_familiar_borboleta_cd_resistencia(personagem_base):
    f = _ficha_arcanista(personagem_base)
    f.habilidades = [_hab("Familiar", {"familiar": "Borboleta"})]
    aplicar_poderes_arcanista(f)
    assert f.combate.cd_por_resistencia == {"Vontade": 1}


def test_familiar_gato_sentidos(personagem_base):
    f = _ficha_arcanista(personagem_base)
    f.habilidades = [_hab("Familiar", {"familiar": "Gato"})]
    aplicar_poderes_arcanista(f)
    assert "Visão no Escuro" in f.status.sentidos


def test_linhagem_draconica_basica(personagem_base):
    f = _ficha_arcanista(personagem_base, subclasse="Feiticeiro")
    f.atributos.carisma = 3
    f.habilidades = [Habilidade(nome="Linhagem Dracônica", tipo="Habilidade de Classe",
                                descricao="", escolhas_aplicadas={"tipo_dano": "fogo"})]
    aplicar_poderes_arcanista(f)
    assert any(fr.fonte == "Linhagem Dracônica (básica)" for fr in f.status.pv_calc.fontes)
    assert "fogo 5" in f.status.rd


def test_linhagem_feerica_superior_carisma(personagem_base):
    f = _ficha_arcanista(personagem_base, subclasse="Feiticeiro")
    f.habilidades = [
        Habilidade(nome="Linhagem Feérica", tipo="Habilidade de Classe", descricao=""),
        _hab("Herança Aprimorada"), _hab("Herança Superior"),
    ]
    aplicar_poderes_arcanista(f)
    assert f.atributos.carisma == 2


def test_linhagem_feerica_basica_limite_magias(personagem_base):
    f = _ficha_arcanista(personagem_base, subclasse="Feiticeiro")
    f.combate.magias_calc = StatCalculado(base=3, total=3)
    f.combate.limite_magias = 3
    f.habilidades = [Habilidade(nome="Linhagem Feérica", tipo="Habilidade de Classe", descricao="")]
    aplicar_poderes_arcanista(f)
    assert f.combate.limite_magias == 4


# ═══════════════════════════════════════════
# 🧪 TESTES COMPLEMENTARES (COBERTURA LOTE 1 COMPLETA)
# ═══════════════════════════════════════════


def test_alta_arcana_nao_ativa_antes_do_nivel_20(personagem_base):
    """Alta Arcana NÃO deve marcar custo_arcano_metade em nível < 20."""
    f = _ficha_arcanista(personagem_base, nivel=19)
    aplicar_poderes_arcanista(f)
    assert f.combate.custo_arcano_metade is False


def test_alta_arcana_nao_ativa_para_outras_classes(personagem_base):
    """Alta Arcana é exclusividade do Arcanista — outras classes nunca ativam."""
    f = personagem_base
    f.classes = [ClasseInfo(nome="Clérigo", nivel=20, primaria=True)]
    aplicar_poderes_arcanista(f)
    assert f.combate.custo_arcano_metade is False


def test_envolto_em_misterio_nota_condicional(personagem_base):
    """Envolto em Mistério deve anotar nas fontes_bonus de Enganação e Intimidação."""
    from src.models import PericiaInfo
    f = _ficha_arcanista(personagem_base)
    f.pericias = {
        "Enganação": PericiaInfo(treino=0, total=0),
        "Intimidação": PericiaInfo(treino=0, total=0),
    }
    f.habilidades = [_hab("Envolto em Mistério")]
    aplicar_poderes_arcanista(f)
    assert any("Envolto em Mistério" in nota for nota in f.pericias["Enganação"].fontes_bonus)
    assert any("Envolto em Mistério" in nota for nota in f.pericias["Intimidação"].fontes_bonus)


def test_familiar_cobra_cd_fortitude(personagem_base):
    """Cobra adiciona +1 CD Fortitude."""
    f = _ficha_arcanista(personagem_base)
    f.habilidades = [_hab("Familiar", {"familiar": "Cobra"})]
    aplicar_poderes_arcanista(f)
    assert f.combate.cd_por_resistencia == {"Fortitude": 1}


def test_familiar_lagarto_cd_reflexos(personagem_base):
    """Lagarto adiciona +1 CD Reflexos."""
    f = _ficha_arcanista(personagem_base)
    f.habilidades = [_hab("Familiar", {"familiar": "Lagarto"})]
    aplicar_poderes_arcanista(f)
    assert f.combate.cd_por_resistencia == {"Reflexos": 1}


def test_familiar_falcao_imunidades(personagem_base):
    """Falcão concede imunidades: não surpreendido, não desprevenido."""
    f = _ficha_arcanista(personagem_base)
    f.habilidades = [_hab("Familiar", {"familiar": "Falcão"})]
    aplicar_poderes_arcanista(f)
    assert "Não pode ser surpreendido" in f.status.imunidades
    assert "Não fica desprevenido" in f.status.imunidades


def test_familiar_morcego_sentidos(personagem_base):
    """Morcego concede Percepção às cegas (curto)."""
    f = _ficha_arcanista(personagem_base)
    f.habilidades = [_hab("Familiar", {"familiar": "Morcego"})]
    aplicar_poderes_arcanista(f)
    assert "Percepção às cegas (curto)" in f.status.sentidos


def test_familiar_sapo_com_attr_zero(personagem_base):
    """Sapo com atributo-chave 0 não deve adicionar bônus (mod=0)."""
    f = _ficha_arcanista(personagem_base)
    f.atributos.inteligencia = 0  # mod = 0
    f.habilidades = [_hab("Familiar", {"familiar": "Sapo"})]
    aplicar_poderes_arcanista(f)
    fontes_sapo = [fr for fr in f.status.pv_calc.fontes if fr.fonte == "Familiar: Sapo"]
    assert len(fontes_sapo) == 0


def test_familiar_sapo_feiticeiro_usa_carisma(personagem_base):
    """Sapo + Feiticeiro soma mod CAR no PV, não INT."""
    f = _ficha_arcanista(personagem_base, subclasse="Feiticeiro")
    f.atributos.carisma = 4
    f.atributos.inteligencia = 0
    f.habilidades = [_hab("Familiar", {"familiar": "Sapo"})]
    aplicar_poderes_arcanista(f)
    fonte = next((fr for fr in f.status.pv_calc.fontes if fr.fonte == "Familiar: Sapo"), None)
    assert fonte is not None
    assert fonte.valor == 4  # mod de CAR=4


def test_linhagem_draconica_superior_imunidade(personagem_base):
    """Linhagem Dracônica superior concede imunidade ao tipo de dano."""
    f = _ficha_arcanista(personagem_base, subclasse="Feiticeiro")
    f.atributos.carisma = 3
    f.habilidades = [
        Habilidade(nome="Linhagem Dracônica", tipo="Habilidade de Classe", descricao="",
                   escolhas_aplicadas={"tipo_dano": "fogo"}),
        _hab("Herança Aprimorada"),
        _hab("Herança Superior"),
    ]
    aplicar_poderes_arcanista(f)
    assert "Imune a fogo" in f.status.imunidades
    # E continua dando RD básica
    assert "fogo 5" in f.status.rd


def test_linhagem_draconica_basica_sem_tipo_dano(personagem_base):
    """Dracônica sem tipo_dano escolhido não adiciona RD nem imunidade."""
    f = _ficha_arcanista(personagem_base, subclasse="Feiticeiro")
    f.atributos.carisma = 3
    f.habilidades = [Habilidade(
        nome="Linhagem Dracônica", tipo="Habilidade de Classe",
        descricao="", escolhas_aplicadas={})]
    aplicar_poderes_arcanista(f)
    assert f.status.rd == []


def test_fortalecimento_arcano_sem_o_poder(personagem_base):
    """Sem Fortalecimento Arcano, cd_magias fica em 10 (base)."""
    f = _ficha_arcanista(personagem_base)
    aplicar_poderes_arcanista(f)
    assert f.combate.cd_magias == 10


def test_especialista_sem_escolha_de_escola(personagem_base):
    """Especialista em Escola sem escola escolhida não deve poluir cd_por_escola."""
    f = _ficha_arcanista(personagem_base)
    f.habilidades = [_hab("Especialista em Escola", {})]  # sem 'escola'
    aplicar_poderes_arcanista(f)
    assert f.combate.cd_por_escola == {}


def test_ordem_da_pipeline_familiar_no_pv(personagem_base):
    """Regressão: o processador de poderes roda DEPOIS de calcular_pv_pm,
    então a fonte 'Familiar: Sapo' aparece na pilha final."""
    f = _ficha_arcanista(personagem_base)
    f.atributos.inteligencia = 3
    f.habilidades = [_hab("Familiar", {"familiar": "Sapo"})]
    # Simula a pipeline real
    from src.regras.status import calcular_pv_pm
    calcular_pv_pm(f)
    aplicar_poderes_arcanista(f)
    # A fonte do familiar está presente mesmo após calcular_pv_pm
    fontes = [fr.fonte for fr in f.status.pv_calc.fontes]
    assert "Familiar: Sapo" in fontes


def test_multiplos_poderes_acumulam(personagem_base):
    """Poder Mágico + Familiar + Fortalecimento todos aplicam juntos."""
    f = _ficha_arcanista(personagem_base, nivel=5)
    f.atributos.inteligencia = 3
    f.combate.circulo_maximo = 2
    f.habilidades = [
        _hab("Poder Mágico"),
        _hab("Fortalecimento Arcano"),
        _hab("Familiar", {"familiar": "Sapo"}),
    ]
    aplicar_poderes_arcanista(f)
    # PM: classe base + INT + Poder Mágico (5 níveis)
    assert any("Poder Mágico" in fr.fonte and fr.valor == 5 for fr in f.status.pm_calc.fontes)
    # CD: 10 + 1 (Fortalecimento)
    assert f.combate.cd_magias == 11
    # PV: familiar aplicado
    assert any("Familiar: Sapo" in fr.fonte for fr in f.status.pv_calc.fontes)


def test_arcano_de_batalha_feiticeiro_usa_car(personagem_base):
    """Arcano de Batalha + Feiticeiro deve usar CAR (não INT) no dano."""
    f = _ficha_arcanista(personagem_base, subclasse="Feiticeiro")
    f.atributos.carisma = 4
    f.atributos.inteligencia = 0
    f.habilidades = [_hab("Arcano de Batalha")]
    aplicar_poderes_arcanista(f)
    assert f.combate.bonus_dano_magias == 4


def test_descansar_mantem_pv_cheio_com_familiar(personagem_base):
    """Regressão: após Descansar, o PV cheio deve incluir o bônus do Sapo.
    (calcular_pv_pm clampava antes de aplicar_poderes subir o máximo.)"""
    from src.regras.status import calcular_pv_pm
    f = _ficha_arcanista(personagem_base)
    f.atributos.inteligencia = 4
    f.habilidades = [_hab("Familiar", {"familiar": "Sapo"})]
    calcular_pv_pm(f)                      # maximo intermediário = 10, atual clampado = 10 (cheio)
    f.status.pv.atual = f.status.pv.maximo  # simula o clique em Descansar
    aplicar_poderes_arcanista(f)           # sobe máximo p/ 14 e preserva "cheio"
    assert f.status.pv.maximo == 15
    assert f.status.pv.atual == 15


def test_caminho_recebe_chip_da_subclasse(personagem_base):
    """Caminho do Arcanista ganha escolhas_aplicadas.subclasse (chip no card)
    e limpa a poluição antiga de saves (escolha_subclasse)."""
    from src.regras.habilidades import sincronizar_escolhas_de_caminho
    f = _ficha_arcanista(personagem_base, subclasse="Bruxo")
    f.habilidades = [Habilidade(
        nome="Caminho do Arcanista", tipo="Classe", descricao="",
        efeitos={"escolha_subclasse": ["Bruxo", "Feiticeiro", "Mago"]},
        escolhas_aplicadas={"escolha_subclasse": ["Bruxo", "Feiticeiro", "Mago"]},
    )]
    sincronizar_escolhas_de_caminho(f)
    assert f.habilidades[0].escolhas_aplicadas.get("subclasse") == "Bruxo"
    assert "escolha_subclasse" not in f.habilidades[0].escolhas_aplicadas
