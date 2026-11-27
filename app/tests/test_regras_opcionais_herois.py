"""Testes das Regras Opcionais — Heróis de Arton (Capítulo 4, p. 280–328)."""
import pytest
from src.models import (
    Personagem,
    Cabecalho,
    ClasseInfo,
    Atributos,
    Habilidade,
    ComplicacaoPersonagem,
    Descricao,
    TamanhoEnum,
)
from src.regras import atualizar_ficha
from src.dados_suplementos import FONTE_HEROIS
from src.dados_habilidades import HABILIDADES_GERAIS
from src.dados_regras_opcionais_herois import (
    LISTA_REGRAS_OPCIONAIS,
    ESTILOS_DE_JOGO,
    METODOS_GERACAO_ATRIBUTOS,
    DADOS_COMPLICACOES_GERAIS,
    DADOS_COMPLICACOES_CLASSE,
    DADOS_COMPLICACOES_IDADE,
    DADOS_IDADES_VARIADAS,
    DADOS_OBJETIVOS_HEROICOS,
    DADOS_PAPEIS_GRUPO,
    PODERES_CULINARIA_HEROIS,
    obter_catalogo_regras_opcionais,
)
from src.regras.regras_opcionais_herois import (
    gerar_atributos_metodo,
    validar_complicacao_classe,
    calcular_pm_dominio_mistico,
    avaliar_teste_morte_alternativa,
    arma_e_agil_com_regra_opcional,
)


def _ficha_base(classe="Guerreiro", nivel=4, raca="Humano", subclasse="", **kwargs) -> Personagem:
    return Personagem(
        cabecalho=Cabecalho(nome="Herói Teste", raca=raca),
        classes=[ClasseInfo(nome=classe, nivel=nivel, primaria=True, subclasse=subclasse)],
        atributos_base=Atributos(
            forca=2, destreza=2, constituicao=2, inteligencia=1, sabedoria=1, carisma=0
        ),
        **kwargs,
    )


# =====================================================================
# 1. INTEGRIDADE DOS CATÁLOGOS
# =====================================================================

def test_catalogos_herois_cap4_completos():
    assert len(DADOS_COMPLICACOES_GERAIS) == 32
    assert len(DADOS_COMPLICACOES_CLASSE) == 22
    assert len(DADOS_COMPLICACOES_IDADE) == 19
    assert len(DADOS_IDADES_VARIADAS) == 7
    assert len(DADOS_OBJETIVOS_HEROICOS) == 7
    assert len(DADOS_PAPEIS_GRUPO) == 9
    assert len(METODOS_GERACAO_ATRIBUTOS) == 6
    assert set(ESTILOS_DE_JOGO.keys()) == {"Tática", "Épica", "Velha Guarda"}
    assert "As_da_Cozinha" in HABILIDADES_GERAIS
    assert "Bom_de_Garfo" in HABILIDADES_GERAIS
    assert HABILIDADES_GERAIS["Bom_de_Garfo"]["fonte"] == FONTE_HEROIS
    cat = obter_catalogo_regras_opcionais()
    assert cat["fonte"] == FONTE_HEROIS
    assert "defesa_epica" in cat["regras"]


# =====================================================================
# 2. ISOLAMENTO OPT-IN (ZERO IMPACTO EM FICHAS NORMAIS)
# =====================================================================

def test_ficha_normal_sem_regras_opcionais_nao_e_afetada():
    f = _ficha_base(classe="Guerreiro", nivel=6)
    atualizar_ficha(f)
    # Defesa base 10 + Des 2 = 12 (sem Defesa Épica +3!)
    assert f.status.defesa.total == 12
    assert f.status.deslocamento == 9.0
    assert not any(h.tipo in ("Complicação", "Papel no Grupo", "Idade Variada") for h in f.habilidades)


# =====================================================================
# 3. COMPLICAÇÕES GERAIS, DE CLASSE E DE IDADE
# =====================================================================

