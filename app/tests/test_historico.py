from src.models import Habilidade, Personagem, ClasseInfo
from src.regras.historico import resumir_mudancas


def _ficha(nivel=1):
    f = Personagem()
    f.cabecalho.nome = "Boneco de Teste"
    f.classes = [ClasseInfo(nome="Guerreiro", nivel=nivel)]
    f.cabecalho.nivel_total = nivel
    return f


def test_resumo_detecta_nivel_e_pv():
    antes = _ficha(1)
    antes.status.pv.maximo = 14
    depois = _ficha(2)
    depois.status.pv.maximo = 20
    resumo = resumir_mudancas(antes, depois)
    assert any("Nível 1 → 2" in r for r in resumo)
    assert any("PV máximo 14 → 20 (+6)" in r for r in resumo)


def test_resumo_vazio_sem_mudancas():
    f = _ficha(3)
    assert resumir_mudancas(f, f.model_copy(deep=True)) == []


def test_resumo_detecta_habilidade_e_magia_novas():
    antes = _ficha(2)
    depois = _ficha(2)
    depois.habilidades = [Habilidade(nome="Ataque Poderoso", tipo="Poder de Guerreiro")]
    from src.models import Magia
    depois.combate.magias = [Magia(nome="Luz", circulo=1)]
    resumo = resumir_mudancas(antes, depois)
    assert any("Nova habilidade: Ataque Poderoso" in r for r in resumo)
    assert any("Nova magia: Luz" in r for r in resumo)


def test_resumo_detecta_circulo_e_limite():
    antes = _ficha(4)
    depois = _ficha(5)
    antes.combate.circulo_maximo = 1
    depois.combate.circulo_maximo = 2
    antes.combate.limite_magias = 3
    depois.combate.limite_magias = 4
    resumo = resumir_mudancas(antes, depois)
    assert any("Círculo máximo" in r and "2º" in r for r in resumo)
    assert any("Limite de magias" in r for r in resumo)
