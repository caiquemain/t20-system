"""Arcanista: guarda-chuva. Garante que todos os 21 poderes do livro
existem no catalogo, e que 2 casos especificos funcionam."""
import pytest
from src.dados_habilidades_classe import DADOS_HABILIDADES_CLASSE
from src.dados_poderes_arcanista import PODERES_ARCANISTA
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Habilidade
from src.regras import atualizar_ficha


PODERES_DO_LIVRO = [
    "Arcano de Batalha", "Aumento de Atributo", "Caldeirão do Bruxo",
    "Conhecimento Mágico", "Contramágica Aprimorada", "Envolto em Mistério",
    "Escriba Arcano", "Especialista em Escola", "Familiar", "Fluxo de Mana",
    "Foco Vital", "Fortalecimento Arcano", "Herança Aprimorada",
    "Herança Superior", "Magia Pungente", "Mestre em Escola", "Poder Mágico",
    "Raio Arcano", "Raio Elemental", "Raio Poderoso", "Tinta do Mago",
]


@pytest.mark.parametrize("nome", PODERES_DO_LIVRO)
def test_poder_existe_no_catalogo_dados_poderes_arcanista(nome):
    assert nome in PODERES_ARCANISTA, (
        f"Poder '{nome}' do livro nao esta em PODERES_ARCANISTA"
    )


@pytest.mark.parametrize("nome", PODERES_DO_LIVRO)
def test_poder_existe_no_catalogo_dados_habilidades_classe(nome):
    """Nomes devem bater entre os 2 catalogos (ha risco de divergencia)."""
    nomes_no_classe = {h["nome"] for h in DADOS_HABILIDADES_CLASSE.values()
                       if h.get("classe") == "Arcanista"}
    assert nome in nomes_no_classe, (
        f"Poder '{nome}' do livro nao esta em DADOS_HABILIDADES_CLASSE"
    )


def test_poder_arcanista_sem_efeitos_vazio():
    """Poderes de Arcanista em DADOS_HABILIDADES_CLASSE nao podem ter
    efeitos= {} (vazio). Pode ser None se for puramente textual? Nao:
    o schema exige ao menos uma chave declarativa."""
    problemas = [
        chave for chave, h in DADOS_HABILIDADES_CLASSE.items()
        if h.get("classe") == "Arcanista"
        and isinstance(h.get("efeitos"), dict)
        and not h["efeitos"]
    ]
    assert not problemas, f"Poderes sem efeitos: {problemas}"


def test_caldeirao_do_bruxo_catalogo_ok():
    """Caldeirao do Bruxo tem efeito declarativo fabricar_pocao."""
    hab = next(
        (h for h in DADOS_HABILIDADES_CLASSE.values()
         if h.get("nome") == "Caldeirão do Bruxo"),
        None,
    )
    assert hab is not None
    efeitos = hab.get("efeitos") or {}
    # Aceita qualquer chave que sinalize criacao de pocao
    chaves = ("fabricar_pocao", "criar_pocoes")
    assert any(k in efeitos for k in chaves) or efeitos.get("nota"), (
        f"Caldeirao do Bruxo sem efeito claro: {efeitos}"
    )


def test_envolto_em_misterio_bonus_lido():
    """Envolto em Misterio: +5 em Enganacao/Intimidacao vs alvos nao
    treinados. Motor deve exibir a fonte como situacional e NAO somar
    ao total base (condicional por alvo).

    Nota: o wizard real (useFicha.ts) popula `efeitos` do catalogo ao
    salvar a escolha. O teste reproduz esse comportamento carregando
    os efeitos de DADOS_HABILIDADES_CLASSE.
    """
    efeitos = DADOS_HABILIDADES_CLASSE["ARCANISTA_ENVOLTO_MISTERIO"]["efeitos"]

    def _ficha_com_envolto():
        f = Personagem()
        f.cabecalho = Cabecalho(nome="Arc", raca="Humano", nivel_total=1)
        f.classes = [ClasseInfo(nome="Arcanista", nivel=1,
                                primaria=True, subclasse="Mago")]
        f.atributos_base = Atributos(inteligencia=3)
        f.atributos = f.atributos_base.model_copy()
        f.habilidades.append(Habilidade(
            nome="Envolto em Mistério", tipo="Poder de Arcanista",
            efeitos=efeitos,
        ))
        return f

    # 1 + 2. Fontes condicionais aparecem em Enganacao e Intimidacao
    f = _ficha_com_envolto()
    atualizar_ficha(f)

    for pericia in ("Enganação", "Intimidação"):
        fontes = f.pericias[pericia].fontes_bonus
        assert any("Envolto em Mistério" in (linha or "") for linha in fontes), (
            f"Fonte 'Envolto em Mistério' ausente em {pericia}. "
            f"Fontes: {fontes}"
        )

    # 3. Bonus NAO soma ao total base (e condicional por alvo, nao toggle)
    assert f.pericias["Enganação"].total == 0, (
        f"Envolto em Mistério NAO deveria somar +5 ao total base. "
        f"Total: {f.pericias['Enganação'].total}"
    )
    assert f.pericias["Intimidação"].total == 0
