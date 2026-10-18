from fastapi import APIRouter, HTTPException, Response, Depends
from io import BytesIO
import logging
import os
import unicodedata
import fitz  # PyMuPDF
from bson import ObjectId

from ..models import Personagem
from ..dependencies import get_db
from ..regras.atributos import (
    aplicar_bonus_atributos_raciais, 
    calcular_atributos_finais, 
    aplicar_escolhas_atributos_raciais
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/personagens", tags=["PDF"])

# Prefixos base de cada perícia no PDF (x0=Total, x1=1/2 Nível, x3=Mod Atributo, x4=Outros)
SKILL_PREFIXES = {
    'Acrobacia': '01', 'Adestramento': '02', 'Atletismo': '03',
    'Atuação': '04', 'Cavalgar': '05', 'Conhecimento': '06',
    'Cura': '07', 'Diplomacia': '08', 'Enganação': '09',
    'Fortitude': '10', 'Furtividade': '11', 'Guerra': '12',
    'Iniciativa': '13', 'Intimidação': '14', 'Intuição': '15',
    'Investigação': '16', 'Jogatina': '17', 'Ladinagem': '18',
    'Luta': '19', 'Misticismo': '20', 'Pilotagem': '21',
    'Nobreza': '22', 'Ofício 1': '23', 'Ofício 2': '24',
    'Percepção': '25', 'Pontaria': '26', 'Reflexos': '27',
    'Religião': '28', 'Sobrevivência': '29', 'Vontade': '30'
}

TRAINED_FIELDS = {
    'Acrobacia': 'Mar Trei acro', 'Adestramento': 'Mar Trei ades',
    'Atletismo': 'Mar Trei atle', 'Atuação': 'Mar Trei atua',
    'Cavalgar': 'Mar Trei caval', 'Conhecimento': 'Mar Trei conhe',
    'Cura': 'Mar Trei cura', 'Diplomacia': 'Mar Trei dipl',
    'Enganação': 'Mar Trei enga', 'Fortitude': 'Mar Trei forti',
    'Furtividade': 'Mar Trei furti', 'Guerra': 'Mar Trei guerra',
    'Iniciativa': 'Mar Trei ini', 'Intimidação': 'Mar Trei inti',
    'Intuição': 'Mar Trei intu', 'Investigação': 'Mar Trei inve',
    'Jogatina': 'Mar Trei joga', 'Ladinagem': 'Mar Trei ladi',
    'Luta': 'Mar Trei luta', 'Misticismo': 'Mar Trei misti',
    'Pilotagem': 'Mar Trei pilo', 'Nobreza': 'Mar Trei nobre',
    'Ofício 1': 'Mar Trei ofi1', 'Ofício 2': 'Mar Trei ofi2',
    'Percepção': 'Mar Trei perce', 'Pontaria': 'Mar Trei ponta',
    'Reflexos': 'Mar Trei refle', 'Religião': 'Mar Trei reli',
    'Sobrevivência': 'Mar Trei sobre', 'Vontade': 'Mar Trei vonta'
}

@router.get("/{personagem_id}/pdf")
async def gerar_pdf(personagem_id: str, db = Depends(get_db)):
    """Gera PDF da ficha de personagem preenchida usando PyMuPDF."""
    try:
        try:
            oid = ObjectId(personagem_id)
        except Exception:
            raise HTTPException(status_code=404, detail="ID inválido")
            
        personagem_doc = await db.personagens.find_one({"_id": oid})
        if not personagem_doc:
            raise HTTPException(status_code=404, detail="Personagem não encontrado")
        
        personagem = Personagem(**personagem_doc)
        
        # 1. RECALCULAR ATRIBUTOS
        try:
            from ..dados_racas import DADOS_RACAS
            def normalizar(txt):
                if not txt: return ""
                return unicodedata.normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII').lower()

            raca_original = personagem.cabecalho.raca
            raca_normalizada = normalizar(raca_original)
            for chave in DADOS_RACAS.keys():
                if normalizar(chave) == raca_normalizada:
                    personagem.cabecalho.raca = chave
                    break

            aplicar_bonus_atributos_raciais(personagem)
            calcular_atributos_finais(personagem)
            aplicar_escolhas_atributos_raciais(personagem)
            personagem.cabecalho.raca = raca_original
        except Exception as e:
            logger.warning(f"Não foi possível recalcular os atributos: {e}")

        # 2. CARREGAR TEMPLATE
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        template_path = os.path.join(base_dir, "assets", "ficha-t20-template.pdf")
        doc = fitz.open(template_path)
        
        def safe_str(val):
            return str(val) if val is not None else ""

        def format_mod(val):
            if val is None: return "+0"
            return f"+{val}" if val > 0 else str(val)

        fields_to_fill = {}
        
        # CABEÇALHO
        fields_to_fill["NOME DO PERSONAGEM"] = safe_str(personagem.cabecalho.nome)
        fields_to_fill["JOGADOR"] = safe_str(personagem.cabecalho.jogador)
        fields_to_fill["RAÇA"] = safe_str(personagem.cabecalho.raca)
        fields_to_fill["ORIGEM"] = safe_str(personagem.cabecalho.origem)
        fields_to_fill["CLASSE"] = safe_str(personagem.classes[0].nome) if personagem.classes else ""
        fields_to_fill["Lv"] = safe_str(personagem.cabecalho.nivel_total)
        fields_to_fill["DIVINDADE"] = safe_str(personagem.cabecalho.deus)
        
        # ATRIBUTOS (Converter Modificador para Valor)
        # O template do PDF usa a fórmula mod = (valor - 10) / 2, então precisamos converter de volta para o valor.
        campos_atributos = [
            ('forca', 'For'),
            ('destreza', 'Des'),
            ('constituicao', 'Con'),
            ('inteligencia', 'Int'),
            ('sabedoria', 'Sab'),
            ('carisma', 'Car')
        ]
        for attr, field_total in campos_atributos:
            modifier = getattr(personagem.atributos, attr) or 0
            val = 10 + (2 * modifier)
            fields_to_fill[field_total] = safe_str(val)
        
        # STATUS
        fields_to_fill["PVs Totais"] = safe_str(personagem.status.pv.maximo)
        fields_to_fill["PVs Atuais"] = safe_str(personagem.status.pv.atual)
        fields_to_fill["PMs Totais"] = safe_str(personagem.status.pm.maximo)
        fields_to_fill["PMs Atuais"] = safe_str(personagem.status.pm.atual)
        fields_to_fill["CA"] = safe_str(personagem.status.defesa.total)
        fields_to_fill["Desloc"] = safe_str(personagem.status.deslocamento)
        fields_to_fill["Exp"] = safe_str(personagem.cabecalho.xp.atual)
        
        # PERÍCIAS
        for nome_pericia, prefixo in SKILL_PREFIXES.items():
            p_nome = 'Ofício' if nome_pericia.startswith('Ofício') and 'Ofício' in personagem.pericias else nome_pericia
            pericia = personagem.pericias.get(p_nome)
            if pericia:
                # Somar os bônus automáticos condicionais (ex: Conhecimento das Rochas)
                outros = (pericia.outros or 0) + (pericia.bonus_automatico or 0)
                if outros != 0:
                    fields_to_fill[f"{prefixo}4"] = format_mod(outros)
                
                # Checkbox de Treinado
                if pericia.treino > 0:
                    fields_to_fill[TRAINED_FIELDS[nome_pericia]] = "/Yes"
                else:
                    fields_to_fill[TRAINED_FIELDS[nome_pericia]] = "/Off"
        
        # ATAQUES
        for i, ataque in enumerate(personagem.combate.ataques[:5], 1):
            fields_to_fill[f"Ataque {i}"] = safe_str(ataque.nome)
            fields_to_fill[f"Bônus Atq {i}"] = safe_str(ataque.bonus_ataque)
            fields_to_fill[f"Dano {i}"] = safe_str(ataque.dano)
            fields_to_fill[f"Crítico {i}"] = safe_str(ataque.critico)
            fields_to_fill[f"Tipo {i}"] = safe_str(ataque.tipo)
            fields_to_fill[f"Alcance {i}"] = safe_str(ataque.alcance)
        
        # EQUIPAMENTO
        for i, item in enumerate(personagem.inventario.equipamentos[:15], 1):
            fields_to_fill[f"Item{i}"] = safe_str(item.nome)
            fields_to_fill[f"PesoItem{i}"] = safe_str(item.espaco * item.qtd)
        
        fields_to_fill["CargaTotal"] = safe_str(personagem.inventario.carga_total)
        fields_to_fill["CargaMax"] = safe_str(personagem.inventario.carga_maxima)
        
        # HABILIDADES
        habs_raca_origem = "\n".join([
            f"• {h.nome}: {h.descricao}" 
            for h in personagem.habilidades 
            if h.tipo and any(t in h.tipo.lower() for t in ['racial', 'origem'])
        ])
        
        habs_classe = "\n".join([
            f"• {h.nome}: {h.descricao}" 
            for h in personagem.habilidades 
            if h.tipo and any(t in h.tipo.lower() for t in ['classe', 'poder', 'arcanista'])
        ])
        
        fields_to_fill["HabRaçasOrigem"] = habs_raca_origem[:3000]
        fields_to_fill["HabClassePoderes"] = habs_classe[:3000]
        
        # MAGIAS (Com todas as descrições e detalhes)
        magias_str = ""
        for m in personagem.combate.magias:
            magias_str += f"• {m.nome} ({m.circulo}º Círculo)\n"
            magias_str += f"Tipo: {m.tipo} | Escola: {m.escola} | Execução: {m.execucao}\n"
            magias_str += f"Alcance: {m.alcance} | Alvo: {m.alvo or m.alvo_area or '-'} | Duração: {m.duracao} | Resistência: {m.resistencia or '-'}\n"
            magias_str += f"Custo: {m.custo_pm} PM\n"
            magias_str += f"Descrição: {m.descricao}\n"
            if m.aprimoramentos:
                magias_str += "Aprimoramentos:\n"
                for ap in m.aprimoramentos:
                    # Trata tanto se for dicionário (vindo do Mongo) quanto objeto (Pydantic)
                    c = ap.get('custo', '') if isinstance(ap, dict) else getattr(ap, 'custo', '')
                    d = ap.get('descricao', '') if isinstance(ap, dict) else getattr(ap, 'descricao', '')
                    magias_str += f"  - {c}: {d}\n"
            magias_str += "\n"
            
        fields_to_fill["Magias"] = magias_str[:4000]
        fields_to_fill["Observação"] = safe_str(personagem.descricao.anotacoes or personagem.descricao.historia)[:3000]
        
        # 3. PREENCHER CAMPOS COM PYMUPDF
        for page in doc:
            for widget in page.widgets():
                if widget.field_name in fields_to_fill:
                    val = fields_to_fill[widget.field_name]
                    if val == "/Yes":
                        widget.field_value = True
                    elif val == "/Off":
                        widget.field_value = False
                    else:
                        widget.field_value = str(val)
                    widget.update()
        
        # 4. GERAR PDF
        output = BytesIO()
        doc.save(output, garbage=4, deflate=True)
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
