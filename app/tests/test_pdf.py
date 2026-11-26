"""Testes automatizados da exportação de ficha em PDF (PyMuPDF)."""
import pymupdf
from src.models import Personagem, Cabecalho, ClasseInfo, PericiaInfo
from src.regras import atualizar_ficha
from src.routers.pdf import gerar_pdf_bytes, _sanitizar_nome_arquivo


def _extrair_campos(pdf_bytes: bytes) -> dict[str, object]:
    campos = {}
    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page in doc:
            for widget in page.widgets():
                if widget.field_name:
                    campos[widget.field_name] = widget.field_value
    return campos


def test_sanitizar_nome_arquivo():
    assert _sanitizar_nome_arquivo("Tordek Anão da Montanha") == "tordek-anao-da-montanha"
    assert _sanitizar_nome_arquivo("João / Magos & Cia!") == "joao-magos-cia"
    assert _sanitizar_nome_arquivo("") == "personagem"
    assert _sanitizar_nome_arquivo(None) == "personagem"
    assert _sanitizar_nome_arquivo("!!!") == "personagem"


def test_gerar_pdf_ficha_completa():
    f = Personagem()
    f.cabecalho = Cabecalho(
        nome="Tordek Ferro",
        jogador="Caique",
        raca="Anão",
        origem="Artesão",
        deus="Khalmyr",
        nivel_total=3,
    )
    f.classes = [ClasseInfo(nome="Guerreiro", nivel=3, primaria=True)]
    f.pericias["Luta"] = PericiaInfo(treino=1, total=0)
    atualizar_ficha(f)

    pdf_bytes = gerar_pdf_bytes(f)
    assert pdf_bytes.startswith(b"%PDF")
    assert len(pdf_bytes) > 10_000

    campos = _extrair_campos(pdf_bytes)
    assert campos["NOME DO PERSONAGEM"] == "Tordek Ferro"
    assert campos["JOGADOR"] == "Caique"
    assert campos["RAÇA"] == "Anão"
    assert campos["CLASSE"] == "Guerreiro"
    assert campos["Lv"] == "3"
    assert campos["PVs Totais"] == str(f.status.pv.maximo)
    assert campos["PMs Totais"] == str(f.status.pm.maximo)
    assert campos["CA"] == str(f.status.defesa.total)
    assert campos["Mar Trei luta"] in (True, "Yes", "/Yes")
    assert "Duro como Pedra" in str(campos.get("HabRaçasOrigem", ""))