def test_complicacao_geral_penalidades_e_poder_bonus():
    f_sem = _ficha_base(classe="Guerreiro", nivel=4)
    atualizar_ficha(f_sem)
    pv_base = f_sem.status.pv.maximo
    fort_base = f_sem.pericias["Fortitude"].total
    def_base = f_sem.status.defesa.total

    f_com = _ficha_base(
        classe="Guerreiro",
        nivel=4,
        complicacoes=[ComplicacaoPersonagem(nome="Combalido", poder_bonus="Esquiva")],
    )
    atualizar_ficha(f_com)
    # Combalido: -1 PV/nv (-4 PV) e -5 Fortitude; Esquiva: +2 Defesa e +2 Reflexos
    assert f_com.status.pv.maximo == pv_base - 4
    assert f_com.pericias["Fortitude"].total == fort_base - 5
    assert f_com.status.defesa.total == def_base + 2

    # Idempotência ao recalcular duas vezes
    atualizar_ficha(f_com)
    assert f_com.status.pv.maximo == pv_base - 4
    assert f_com.status.defesa.total == def_base + 2


def test_complicacao_desprotegido_e_indolente_e_marcado():
    f0 = _ficha_base(classe="Arcanista", nivel=4, subclasse="Mago")
    atualizar_ficha(f0)

    f1 = _ficha_base(
        classe="Arcanista",
        nivel=4,
        subclasse="Mago",
        complicacoes=[
            ComplicacaoPersonagem(nome="Desprotegido"),
            ComplicacaoPersonagem(nome="Indolente"),
            ComplicacaoPersonagem(nome="Marcado pelo Passado"),
        ],
    )
    atualizar_ficha(f1)
    assert f1.status.defesa.total == f0.status.defesa.total - 2
    assert f1.status.deslocamento == f0.status.deslocamento - 3
    assert f1.status.pm.maximo == f0.status.pm.maximo - 4
    assert f1.pericias["Reflexos"].total == f0.pericias["Reflexos"].total - 7  # -2 Desprotegido -5 Indolente
    assert f1.pericias["Diplomacia"].total == f0.pericias["Diplomacia"].total - 5


def test_complicacao_fracote_vagaroso_e_totem_gigante():
    f0 = _ficha_base(classe="Bárbaro", nivel=2)
    atualizar_ficha(f0)

    f_frac = _ficha_base(
        classe="Bárbaro",
        nivel=2,
        complicacoes=[ComplicacaoPersonagem(nome="Fracote")],
    )
    atualizar_ficha(f_frac)
    assert f_frac.pericias["Atletismo"].total == f0.pericias["Atletismo"].total - 2
    assert f_frac.pericias["Acrobacia"].total == f0.pericias["Acrobacia"].total - 2
    assert f_frac.pericias["Fortitude"].total == f0.pericias["Fortitude"].total - 2

    f_vag = _ficha_base(
        classe="Bárbaro",
        nivel=2,
        complicacoes=[ComplicacaoPersonagem(nome="Vagaroso")],
    )
    atualizar_ficha(f_vag)
    assert f_vag.status.deslocamento == 4.5

    f_totem = _ficha_base(
        classe="Bárbaro",
        nivel=2,
        complicacoes=[ComplicacaoPersonagem(nome="Totem Gigante", poder_bonus="Esquiva")],
    )
    atualizar_ficha(f_totem)
    assert f_totem.status.penalidade_armadura == 5
    assert f_totem.pericias["Acrobacia"].total == f0.pericias["Acrobacia"].total - 5
    assert any(h.nome == "Esquiva" for h in f_totem.habilidades)


def test_complicacao_classe_regra_50_por_cento():
    # 1 nível Bárbaro + 3 níveis Guerreiro (25% Bárbaro < 50%): poder bônus bloqueado!
    f = Personagem(
        cabecalho=Cabecalho(nome="Multiclasse", raca="Humano"),
        classes=[
            ClasseInfo(nome="Guerreiro", nivel=3, primaria=True),
            ClasseInfo(nome="Bárbaro", nivel=1),
        ],
        atributos_base=Atributos(forca=2, destreza=2, constituicao=2),
        complicacoes=[ComplicacaoPersonagem(nome="De Peito Aberto", poder_bonus="Esquiva")],
    )
    assert validar_complicacao_classe(f, "De Peito Aberto")["valida"] is False
    atualizar_ficha(f)
    assert not any(h.nome == "Esquiva" for h in f.habilidades)

    # Subindo Bárbaro para 3 (50%): poder bônus liberado!
    f.classes[1].nivel = 3
    assert validar_complicacao_classe(f, "De Peito Aberto")["valida"] is True
    atualizar_ficha(f)
    assert any(h.nome == "Esquiva" for h in f.habilidades)


