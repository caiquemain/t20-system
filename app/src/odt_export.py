"""Gerador nativo de ficha editável em formato LibreOffice Writer (.odt — ODF 1.2)."""
from datetime import datetime
from io import BytesIO
import logging
import math
import xml.etree.ElementTree as ET
import zipfile

from .dados_equipamentos import DADOS_ARMADURAS
from .dados_pericias import DADOS_PERICIAS
from .models import Personagem
from .regras import atualizar_ficha
from .regras.custo_magia import calcular_limite_pm_magia, obter_atributo_chave_magia
from .regras.utils import calcular_modificador

logger = logging.getLogger(__name__)

ODT_MIMETYPE = "application/vnd.oasis.opendocument.text"

_NS_OFFICE = "urn:oasis:names:tc:opendocument:xmlns:office:1.0"
_NS_STYLE = "urn:oasis:names:tc:opendocument:xmlns:style:1.0"
_NS_TEXT = "urn:oasis:names:tc:opendocument:xmlns:text:1.0"
_NS_TABLE = "urn:oasis:names:tc:opendocument:xmlns:table:1.0"
_NS_FO = "urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
_NS_SVG = "urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
_NS_DC = "http://purl.org/dc/elements/1.1/"
_NS_META = "urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
_NS_MANIFEST = "urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"

_ATTR_SHORT = {
    "forca": "FOR",
    "destreza": "DES",
    "constituicao": "CON",
    "inteligencia": "INT",
    "sabedoria": "SAB",
    "carisma": "CAR",
    "for": "FOR",
    "des": "DES",
    "con": "CON",
    "int": "INT",
    "sab": "SAB",
    "car": "CAR",
}


def _q(ns: str, tag: str) -> str:
    return f"{{{ns}}}{tag}"


def _fmt_mod(val: int | float | None) -> str:
    v = int(val or 0)
    return f"+{v}" if v > 0 else str(v)


def _formatar_classes(ficha: Personagem) -> str:
    classes = ficha.classes or []
    if not classes:
        return "—"
    if len(classes) == 1:
        c = classes[0]
        sub = f" ({c.subclasse})" if c.subclasse else ""
        return f"{c.nome}{sub} — Nível {c.nivel}"
    return " / ".join(f"{c.nome} {c.nivel}" for c in classes)


