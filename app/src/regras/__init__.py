import logging
from .utils import calcular_nivel_personagem
from .atributos import aplicar_bonus_atributos_raciais, calcular_atributos_finais
from .habilidades import (
    limpar_habilidades_fixas,
    garantir_habilidades_iniciais,
    sincronizar_poderes_habilidades,
    sincronizar_escolhas_de_caminho,
    processar_acumulo_habilidades,
    atualizar_efeitos_ativos
)
from .magias import sincronizar_magias_habilidades, validar_circulos_magias, validar_magias_conhecidas
from .poderes_arcanista import aplicar_poderes_arcanista, sincronizar_ataques_magicos
from .pericias import inicializar_pericias

# 1. ATUALIZADO: Importamos a nova função 'calcular_proficiencias_e_extras' daqui
from .status import (
    calcular_pv_pm,
    calcular_defesa_e_deslocamento,
    calcular_reducoes_dano,
    calcular_proficiencias_e_extras
)

# 2. ATUALIZADO: Removemos 'calcular_proficiencias_e_sentidos' daqui (pois movida para status)
from .combate import sincronizar_ataques

from ..models import Personagem

logger = logging.getLogger("RegrasT20")


def atualizar_ficha(ficha: Personagem) -> Personagem:
    logger.info(f"🔄 INICIANDO ATUALIZAÇÃO: {ficha.cabecalho.nome}")

    # 1. Limpeza Inteligente:
    memoria_escolhas = limpar_habilidades_fixas(ficha)

    # 2. Cálculos Básicos
    ficha.cabecalho.nivel_total = calcular_nivel_personagem(ficha)
    ficha = aplicar_bonus_atributos_raciais(ficha)

    # 3. Reconstrução de Habilidades:
    garantir_habilidades_iniciais(ficha, memoria_escolhas)
    sincronizar_poderes_habilidades(ficha, memoria_escolhas)
    sincronizar_escolhas_de_caminho(ficha)

    # 4. Processamentos Adicionais de Habilidades
    sincronizar_magias_habilidades(ficha)
    validar_circulos_magias(ficha)
    validar_magias_conhecidas(ficha)
    processar_acumulo_habilidades(ficha)

    # 5. Atributos Finais
    calcular_atributos_finais(ficha)

    # 6. Estatísticas Derivadas
    inicializar_pericias(ficha)
    calcular_pv_pm(ficha)
    calcular_defesa_e_deslocamento(ficha)
    # [LOTE 1] Poderes de Arcanista aplicam DEPOIS de PV/PM (para não serem sobrescritos)
    aplicar_poderes_arcanista(ficha)

    # 3. ATUALIZADO: Chamada da nova função
    calcular_proficiencias_e_extras(ficha)

    calcular_reducoes_dano(ficha)
    sincronizar_ataques(ficha)
    sincronizar_ataques_magicos(ficha)
    atualizar_efeitos_ativos(ficha)

    logger.info("✅ Ficha atualizada com sucesso.")
    return ficha
