"""Bardo — testes de poderes de classe e cobertura completa do catálogo (T20 JdA p.43-44)."""
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Habilidade, Item
from src.dados_habilidades_classe import DADOS_HABILIDADES_CLASSE
from src.regras import atualizar_ficha


def _bardo(nivel=6, forca=0, car=5, poderes=None, condicoes=None, itens=None):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Trova", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Bardo", nivel=nivel, primaria=True)]
    f.atributos_base = Atributos(forca=forca, destreza=2, constituicao=1, carisma=car)
    f.atributos = f.atributos_base.model_copy()
    if condicoes:
        f.condicoes_ativas = list(condicoes)
    for chave in (poderes or []):
        d = DADOS_HABILIDADES_CLASSE[chave]
        f.habilidades.append(Habilidade(
            nome=d["nome"],
            tipo=d["tipo"],
            descricao=d["descricao"],
            efeitos=dict(d.get("efeitos", {})),
            fonte="Poder de Bardo",
        ))
    for nome_item in (itens or []):
        f.inventario.equipamentos.append(Item(nome=nome_item, equipado=True))
    return f


# ===================================================================
# 1. Aumentar Repertório (acumulável)
# ===================================================================

def test_aumentar_repertorio_soma_2_e_acumula():
    # Nível 4 base: 2 iniciais + 2 pares = 4 magias conhecidas
    f0 = _bardo(nivel=4)
    atualizar_ficha(f0)
    assert f0.combate.limite_magias == 4

    # 1x Aumentar Repertório: +2 = 6
    f1 = _bardo(nivel=4, poderes=["BARDO_AUMENTAR_REPERTORIO"])
    atualizar_ficha(f1)
    assert f1.combate.limite_magias == 6

    # 2x Aumentar Repertório: +4 = 8 ("pode escolher quantas vezes quiser")
    f2 = _bardo(nivel=4, poderes=["BARDO_AUMENTAR_REPERTORIO", "BARDO_AUMENTAR_REPERTORIO"])
    atualizar_ficha(f2)
    assert f2.combate.limite_magias == 8


# ===================================================================
# 2. Aumento de Atributo
# ===================================================================

def test_bardo_aumento_atributo():
    f = _bardo(nivel=4, car=4)
    d = DADOS_HABILIDADES_CLASSE["BARDO_AUMENTO_ATRIBUTO"]
    f.habilidades.append(Habilidade(
        nome=d["nome"],
        tipo=d["tipo"],
        descricao=d["descricao"],
        efeitos=dict(d["efeitos"]),
        escolhas_aplicadas={"atributo": "car"},
        fonte="Poder de Bardo",
    ))
    atualizar_ficha(f)
    assert f.atributos.carisma == 5


# ===================================================================
# 3. Esgrima Mágica
# ===================================================================

def test_esgrima_magica_troca_luta_por_atuacao_sob_inspiracao():
    # Com Inspiração ativa e Atuação > Luta: Florete (Uma Mão) e Machadinha (Leve) usam Atuação;
    # Montante (Duas Mãos) continua Luta; Arco curto (À Distância) continua Pontaria.
    f = _bardo(
        nivel=6,
        forca=0,
        car=5,
        poderes=["BARDO_ESGRIMA_MAGICA"],
        condicoes=["inspiracao"],
        itens=["Florete", "Machadinha", "Montante", "Arco curto"],
    )
    atualizar_ficha(f)
    por_nome = {a.nome: a for a in f.combate.ataques}

    assert por_nome["Florete"].teste == "Atuação"
    assert "Esgrima Mágica" in por_nome["Florete"].especial
    assert por_nome["Machadinha"].teste == "Atuação"
    assert "Esgrima Mágica" in por_nome["Machadinha"].especial
    assert por_nome["Montante"].teste == "Luta"
    assert por_nome["Arco curto"].teste == "Pontaria"


def test_esgrima_magica_inativa_sem_inspiracao():
    f = _bardo(
        nivel=6,
        forca=0,
        car=5,
        poderes=["BARDO_ESGRIMA_MAGICA"],
        condicoes=[],
        itens=["Florete"],
    )
    atualizar_ficha(f)
    por_nome = {a.nome: a for a in f.combate.ataques}
    assert por_nome["Florete"].teste == "Luta"


# ===================================================================
# 4. Integridade completa do catálogo de Bardo (4 fixas + 20 poderes)
# ===================================================================

PODERES_ESPERADOS = {
    "Arte Mágica",
    "Aumentar Repertório",
    "Aumento de Atributo",
    "Dança das Lâminas",
    "Esgrima Mágica",
    "Estrelato",
    "Fascinar em Massa",
    "Golpe Elemental",
    "Golpe Mágico",
    "Inspiração Marcial",
    "Lendas e Histórias",
    "Manipular",
    "Manipular em Massa",
    "Música: Balada Fascinante",
    "Música: Canção Assustadora",
    "Música: Melodia Curativa",
    "Melodia Restauradora",
    "Mestre dos Sussurros",
    "Paródia",
    "Prestidigitação",
}

FIXAS_ESPERADAS = {
    "Inspiração": 1,
    "Magias (Bardo)": 1,
    "Eclético": 2,
    "Artista Completo": 20,
}


def test_catalogo_bardo_completo_24_entradas():
    bardo_entries = [
        v for v in DADOS_HABILIDADES_CLASSE.values()
        if v.get("classe") == "Bardo" and v.get("fonte", "T20 JdA") == "T20 JdA"
    ]
    fixas = {v["nome"]: v.get("nivel") for v in bardo_entries if v.get("tipo") == "Habilidade de Classe"}
    poderes = {v["nome"] for v in bardo_entries if v.get("tipo") == "Poder de Bardo"}

    assert fixas == FIXAS_ESPERADAS
    assert poderes == PODERES_ESPERADOS
    assert len(bardo_entries) == 24


def test_musicas_de_bardo_seguem_regra_base():
    musicas = [
        "BARDO_MUSICA_BALADA_FASCINANTE",
        "BARDO_MUSICA_CANCAO_ASSUSTADORA",
        "BARDO_MUSICA_MELODIA_CURATIVA",
    ]
    for chave in musicas:
        m = DADOS_HABILIDADES_CLASSE[chave]["efeitos"]["musica_bardo"]
        assert m["acao"] == "padrão"
        assert m["custo_pm"] == 1
        assert m["alcance"] == "curto"
        assert m["requer_instrumento"] is True
        assert m["requer_pericia"] == "Atuação"


def test_efeitos_ativos_poderes_situacionais_bardo():
    f = _bardo(
        nivel=6,
        poderes=["BARDO_ESTRELATO", "BARDO_MESTRE_SUSSURROS", "BARDO_GOLPE_MAGICO"],
    )
    atualizar_ficha(f)
    efeitos_txt = " | ".join(f.status.efeitos_ativos)
    assert "Estrelato" in efeitos_txt
    assert "Investigação (interrogar)" in efeitos_txt
    assert "Enganação (intriga)" in efeitos_txt
    assert "Golpe Mágico" in efeitos_txt
