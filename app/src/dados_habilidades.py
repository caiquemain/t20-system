# src/dados_habilidades.py

# =========================================================
# Efeitos Chave (para integração com o React/TypeScript):
# - pericia_escolha (int): Nível de treino extra em perícia à escolha.
# - poder_escolha (int): Quantos poderes gerais o jogador pode escolher.
# - pv_max_ini (int): Bônus fixo no PV máximo (nível 1).
# - pv_max_nivel (int): Bônus por nível no PV máximo (nível 2+).
# - pm_max_nivel (int): Bônus por nível no PM máximo.
# - deslocamento (int): Novo deslocamento base (em metros).
# - defesa_bonus (int): Bônus fixo na Defesa total.
# - penalidade_armadura (int): Penalidade na Defesa devido à raça.
# - resistencia_dano (dict): Ex: {"tipo": "veneno", "valor": 5, "teste": "Fortitude"}.
# - resistencia_rd (dict): Ex: {"frio": 10}.
# - bonus_pericia (dict): Ex: {"Percepção": 2}.
# - dano_arma_base (dict): Ex: {"tipo": "arremesso", "passos": 1}
# =========================================================
from .dados_habilidades_raciais import DADOS_HABILIDADES_RACIAIS
from .dados_poderes_origem import DADOS_PODERES_ORIGEM
from typing import Dict, Any