def test_complicacao_idade_turrao_e_abatido():
    f0 = _ficha_base(classe="Guerreiro", nivel=6)
    atualizar_ficha(f0)
    assert f0.pericias["Conhecimento"].bonus_nivel == 3

    f1 = _ficha_base(
        classe="Guerreiro",
        nivel=6,
        complicacoes=[
            ComplicacaoPersonagem(nome="Turrão"),
            ComplicacaoPersonagem(nome="Abatido"),
        ],
    )
    atualizar_ficha(f1)
    # Conhecimento não treinada perde metade do nível (3 -> 0)
    assert f1.pericias["Conhecimento"].bonus_nivel == 0
    assert f1.pericias["Conhecimento"].total == f0.pericias["Conhecimento"].total - 3
    # Abatido: -2 PV/nv (-12 PV)
    assert f1.status.pv.maximo == f0.status.pv.maximo - 12


# =====================================================================
# 4. IDADES VARIADAS (TABELA 4-2, OPT-IN)
# =====================================================================

def test_idades_variadas_crianca_adolescente_velho_anciao():
    # Criança: For -2, Con -1, Sab -1, Tamanho Pequeno, Protegido dos Deuses (+2 Def, +5 TR)
    f_cri = _ficha_base(
        classe="Guerreiro",
        nivel=1,
        regras_opcionais_ativas=["idades_variadas"],
        descricao=Descricao(idade=10),
    )
    atualizar_ficha(f_cri)
    assert f_cri.descricao.faixa_etaria == "Criança"
    assert f_cri.descricao.tamanho == TamanhoEnum.PEQUENO
    assert f_cri.atributos.forca == 0      # 2 - 2
    assert f_cri.atributos.constituicao == 1  # 2 - 1
    assert f_cri.atributos.sabedoria == 0  # 1 - 1
    assert f_cri.status.defesa.total == 14  # 10 + Des 2 + Protegido 2
    assert any(h.nome == "Protegido dos Deuses" for h in f_cri.habilidades)

    # Adolescente: Sab -1, Ímpeto Juvenil (+3 PM)
    f_base_pm = _ficha_base(classe="Guerreiro", nivel=1)
    atualizar_ficha(f_base_pm)
    f_ado = _ficha_base(
        classe="Guerreiro",
        nivel=1,
        regras_opcionais_ativas=["idades_variadas"],
        descricao=Descricao(idade=15),
    )
    atualizar_ficha(f_ado)
    assert f_ado.descricao.faixa_etaria == "Adolescente"
    assert f_ado.atributos.sabedoria == 0
    assert f_ado.status.pm.maximo == f_base_pm.status.pm.maximo + 3

    # Ancião: For/Des/Con -2 e bloqueia Aumento de Atributo físico (mas permite mental!)
    f_anc = _ficha_base(
        classe="Guerreiro",
        nivel=4,
        regras_opcionais_ativas=["idades_variadas"],
        descricao=Descricao(idade=85),
        habilidades=[
            Habilidade(nome="Aumento de Atributo", tipo="Poder de Classe", escolhas_aplicadas={"atributo": "forca"}),
            Habilidade(nome="Aumento de Atributo", tipo="Poder de Classe", escolhas_aplicadas={"atributo": "sabedoria"}),
        ],
    )
    atualizar_ficha(f_anc)
    assert f_anc.descricao.faixa_etaria == "Ancião"
    assert f_anc.atributos.forca == 0       # 2 - 2 (Aumento em For bloqueado!)
    assert f_anc.atributos.destreza == 0    # 2 - 2
    assert f_anc.atributos.constituicao == 0  # 2 - 2
    assert f_anc.atributos.sabedoria == 2   # 1 + 1 (Aumento mental permitido!)


