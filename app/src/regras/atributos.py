import logging
from ..models import Personagem, TamanhoEnum, StatCalculado
from ..dados_racas import DADOS_RACAS
from .utils import calcular_modificador

logger = logging.getLogger("RegrasT20")

MAPA_ATRIBUTOS = {
    'for': 'forca', 'des': 'destreza', 'con': 'constituicao',
    'int': 'inteligencia', 'sab': 'sabedoria', 'car': 'carisma'
}

def _inicializar_atributos_calc(ficha: Personagem):
    """Copia os atributos base para a pilha de cálculo e reseta os totais."""
    if not ficha.atributos_calc:
        ficha.atributos_calc = {}
    
    for attr_full in MAPA_ATRIBUTOS.values():
        base_val = getattr(ficha.atributos_base, attr_full)
        if attr_full not in ficha.atributos_calc:
            ficha.atributos_calc[attr_full] = StatCalculado() # Usa o import implícito do models
        ficha.atributos_calc[attr_full].resetar(base_val)

def aplicar_bonus_atributos_raciais(ficha: Personagem):
    logger.info(f"--- [1] Aplicando Raça: {ficha.cabecalho.raca} ---")

    # 1. Inicializa a pilha com os valores base
    _inicializar_atributos_calc(ficha)
    
    # Reseta o objeto antigo de atributos para não acumular sujeira
    ficha.atributos = ficha.atributos_base.model_copy()
    ficha.status.deslocamento = 9.0

    raca_nome = ficha.cabecalho.raca
    dados_raca = DADOS_RACAS.get(raca_nome)
    ficha.modificadores_raciais = {}

    if dados_raca:
        # A. Atributos Fixos da Raça
        if "attrs" in dados_raca:
            for attr, val in dados_raca["attrs"].items():
                if not attr: continue
                short_key = str(attr).lower()[:3]
                full_key = MAPA_ATRIBUTOS.get(short_key, short_key)
                
                if full_key in ficha.atributos_calc:
                    ficha.atributos_calc[full_key].adicionar_bonus(
                        fonte=f"Raça: {raca_nome}",
                        categoria="Racial",
                        valor=int(val)
                    )
                    ficha.modificadores_raciais[full_key] = int(val)

        # B. Escolhas Variáveis: agora em aplicar_escolhas_atributos_raciais
        #    (roda DEPOIS de calcular_atributos_finais, senão o rebuild apaga)

        # C. Tamanho e Deslocamento
        tamanho = dados_raca.get("tamanho", TamanhoEnum.MEDIO)
        ficha.descricao.tamanho = tamanho
        if "deslocamento" in dados_raca:
            ficha.status.deslocamento = dados_raca["deslocamento"]

    return ficha


