from ..models import Personagem, Habilidade, FonteBonus
from ..dados_familiares import FAMILIARES_ARCANOS
from ..dados_progressao_magias import MAPA_SUBCLASSE_PARA_CLASSE
from .status import calcular_pv_pm
from .utils import calcular_modificador
import logging

logger = logging.getLogger("RegrasT20")

def aplicar_poderes_arcanista(ficha: Personagem):
    """Processa todos os poderes de Arcanista e aplica efeitos."""
    logger.info("--- [8] Aplicando Poderes de Arcanista ---")
    
    # Verifica se é Arcanista
    classe_arcanista = None
    for c in ficha.classes:
        nome_classe = c.nome or ""
        nome_base = MAPA_SUBCLASSE_PARA_CLASSE.get(nome_classe, nome_classe)
        if nome_base == "Arcanista":
            classe_arcanista = c
            break
    
    if not classe_arcanista:
        return ficha
    
    subclasse = (classe_arcanista.subclasse or "").strip()
    
    # Reset de estados
    ficha.combate.custo_arcano_metade = False
    ficha.combate.fluxo_de_mana = False
    ficha.combate.foco_vital = False
    ficha.combate.reducao_pm_tipo = {}
    ficha.combate.bonus_dano_dado_tipo = {}
    
    # Determina atributo-chave
    if subclasse == "Feiticeiro":
        attr_chave = "carisma"
        mod_attr = calcular_modificador(ficha.atributos.carisma)
    else:  # Bruxo ou Mago
        attr_chave = "inteligencia"
        mod_attr = calcular_modificador(ficha.atributos.inteligencia)
    
    # Processa cada habilidade
    for hab in ficha.habilidades:
        nome = hab.nome
        efeitos = hab.efeitos or {}
        escolhas = hab.escolhas_aplicadas or {}
        
        # ═══════════════════════════════════════
        # PODERES DE ARCANISTA
        # ═══════════════════════════════════════
        
        # Alta Arcana (nível 20)
        if nome == "Alta Arcana" and classe_arcanista.nivel >= 20:
            ficha.combate.custo_arcano_metade = True
        
        # Arcano de Batalha
        elif nome == "Arcano de Batalha":
            ficha.combate.bonus_dano_magias += mod_attr
        
        # Aumento de Atributo
        elif nome == "Aumento de Atributo":
            attr_escolhido = escolhas.get("atributo")
            if attr_escolhido and attr_escolhido in ficha.atributos_calc:
                ficha.atributos_calc[attr_escolhido].adicionar_bonus(
                    fonte="Poder: Aumento de Atributo",
                    categoria="Poder",
                    valor=1
                )
        
        # Conhecimento Mágico
        elif nome == "Conhecimento Mágico":
            # Apenas marca que aprende 2 magias (lógica externa)
            pass
        
        # Especialista em Escola
        elif nome == "Especialista em Escola":
            escola = escolhas.get("escola")
            if escola:
                atual = ficha.combate.cd_por_escola.get(escola, 0)
                ficha.combate.cd_por_escola[escola] = atual + 2
        
        # Mestre em Escola
        elif nome == "Mestre em Escola":
            escola = escolhas.get("escola")
            if escola:
                ficha.combate.custo_por_escola[escola] = ficha.combate.custo_por_escola.get(escola, 0) - 1
        
        # Familiar
        elif nome == "Familiar":
            familiar_escolhido = escolhas.get("familiar")
            if familiar_escolhido and familiar_escolhido in FAMILIARES_ARCANOS:
                ben = FAMILIARES_ARCANOS[familiar_escolhido]
                
                # Injeta habilidade_ativavel se presente (Coruja/Corvo)
                if ben.get("habilidade_ativavel"):
                    if not isinstance(hab.efeitos, dict):
                        hab.efeitos = {}
                    hab.efeitos["habilidade_ativavel"] = ben["habilidade_ativavel"]
                
                # Sapo: soma mod_attr no PV
                if familiar_escolhido == "Sapo" and mod_attr > 0:
                    if ficha.status.pv_calc is None:
                        calcular_pv_pm(ficha)
                    ficha.status.pv_calc.adicionar_bonus(
                        fonte=f"Familiar: {familiar_escolhido}",
                        categoria="Poder",
                        valor=mod_attr
                    )
                    ficha.status.pv.maximo += mod_attr
                    if ficha.status.pv.atual > 0:
                        ficha.status.pv.atual += mod_attr
                
                # Borboleta: +1 CD Vontade
                elif familiar_escolhido == "Borboleta":
                    ficha.combate.cd_por_resistencia["Vontade"] = ficha.combate.cd_por_resistencia.get("Vontade", 0) + 1
                
                # Cobra: +1 CD Fortitude
                elif familiar_escolhido == "Cobra":
                    ficha.combate.cd_por_resistencia["Fortitude"] = ficha.combate.cd_por_resistencia.get("Fortitude", 0) + 1
                
                # Lagarto: +1 CD Reflexos
                elif familiar_escolhido == "Lagarto":
                    ficha.combate.cd_por_resistencia["Reflexos"] = ficha.combate.cd_por_resistencia.get("Reflexos", 0) + 1
                
                # Gato: Visão no Escuro + Furtividade
                elif familiar_escolhido == "Gato":
                    if "Visão no Escuro" not in ficha.status.sentidos:
                        ficha.status.sentidos.append("Visão no Escuro")
                
                # Falcão: Imunidades
                elif familiar_escolhido == "Falcão":
                    if "Não pode ser surpreendido" not in ficha.status.imunidades:
                        ficha.status.imunidades.append("Não pode ser surpreendido")
                    if "Nunca fica desprevenido" not in ficha.status.imunidades:
                        ficha.status.imunidades.append("Nunca fica desprevenido")
                
                # Morcego: Percepção às cegas
                elif familiar_escolhido == "Morcego":
                    if "Percepção às cegas (curto)" not in ficha.status.sentidos:
                        ficha.status.sentidos.append("Percepção às cegas (curto)")
        
        # Fortalecimento Arcano
        elif nome == "Fortalecimento Arcano":
            bonus = 2 if ficha.combate.circulo_maximo >= 4 else 1
            ficha.combate.cd_magias += bonus
        
        # Poder Mágico
        elif nome == "Poder Mágico":
            bonus_pm = classe_arcanista.nivel
            if ficha.status.pm_calc is None:
                calcular_pv_pm(ficha)
            ficha.status.pm_calc.adicionar_bonus(
                fonte="Poder Mágico",
                categoria="Poder",
                valor=bonus_pm
            )
            ficha.status.pm.maximo += bonus_pm
            if ficha.status.pm.atual > 0:
                ficha.status.pm.atual += bonus_pm
        
        # Fluxo de Mana
        elif nome == "Fluxo de Mana":
            ficha.combate.fluxo_de_mana = True
        
        # Foco Vital
        elif nome == "Foco Vital":
            ficha.combate.foco_vital = True
        
        # Magia Pungente
        elif nome == "Magia Pungente":
            if not isinstance(hab.efeitos, dict):
                hab.efeitos = {}
            hab.efeitos["habilidade_ativavel"] = {
                "custo": 1,
                "acao": "Livre",
                "alcance": "Pessoal",
                "duracao": "Cena",
                "efeito": "+2 CD na próxima magia",
                "modificadores": [{"atributo": "cd_magias", "valor": 2}]
            }
        
        # Raio Arcano
        elif nome == "Raio Arcano":
            circulo = ficha.combate.circulo_maximo
            dado_base = "1d8"
            dado_bonus = f"+{circulo - 1}d8" if circulo > 1 else ""
            dano_total = f"{dado_base}{dado_bonus}"
            
            # Adiciona como ataque
            from ..models import Ataque
            ataque = Ataque(
                nome="Raio Arcano",
                bonus_ataque=f"+{mod_attr}",
                dano=dano_total,
                critico="x2",
                tipo="Essência",
                alcance="Curto",
                teste="Reflexos",
                especial="Reflexos reduz à metade"
            )
            ficha.combate.ataques.append(ataque)
        
        # Raio Poderoso
        elif nome == "Raio Poderoso":
            # Remove Raio Arcano antigo e adiciona versão melhorada
            ficha.combate.ataques = [a for a in ficha.combate.ataques if a.nome != "Raio Arcano"]
            circulo = ficha.combate.circulo_maximo
            dado_base = "1d12"
            dado_bonus = f"+{circulo - 1}d12" if circulo > 1 else ""
            dano_total = f"{dado_base}{dado_bonus}"
            
            from ..models import Ataque
            ataque = Ataque(
                nome="Raio Arcano",
                bonus_ataque=f"+{mod_attr}",
                dano=dano_total,
                critico="x2",
                tipo="Essência",
                alcance="Médio",
                teste="Reflexos",
                especial="Reflexos reduz à metade"
            )
            ficha.combate.ataques.append(ataque)
        
        # Raio Elemental
        elif nome == "Raio Elemental":
            # Marca que Raio Arcano pode causar dano elemental
            pass
    
    # Alta Arcana é habilidade de classe AUTOMÁTICA no 20º nível
    if classe_arcanista.nivel >= 20:
        ficha.combate.custo_arcano_metade = True

    # ── CD de magias: PILHA transparente (base 10 + Fortalecimento + Pungente) ──
    from ..models import StatCalculado as _SCcd
    cd_calc = _SCcd(base=10, total=10)
    if any(h.nome == "Fortalecimento Arcano" for h in ficha.habilidades):
        cd_calc.adicionar_bonus(
            fonte="Poder: Fortalecimento Arcano", categoria="Poder",
            valor=2 if (ficha.combate.circulo_maximo or 0) >= 4 else 1)
    for b in ficha.status.buffs:
        if b.origem == "Magia Pungente" and b.atributo == "cd_magias":
            cd_calc.adicionar_bonus(
                fonte="Magia Pungente (ativa)", categoria="Poder", valor=b.valor)
    ficha.combate.cd_magias_calc = cd_calc
    ficha.combate.cd_magias = cd_calc.total

    # ═══════════════════════════════════════
    # LINHAGENS DO FEITICEIRO
    # ═══════════════════════════════════════
    
    if subclasse == "Feiticeiro":
        linhagem_draconica = any(h.nome == "Linhagem Dracônica" for h in ficha.habilidades)
        linhagem_feerica = any(h.nome == "Linhagem Feérica" for h in ficha.habilidades)
        heranca_aprimorada = any(h.nome == "Herança Aprimorada" for h in ficha.habilidades)
        heranca_superior = any(h.nome == "Herança Superior" for h in ficha.habilidades)
        
        # Linhagem Dracônica
        if linhagem_draconica:
            # Pega tipo de dano das escolhas
            tipo_dano = None
            for hab in ficha.habilidades:
                if hab.nome == "Linhagem Dracônica":
                    tipo_dano = (hab.escolhas_aplicadas or {}).get("tipo_dano")
                    break
            
            # Básica: +CAR no PV inicial + RD 5
            mod_car = calcular_modificador(ficha.atributos.carisma)
            if mod_car > 0:
                if ficha.status.pv_calc is None:
                    calcular_pv_pm(ficha)
                ficha.status.pv_calc.adicionar_bonus(
                    fonte="Linhagem Dracônica (básica)",
                    categoria="Poder",
                    valor=mod_car
                )
                ficha.status.pv.maximo += mod_car
                if ficha.status.pv.atual > 0:
                    ficha.status.pv.atual += mod_car
            
            if tipo_dano:
                rd_str = f"{tipo_dano} 5"
                if rd_str not in ficha.status.rd:
                    ficha.status.rd.append(rd_str)
            
            # Aprimorada/Superior: -1 PM e +1 dano por dado
            if heranca_aprimorada and tipo_dano:
                ficha.combate.reducao_pm_tipo[tipo_dano] = ficha.combate.reducao_pm_tipo.get(tipo_dano, 0) + 1
                ficha.combate.bonus_dano_dado_tipo[tipo_dano] = ficha.combate.bonus_dano_dado_tipo.get(tipo_dano, 0) + 1
            
            # Superior: imunidade ao tipo
            if heranca_superior and tipo_dano:
                imunidade_str = f"Imune a {tipo_dano}"
                if imunidade_str not in ficha.status.imunidades:
                    ficha.status.imunidades.append(imunidade_str)
        
        # Linhagem Feérica
        if linhagem_feerica:
            # Básica: +1 magia de 1º círculo
            if ficha.combate.magias_calc:
                ficha.combate.limite_magias = (ficha.combate.limite_magias or 3) + 1
            # Básica: torna-se treinado em Enganação
            info_eng = ficha.pericias.get("Enganação")
            if info_eng is not None and (info_eng.treino or 0) < 1:
                info_eng.treino = 1
                if "Treinada por Linhagem Feérica (básica)" not in info_eng.fontes_bonus:
                    info_eng.fontes_bonus.append("Treinada por Linhagem Feérica (básica)")
            
            # Aprimorada: +2 CD Encantamento/Ilusão, -1 PM
            if heranca_aprimorada:
                ficha.combate.cd_por_escola["Encantamento"] = ficha.combate.cd_por_escola.get("Encantamento", 0) + 2
                ficha.combate.cd_por_escola["Ilusão"] = ficha.combate.cd_por_escola.get("Ilusão", 0) + 2
                ficha.combate.custo_por_escola["Encantamento"] = ficha.combate.custo_por_escola.get("Encantamento", 0) - 1
                ficha.combate.custo_por_escola["Ilusão"] = ficha.combate.custo_por_escola.get("Ilusão", 0) - 1
            
            # Superior: +2 Carisma
            if heranca_superior:
                ficha.atributos.carisma += 2
                if "carisma" in ficha.atributos_calc:
                    ficha.atributos_calc["carisma"].adicionar_bonus(
                        fonte="Linhagem Feérica (superior)",
                        categoria="Poder",
                        valor=2
                    )
    
    # ── Linhagem Rubra (Tormenta) ──
    linhagem_rubra = any(h.nome == "Linhagem Rubra" for h in ficha.habilidades)
    if linhagem_rubra:
        qtd_tormenta = sum(1 for h in ficha.habilidades if h.tipo and "Tormenta" in h.tipo)
        # Superior: +4 PM para cada poder da Tormenta
        if heranca_superior and qtd_tormenta > 0:
            if ficha.status.pm_calc is None:
                calcular_pv_pm(ficha)
            ficha.status.pm_calc.adicionar_bonus(
                fonte=f"Linhagem Rubra (superior: {qtd_tormenta} poder(es) Tormenta)",
                categoria="Poder", valor=4 * qtd_tormenta)
            ficha.status.pm.maximo = ficha.status.pm_calc.total

    # ═══════════════════════════════════════
    # ENVOLTO EM MISTÉRIO
    # ═══════════════════════════════════════
    
    if any(h.nome == "Envolto em Mistério" for h in ficha.habilidades):
        for pericia_nome in ["Enganação", "Intimidação"]:
            if pericia_nome in ficha.pericias:
                if not ficha.pericias[pericia_nome].fontes_bonus:
                    ficha.pericias[pericia_nome].fontes_bonus = []
                ficha.pericias[pericia_nome].fontes_bonus.append("Envolto em Mistério (+5 condicional)")
    
    # ═══════════════════════════════════════
    # 🧙 BRUXO: foco (RD 10, PV = metade dos seus)
    # ═══════════════════════════════════════
    
    if subclasse == "Bruxo":
        metade = ficha.status.pv.maximo // 2
        if ficha.combate.foco_pv_maximo != metade:
            ficha.combate.foco_pv_maximo = metade
            ficha.combate.foco_pv_atual = metade
        elif ficha.combate.foco_pv_atual > metade:
            ficha.combate.foco_pv_atual = metade
    else:
        ficha.combate.foco_pv_maximo = 0
        ficha.combate.foco_pv_atual = 0
    
    # Sincroniza atributos finais
    for attr_full, stat in ficha.atributos_calc.items():
        if hasattr(ficha.atributos, attr_full):
            setattr(ficha.atributos, attr_full, stat.total)
    
    return ficha


