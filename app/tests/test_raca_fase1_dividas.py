"""Testes da Fase 1 — Dívidas das Raças do Livro Básico (T20 JdA)."""
from src.models import Personagem, Cabecalho, ClasseInfo, Habilidade
from src.regras import atualizar_ficha
from src.routers.dados import listar_nomes_racas, obter_detalhes_racas
from src.dados_habilidades_raciais import DADOS_HABILIDADES_RACIAIS


def _ficha(raca: str, classe: str = "Guerreiro", nivel: int = 1) -> Personagem:
    f = Personagem()
    f.cabecalho = Cabecalho(nome=f"Teste {raca} {classe}", raca=raca, nivel_total=nivel)
    f.classes = [ClasseInfo(nome=classe, nivel=nivel, primaria=True)]
    return f


# --- 1. Filtro Livro Básico vs Suplementos em /racas e /dados/racas ---

def test_racas_padrao_retorna_apenas_livro_basico():
    nomes = listar_nomes_racas()
    detalhes = obter_detalhes_racas()
    assert len(nomes) == 18  # 17 raças base (Suraggel Aggelus + Sulfure)
    assert len(detalhes) == 18
    assert all(d.get("fonte") == "T20 JdA" for d in detalhes.values())
    assert "Humano" in nomes
    assert "Hynne" in nomes
    assert "Duende" not in nomes


def test_racas_com_suplementos_retorna_catalogo_completo():
    nomes_todos = listar_nomes_racas(incluir_suplementos=True)
    detalhes_todos = obter_detalhes_racas(incluir_suplementos=True)
    assert len(nomes_todos) > 18
    assert len(detalhes_todos) == len(nomes_todos)
    assert "Duende" in nomes_todos
    assert "Humano" in nomes_todos


def test_racas_filtro_por_fonte_explicita():
    nomes = listar_nomes_racas(fonte="T20 JdA")
    assert len(nomes) == 18
    assert "Duende" not in nomes


# --- 2. Efeitos raciais conectados (Medusa e Goblin) ---

def test_medusa_resistencia_veneno_em_efeitos_e_fortitude():
    f = _ficha("Medusa")
    atualizar_ficha(f)

    assert any("+5 em resistências contra veneno" in e for e in f.status.efeitos_ativos)
    fort = f.pericias["Fortitude"]
    assert fort.bonus_automatico == 0  # situacional não infla Fortitude base
    assert any("Natureza Venenosa" in linha and "veneno" in linha for linha in fort.fontes_bonus)


def test_goblin_espelunqueiro_deslocamento_escalada_em_efeitos():
    f = _ficha("Goblin")
    atualizar_ficha(f)

    assert f.status.deslocamento == 9
    assert any("Deslocamento de escalada: 9m" in e for e in f.status.efeitos_ativos)


# --- 3. Reaprendizado de habilidades duplicadas ---

def test_dahllan_druida_empatia_selvagem_concede_mais_2_adestramento():
    f = _ficha("Dahllan", classe="Druida", nivel=1)
    atualizar_ficha(f)

    adestramento = f.pericias["Adestramento"]
    assert adestramento.bonus_automatico == 2
    assert any("Empatia Selvagem" in linha for linha in adestramento.fontes_bonus)

    hab = next(h for h in f.habilidades if h.nome == "Empatia Selvagem")
    assert "Reaprendida: +2 Adestramento" in hab.descricao
    assert "Druida" in (hab.fonte or "")

    # Idempotência em múltiplos recálculos
    atualizar_ficha(f)
    assert f.pericias["Adestramento"].bonus_automatico == 2


def test_dahllan_sem_druida_nao_ganha_bonus_duplicata_adestramento():
    f = _ficha("Dahllan", classe="Guerreiro", nivel=1)
    atualizar_ficha(f)

    assert f.pericias["Adestramento"].bonus_automatico == 0


def test_kliren_inventor_engenhosidade_reduz_custo_para_1_pm():
    f = _ficha("Kliren", classe="Inventor", nivel=1)
    atualizar_ficha(f)

    hab = next(h for h in f.habilidades if h.nome == "Engenhosidade")
    assert hab.efeitos["habilidade_ativavel"]["custo"] == 1
    assert "[Custo reduzido por duplicata: 1 PM]" in hab.descricao
    assert "Inventor" in (hab.fonte or "")

    # Idempotência + catálogo global intacto
    atualizar_ficha(f)
    hab = next(h for h in f.habilidades if h.nome == "Engenhosidade")
    assert hab.efeitos["habilidade_ativavel"]["custo"] == 1
    assert DADOS_HABILIDADES_RACIAIS["Engenhosidade_Kliren"]["efeitos"]["habilidade_ativavel"]["custo"] == 2


def test_kliren_sem_inventor_mantem_engenhosidade_2_pm():
    f = _ficha("Kliren", classe="Guerreiro", nivel=1)
    atualizar_ficha(f)

    hab = next(h for h in f.habilidades if h.nome == "Engenhosidade")
    assert hab.efeitos["habilidade_ativavel"]["custo"] == 2
    assert "[Custo reduzido por duplicata:" not in hab.descricao


def test_reaprendizado_generico_com_duas_habilidades_separadas():
    """Mesmo quando duas habilidades com o mesmo nome coexistem na lista, o bônus aplica 1 vez."""
    from src.regras.habilidades import processar_acumulo_habilidades

    f = _ficha("Humano")
    f.habilidades = [
        Habilidade(
            nome="Empatia Selvagem",
            tipo="Racial",
            descricao="Origem 1.",
            efeitos={"bonus_pericia_se_duplicada": {"Adestramento": 2}},
        ),
        Habilidade(
            nome="Empatia Selvagem",
            tipo="Classe",
            descricao="Origem 2.",
            efeitos={"bonus_pericia_se_duplicada": {"Adestramento": 2}},
        ),
    ]
    processar_acumulo_habilidades(f)
    com_bonus = [h for h in f.habilidades if (h.efeitos or {}).get("bonus_pericia", {}).get("Adestramento") == 2]
    assert len(com_bonus) == 1
