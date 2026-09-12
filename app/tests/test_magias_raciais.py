from src.models import Personagem, Cabecalho, Habilidade, Magia


def _ficha(raca="Dahllan", nivel=1):
    return Personagem(cabecalho=Cabecalho(nome="Teste", raca=raca, nivel_total=nivel))


def test_dahllan_injeta_controlar_plantas():
    from src.regras.magias import sincronizar_magias_raciais
    f = _ficha()
    f.habilidades = [Habilidade(
        nome="Amiga das Plantas", tipo="Racial", descricao="",
        efeitos={"magia_adicional": {"nome": "Controlar Plantas", "atributo": "Sab"},
                 "reducao_custo_magia": {"nomes": ["Controlar Plantas"], "valor": 1}})]
    sincronizar_magias_raciais(f)
    m = next((x for x in f.combate.magias if x.nome == "Controlar Plantas"), None)
    assert m is not None
    assert m.fonte_origem == "Racial: Amiga das Plantas"
    assert m.isento_armadura is True
    assert m.atributo_chave == "Sab"


def test_troca_de_escolha_remove_magia_antiga():
    from src.regras.magias import sincronizar_magias_raciais
    f = _ficha("Sílfide")
    hab = Habilidade(
        nome="Magia das Fadas", tipo="Racial", descricao="",
        efeitos={"magia_adicional_escolha": {"quantidade": 1, "atributo": "Car"}})
    f.habilidades = [hab]
    hab.escolhas_aplicadas = {"magia_0": "Luz"}
    sincronizar_magias_raciais(f)
    assert any(m.nome == "Luz" for m in f.combate.magias)
    hab.escolhas_aplicadas = {"magia_0": "Sono"}
    sincronizar_magias_raciais(f)
    nomes = [m.nome for m in f.combate.magias if (m.fonte_origem or "").startswith("Racial:")]
    assert nomes == ["Sono"]


def test_custo_minimo_1_pm_com_reducao_racial():
    from src.regras.magias import sincronizar_magias_raciais
    from src.regras.custo_magia import calcular_custo_magia
    f = _ficha()
    f.habilidades = [Habilidade(
        nome="Amiga das Plantas", tipo="Racial", descricao="",
        efeitos={"magia_adicional": {"nome": "Controlar Plantas", "atributo": "Sab"},
                 "reducao_custo_magia": {"nomes": ["Controlar Plantas"], "valor": 1}})]
    sincronizar_magias_raciais(f)
    m = next(x for x in f.combate.magias if x.nome == "Controlar Plantas")
    calc = calcular_custo_magia(f, m)
    assert calc.total == 1  # 1 base − 1 redução → mínimo 1 PM
    assert any("Redução" in fo.categoria for fo in calc.fontes)


def test_alta_arcana_metade_arredondada_para_baixo():
    from src.regras.custo_magia import calcular_custo_magia
    f = _ficha("Humano", nivel=18)
    f.habilidades = [Habilidade(nome="Alta Arcana", tipo="Poder de Classe",
                                descricao="", efeitos={"reducao_custo_magia_global": 0.5})]
    m = Magia(nome="Bola de Fogo", circulo=3, custo_pm=6)
    calc = calcular_custo_magia(f, m)
    assert calc.total == 3  # floor(6 × 0.5)


def test_truque_custa_zero():
    from src.regras.custo_magia import calcular_custo_magia
    f = _ficha()
    m = Magia(nome="Luz", circulo=1, custo_pm=1)
    calc = calcular_custo_magia(f, m, eh_truque=True)
    assert calc.total == 0


def test_reducao_se_conhecida_aplica_quando_magia_ja_existe():
    from src.regras.magias import sincronizar_magias_raciais
    from src.regras.custo_magia import calcular_custo_magia
    f = _ficha()
    # Magia já no Grimório como racial (Dahllan)
    f.habilidades = [Habilidade(
        nome="Amiga das Plantas", tipo="Racial", descricao="",
        efeitos={"magia_adicional": {"nome": "Controlar Plantas", "atributo": "Sab"},
                 "reducao_custo_magia": {"nomes": ["Controlar Plantas"], "valor": 1}})]
    sincronizar_magias_raciais(f)
    m = next(x for x in f.combate.magias if x.nome == "Controlar Plantas")
    # Agora aprende de novo via Qareen (reducao_custo_se_conhecida: 1)
    f.habilidades.append(Habilidade(
        nome="Tatuagem Mística", tipo="Racial", descricao="",
        efeitos={"reducao_custo_se_conhecida": 1}))
    calc = calcular_custo_magia(f, m)
    assert calc.total == 1  # base 1 − racial 1 − se_conhecida 1 = mínimo 1 PM
    labels = [fo.fonte for fo in calc.fontes]
    assert any("reaprendizado" in l for l in labels)
