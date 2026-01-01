import logging
from .utils import calcular_nivel_personagem
from .atributos import aplicar_bonus_atributos_raciais, calcular_atributos_finais
from .habilidades import (limpar_habilidades_fixas, garantir_habilidades_iniciais,
                          sincronizar_poderes_habilidades, processar_acumulo_habilidades, atualizar_efeitos_ativos)
from .magias import sincronizar_magias_habilidades
from .pericias import inicializar_pericias
from .status import calcular_pv_pm, calcular_defesa_e_deslocamento, calcular_reducoes_dano
from .combate import calcular_proficiencias_e_sentidos, sincronizar_ataques
from ..models import Personagem

logger = logging.getLogger("RegrasT20")


def atualizar_ficha(ficha: Personagem) -> Personagem:
    logger.info(f"🔄 INICIANDO ATUALIZAÇÃO: {ficha.cabecalho.nome}")

    # Preserva escolhas
    escolhas_preservadas = {
        h.nome: h.escolhas_aplicadas for h in ficha.habilidades if h.escolhas_aplicadas}

    # Pipeline de Regras
    limpar_habilidades_fixas(ficha)
    ficha.cabecalho.nivel_total = calcular_nivel_personagem(ficha)
    ficha = aplicar_bonus_atributos_raciais(ficha)
    garantir_habilidades_iniciais(ficha, escolhas_preservadas)

    sincronizar_poderes_habilidades(ficha)
    sincronizar_magias_habilidades(ficha)
    processar_acumulo_habilidades(ficha)

    calcular_atributos_finais(ficha)

    inicializar_pericias(ficha)
    calcular_pv_pm(ficha)
    calcular_defesa_e_deslocamento(ficha)
    calcular_proficiencias_e_sentidos(ficha)
    calcular_reducoes_dano(ficha)
    sincronizar_ataques(ficha)
    atualizar_efeitos_ativos(ficha)

    logger.info("✅ Ficha atualizada com sucesso.")
    return ficha
