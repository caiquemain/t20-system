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

        # B. Escolhas Variáveis de Atributos Raciais
        for key_escolha in ficha.escolhas_atributos_raciais:
            chave_segura = str(key_escolha)
            if chave_segura in ficha.atributos_calc:
                ficha.atributos_calc[chave_segura].adicionar_bonus(
                    fonte=f"Escolha Racial ({raca_nome})",
                    categoria="Racial",
                    valor=1
                )
                prev = ficha.modificadores_raciais.get(chave_segura, 0)
                ficha.modificadores_raciais[chave_segura] = prev + 1

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

    # --- SINCRONIZAÇÃO FINAL (Compatibilidade com Frontend) ---
    # Copia os totais calculados para o objeto 'atributos' que o frontend já lê
    for attr_full, stat in ficha.atributos_calc.items():
        if hasattr(ficha.atributos, attr_full):
            setattr(ficha.atributos, attr_full, stat.total)