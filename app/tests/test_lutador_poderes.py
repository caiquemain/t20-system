"""Lutador — testes de poderes de classe e cobertura completa do catálogo (T20 JdA p.75-77)."""
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Habilidade, Item
from src.dados_habilidades_classe import DADOS_HABILIDADES_CLASSE
from src.regras import atualizar_ficha


def _lutador(nivel=10, forca=4, des=2, con=3, poderes=None, itens=None):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Rexthor", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Lutador", nivel=nivel, primaria=True)]
    f.atributos_base = Atributos(forca=forca, destreza=des, constituicao=con)
    f.atributos = f.atributos_base.model_copy()
    for chave in (poderes or []):
        d = DADOS_HABILIDADES_CLASSE[chave]
        f.habilidades.append(Habilidade(
            nome=d["nome"],
            tipo=d["tipo"],
            descricao=d["descricao"],
            efeitos=dict(d.get("efeitos", {})),
            fonte="Poder de Lutador",
        ))
    for nome_item in (itens or []):
        f.inventario.equipamentos.append(Item(nome=nome_item, equipado=True))
    return f


def test_bracos_calejados_soma_forca_apenas_sem_armadura():
    # Nível 2 sem armadura, Des 2, For 4: Defesa = 10 + 2 + min(4, 2) = 14
    f_sem = _lutador(nivel=2, forca=4, des=2, con=0, poderes=["LUTADOR_BRACOS_CALEJADOS"])
    atualizar_ficha(f_sem)
    assert f_sem.status.defesa.total == 14

    # Com armadura leve (Armadura de couro +2): Braços Calejados desliga -> 10 + 2 + 2 = 14 (sem For)
    f_leve = _lutador(nivel=4, forca=4, des=2, con=0, poderes=["LUTADOR_BRACOS_CALEJADOS"], itens=["Armadura de couro"])
    atualizar_ficha(f_leve)
    assert f_leve.status.defesa.total == 14


def test_sarado_soma_forca_em_pv_e_fortitude():
    f_base = _lutador(nivel=4, forca=4, con=3)
    atualizar_ficha(f_base)

    f_sarado = _lutador(nivel=4, forca=4, con=3, poderes=["LUTADOR_SARADO"])
    atualizar_ficha(f_sarado)
    assert f_sarado.status.pv.maximo == f_base.status.pv.maximo + 4
    assert f_sarado.pericias["Fortitude"].total == f_base.pericias["Fortitude"].total + 4


def test_trincado_e_punhos_de_adamante_em_briga_calc():
    f = _lutador(nivel=10, con=4, poderes=["LUTADOR_TRINCADO", "LUTADOR_PUNHOS_ADAMANTE"])
    atualizar_ficha(f)
    bc = f.combate.briga_calc
    assert bc["dano_con_trincado"] == 4
    assert bc["ignora_rd"] == 10


FIXAS_ESPERADAS = {
    "Briga": 1,
    "Golpe Relâmpago": 1,
    "Casca Grossa": 3,
    "Golpe Cruel": 5,
    "Golpe Violento": 9,
    "Dono da Rua": 20,
}

PODERES_ESPERADOS = {
    "Arma Improvisada",
    "Até Acertar",
    "Aumento de Atributo",
    "Braços Calejados",
    "Cabeçada",
    "Chave",
    "Confiança dos Ringues",
    "Convencido",
    "Golpe Baixo",
    "Golpe Imprudente",
    "Imobilização",
    "Língua dos Becos",
    "Lutador de Chão",
    "Nome na Arena",
    "Punhos de Adamante",
    "Rasteira",
    "Sarado",
    "Sequência Destruidora",
    "Trincado",
    "Trocação",
    "Trocação Tumultuosa",
    "Valentão",
    "Voadora",
}


def test_catalogo_lutador_completo_29_entradas():
    entries = [v for v in DADOS_HABILIDADES_CLASSE.values() if v.get("classe") == "Lutador"]
    fixas = {v["nome"]: v.get("nivel") for v in entries if v.get("tipo") == "Habilidade de Classe"}
    poderes = {v["nome"] for v in entries if v.get("tipo") == "Poder de Lutador"}

    assert fixas == FIXAS_ESPERADAS
    assert poderes == PODERES_ESPERADOS
    assert len(entries) == 29
    assert all(v.get("efeitos") for v in entries)