# =====================================================================
# 5. DEFESA ÉPICA, PAPÉIS NO GRUPO E BOM DE GARFO
# =====================================================================

def test_defesa_epica_opt_in():
    f = _ficha_base(classe="Guerreiro", nivel=6, regras_opcionais_ativas=["defesa_epica"])
    atualizar_ficha(f)
    # Base 10 + Des 2 + Defesa Épica (+3 no nv 6) = 15
    assert f.status.defesa.total == 15


def test_papeis_no_grupo():
    f0 = _ficha_base(classe="Guerreiro", nivel=2)
    atualizar_ficha(f0)

    f_adv = _ficha_base(classe="Guerreiro", nivel=2, papel_grupo="Advogado")
    atualizar_ficha(f_adv)
    assert f_adv.status.pm.maximo == f0.status.pm.maximo + 1

    f_xer = _ficha_base(classe="Guerreiro", nivel=2, papel_grupo="Xerife")
    atualizar_ficha(f_xer)
    assert f_xer.pericias["Iniciativa"].total == f0.pericias["Iniciativa"].total + 1

    f_tes = _ficha_base(classe="Guerreiro", nivel=2, papel_grupo="Tesoureiro (Ofício)")
    atualizar_ficha(f_tes)
    assert f_tes.pericias["Ofício"].total == f0.pericias["Ofício"].total + 1


def test_bom_de_garfo_pv_por_patamar():
    # Nível 11 = 3 patamares (Iniciante, Veterano, Campeão) -> +9 PV
    f0 = _ficha_base(classe="Guerreiro", nivel=11)
    atualizar_ficha(f0)

    f1 = _ficha_base(
        classe="Guerreiro",
        nivel=11,
        habilidades=[Habilidade(nome="Bom de Garfo", tipo="Poder de Destino")],
    )
    atualizar_ficha(f1)
    assert f1.status.pv.maximo == f0.status.pv.maximo + 9


# =====================================================================
# 6. HELPERS DE MESA (ATRIBUTOS, MORTE, ARMAS ÁGEIS, DOMÍNIOS)
# =====================================================================

def test_helpers_mesa_herois_cap4():
    assert gerar_atributos_metodo("Khalmyr")["valores"] == [3, 3, 2, 1, 0, -1]
    assert len(gerar_atributos_metodo("Clássica", seed=42)["valores"]) == 6
    assert len(gerar_atributos_metodo("Épica", seed=42)["valores"]) == 6
    assert len(gerar_atributos_metodo("Valkaria", seed=42)["dados_7d6"]) == 7
    assert len(gerar_atributos_metodo("Nimb", seed=42)["valores"]) == 6
    assert gerar_atributos_metodo("Pontos Variados", pontos=15)["pontos_disponiveis"] == 15

    assert calcular_pm_dominio_mistico(1) == 1
    assert calcular_pm_dominio_mistico(4) == 16
    assert calcular_pm_dominio_mistico(5) == 25

    assert avaliar_teste_morte_alternativa(20)["recupera_1_pv"] is True
    assert avaliar_teste_morte_alternativa(1)["falhas_adicionadas"] == 2
    assert avaliar_teste_morte_alternativa(12, cd=10)["sucessos_adicionados"] == 1
    assert avaliar_teste_morte_alternativa(5, cd=10)["falhas_adicionadas"] == 1

    f_off = _ficha_base()
    f_on = _ficha_base(regras_opcionais_ativas=["mais_armas_ageis"])
    assert arma_e_agil_com_regra_opcional(f_off, "Lança") is False
    assert arma_e_agil_com_regra_opcional(f_on, "Lança") is True
    assert arma_e_agil_com_regra_opcional(f_on, "Bordão") is True
    assert arma_e_agil_com_regra_opcional(f_on, "Azagaia") is True
    assert arma_e_agil_com_regra_opcional(f_on, "Montante") is False