HABILIDADES_GERAIS = {


    # ------------------------------------------------------------------
    # --- PODERES DE COMBATE ---
    # ------------------------------------------------------------------
    "Acuidade_Com_Arma": {
        "nome": "Acuidade com Arma",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Usa Destreza em vez de Força em ataques e dano com armas leves ou de arremesso.",
        "fonte": "T20 JdA",
        "requisitos": ["Des 1"],
        "efeitos": {"ataque_atributo_troca": {"origem": "for", "destino": "des", "tipo_arma": ["leve", "arremesso"]}}
    },
    "Arma_Secundaria_Grande": {
        "nome": "Arma Secundária Grande",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Pode empunhar duas armas de uma mão com Estilo de Duas Armas.",
        "fonte": "T20 JdA",
        "requisitos": ["Estilo de Duas Armas"],
        "efeitos": {}
    },
    "Arremesso_Potente": {
        "nome": "Arremesso Potente",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Usa Força em vez de Destreza em ataques com armas de arremesso. Permite usar Ataque Poderoso com elas.",
        "fonte": "T20 JdA",
        "requisitos": ["For 1", "Estilo de Arremesso"],
        "efeitos": {"ataque_atributo_troca": {"origem": "des", "destino": "for", "tipo_arma": ["arremesso"]}}
    },
    "Arremesso_Multiplo": {
        "nome": "Arremesso Múltiplo",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Gaste 1 PM para fazer um ataque extra com arma de arremesso (1/rodada).",
        "fonte": "T20 JdA",
        "requisitos": ["Des 1", "Estilo de Arremesso"],
        "efeitos": {}
    },
    "Ataque_Escudo": {
        "nome": "Ataque com Escudo",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Gaste 1 PM para fazer ataque extra com escudo ao agredir. Mantém bônus de defesa.",
        "fonte": "T20 JdA",
        "requisitos": ["Estilo de Arma e Escudo"],
        "efeitos": {}
    },
    "Ataque_Pesado": {
        "nome": "Ataque Pesado",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Ao atacar com arma de duas mãos, gaste 1 PM. Se acertar, faz manobra derrubar ou empurrar como ação livre.",
        "fonte": "T20 JdA",
        "requisitos": ["Estilo de Duas Mãos"],
        "efeitos": {}
    },
    "Ataque_Poderoso": {
        "nome": "Ataque Poderoso",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Sofre -2 no ataque para receber +5 no dano.",
        "fonte": "T20 JdA",
        "requisitos": ["For 1"],
        "efeitos": {}
    },
    "Ataque_Preciso": {
        "nome": "Ataque Preciso",
        "tipo": "Poder Geral (Combate)",
        "descricao": "+2 na margem de ameaça e +1 no multiplicador de crítico (uma mão, outra livre).",
        "fonte": "T20 JdA",
        "requisitos": ["Estilo de Uma Arma"],
        "efeitos": {}
    },
    "Bloqueio_Escudo": {
        "nome": "Bloqueio com Escudo",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Reação: gaste 1 PM para ganhar RD igual ao bônus do escudo contra um dano.",
        "fonte": "T20 JdA",
        "requisitos": ["Estilo de Arma e Escudo"],
        "efeitos": {}
    },
    "Carga_Cavalaria": {
        "nome": "Carga de Cavalaria",
        "tipo": "Poder Geral (Combate)",
        "descricao": "+2d8 dano em investida montada. Pode continuar se movendo.",
        "fonte": "T20 JdA",
        "requisitos": ["Ginete"],
        "efeitos": {}
    },
    "Combate_Defensivo": {
        "nome": "Combate Defensivo",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Ao agredir, sofra -2 no ataque para ganhar +5 na Defesa.",
        "fonte": "T20 JdA",
        "requisitos": ["Int 1"],
        "efeitos": {}
    },
    "Derrubar_Aprimorado": {
        "nome": "Derrubar Aprimorado",
        "tipo": "Poder Geral (Combate)",
        "descricao": "+2 em derrubar. Gaste 1 PM para ataque extra ao derrubar.",
        "fonte": "T20 JdA",
        "requisitos": ["Combate Defensivo"],
        "efeitos": {"bonus_manobra": {"derrubar": 2}}
    },
    "Desarmar_Aprimorado": {
        "nome": "Desarmar Aprimorado",
        "tipo": "Poder Geral (Combate)",
        "descricao": "+2 em desarmar. Gaste 1 PM para arremessar a arma longe.",
        "fonte": "T20 JdA",
        "requisitos": ["Combate Defensivo"],
        "efeitos": {"bonus_manobra": {"desarmar": 2}}
    },
    "Disparo_Preciso": {
        "nome": "Disparo Preciso",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Ignora penalidade de -5 contra oponentes em combate corpo a corpo.",
        "fonte": "T20 JdA",
        "requisitos": ["Estilo de Disparo ou Estilo de Arremesso"],
        "efeitos": {}
    },
    "Disparo_Rapido": {
        "nome": "Disparo Rápido",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Ação completa agredir: um ataque adicional com arma de disparo (-2 em todos os ataques).",
        "fonte": "T20 JdA",
        "requisitos": ["Des 1", "Estilo de Disparo"],
        "efeitos": {}
    },
    "Empunhadura_Poderosa": {
        "nome": "Empunhadura Poderosa",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Usa armas de tamanho maior com penalidade -2 (em vez de -5).",
        "fonte": "T20 JdA",
        "requisitos": ["For 3"],
        "efeitos": {}
    },
    "Encouraçado": {
        "nome": "Encouraçado",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Se usar armadura pesada, recebe +2 na Defesa.",
        "fonte": "T20 JdA",
        "requisitos": ["Armaduras Pesadas"],
        "efeitos": {"defesa_bonus_condicional": {"tipo": "armadura_pesada", "valor": 2}}
    },
    "Esquiva": {
        "nome": "Esquiva",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Você recebe +2 na Defesa e Reflexos.",
        "fonte": "T20 JdA",
        "requisitos": ["Des 1"],
        "efeitos": {"defesa_bonus": 2, "bonus_pericia": {"Reflexos": 2}}
    },
    "Estilo_Arma_Escudo": {
        "nome": "Estilo de Arma e Escudo",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Se usar escudo, bônus de defesa do escudo aumenta em +2.",
        "fonte": "T20 JdA",
        "requisitos": ["Treinado em Luta", "Escudos"],
        "efeitos": {"bonus_escudo": 2}
    },
    "Estilo_Arma_Longa": {
        "nome": "Estilo de Arma Longa",
        "tipo": "Poder Geral (Combate)",
        "descricao": "+2 em ataques com armas alongadas. Pode atacar adjacentes.",
        "fonte": "T20 JdA",
        "requisitos": ["For 1", "Treinado em Luta"],
        "efeitos": {}
    },
    "Estilo_Arremesso": {
        "nome": "Estilo de Arremesso",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Saca armas de arremesso como livre. +2 dano. Com Saque Rápido, +2 ataque.",
        "fonte": "T20 JdA",
        "requisitos": ["Treinado em Pontaria"],
        "efeitos": {"bonus_dano_tipo": {"arremesso": 2}}
    },
    "Estilo_Disparo": {
        "nome": "Estilo de Disparo",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Soma Destreza nas rolagens de dano com armas de disparo.",
        "fonte": "T20 JdA",
        "requisitos": ["Treinado em Pontaria"],
        "efeitos": {"dano_atributo_extra": "des"}
    },
    "Estilo_Duas_Armas": {
        "nome": "Estilo de Duas Armas",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Ao agredir com duas armas, faz dois ataques (-2 em ambos).",
        "fonte": "T20 JdA",
        "requisitos": ["Des 2", "Treinado em Luta"],
        "efeitos": {}
    },
    "Estilo_Duas_Maos": {
        "nome": "Estilo de Duas Mãos",
        "tipo": "Poder Geral (Combate)",
        "descricao": "+5 dano com arma de duas mãos (não leve).",
        "fonte": "T20 JdA",
        "requisitos": ["For 2", "Treinado em Luta"],
        "efeitos": {}
    },
    "Estilo_Uma_Arma": {
        "nome": "Estilo de Uma Arma",
        "tipo": "Poder Geral (Combate)",
        "descricao": "+2 Defesa e Ataque se usar uma arma e nada na outra mão.",
        "fonte": "T20 JdA",
        "requisitos": ["Treinado em Luta"],
        "efeitos": {}
    },
    "Estilo_Desarmado": {
        "nome": "Estilo Desarmado",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Ataques desarmados causam 1d6 e podem ser letais.",
        "fonte": "T20 JdA",
        "requisitos": ["Treinado em Luta"],
        "efeitos": {"dano_desarmado": "1d6"}
    },
    "Fanatico": {
        "nome": "Fanático",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Deslocamento não reduz por armadura pesada.",
        "fonte": "T20 JdA",
        "requisitos": ["12º nível", "Encouraçado"],
        "efeitos": {"imunidade_penalidade_mov": ["armadura"]}
    },
    "Finta_Aprimorada": {
        "nome": "Finta Aprimorada",
        "tipo": "Poder Geral (Combate)",
        "descricao": "+2 em Enganação para fintar. Finta como ação de movimento.",
        "fonte": "T20 JdA",
        "requisitos": ["Treinado em Enganação"],
        "efeitos": {}
    },
    "Foco_Arma": {
        "nome": "Foco em Arma",
        "tipo": "Poder Geral (Combate)",
        "descricao": "+2 em ataque com uma arma escolhida.",
        "fonte": "T20 JdA",
        "requisitos": ["Proficiência com a arma"],
        "efeitos": {"arma_escolha_bonus_ataque": 2}
    },
    "Ginete": {
        "nome": "Ginete",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Passa auto em testes para não cair. Sem penalidade ataque/magia montado.",
        "fonte": "T20 JdA",
        "requisitos": ["Treinado em Cavalgar"],
        "efeitos": {}
    },
    "Inexpugnavel": {
        "nome": "Inexpugnável",
        "tipo": "Poder Geral (Combate)",
        "descricao": "+2 em testes de resistência se usar armadura pesada.",
        "fonte": "T20 JdA",
        "requisitos": ["Encouraçado", "6º nível"],
        "efeitos": {"resistencia_bonus_condicional": {"tipo": "armadura_pesada", "valor": 2}}
    },
    "Mira_Apurada": {
        "nome": "Mira Apurada",
        "tipo": "Poder Geral (Combate)",
        "descricao": "+2 ataque e margem de ameaça com mirar.",
        "fonte": "T20 JdA",
        "requisitos": ["Sab 1", "Disparo Preciso"],
        "efeitos": {}
    },
    "Piqueiro": {
        "nome": "Piqueiro",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Ataque de oportunidade com arma alongada quando inimigo entra no alcance.",
        "fonte": "T20 JdA",
        "requisitos": ["Estilo de Arma Longa"],
        "efeitos": {}
    },
    "Presenca_Aterradora": {
        "nome": "Presença Aterradora",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Ação padrão e 1 PM para assustar criaturas em alcance curto.",
        "fonte": "T20 JdA",
        "requisitos": ["Treinado em Intimidação"],
        "efeitos": {}
    },
    "Proficiencia": {
        "nome": "Proficiência",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Recebe uma proficiência (marciais, fogo, pesadas, escudos ou exóticas).",
        "fonte": "T20 JdA",
        "requisitos": [],
        "efeitos": {"proficiencia_escolha": 1}
    },
    "Quebrar_Aprimorado": {
        "nome": "Quebrar Aprimorado",
        "tipo": "Poder Geral (Combate)",
        "descricao": "+2 em quebrar. Ataque extra ao destruir arma.",
        "fonte": "T20 JdA",
        "requisitos": ["Ataque Poderoso"],
        "efeitos": {"bonus_manobra": {"quebrar": 2}}
    },
    "Reflexos_Combate": {
        "nome": "Reflexos de Combate",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Ação de movimento extra no primeiro turno.",
        "fonte": "T20 JdA",
        "requisitos": ["Des 1"],
        "efeitos": {}
    },
    "Saque_Rapido": {
        "nome": "Saque Rápido",
        "tipo": "Poder Geral (Combate)",
        "descricao": "+2 Iniciativa. Sacar como livre. Recarga diminui um passo.",
        "fonte": "T20 JdA",
        "requisitos": ["Treinado em Iniciativa"],
        "efeitos": {"bonus_pericia": {"Iniciativa": 2}}
    },
    "Trespassar": {
        "nome": "Trespassar",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Ao reduzir inimigo a 0 PV, gaste 1 PM para ataque extra.",
        "fonte": "T20 JdA",
        "requisitos": ["Ataque Poderoso"],
        "efeitos": {}
    },
    "Vitalidade": {
        "nome": "Vitalidade",
        "tipo": "Poder Geral (Combate)",
        "descricao": "+1 PV por nível e +2 Fortitude.",
        "fonte": "T20 JdA",
        "requisitos": ["Con 1"],
        "efeitos": {"pv_max_nivel": 1, "bonus_pericia": {"Fortitude": 2}}
    },

    # ------------------------------------------------------------------
    # --- PODERES DE DESTINO ---
    # ------------------------------------------------------------------
    "Acrobatico": {
        "nome": "Acrobático",
        "tipo": "Poder Geral (Destino)",
        "descricao": "Usa Destreza em Atletismo. Ignora terreno difícil. Pode investir em terreno difícil.",
        "fonte": "T20 JdA",
        "requisitos": ["Des 2"],
        "efeitos": {"atletismo_des": True, "imunidade_terreno_dificil": True}
    },
    "Ao_Sabor_Destino": {
        "nome": "Ao Sabor do Destino",
        "tipo": "Poder Geral (Destino)",
        "descricao": "Bônus escalonados se não usar itens mágicos.",
        "fonte": "T20 JdA",
        "requisitos": ["6º nível"],
        "efeitos": {}
    },
    "Aparencia_Inofensiva": {
        "nome": "Aparência Inofensiva",
        "tipo": "Poder Geral (Destino)",
        "descricao": "Primeira criatura a atacar deve passar em Vontade ou perde ação (1/cena).",
        "fonte": "T20 JdA",
        "requisitos": ["Car 1"],
        "efeitos": {}
    },
    "Atletico": {
        "nome": "Atlético",
        "tipo": "Poder Geral (Destino)",
        "descricao": "+2 em Atletismo e +3m de deslocamento.",
        "fonte": "T20 JdA",
        "requisitos": ["For 2"],
        "efeitos": {"bonus_pericia": {"Atletismo": 2}, "deslocamento_bonus": 3}
    },
    "Atraente": {
        "nome": "Atraente",
        "tipo": "Poder Geral (Destino)",
        "descricao": "+2 em perícias de Carisma contra quem se atrai.",
        "fonte": "T20 JdA",
        "requisitos": ["Car 1"],
        "efeitos": {}
    },
    "Comandar": {
        "nome": "Comandar",
        "tipo": "Poder Geral (Destino)",
        "descricao": "Ação movimento e 1 PM: Aliados em alcance médio recebem +1 em perícias.",
        "fonte": "T20 JdA",
        "requisitos": ["Car 1"],
        "efeitos": {}
    },
    "Costas_Largas": {
        "nome": "Costas Largas",
        "tipo": "Poder Geral (Destino)",
        "descricao": "+5 espaços de carga e +1 item vestido.",
        "fonte": "T20 JdA",
        "requisitos": ["Con 1", "For 1"],
        "efeitos": {"carga_max_bonus": 5}
    },
    "Foco_Pericia": {
        "nome": "Foco em Perícia",
        "tipo": "Poder Geral (Destino)",
        "descricao": "Escolha uma perícia. Pode rolar dois dados e usar o melhor (1 PM).",
        "fonte": "T20 JdA",
        "requisitos": ["Treinado na perícia"],
        "efeitos": {"foco_pericia_escolha": 1}
    },
    "Inventario_Organizado": {
        "nome": "Inventário Organizado",
        "tipo": "Poder Geral (Destino)",
        "descricao": "Soma INT na carga. Itens pequenos ocupam 1/4.",
        "fonte": "T20 JdA",
        "requisitos": ["Int 1"],
        "efeitos": {"carga_soma_atributo": "int"}
    },
    "Investigador": {
        "nome": "Investigador",
        "tipo": "Poder Geral (Destino)",
        "descricao": "+2 em Investigação e soma INT em Intuição.",
        "fonte": "T20 JdA",
        "requisitos": ["Int 1"],
        "efeitos": {"bonus_pericia": {"Investigação": 2}, "pericia_soma_atributo": {"Intuição": "int"}}
    },
    "Lobo_Solitario": {
        "nome": "Lobo Solitário",
        "tipo": "Poder Geral (Destino)",
        "descricao": "+1 em perícias e Defesa se sem aliados perto. Cura em si mesmo sem penalidade.",
        "fonte": "T20 JdA",
        "requisitos": [],
        "efeitos": {}
    },
    "Medicina": {
        "nome": "Medicina",
        "tipo": "Poder Geral (Destino)",
        "descricao": "Ação completa para curar PV com teste de Cura.",
        "fonte": "T20 JdA",
        "requisitos": ["Sab 1", "Treinado em Cura"],
        "efeitos": {}
    },
    "Parceiro": {
        "nome": "Parceiro",
        "tipo": "Poder Geral (Destino)",
        "descricao": "Recebe um parceiro iniciante.",
        "fonte": "T20 JdA",
        "requisitos": ["Treinado em Adestramento ou Diplomacia", "5º nível"],
        "efeitos": {"parceiro_adicional": 1}
    },
    "Sentidos_Agucados": {
        "nome": "Sentidos Aguçados",
        "tipo": "Poder Geral (Destino)",
        "descricao": "+2 em Percepção, não fica desprevenido vs invisível, rerola falha por camuflagem.",
        "fonte": "T20 JdA",
        "requisitos": ["Sab 1", "Treinado em Percepção"],
        "efeitos": {"bonus_pericia": {"Percepção": 2}}
    },
    "Sortudo": {
        "nome": "Sortudo",
        "tipo": "Poder Geral (Destino)",
        "descricao": "Gaste 3 PM para rerolar um teste.",
        "fonte": "T20 JdA",
        "requisitos": [],
        "efeitos": {}
    },
    "Surto_Heroico": {
        "nome": "Surto Heroico",
        "tipo": "Poder Geral (Destino)",
        "descricao": "Gaste 5 PM para ação padrão ou movimento extra (1/rodada).",
        "fonte": "T20 JdA",
        "requisitos": [],
        "efeitos": {}
    },
    "Torcida": {
        "nome": "Torcida",
        "tipo": "Poder Geral (Destino)",
        "descricao": "+2 em perícias e Defesa se tiver torcida.",
        "fonte": "T20 JdA",
        "requisitos": ["Car 1"],
        "efeitos": {}
    },
    "Treinamento_Pericia": {
        "nome": "Treinamento em Perícia",
        "tipo": "Poder Geral (Destino)",
        "descricao": "Torna-se treinado em uma perícia.",
        "fonte": "T20 JdA",
        "requisitos": [],
        "efeitos": {"pericia_escolha": 1}
    },
    "Veneficio": {
        "nome": "Venefício",
        "tipo": "Poder Geral (Destino)",
        "descricao": "Uso seguro de venenos. CD +2.",
        "fonte": "T20 JdA",
        "requisitos": ["Treinado em Ofício (alquimista)"],
        "efeitos": {}
    },
    "Vontade_Ferro": {
        "nome": "Vontade de Ferro",
        "tipo": "Poder Geral (Destino)",
        "descricao": "+1 PM a cada dois níveis e +2 em Vontade.",
        "fonte": "T20 JdA",
        "requisitos": ["Sab 1"],
        "efeitos": {"pm_max_nivel_fracionado": 0.5, "bonus_pericia": {"Vontade": 2}}
    },

    # ------------------------------------------------------------------
    # --- PODERES DE MAGIA ---
    # ------------------------------------------------------------------
    "Celebrar_Ritual": {
        "nome": "Celebrar Ritual",
        "tipo": "Poder Geral (Magia)",
        "descricao": "Pode lançar magias como rituais (dobro PM, tempo longo, custo $).",
        "fonte": "T20 JdA",
        "requisitos": ["8º nível", "Treinado em Misticismo ou Religião"],
        "efeitos": {}
    },
    "Escrever_Pergaminho": {
        "nome": "Escrever Pergaminho",
        "tipo": "Poder Geral (Magia)",
        "descricao": "Pode fabricar pergaminhos.",
        "fonte": "T20 JdA",
        "requisitos": ["Magias", "Treinado em Ofício (escriba)"],
        "efeitos": {}
    },
    "Foco_Magia": {
        "nome": "Foco em Magia",
        "tipo": "Poder Geral (Magia)",
        "descricao": "-1 PM em uma magia escolhida.",
        "fonte": "T20 JdA",
        "requisitos": ["Lançar magias"],
        "efeitos": {}
    },
    "Magia_Acelerada": {
        "nome": "Magia Acelerada",
        "tipo": "Poder Geral (Magia)",
        "descricao": "Aprimoramento: Muda execução para livre (+4 PM).",
        "fonte": "T20 JdA",
        "requisitos": ["Magias 2º círculo"],
        "efeitos": {}
    },
    "Magia_Ampliada": {
        "nome": "Magia Ampliada",
        "tipo": "Poder Geral (Magia)",
        "descricao": "Aprimoramento: Aumenta alcance ou dobra área (+2 PM).",
        "fonte": "T20 JdA",
        "requisitos": ["Lançar magias"],
        "efeitos": {}
    },
    "Magia_Discreta": {
        "nome": "Magia Discreta",
        "tipo": "Poder Geral (Magia)",
        "descricao": "Aprimoramento: Lança sem gesticular/falar (+2 PM).",
        "fonte": "T20 JdA",
        "requisitos": ["Lançar magias"],
        "efeitos": {}
    },
    "Magia_Ilimitada": {
        "nome": "Magia Ilimitada",
        "tipo": "Poder Geral (Magia)",
        "descricao": "Soma atributo-chave ao limite de PM por magia.",
        "fonte": "T20 JdA",
        "requisitos": ["Lançar magias"],
        "efeitos": {}
    },
    "Preparar_Pocao": {
        "nome": "Preparar Poção",
        "tipo": "Poder Geral (Magia)",
        "descricao": "Pode fabricar poções.",
        "fonte": "T20 JdA",
        "requisitos": ["Magias", "Treinado em Ofício (alquimista)"],
        "efeitos": {}
    },

    # ------------------------------------------------------------------
    # --- PODERES CONCEDIDOS ---
    # ------------------------------------------------------------------
    "Coragem_Total": {
        "nome": "Coragem Total",
        "tipo": "Poder Concedido",
        "descricao": "Imune a medo.",
        "fonte": "T20 JdA",
        "requisitos": ["Devoto de Arsenal, Khalmyr, Lin-Wu ou Valkaria"],
        "efeitos": {"imunidade": ["medo"]}
    },
    "Escamas_Draconicas": {
        "nome": "Escamas Dracônicas",
        "tipo": "Poder Concedido",
        "descricao": "+2 Defesa e Fortitude.",
        "fonte": "T20 JdA",
        "requisitos": ["Devoto de Kallyadranoch"],
        "efeitos": {"defesa_bonus": 2, "bonus_pericia": {"Fortitude": 2}}
    },
    "Sangue_Ferro": {
        "nome": "Sangue de Ferro",
        "tipo": "Poder Concedido",
        "descricao": "3 PM para receber +2 dano e RD 5.",
        "fonte": "T20 JdA",
        "requisitos": ["Devoto de Arsenal"],
        "efeitos": {}
    },
    "Zumbificar": {
        "nome": "Zumbificar",
        "tipo": "Poder Concedido",
        "descricao": "3 PM para reanimar cadáver como parceiro.",
        "fonte": "T20 JdA",
        "requisitos": ["Devoto de Tenebra"],
        "efeitos": {}
    }
}
HABILIDADES_GERAIS.update(DADOS_HABILIDADES_RACIAIS)
HABILIDADES_GERAIS.update(DADOS_PODERES_ORIGEM)
