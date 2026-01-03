import logging
from ..models import Personagem, TamanhoEnum
from ..dados_racas import DADOS_RACAS
from .utils import calcular_modificador

logger = logging.getLogger("RegrasT20")


def aplicar_bonus_atributos_raciais(ficha: Personagem):
    logger.info(f"--- [1] Aplicando Raça: {ficha.cabecalho.raca} ---")

    # Reseta para base
    ficha.atributos = ficha.atributos_base.model_copy()
    ficha.status.deslocamento = 9.0

    raca_nome = ficha.cabecalho.raca
    dados_raca = DADOS_RACAS.get(raca_nome)

    ficha.modificadores_raciais = {}

    if dados_raca:
        # A. Atributos Fixos
        if "attrs" in dados_raca:
            for attr, val in dados_raca["attrs"].items():
                if not attr:
                    continue
                short_key = str(attr).lower()[:3]
                mapa = {'for': 'forca', 'des': 'destreza', 'con': 'constituicao',
                        'int': 'inteligencia', 'sab': 'sabedoria', 'car': 'carisma'}
                full_key = str(mapa.get(short_key, short_key))

                if hasattr(ficha.atributos, full_key):
                    atual = getattr(ficha.atributos, full_key)
                    setattr(ficha.atributos, full_key, int(atual) + int(val))
                    ficha.modificadores_raciais[full_key] = int(val)

        # B. Escolhas Variáveis
        for key_escolha in ficha.escolhas_atributos_raciais:
            chave_segura = str(key_escolha)
            if hasattr(ficha.atributos, chave_segura):
                atual = getattr(ficha.atributos, chave_segura)
                setattr(ficha.atributos, chave_segura, int(atual) + 1)
                prev = ficha.modificadores_raciais.get(chave_segura, 0)
                ficha.modificadores_raciais[chave_segura] = prev + 1

        tamanho = dados_raca.get("tamanho", TamanhoEnum.MEDIO)
        ficha.descricao.tamanho = tamanho

        if "deslocamento" in dados_raca:
            ficha.status.deslocamento = dados_raca["deslocamento"]

    return ficha


def calcular_atributos_finais(ficha: Personagem):
    logger.info("--- [2.5] Calculando Atributos Finais ---")
    mapa_attr = {'for': 'forca', 'des': 'destreza', 'con': 'constituicao',
                 'int': 'inteligencia', 'sab': 'sabedoria', 'car': 'carisma'}

    for hab in ficha.habilidades:
        efeitos = (hab.efeitos or {}).copy()
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)

        mods = efeitos.get("atributo_bonus")

        if mods:
            # --- CORREÇÃO DO ERRO 500 ---
            # Se vier lista ['for', 'int'], converte para {'for': 1, 'int': 1}
            if isinstance(mods, list):
                temp_mods = {}
                for item in mods:
                    if isinstance(item, str) and item:
                        temp_mods[item] = temp_mods.get(item, 0) + 1
                mods = temp_mods
            # ---------------------------

            if isinstance(mods, dict):
                for attr_short, valor in mods.items():
                    attr_full = str(mapa_attr.get(attr_short, attr_short))

                    if (hab.fonte == "Habilidade: Deformidade" and attr_short == "car" and int(valor) < 0):
                        continue

                    if hasattr(ficha.atributos, attr_full):
                        valor_atual = getattr(ficha.atributos, attr_full)
                        try:
                            setattr(ficha.atributos, attr_full,
                                    valor_atual + int(valor))
                        except ValueError:
                            pass

        if "tamanho" in efeitos:
            try:
                ficha.descricao.tamanho = TamanhoEnum(efeitos["tamanho"])
            except ValueError:
                pass