def gerar_odt_bytes(personagem: Personagem) -> bytes:
    """Gera um documento LibreOffice Writer (.odt) ODF 1.2 estruturado e 100% editável."""
    ficha = personagem.model_copy(deep=True)
    pv_atual_orig = ficha.status.pv.atual
    pm_atual_orig = ficha.status.pm.atual
    try:
        atualizar_ficha(ficha)
        if 0 < pv_atual_orig <= ficha.status.pv.maximo:
            ficha.status.pv.atual = pv_atual_orig
        if 0 < pm_atual_orig <= ficha.status.pm.maximo:
            ficha.status.pm.atual = pm_atual_orig
    except Exception as e:
        logger.warning(f"Não foi possível recalcular a ficha completa para o ODT: {e}")

    for prefix, uri in [
        ("office", _NS_OFFICE),
        ("style", _NS_STYLE),
        ("text", _NS_TEXT),
        ("table", _NS_TABLE),
        ("fo", _NS_FO),
        ("svg", _NS_SVG),
        ("dc", _NS_DC),
        ("meta", _NS_META),
        ("manifest", _NS_MANIFEST),
    ]:
        ET.register_namespace(prefix, uri)

    # ── 1. manifest.xml ──
    manifest = ET.Element(_q(_NS_MANIFEST, "manifest"), {_q(_NS_MANIFEST, "version"): "1.2"})
    for full_path, media_type in [
        ("/", ODT_MIMETYPE),
        ("content.xml", "text/xml"),
        ("styles.xml", "text/xml"),
        ("meta.xml", "text/xml"),
    ]:
        ET.SubElement(manifest, _q(_NS_MANIFEST, "file-entry"), {
            _q(_NS_MANIFEST, "full-path"): full_path,
            _q(_NS_MANIFEST, "media-type"): media_type,
        })
    manifest_xml = ET.tostring(manifest, encoding="utf-8", xml_declaration=True)

    # ── 2. meta.xml ──
    meta_doc = ET.Element(_q(_NS_OFFICE, "document-meta"), {_q(_NS_OFFICE, "version"): "1.2"})
    meta_el = ET.SubElement(meta_doc, _q(_NS_OFFICE, "meta"))
    ET.SubElement(meta_el, _q(_NS_DC, "title")).text = f"Ficha T20 - {ficha.cabecalho.nome or 'Personagem'}"
    ET.SubElement(meta_el, _q(_NS_META, "generator")).text = "T20 System Exporter"
    ET.SubElement(meta_el, _q(_NS_META, "creation-date")).text = datetime.now().isoformat(timespec="seconds")
    meta_xml = ET.tostring(meta_doc, encoding="utf-8", xml_declaration=True)

    # ── 3. styles.xml (A4 com margens 1.2cm -> largura útil 18.6cm) ──
    styles_doc = ET.Element(_q(_NS_OFFICE, "document-styles"), {_q(_NS_OFFICE, "version"): "1.2"})
    font_decls_s = ET.SubElement(styles_doc, _q(_NS_OFFICE, "font-face-decls"))
    ET.SubElement(font_decls_s, _q(_NS_STYLE, "font-face"), {
        _q(_NS_STYLE, "name"): "Liberation Sans",
        _q(_NS_SVG, "font-family"): "'Liberation Sans', Arial, sans-serif",
        _q(_NS_STYLE, "font-family-generic"): "swiss",
        _q(_NS_STYLE, "font-pitch"): "variable",
    })
    auto_styles_s = ET.SubElement(styles_doc, _q(_NS_OFFICE, "automatic-styles"))
    pm1 = ET.SubElement(auto_styles_s, _q(_NS_STYLE, "page-layout"), {_q(_NS_STYLE, "name"): "PM1"})
    ET.SubElement(pm1, _q(_NS_STYLE, "page-layout-properties"), {
        _q(_NS_FO, "page-width"): "21.000cm",
        _q(_NS_FO, "page-height"): "29.700cm",
        _q(_NS_STYLE, "print-orientation"): "portrait",
        _q(_NS_FO, "margin-top"): "1.200cm",
        _q(_NS_FO, "margin-bottom"): "1.200cm",
        _q(_NS_FO, "margin-left"): "1.200cm",
        _q(_NS_FO, "margin-right"): "1.200cm",
    })
    master_styles = ET.SubElement(styles_doc, _q(_NS_OFFICE, "master-styles"))
    ET.SubElement(master_styles, _q(_NS_STYLE, "master-page"), {
        _q(_NS_STYLE, "name"): "Standard",
        _q(_NS_STYLE, "page-layout-name"): "PM1",
    })
    styles_xml = ET.tostring(styles_doc, encoding="utf-8", xml_declaration=True)

    # ── 4. content.xml ──
    content_doc = ET.Element(_q(_NS_OFFICE, "document-content"), {_q(_NS_OFFICE, "version"): "1.2"})
    font_decls_c = ET.SubElement(content_doc, _q(_NS_OFFICE, "font-face-decls"))
    ET.SubElement(font_decls_c, _q(_NS_STYLE, "font-face"), {
        _q(_NS_STYLE, "name"): "Liberation Sans",
        _q(_NS_SVG, "font-family"): "'Liberation Sans', Arial, sans-serif",
        _q(_NS_STYLE, "font-family-generic"): "swiss",
        _q(_NS_STYLE, "font-pitch"): "variable",
    })
    auto_styles = ET.SubElement(content_doc, _q(_NS_OFFICE, "automatic-styles"))

    def _add_p_style(name: str, p_props: dict, t_props: dict):
        st = ET.SubElement(auto_styles, _q(_NS_STYLE, "style"), {
            _q(_NS_STYLE, "name"): name,
            _q(_NS_STYLE, "family"): "paragraph",
        })
        if p_props:
            ET.SubElement(st, _q(_NS_STYLE, "paragraph-properties"), p_props)
        base_t = {_q(_NS_STYLE, "font-name"): "Liberation Sans"}
        base_t.update(t_props)
        ET.SubElement(st, _q(_NS_STYLE, "text-properties"), base_t)

    def _add_table_style(name: str, width_cm: str = "18.600cm"):
        st = ET.SubElement(auto_styles, _q(_NS_STYLE, "style"), {
            _q(_NS_STYLE, "name"): name,
            _q(_NS_STYLE, "family"): "table",
        })
        ET.SubElement(st, _q(_NS_STYLE, "table-properties"), {
            _q(_NS_STYLE, "width"): width_cm,
            _q(_NS_TABLE, "align"): "margins",
            _q(_NS_FO, "margin-bottom"): "0.18cm",
        })

    def _add_col_style(name: str, width_cm: float):
        st = ET.SubElement(auto_styles, _q(_NS_STYLE, "style"), {
            _q(_NS_STYLE, "name"): name,
            _q(_NS_STYLE, "family"): "table-column",
        })
        ET.SubElement(st, _q(_NS_STYLE, "table-column-properties"), {
            _q(_NS_STYLE, "column-width"): f"{width_cm:.3f}cm",
        })

    def _add_cell_style(name: str, bg: str | None = None, border: str = "0.5pt solid #c9c2b8", pad: str = "0.08cm"):
        st = ET.SubElement(auto_styles, _q(_NS_STYLE, "style"), {
            _q(_NS_STYLE, "name"): name,
            _q(_NS_STYLE, "family"): "table-cell",
        })
        props = {
            _q(_NS_FO, "padding"): pad,
            _q(_NS_FO, "border"): border,
            _q(_NS_STYLE, "vertical-align"): "middle",
        }
        if bg:
            props[_q(_NS_FO, "background-color")] = bg
        ET.SubElement(st, _q(_NS_STYLE, "table-cell-properties"), props)

    # Estilos de parágrafo
    _add_p_style("P_Title", {
        _q(_NS_FO, "margin-bottom"): "0.06cm",
        _q(_NS_FO, "border-bottom"): "1.5pt solid #8b1e1e",
        _q(_NS_FO, "padding-bottom"): "0.08cm",
    }, {
        _q(_NS_FO, "font-size"): "16pt",
        _q(_NS_FO, "font-weight"): "bold",
        _q(_NS_FO, "color"): "#8b1e1e",
    })
    _add_p_style("P_Subtitle", {
        _q(_NS_FO, "margin-bottom"): "0.22cm",
    }, {
        _q(_NS_FO, "font-size"): "8.5pt",
        _q(_NS_FO, "color"): "#555555",
    })
    _add_p_style("P_Section", {
        _q(_NS_FO, "margin-top"): "0.24cm",
        _q(_NS_FO, "margin-bottom"): "0.10cm",
        _q(_NS_FO, "background-color"): "#8b1e1e",
        _q(_NS_FO, "padding"): "0.09cm 0.16cm",
        _q(_NS_FO, "keep-with-next"): "always",
    }, {
        _q(_NS_FO, "font-size"): "10pt",
        _q(_NS_FO, "font-weight"): "bold",
        _q(_NS_FO, "color"): "#ffffff",
    })
    _add_p_style("P_Label", {
        _q(_NS_FO, "margin-bottom"): "0.02cm",
    }, {
        _q(_NS_FO, "font-size"): "7.5pt",
        _q(_NS_FO, "font-weight"): "bold",
        _q(_NS_FO, "color"): "#7a1c1c",
    })
    _add_p_style("P_LabelCenter", {
        _q(_NS_FO, "text-align"): "center",
        _q(_NS_FO, "margin-bottom"): "0.02cm",
    }, {
        _q(_NS_FO, "font-size"): "7.5pt",
        _q(_NS_FO, "font-weight"): "bold",
        _q(_NS_FO, "color"): "#7a1c1c",
    })
    _add_p_style("P_Value", {}, {
        _q(_NS_FO, "font-size"): "9pt",
        _q(_NS_FO, "color"): "#111111",
    })
    _add_p_style("P_ValueBold", {}, {
        _q(_NS_FO, "font-size"): "9.5pt",
        _q(_NS_FO, "font-weight"): "bold",
        _q(_NS_FO, "color"): "#111111",
    })
    _add_p_style("P_Center", {
        _q(_NS_FO, "text-align"): "center",
    }, {
        _q(_NS_FO, "font-size"): "8.5pt",
        _q(_NS_FO, "color"): "#111111",
    })
    _add_p_style("P_CenterBold", {
        _q(_NS_FO, "text-align"): "center",
    }, {
        _q(_NS_FO, "font-size"): "9pt",
        _q(_NS_FO, "font-weight"): "bold",
        _q(_NS_FO, "color"): "#111111",
    })
    _add_p_style("P_AttrBig", {
        _q(_NS_FO, "text-align"): "center",
    }, {
        _q(_NS_FO, "font-size"): "13.5pt",
        _q(_NS_FO, "font-weight"): "bold",
        _q(_NS_FO, "color"): "#8b1e1e",
    })
    _add_p_style("P_ThLeft", {}, {
        _q(_NS_FO, "font-size"): "8pt",
        _q(_NS_FO, "font-weight"): "bold",
        _q(_NS_FO, "color"): "#7a1c1c",
    })
    _add_p_style("P_ThCenter", {
        _q(_NS_FO, "text-align"): "center",
    }, {
        _q(_NS_FO, "font-size"): "8pt",
        _q(_NS_FO, "font-weight"): "bold",
        _q(_NS_FO, "color"): "#7a1c1c",
    })
    _add_p_style("P_Small", {
        _q(_NS_FO, "margin-bottom"): "0.06cm",
    }, {
        _q(_NS_FO, "font-size"): "8.5pt",
        _q(_NS_FO, "color"): "#222222",
    })
    _add_p_style("P_SmallMuted", {
        _q(_NS_FO, "margin-bottom"): "0.06cm",
    }, {
        _q(_NS_FO, "font-size"): "8pt",
        _q(_NS_FO, "color"): "#555555",
    })
    _add_p_style("P_ItemTitle", {
        _q(_NS_FO, "margin-top"): "0.10cm",
        _q(_NS_FO, "margin-bottom"): "0.02cm",
        _q(_NS_FO, "keep-with-next"): "always",
    }, {
        _q(_NS_FO, "font-size"): "9pt",
        _q(_NS_FO, "font-weight"): "bold",
        _q(_NS_FO, "color"): "#1a1a1a",
    })
    _add_p_style("P_Footer", {
        _q(_NS_FO, "text-align"): "end",
        _q(_NS_FO, "margin-top"): "0.25cm",
    }, {
        _q(_NS_FO, "font-size"): "7.5pt",
        _q(_NS_FO, "color"): "#777777",
    })

    # Estilos de tabela e célula
    _add_table_style("T_Full")
    _add_cell_style("C_Normal", bg="#ffffff")
    _add_cell_style("C_Alt", bg="#f8f5f1")
    _add_cell_style("C_Head", bg="#f2e4e4")
    _add_cell_style("C_Box", bg="#faf8f5", pad="0.10cm")

    col_style_cache: dict[str, str] = {}

    def _get_col_style(width_cm: float) -> str:
        key = f"{width_cm:.3f}"
        if key not in col_style_cache:
            st_name = f"Col_{len(col_style_cache) + 1}"
            _add_col_style(st_name, width_cm)
            col_style_cache[key] = st_name
        return col_style_cache[key]

    body = ET.SubElement(content_doc, _q(_NS_OFFICE, "body"))
    text_body = ET.SubElement(body, _q(_NS_OFFICE, "text"))

    def _p(parent, texto: object, style: str = "P_Small"):
        el = ET.SubElement(parent, _q(_NS_TEXT, "p"), {_q(_NS_TEXT, "style-name"): style})
        el.text = "" if texto is None else str(texto)
        return el

    def _section(titulo: str):
        _p(text_body, titulo.upper(), "P_Section")

    def _new_table(name: str, col_widths: list[float]):
        tbl = ET.SubElement(text_body, _q(_NS_TABLE, "table"), {
            _q(_NS_TABLE, "name"): name,
            _q(_NS_TABLE, "style-name"): "T_Full",
        })
        for w in col_widths:
            ET.SubElement(tbl, _q(_NS_TABLE, "table-column"), {
                _q(_NS_TABLE, "style-name"): _get_col_style(w),
            })
        return tbl

    def _add_row(tbl, cells: list[tuple[str, str, str]]):
        """cells: lista de (texto, cell_style, p_style)."""
        row = ET.SubElement(tbl, _q(_NS_TABLE, "table-row"))
        for texto, c_style, p_style in cells:
            cell = ET.SubElement(row, _q(_NS_TABLE, "table-cell"), {
                _q(_NS_TABLE, "style-name"): c_style,
                _q(_NS_OFFICE, "value-type"): "string",
            })
            for linha in (texto or "").split("\n"):
                _p(cell, linha, p_style)
        return row

    def _add_kv_row(tbl, pairs: list[tuple[str, str]]):
        row = ET.SubElement(tbl, _q(_NS_TABLE, "table-row"))
        for label, valor in pairs:
            cell = ET.SubElement(row, _q(_NS_TABLE, "table-cell"), {
                _q(_NS_TABLE, "style-name"): "C_Box",
                _q(_NS_OFFICE, "value-type"): "string",
            })
            _p(cell, label.upper(), "P_Label")
            _p(cell, valor or "—", "P_ValueBold")

    # ── TÍTULO & CABEÇALHO ──
    nivel_total = max(1, int(ficha.cabecalho.nivel_total or 1))
    metade_nivel = math.floor(nivel_total / 2)
    bonus_treino_nivel = 2 if nivel_total <= 6 else (4 if nivel_total <= 14 else 6)

    nome_char = ficha.cabecalho.nome or "Personagem sem Nome"
    _p(text_body, nome_char, "P_Title")
    _p(
        text_body,
        f"Tormenta20 (Jogo do Ano) • Jogador: {ficha.cabecalho.jogador or '—'} • Nível Total: {nivel_total} • XP: {ficha.cabecalho.xp.atual}",
        "P_Subtitle",
    )

    tam_raw = getattr(ficha.descricao.tamanho, "value", ficha.descricao.tamanho) or "Médio"
    tbl_cab = _new_table("Cabecalho", [4.65, 4.65, 4.65, 4.65])
    _add_kv_row(tbl_cab, [
        ("Raça", ficha.cabecalho.raca or "—"),
        ("Origem", ficha.cabecalho.origem or "—"),
        ("Classe / Nível", _formatar_classes(ficha)),
        ("Divindade", ficha.cabecalho.deus or "—"),
    ])
    prof_raw = ficha.status.proficiencias
    prof_str = ", ".join(prof_raw) if isinstance(prof_raw, list) else (str(prof_raw) if prof_raw else "—")
    _add_kv_row(tbl_cab, [
        ("Tamanho", str(tam_raw)),
        ("Deslocamento", f"{ficha.status.deslocamento}m"),
        ("Penalidade Armadura", str(int(ficha.status.penalidade_armadura or 0))),
        ("Proficiências", prof_str or "—"),
    ])

    # ── ATRIBUTOS ──
    _section("Atributos")
    tbl_attr = _new_table("Atributos", [3.1, 3.1, 3.1, 3.1, 3.1, 3.1])
    row_attr = ET.SubElement(tbl_attr, _q(_NS_TABLE, "table-row"))
    for label, attr in [
        ("FORÇA", "forca"),
        ("DESTREZA", "destreza"),
        ("CONSTITUIÇÃO", "constituicao"),
        ("INTELIGÊNCIA", "inteligencia"),
        ("SABEDORIA", "sabedoria"),
        ("CARISMA", "carisma"),
    ]:
        val = int(getattr(ficha.atributos, attr) or 0)
        cell = ET.SubElement(row_attr, _q(_NS_TABLE, "table-cell"), {
            _q(_NS_TABLE, "style-name"): "C_Box",
            _q(_NS_OFFICE, "value-type"): "string",
        })
        _p(cell, label, "P_LabelCenter")
        _p(cell, _fmt_mod(val), "P_AttrBig")

    # ── COMBATE & STATUS ──
    _section("Combate & Status")
    armadura_nome = "—"
    b_arm = 0
    escudo_nome = "—"
    b_esc = 0
    usa_pesada = False
    for it in (ficha.inventario.equipamentos or []):
        if not it.equipado:
            continue
        dados_arm = DADOS_ARMADURAS.get(it.nome)
        if not dados_arm:
            continue
        tipo_arm = dados_arm.get("tipo_armadura")
        if tipo_arm in ("Leve", "Pesada") and armadura_nome == "—":
            armadura_nome = it.nome
            b_arm = int(dados_arm.get("bonus_defesa", 0) or 0)
            usa_pesada = tipo_arm == "Pesada"
        elif tipo_arm == "Escudo" and escudo_nome == "—":
            escudo_nome = it.nome
            b_esc = int(dados_arm.get("bonus_defesa", 0) or 0)

    mod_des = calcular_modificador(ficha.atributos.destreza)
    defesa_total = int(ficha.status.defesa.total or 10)
    des_na_ca = 0 if usa_pesada else mod_des
    outros_ca = defesa_total - 10 - des_na_ca - b_arm - b_esc

    tbl_status = _new_table("Status", [3.7, 3.7, 3.7, 7.5])
    _add_kv_row(tbl_status, [
        ("Pontos de Vida (PV)", f"{ficha.status.pv.atual} / {ficha.status.pv.maximo}"),
        ("Pontos de Mana (PM)", f"{ficha.status.pm.atual} / {ficha.status.pm.maximo}"),
        ("Defesa (CA)", str(defesa_total)),
        (
            "Composição da Defesa",
            f"10 + DES ({_fmt_mod(des_na_ca)}) + Armadura ({b_arm}: {armadura_nome}) + Escudo ({b_esc}: {escudo_nome}) + Outros ({_fmt_mod(outros_ca)})",
        ),
    ])

    # ── ATAQUES ──
    if ficha.combate.ataques:
        _section("Ataques")
        tbl_atq = _new_table("Ataques", [5.2, 2.2, 3.2, 2.4, 2.8, 2.8])
        _add_row(tbl_atq, [
            ("Ataque", "C_Head", "P_ThLeft"),
            ("Teste", "C_Head", "P_ThCenter"),
            ("Dano", "C_Head", "P_ThCenter"),
            ("Crítico", "C_Head", "P_ThCenter"),
            ("Tipo", "C_Head", "P_ThCenter"),
            ("Alcance", "C_Head", "P_ThCenter"),
        ])
        for idx, atq in enumerate(ficha.combate.ataques):
            cs = "C_Alt" if idx % 2 else "C_Normal"
            _add_row(tbl_atq, [
                (atq.nome or "—", cs, "P_ValueBold"),
                (atq.bonus_ataque or "—", cs, "P_Center"),
                (atq.dano or "—", cs, "P_Center"),
                (atq.critico or "—", cs, "P_Center"),
                (atq.tipo or "—", cs, "P_Center"),
                (atq.alcance or "—", cs, "P_Center"),
            ])

    # ── PERÍCIAS (TABELA COMPACTA EM 2 BLOCOS LADO A LADO) ──
    _section(f"Perícias (1/2 Nível: +{metade_nivel} • Bônus de Treino: +{bonus_treino_nivel})")
    nomes_pericias = sorted(
        set(DADOS_PERICIAS.keys()) | set((ficha.pericias or {}).keys()),
        key=lambda x: x.lower(),
    )
    # Remove "Ofício" genérico se houver ofícios específicos na ficha
    if any(k.startswith("Ofício (") for k in nomes_pericias) and "Ofício" in nomes_pericias:
        nomes_pericias.remove("Ofício")

    linhas_per: list[tuple[str, str, str, str]] = []
    for nome_p in nomes_pericias:
        per = ficha.pericias.get(nome_p)
        meta_p = DADOS_PERICIAS.get(nome_p, {})
        attr_key = (getattr(per, "atributo_usado", None) or meta_p.get("atributo") or "int").lower()
        attr_lbl = _ATTR_SHORT.get(attr_key, "INT")
        treinado = bool(per and per.treino and per.treino > 0)
        if per is not None:
            total_p = int(per.total or 0)
        else:
            attr_map = {"FOR": "forca", "DES": "destreza", "CON": "constituicao", "INT": "inteligencia", "SAB": "sabedoria", "CAR": "carisma"}
            total_p = metade_nivel + int(getattr(ficha.atributos, attr_map[attr_lbl]) or 0)
        linhas_per.append(("✓" if treinado else "", nome_p, attr_lbl, _fmt_mod(total_p)))

    meio = math.ceil(len(linhas_per) / 2)
    esq = linhas_per[:meio]
    dir_ = linhas_per[meio:]

    tbl_per = _new_table("Pericias", [0.8, 5.2, 1.5, 1.8, 0.8, 5.2, 1.5, 1.8])
    _add_row(tbl_per, [
        ("Tr", "C_Head", "P_ThCenter"),
        ("Perícia", "C_Head", "P_ThLeft"),
        ("Atrib.", "C_Head", "P_ThCenter"),
        ("Total", "C_Head", "P_ThCenter"),
        ("Tr", "C_Head", "P_ThCenter"),
        ("Perícia", "C_Head", "P_ThLeft"),
        ("Atrib.", "C_Head", "P_ThCenter"),
        ("Total", "C_Head", "P_ThCenter"),
    ])
    for i in range(meio):
        cs = "C_Alt" if i % 2 else "C_Normal"
        l_tr, l_nm, l_at, l_tot = esq[i]
        if i < len(dir_):
            r_tr, r_nm, r_at, r_tot = dir_[i]
        else:
            r_tr, r_nm, r_at, r_tot = "", "", "", ""
        _add_row(tbl_per, [
            (l_tr, cs, "P_CenterBold"),
            (l_nm, cs, "P_ValueBold" if l_tr else "P_Value"),
            (l_at, cs, "P_Center"),
            (l_tot, cs, "P_CenterBold"),
            (r_tr, cs, "P_CenterBold"),
            (r_nm, cs, "P_ValueBold" if r_tr else "P_Value"),
            (r_at, cs, "P_Center"),
            (r_tot, cs, "P_CenterBold"),
        ])

    # ── HABILIDADES & PODERES ──
    habs_raca_origem = [
        h for h in (ficha.habilidades or [])
        if h.tipo and any(t in h.tipo.lower() for t in ["racial", "origem"])
    ]
    habs_outras = [
        h for h in (ficha.habilidades or [])
        if not (h.tipo and any(t in h.tipo.lower() for t in ["racial", "origem"]))
    ]

    if habs_raca_origem:
        _section("Habilidades de Raça & Origem")
        for h in habs_raca_origem:
            _p(text_body, f"• {h.nome} ({h.tipo})", "P_ItemTitle")
            if h.descricao:
                _p(text_body, h.descricao, "P_Small")

    if habs_outras:
        _section("Habilidades de Classe & Poderes")
        for h in habs_outras:
            tipo_lbl = f" ({h.tipo})" if h.tipo else ""
            _p(text_body, f"• {h.nome}{tipo_lbl}", "P_ItemTitle")
            if h.descricao:
                _p(text_body, h.descricao, "P_Small")

    # ── MAGIAS ──
    if ficha.combate.magias:
        attr_magia = obter_atributo_chave_magia(ficha) or "inteligencia"
        mod_magia = int(getattr(ficha.atributos, attr_magia) or 0)
        cd_magia = ficha.combate.cd_magias or (10 + metade_nivel + mod_magia)
        limite_pm = calcular_limite_pm_magia(ficha)
        _section(
            f"Grimório & Magias (Atributo: {_ATTR_SHORT.get(attr_magia, 'INT')} {_fmt_mod(mod_magia)} • CD: {cd_magia} • Limite: {limite_pm} PM)"
        )
        for m in ficha.combate.magias:
            _p(text_body, f"• {m.nome} — {m.circulo}º Círculo ({m.custo_pm} PM)", "P_ItemTitle")
            _p(
                text_body,
                f"{m.tipo} • {m.escola} | Execução: {m.execucao} | Alcance: {m.alcance} | Alvo: {m.alvo or '—'} | Duração: {m.duracao} | Resistência: {m.resistencia or '—'}",
                "P_SmallMuted",
            )
            if m.descricao:
                _p(text_body, m.descricao, "P_Small")
            for ap in (m.aprimoramentos or []):
                c = ap.get("custo", "") if isinstance(ap, dict) else getattr(ap, "custo", "")
                d = ap.get("descricao", "") if isinstance(ap, dict) else getattr(ap, "descricao", "")
                _p(text_body, f"    {c}: {d}", "P_SmallMuted")

    # ── EQUIPAMENTO & DINHEIRO ──
    _section("Equipamento, Dinheiro & Carga")
    carga_max = int(ficha.inventario.carga_maxima or 0)
    tbl_din = _new_table("Dinheiro", [4.65, 4.65, 4.65, 4.65])
    _add_kv_row(tbl_din, [
        ("Tibar (T$)", str(ficha.inventario.dinheiro.tp)),
        ("Tibar de Ouro (TO)", str(ficha.inventario.dinheiro.to)),
        ("Carga Atual / Máx.", f"{ficha.inventario.carga_total} / {carga_max} espaços"),
        ("Levantar (Máx. ×2)", f"{carga_max * 2} espaços"),
    ])

    if ficha.inventario.equipamentos:
        tbl_eq = _new_table("Equipamentos", [11.6, 2.0, 2.5, 2.5])
        _add_row(tbl_eq, [
            ("Item", "C_Head", "P_ThLeft"),
            ("Qtd", "C_Head", "P_ThCenter"),
            ("Espaço", "C_Head", "P_ThCenter"),
            ("Equipado", "C_Head", "P_ThCenter"),
        ])
        for idx, it in enumerate(ficha.inventario.equipamentos):
            cs = "C_Alt" if idx % 2 else "C_Normal"
            peso = (it.espaco or 0) * (it.qtd or 1)
            peso_str = str(int(peso) if float(peso).is_integer() else peso)
            _add_row(tbl_eq, [
                (it.nome or "—", cs, "P_Value"),
                (str(it.qtd or 1), cs, "P_Center"),
                (peso_str, cs, "P_Center"),
                ("Sim" if it.equipado else "Não", cs, "P_Center"),
            ])

    # ── DESCRIÇÃO & ANOTAÇÕES ──
    desc = ficha.descricao
    blocos_desc = []
    if desc.idade or desc.alinhamento:
        partes_meta = []
        if desc.idade:
            faixa = f" ({desc.faixa_etaria})" if desc.faixa_etaria else ""
            partes_meta.append(f"Idade: {desc.idade}{faixa}")
        if desc.alinhamento:
            partes_meta.append(f"Alinhamento: {desc.alinhamento}")
        blocos_desc.append(("Dados Pessoais", " | ".join(partes_meta)))
    if desc.aparencia:
        blocos_desc.append(("Aparência", desc.aparencia))
    if desc.personalidade:
        blocos_desc.append(("Personalidade", desc.personalidade))
    if desc.historia:
        blocos_desc.append(("História", desc.historia))
    if desc.anotacoes:
        blocos_desc.append(("Anotações", desc.anotacoes))

    if blocos_desc:
        _section("Descrição & Anotações")
        for titulo_b, texto_b in blocos_desc:
            _p(text_body, titulo_b, "P_ItemTitle")
            for linha in texto_b.split("\n"):
                _p(text_body, linha, "P_Small")

    _p(text_body, f"Gerado pelo T20 System em {datetime.now().strftime('%d/%m/%Y')}", "P_Footer")

    content_xml = ET.tostring(content_doc, encoding="utf-8", xml_declaration=True)

    # ── 5. Empacotamento ZIP ODF 1.2 ──
    output = BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("mimetype", ODT_MIMETYPE.encode("ascii"), compress_type=zipfile.ZIP_STORED)
        zf.writestr("META-INF/manifest.xml", manifest_xml)
        zf.writestr("meta.xml", meta_xml)
        zf.writestr("styles.xml", styles_xml)
        zf.writestr("content.xml", content_xml)

    return output.getvalue()