def calcular_atributos_finais(ficha: Personagem):
    logger.info("--- [2.5] Calculando Atributos Finais ---")
    
    for hab in ficha.habilidades:
        efeitos = (hab.efeitos or {}).copy()
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)

        mods = efeitos.get("atributo_bonus")

        if mods:
            # Correção de segurança para listas
            if isinstance(mods, list):
                temp_mods = {}
                for item in mods:
                    if isinstance(item, str) and item:
                        temp_mods[item] = temp_mods.get(item, 0) + 1
                mods = temp_mods

            if isinstance(mods, dict):
                for attr_short, valor in mods.items():
                    attr_full = MAPA_ATRIBUTOS.get(attr_short, attr_short)

                    # Exceção específica de regra do T20
                    if (hab.fonte == "Habilidade: Deformidade" and attr_short == "car" and int(valor) < 0):
                        continue

                    if attr_full in ficha.atributos_calc:
                        ficha.atributos_calc[attr_full].adicionar_bonus(
                            fonte=f"Poder: {hab.nome}",
                            categoria="Poder",
                            valor=int(valor)
                        )

        if "tamanho" in efeitos:
            try:
                ficha.descricao.tamanho = TamanhoEnum(efeitos["tamanho"])
            except ValueError:
                pass

    # Aumento de Atributo por escolha. Duas entradas validas:
    #  (a) efeitos traz "atributo_bonus_escolha": valor do catalogo;
    #  (b) teste/motor so passa escolhas_aplicadas = {"atributo": "forca"},
    #      caso em que assumimos +1 se o nome for "Aumento de Atributo".
    # Arcanista tem tratamento proprio em poderes_arcanista.py — pular.
    for hab in ficha.habilidades:
        efeitos = (hab.efeitos or {}).copy()
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)

        tipo = hab.tipo or ""
        if "Arcanista" in tipo:
            continue

        attr_escolhido = efeitos.get("atributo")
        if not attr_escolhido:
            continue

        valor = efeitos.get("atributo_bonus_escolha")
        if valor is None:
            if hab.nome == "Aumento de Atributo":
                valor = 1
            else:
                continue

        attr_full = MAPA_ATRIBUTOS.get(str(attr_escolhido).lower()[:3], attr_escolhido)
        if attr_full in ficha.atributos_calc:
            ficha.atributos_calc[attr_full].adicionar_bonus(
                fonte=f"Poder: {hab.nome}",
                categoria="Poder",
                valor=int(valor)
            )

    # --- ENVELHECIMENTO (T20 JdA p.108) ---
    # Maduro (45 anos; x2 Anão/Qareen; x5 Dahllan/Elfo/Golem/Osteon/Sílfide): For/Des/Con -1, Int/Sab/Car +1
    # Velho  (70 anos; cumulativo): For/Des/Con -3, Int/Sab/Car +2
    _MULT_LONGEVIDADE = {
        "Anão": 2, "Qareen": 2,
        "Dahllan": 5, "Elfo": 5, "Golem": 5, "Osteon": 5, "Sílfide": 5,
    }
    _MODS_FAIXA = {
        "Maduro": {"forca": -1, "destreza": -1, "constituicao": -1, "inteligencia": 1, "sabedoria": 1, "carisma": 1},
        "Velho": {"forca": -3, "destreza": -3, "constituicao": -3, "inteligencia": 2, "sabedoria": 2, "carisma": 2},
    }
    raca_env = (ficha.cabecalho.raca or "").strip()
    mult_env = _MULT_LONGEVIDADE.get(raca_env, 1)
    faixa = getattr(ficha.descricao, "faixa_etaria", "Adulto") or "Adulto"
    idade_val = getattr(ficha.descricao, "idade", None)
    if isinstance(idade_val, int) and idade_val > 0:
        if idade_val >= 70 * mult_env:
            faixa = "Velho"
        elif idade_val >= 45 * mult_env:
            faixa = "Maduro"
        else:
            faixa = "Adulto"
        ficha.descricao.faixa_etaria = faixa

    if faixa in _MODS_FAIXA:
        ficha.modificadores_envelhecimento = dict(_MODS_FAIXA[faixa])
        for attr_full, val_env in _MODS_FAIXA[faixa].items():
            if attr_full in ficha.atributos_calc:
                ficha.atributos_calc[attr_full].adicionar_bonus(
                    fonte=f"Envelhecimento ({faixa})",
                    categoria="Envelhecimento",
                    valor=val_env,
                )
    else:
        ficha.modificadores_envelhecimento = {}

    # --- PERDA DE CARISMA POR PODERES DA TORMENTA (T20 JdA p.136) ---
    # 1º poder = -1 Car; para cada 2 outros poderes, -1 Car adicional.
    # Afinidade com a Tormenta: o 1º poder da Tormenta não conta para perda de Carisma.
    qtd_tormenta_car = sum(
        1 for h in ficha.habilidades if h.tipo and "Tormenta" in h.tipo
    )
    tem_afinidade = any(
        (h.efeitos or {}).get("primeiro_poder_tormenta_sem_perda_car")
        or (h.nome or "") == "Afinidade com a Tormenta"
        for h in ficha.habilidades
    )
    qtd_efetiva_car = max(0, qtd_tormenta_car - (1 if tem_afinidade else 0))
    if qtd_efetiva_car > 0 and "carisma" in ficha.atributos_calc:
        perda_car = (qtd_efetiva_car + 1) // 2
        ficha.atributos_calc["carisma"].adicionar_bonus(
            fonte=f"Poderes da Tormenta ({qtd_tormenta_car})",
            categoria="Tormenta",
            valor=-perda_car,
        )

    # --- ACESSÓRIOS MÁGICOS DE ATRIBUTO (T20 JdA p.333, 342–345) ---
    # Bônus de itens na mesma característica não se acumulam — usa apenas o maior.
    from ..dados_recompensas import ACESSORIOS_MAGICOS
    _acess_lower = {k.lower(): (k, v) for k, v in ACESSORIOS_MAGICOS.items()}
    melhor_attr_item = {}
    for it in (getattr(ficha.inventario, "equipamentos", None) or []):
        if not it.equipado:
            continue
        par = _acess_lower.get((it.nome or "").strip().lower())
        if not par:
            continue
        nome_canon, dados_ac = par
        for attr_full, val_ac in (dados_ac.get("efeitos", {}).get("bonus_atributo") or {}).items():
            prev = melhor_attr_item.get(attr_full)
            if prev is None or val_ac > prev[1]:
                melhor_attr_item[attr_full] = (nome_canon, int(val_ac))
    for attr_full, (nome_canon, val_ac) in melhor_attr_item.items():
        if attr_full in ficha.atributos_calc and val_ac:
            ficha.atributos_calc[attr_full].adicionar_bonus(
                fonte=f"Item Mágico: {nome_canon}",
                categoria="Item",
                valor=val_ac,
            )

    # --- SINCRONIZAÇÃO FINAL (Compatibilidade com Frontend) ---
    # Copia os totais calculados para o objeto 'atributos' que o frontend já lê
    for attr_full, stat in ficha.atributos_calc.items():
        if hasattr(ficha.atributos, attr_full):
            setattr(ficha.atributos, attr_full, stat.total)

def aplicar_escolhas_atributos_raciais(ficha: Personagem):
    """Escolhas variáveis de atributos raciais (Humano/Lefou/Osteon/Sereia: +1x3).

    Deve rodar DEPOIS de calcular_atributos_finais: o rebuild do
    atributos_calc apagava bônus aplicados antes dele.
    """
    raca_nome = ficha.cabecalho.raca
    dados_raca = DADOS_RACAS.get(raca_nome) or {}
    bonus = int(dados_raca.get("bonus_por_escolha", 1))
    for key_escolha in ficha.escolhas_atributos_raciais or []:
        # Normaliza chave curta ('for') -> chave do modelo ('forca')
        chave = MAPA_ATRIBUTOS.get(str(key_escolha), str(key_escolha))
        if chave not in ficha.atributos_calc:
            continue
        ficha.atributos_calc[chave].adicionar_bonus(
            fonte=f"Escolha Racial ({raca_nome})",
            categoria="Racial",
            valor=bonus
        )
        prev = ficha.modificadores_raciais.get(chave, 0)
        ficha.modificadores_raciais[chave] = prev + bonus
        # Reflete no total final (o rebuild já passou)
        setattr(ficha.atributos, chave, getattr(ficha.atributos, chave, 0) + bonus)
