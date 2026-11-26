"""Testes automatizados da exportação de ficha em PDF (PyMuPDF)."""
import pymupdf
from src.models import (
    Personagem, Cabecalho, ClasseInfo, PericiaInfo, Atributos,
    Inventario, Item, Dinheiro, Descricao, Magia,
)
from src.regras import atualizar_ficha
from src.routers.pdf import (
    gerar_pdf_bytes,
    _sanitizar_nome_arquivo,
    _truncar_texto,
    _carregar_template_bytes,
)


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


def test_truncar_texto_inteligente_e_cache_template():
    texto = "Linha um completa\nLinha dois muito longa para caber no limite"
    trunc = _truncar_texto(texto, 25)
    assert trunc.endswith("...")
    assert len(trunc) <= 25
    # Cache em memória retorna exatamente o mesmo objeto bytes
    assert _carregar_template_bytes() is _carregar_template_bytes()


def test_gerar_pdf_ficha_completa():
    f = Personagem(
        cabecalho=Cabecalho(
            nome="Tordek Ferro",
            jogador="Caique",
            raca="Anão",
            origem="Artesão",
            deus="Khalmyr",
            nivel_total=5,
        ),
        classes=[
            ClasseInfo(nome="Guerreiro", nivel=3, primaria=True),
            ClasseInfo(nome="Clérigo", nivel=2, primaria=False),
        ],
        atributos_base=Atributos(forca=3, destreza=1, constituicao=2, sabedoria=3),
        inventario=Inventario(
            dinheiro=Dinheiro(tp=450, to=12),
            equipamentos=[
                Item(nome="Cota de malha", equipado=True, espaco=5),
                Item(nome="Escudo pesado", equipado=True, espaco=2),
                Item(nome="Poção de Cura", qtd=3, espaco=1),
            ],
        ),
        descricao=Descricao(
            idade="85",
            faixa_etaria="Adulto",
            alinhamento="Leal e Bondoso",
            aparencia="Barba trançada com anéis de ferro",
            historia="Forjado nas profundezas de Doherimm.",
            anotacoes="Lembrar de comprar essência de mana.",
        ),
    )
    f.pericias["Luta"] = PericiaInfo(treino=1, total=0)
    f.pericias["Ofício (Armeiro)"] = PericiaInfo(treino=1, total=0)
    f.combate.magias.append(Magia(nome="Curar Ferimentos", circulo=1, tipo="Divina", escola="Evocação", custo_pm=1))
    atualizar_ficha(f)

    pdf_bytes = gerar_pdf_bytes(f)
    assert pdf_bytes.startswith(b"%PDF")
    assert len(pdf_bytes) > 10_000

    campos = _extrair_campos(pdf_bytes)
    assert campos["NOME DO PERSONAGEM"] == "Tordek Ferro"
    assert campos["JOGADOR"] == "Caique"
    assert campos["RAÇA"] == "Anão"
    # Multiclasse formatada
    assert campos["CLASSE"] == "Guerreiro 3 / Clérigo 2"
    assert campos["Lv"] == "5"
    # Modificadores de atributos preenchidos (não mais 0)
    assert campos["ModFor"] == f"+{f.atributos.forca}"
    assert campos["ModCon"] == f"+{f.atributos.constituicao}"
    assert campos["ModSab"] == f"+{f.atributos.sabedoria}"
    # Status, Defesa, Armadura & Escudo
    assert campos["PVs Totais"] == str(f.status.pv.maximo)
    assert campos["PMs Totais"] == str(f.status.pm.maximo)
    assert campos["CA"] == str(f.status.defesa.total)
    assert campos["Armadura"] == "Cota de malha"
    assert campos["B.Arm"] == "6"
    assert campos["Pa"] == "2"
    assert campos["Escudo"] == "Escudo pesado"
    assert campos["B.Esc"] == "2"
    assert campos["Pe"] == "2"
    assert campos["arm pesa"] in (False, "Off", "/Off", "")
    # Proficiências, Dinheiro & Tamanho
    assert "Armas Marciais" in str(campos["Proficiências"])
    assert campos["T"] == "450"
    assert campos["TO"] == "12"
    assert campos["SeleTamanho"] == "Médio"
    # Perícias completas (Total, 1/2 nível, treino, atributo) + Ofício customizado
    assert campos["Mar Trei luta"] in (True, "Yes", "/Yes")
    assert campos["190"] == str(f.pericias["Luta"].total)
    assert campos["191"] == "2"
    assert campos["193"] == "2"
    assert campos["Ofício 1"] == "Armeiro"
    # Magias (Atributo-chave Sabedoria do Clérigo + CD)
    assert campos["SeleAtribMagia"] == "Sab"
    assert campos["TesteResist"] == str(f.combate.cd_magias)
    # Página 2 (Descrição & Anotações preenchidas; Observação da Pág. 1 intacta)
    assert "Barba trançada" in str(campos["Descrição"])
    assert "essência de mana" in str(campos["Anotações"])
    assert "Carga Total" in str(campos["Observação"])
    assert "Duro como Pedra" in str(campos.get("HabRaçasOrigem", ""))
