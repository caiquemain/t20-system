from fastapi import APIRouter, HTTPException, Response, Depends
from io import BytesIO
import logging
from pypdf import PdfReader, PdfWriter
from bson import ObjectId

from ..models import Personagem
from ..dependencies import get_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/personagens", tags=["PDF"])

SKILL_FIELDS = {
    'Acrobacia': '013', 'Adestramento': '023', 'Atletismo': '033',
    'Atuação': '043', 'Cavalgar': '053', 'Conhecimento': '063',
    'Cura': '073', 'Diplomacia': '083', 'Enganação': '093',
    'Fortitude': '103', 'Furtividade': '113', 'Guerra': '123',
    'Iniciativa': '133', 'Intimidação': '143', 'Intuição': '153',
    'Investigação': '163', 'Ladinagem': '183', 'Luta': '193',
    'Misticismo': '203', 'Pilotagem': '213', 'Nobreza': '223',
    'Percepção': '253', 'Pontaria': '263', 'Reflexos': '273',
    'Religião': '283', 'Sobrevivência': '293', 'Vontade': '303'
}

@router.get("/{personagem_id}/pdf")
async def gerar_pdf(personagem_id: str, db = Depends(get_db)):
    """Gera PDF da ficha de personagem preenchida."""
    try:
        try:
            oid = ObjectId(personagem_id)
        except Exception:
            raise HTTPException(status_code=404, detail="ID inválido")
        personagem_doc = await db.personagens.find_one({"_id": oid})
        if not personagem_doc:
            raise HTTPException(status_code=404, detail="Personagem não encontrado")
        
        personagem = Personagem(**personagem_doc)
        
        # Carregar template
        template_path = "/app/assets/ficha-t20-template.pdf"
        reader = PdfReader(template_path)
        writer = PdfWriter()
        
        # ✅ COPIA TUDO (páginas + AcroForm + metadados)
        writer.append(reader)
        
        fields_to_fill = {}
        
        # CABEÇALHO
        fields_to_fill["NOME DO PERSONAGEM"] = personagem.cabecalho.nome
        fields_to_fill["JOGADOR"] = personagem.cabecalho.jogador
        fields_to_fill["RAÇA"] = personagem.cabecalho.raca
        fields_to_fill["ORIGEM"] = personagem.cabecalho.origem
        fields_to_fill["CLASSE"] = personagem.classes[0].nome if personagem.classes else ""
        fields_to_fill["Lv"] = str(personagem.cabecalho.nivel_total)
        fields_to_fill["DIVINDADE"] = personagem.cabecalho.deus
        
        # ATRIBUTOS
        fields_to_fill["For"] = str(personagem.atributos.forca)
        fields_to_fill["Des"] = str(personagem.atributos.destreza)
        fields_to_fill["Con"] = str(personagem.atributos.constituicao)
        fields_to_fill["Int"] = str(personagem.atributos.inteligencia)
        fields_to_fill["Sab"] = str(personagem.atributos.sabedoria)
        fields_to_fill["Car"] = str(personagem.atributos.carisma)
        
        # STATUS
        fields_to_fill["PVs Totais"] = str(personagem.status.pv.maximo)
        fields_to_fill["PMs Totais"] = str(personagem.status.pm.maximo)
        fields_to_fill["CA"] = str(personagem.status.defesa.total)
        fields_to_fill["Desloc"] = str(personagem.status.deslocamento)
        fields_to_fill["Exp"] = str(personagem.cabecalho.xp.atual)
        
        # PERÍCIAS
        for nome_pericia, campo_pdf in SKILL_FIELDS.items():
            pericia = personagem.pericias.get(nome_pericia)
            if pericia:
                fields_to_fill[campo_pdf] = str(pericia.total)
        
        # ATAQUES
        for i, ataque in enumerate(personagem.combate.ataques[:5], 1):
            fields_to_fill[f"Ataque {i}"] = ataque.nome
            fields_to_fill[f"Bônus Atq {i}"] = ataque.bonus_ataque
            fields_to_fill[f"Dano {i}"] = ataque.dano
            fields_to_fill[f"Crítico {i}"] = ataque.critico
            fields_to_fill[f"Tipo {i}"] = ataque.tipo
            fields_to_fill[f"Alcance {i}"] = ataque.alcance
        
        # EQUIPAMENTO
        for i, item in enumerate(personagem.inventario.equipamentos[:15], 1):
            fields_to_fill[f"Item{i}"] = item.nome
            fields_to_fill[f"PesoItem{i}"] = str(item.espaco * item.qtd)
        
        fields_to_fill["CargaTotal"] = str(personagem.inventario.carga_total)
        fields_to_fill["CargaMax"] = str(personagem.inventario.carga_maxima)
        
        # HABILIDADES
        habs_raca_origem = "\n".join([
            f"• {h.nome}: {h.descricao}"
            for h in personagem.habilidades
            if h.tipo in ['racial', 'origem']
        ])
        habs_classe = "\n".join([
            f"• {h.nome}: {h.descricao}"
            for h in personagem.habilidades
            if h.tipo == 'classe'
        ])
        magias = "\n".join([
            f"• {m.nome} ({m.circulo}º): {m.descricao[:100]}..."
            for m in personagem.combate.magias
        ])
        
        fields_to_fill["HabRaçasOrigem"] = habs_raca_origem
        fields_to_fill["HabClassePoderes"] = habs_classe
        fields_to_fill["Magias"] = magias
        fields_to_fill["Anotações"] = personagem.descricao.anotacoes or personagem.descricao.historia or ""
        
        # ✅ Preencher campos (agora com AcroForm presente)
        for page in writer.pages:
            try:
                writer.update_page_form_field_values(page, fields_to_fill, auto_regenerate=False)
            except Exception as e:
                logger.debug(f"Página sem campos: {e}")
        
        # Gerar PDF
        output = BytesIO()
        writer.write(output)
        output.seek(0)
        
        return Response(
            content=output.read(),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=ficha-{personagem.cabecalho.nome or 'personagem'}.pdf"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao gerar PDF: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro ao gerar PDF: {str(e)}")