def sincronizar_ataques_magicos(ficha: Personagem):
    """Reconstrói o ataque Raio Arcano de forma idempotente.
    Remove qualquer ataque 'Raio Arcano' existente e recria com base
    nos poderes atuais (Raio Arcano / Poderoso / Elemental) e no
    círculo máximo do personagem."""
    from ..models import Ataque
    from ..dados_progressao_magias import MAPA_SUBCLASSE_PARA_CLASSE

    # 1) Remove ataques antigos (idempotência)
    ficha.combate.ataques = [a for a in ficha.combate.ataques if a.nome != "Raio Arcano"]

    # 2) Só continua se tiver o poder
    if not any(h.nome == "Raio Arcano" for h in ficha.habilidades):
        return ficha

    # 3) Localiza a classe Arcanista (ou subclasse mapeada) e o atributo-chave
    classe_arcanista = None
    for c in ficha.classes:
        nome_base = MAPA_SUBCLASSE_PARA_CLASSE.get(c.nome or "", c.nome or "")
        if nome_base == "Arcanista":
            classe_arcanista = c
            break
    if not classe_arcanista:
        return ficha

    subclasse = (classe_arcanista.subclasse or "").strip()
    if subclasse == "Feiticeiro":
        mod_attr = calcular_modificador(ficha.atributos.carisma)
    else:
        mod_attr = calcular_modificador(ficha.atributos.inteligencia)

    # 4) Escala de dano e variantes
    circulo = ficha.combate.circulo_maximo or 0
    poderoso = any(h.nome == "Raio Poderoso" for h in ficha.habilidades)
    elemental = any(h.nome == "Raio Elemental" for h in ficha.habilidades)

    tipo_dado = "d12" if poderoso else "d8"
    alcance = "Médio" if poderoso else "Curto"
    extra = max(0, circulo - 1)
    qtd_dados = max(1, circulo)
    dano = f"{qtd_dados}{tipo_dado}"

    especial = "Reflexos reduz à metade"
    if elemental:
        especial += " • +1 PM: dano elemental (ácido/eletricidade/fogo/frio/trevas) + condição"

    # 5) Recria o ataque
    ficha.combate.ataques.append(Ataque(
        nome="Raio Arcano",
        bonus_ataque=f"+{mod_attr}",
        dano=dano,
        critico="x2",
        tipo="Essência",
        alcance=alcance,
        teste="Reflexos",
        especial=especial,
    ))
    return ficha
