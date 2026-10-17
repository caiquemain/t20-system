from typing import List, Dict, Optional, Any, Union
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, model_validator, field_validator, ConfigDict

# Tenta importar ObjectId do BSON (MongoDB), se falhar usa Any
try:
    from bson import ObjectId
except ImportError:
    ObjectId = Any

# --- ENUMS ---

class TamanhoEnum(str, Enum):
    MINUSCULO = "Minúsculo"
    PEQUENO = "Pequeno"
    MEDIO = "Médio"
    GRANDE = "Grande"
    ENORME = "Enorme"
    COLOSSAL = "Colossal"

    @classmethod
    def _missing_(cls, value):
        return cls.MEDIO

# --- NOVOS MODELOS DA PILHA DE MODIFICADORES (WIZARD) ---

class FonteBonus(BaseModel):
    fonte: str        # Ex: "Raça: Humano", "Poder: Ataque Poderoso"
    categoria: str    # Ex: "Racial", "Poder", "Equipamento", "Magia"
    valor: int        # Ex: +2, -1
    descricao: str = "" 

class StatCalculado(BaseModel):
    base: int = 0
    total: int = 0
    fontes: List[FonteBonus] = Field(default_factory=list)

    def resetar(self, base: int):
        """Limpa a pilha e define o valor base."""
        self.base = base
        self.total = base
        self.fontes = []

    def adicionar_bonus(self, fonte: str, categoria: str, valor: int, descricao: str = ""):
        """Adiciona um bônus à pilha e atualiza o total."""
        if valor != 0:
            self.fontes.append(FonteBonus(fonte=fonte, categoria=categoria, valor=valor, descricao=descricao))
            self.total += valor

# --- SUB-MODELOS DE DETALHES (Cálculos) ---

class DetalhesCalculo(BaseModel):
    inicial: int = 0
    nivel: int = 0
    con: int = 0       # Usado para PV
    atributo: int = 0  # Usado para PM
    habilidades: int = 0
    outros: int = 0
    total: int = 0

class DetalhesDeslocamento(BaseModel):
    base: float = 9.0
    armadura: float = 0.0
    habilidades: float = 0.0
    outros: float = 0.0
    total: float = 9.0

# --- SUB-MODELOS DE DADOS BÁSICOS ---

class XP(BaseModel):
    atual: int = 0
    proximo_nivel: int = 1000

class Cabecalho(BaseModel):
    nome: str = "Sem Nome"
    jogador: str = ""
    raca: str = ""
    origem: str = ""
    deus: str = ""
    nivel_total: int = 1
    xp: XP = Field(default_factory=XP)

    @model_validator(mode='before')
    @classmethod
    def corrigir_dados(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if 'divindade' in data:
                val = data.pop('divindade')
                if not data.get('deus'):
                    data['deus'] = val if val else ""

            for campo in ['nome', 'jogador', 'raca', 'origem', 'deus']:
                if data.get(campo) is None:
                    data[campo] = ""
        return data

class Atributos(BaseModel):
    forca: Optional[int] = 0
    destreza: Optional[int] = 0
    constituicao: Optional[int] = 0
    inteligencia: Optional[int] = 0
    sabedoria: Optional[int] = 0
    carisma: Optional[int] = 0

class Descricao(BaseModel):
    tamanho: TamanhoEnum = TamanhoEnum.MEDIO
    idiomas: List[str] = []
    aparencia: str = ""
    historia: str = ""
    anotacoes: str = ""

    @field_validator('aparencia', 'historia', 'anotacoes', mode='before')
    @classmethod
    def empty_string_if_none(cls, v):
        return v if v is not None else ""

    @field_validator('tamanho', mode='before')
    @classmethod
    def fallback_tamanho(cls, v):
        if not v:
            return TamanhoEnum.MEDIO
        return v

# --- STATUS ---

class Buff(BaseModel):
    origem: str = ""      # Ex: "Armadura de Allihanna"
    atributo: str = ""    # Ex: "defesa"
    valor: int = 0        # Ex: 2
    duracao: str = "Cena"  # Ex: "Cena", "Sustentada"

class StatusDetalhe(BaseModel):
    atual: int = 0
    maximo: int = 0
    temporario: int = 0
    calculo: Optional[DetalhesCalculo] = None

class DefesaDetalhe(BaseModel):
    total: int = 10
    detalhes: Dict[str, int] = {}

class Status(BaseModel):
    pv: StatusDetalhe = Field(default_factory=StatusDetalhe)
    pm: StatusDetalhe = Field(default_factory=StatusDetalhe)
    defesa: DefesaDetalhe = Field(default_factory=DefesaDetalhe)
    rd: List[str] = []
    deslocamento: float = 9.0
    penalidade_armadura: int = 0  # Acumulada: armadura + escudo + sobrecarga (-5)
    detalhes_deslocamento: Optional[DetalhesDeslocamento] = None
    buffs: List[Buff] = []
    efeitos_ativos: List[str] = []

    # 🚀 NOVA PILHA DE MODIFICADORES (FASE 2)
    pv_calc: Optional[StatCalculado] = Field(default=None)
    pm_calc: Optional[StatCalculado] = Field(default=None)
    defesa_calc: Optional[StatCalculado] = Field(default=None)
    deslocamento_calc: Optional[StatCalculado] = Field(default=None)

    # --- NOVOS CAMPOS ADICIONADOS ---
    proficiencias: List[str] = []
    imunidades: List[str] = []
    sentidos: List[str] = []
    vulnerabilidades: List[str] = []      # R5: Ossos Frágeis, Sangue Frio, etc.
    resistencia_magia: int = 0            # Bônus em testes de resistência contra magias (T20 p.42)
    DADOS_CLASSES: Optional[Any] = None   # 🆕 auto-audit
# --- PERÍCIAS E COMBATE ---

class PericiaInfo(BaseModel):
    treino: int = 0
    bonus_nivel: int = 0
    atributo_valor: int = 0
    outros: int = 0
    total: int = 0
    bonus_automatico: Optional[int] = 0
    atributo_selecionado: Optional[str] = None
    atributos_possiveis: List[str] = []
    fontes_bonus: List[str] = []
    # 🚀 NOVO: transparência detalhada (mantém fontes_bonus antigo p/ compatibilidade)
    calculo: Optional[StatCalculado] = None

class Ataque(BaseModel):
    nome: str = ""
    bonus_ataque: str = "+0"
    dano: str = "1d4"
    critico: str = "x2"
    tipo: str = "Corte"
    alcance: str = "Curto"
    teste: str = "Luta"
    especial: Optional[str] = ""
    fonte: Optional[str] = None  # Origem: "Racial" | "Poder" | "Classe" | None (manual/equipamento)

class Magia(BaseModel):
    nome: str
    circulo: Union[int, str]
    escola: Optional[str] = ""
    tipo: str = "Universal"
    execucao: Optional[str] = ""
    alcance: Optional[str] = ""
    alvo: Optional[str] = ""
    duracao: Optional[str] = ""
    resistencia: Optional[str] = ""
    custo_pm: Union[int, str] = 0
    descricao: str = ""
    atributo_chave: Optional[str] = ""
    fonte: Optional[str] = ""
    efeito: Optional[str] = ""
    aprimoramentos: Optional[List[Dict[str, Any]]] = []
    fonte_origem: Optional[str] = ""      # R5: "Racial: Dahllan", "Classe: Mago"
    isento_armadura: bool = False        # R5: raça/poder/item ignoram limitação de armadura

    @model_validator(mode='before')
    @classmethod
    def mapear_alvo_area(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if 'alvo_area' in data and not data.get('alvo'):
                data['alvo'] = data['alvo_area']
        return data

    # Pydantic V2 Config
    model_config = ConfigDict(populate_by_name=True)

class Combate(BaseModel):
    ataques: List[Ataque] = []
    magias: List[Magia] = []
    cd_magias: int = 10
    bba: int = 0
    iniciativa: int = 0
    reducao_pm_tipo: Optional[Dict[str, int]] = None

    bonus_dano_arma: Optional[Dict[str, int]] = None

    foco_vital: Optional[int] = None

    fluxo_de_mana: Optional[int] = None

    bonus_ataque_arma: Optional[Dict[str, int]] = None

    custo_arcano_metade: Optional[bool] = None

    magias_calc: Optional[Any] = None   # R5: breakdown de cálculo do limite
    circulo_maximo: int = 0   # 🆕 R5: círculo máximo de magias que o personagem pode lançar
    limite_magias: Optional[int] = None

    circulo_maximo: int = 1
    bonus_dano_dado_tipo: Optional[Dict[str, int]] = None

    bonus_dano_magias: Optional[int] = None
    # Bônus de dano que se aplicam a QUALQUER ataque (ex.: Instinto Selvagem
    # do Bárbaro, Fúria ativa). O frontend exibe como "+X dano geral".
    bonus_dano_geral: Optional[int] = None
    # Cálculo do bônus ativo de Fúria (Bárbaro): {"bonus": int, "custo": int}.
    # Bônus sobe +1 a cada 5 níveis; Fúria Titânica (20º) dobra.
    furia_calc: Optional[Dict[str, int]] = None
    # Crítico Brutal (Bárbaro, T20 p.42): soma ao multiplicador de crítico
    # em armas corpo a corpo e de arremesso.
    multiplicador_critico_bonus: int = 0

    cd_magias_calc: Optional[Any] = None   # 🆕 auto-audit
    cd_por_escola: Optional[Dict[str, int]] = None

    cd_por_resistencia: Optional[Dict[str, int]] = None

    custo_por_escola: Optional[Dict[str, int]] = None

    foco_pv_atual: Optional[int] = None

    foco_pv_maximo: Optional[int] = None

    passo_dano_arremesso: int = 0   # 🆕 auto-audit

# --- HABILIDADES E EQUIPAMENTO ---

class Habilidade(BaseModel):
    nome: str
    tipo: str
    descricao: str = ""
    fonte: str = ""
    custo_pm: int = 0
    escolhas_aplicadas: Dict[str, Any] = {}
    efeitos: Dict[str, Any] = {}

class Dinheiro(BaseModel):
    tl: int = 0
    tp: int = 0
    to: int = 0

class Item(BaseModel):
    nome: str
    qtd: int = 1
    espaco: int = 1
    descricao: str = ""
    tipo: str = "Geral"
    equipado: bool = False

class Inventario(BaseModel):
    dinheiro: Dinheiro = Field(default_factory=Dinheiro)
    equipamentos: List[Item] = []
    carga_total: int = 0
    carga_maxima: int = 0
    sobrecargado: bool = False  # carga_total > carga_maxima: -5 pen. armadura, -3m desloc.

class ClasseInfo(BaseModel):
    nome: str
    nivel: int = 1
    primaria: bool = False
    subclasse: str = ""

# --- MODELO PRINCIPAL ---

class Personagem(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    usuario_id: str = "guest"

    cabecalho: Cabecalho = Field(default_factory=Cabecalho)
    classes: List[ClasseInfo] = []

    atributos_base: Atributos = Field(default_factory=Atributos)
    atributos: Atributos = Field(default_factory=Atributos)
    
    # 🚀 NOVA PILHA DE MODIFICADORES (WIZARD)
    atributos_calc: Dict[str, StatCalculado] = Field(default_factory=dict)

    modificadores_raciais: Dict[str, int] = {}
    modificadores_envelhecimento: Dict[str, int] = {}
    modificadores_outros: Dict[str, int] = {}

    escolhas_atributos_raciais: List[str] = []
    escolhas_origem: List[str] = []

    descricao: Descricao = Field(default_factory=Descricao)
    status: Status = Field(default_factory=Status)
    fonte: Optional[Any] = None   # 🆕 auto-audit
    valor: Optional[Any] = None   # 🆕 auto-audit

    pericias: Dict[str, PericiaInfo] = {}

    proficiencias: List[str] = []

    combate: Combate = Field(default_factory=Combate)
    habilidades: List[Habilidade] = []
    condicoes_ativas: List[str] = []
    engenhosidade_pericia: Optional[str] = None  # Perícia com Engenhosidade ativa (Kliren)   # R5: subterraneo, sem_armadura, etc.
    inventario: Inventario = Field(default_factory=Inventario)

    @field_validator('id', mode='before')
    @classmethod
    def converter_objectid(cls, v):
        if v is None:
            return None
        return str(v)

    # Pydantic V2 Config
    model_config = ConfigDict(populate_by_name=True)


# --- HISTÓRICO DA FICHA (o "git" da ficha) ---
class EventoFicha(BaseModel):
    """Evento imutável da linha do tempo do personagem.

    Append-only: nunca deletar ou reescrever. Restaurar = evento novo.
    """
    id: Optional[str] = Field(default=None, alias="_id")
    personagem_id: str
    tipo: str = "edicao_manual"   # criacao | level_up | restauracao | edicao_manual
    nivel: int = 1
    resumo: List[str] = Field(default_factory=list)      # linhas legíveis do diff
    escolhas: Dict[str, Any] = Field(default_factory=dict)  # escolhas do jogador
    snapshot: Optional[Dict[str, Any]] = None            # ficha completa no momento
    criado_em: datetime = Field(default_factory=datetime.utcnow)

    @field_validator('id', mode='before')
    @classmethod
    def converter_objectid(cls, v):
        if v is None:
            return None
        return str(v)

    model_config = ConfigDict(populate_by_name=True)


# =====================================================================
# AMEAÇAS (monstros, NPCs, perigos) — Ameaças de Arton
# =====================================================================

class PapelAmeacaEnum(str, Enum):
    SOLO = "solo"
    LACAI0 = "lacaio"
    ESPECIAL = "especial"


class ModalidadeAtaqueEnum(str, Enum):
    CORPO_A_CORPO = "corpo a corpo"
    DISTANCIA = "à distância"


class TipoAcaoEnum(str, Enum):
    PASSIVA = "passiva"
    LIVRE = "livre"
    MOVIMENTO = "movimento"
    REACAO = "reação"
    PADRAO = "padrão"
    COMPLETA = "completa"
    SUSTENTADA = "sustentada"
    AUTOMATICA = "automática"


class PericiaAtaqueEnum(str, Enum):
    LUTA = "Luta"
    PONTARIA = "Pontaria"
    ATUACAO = "Atuação"


class AtaqueAmeaca(BaseModel):
    nome: str
    modalidade: ModalidadeAtaqueEnum = ModalidadeAtaqueEnum.CORPO_A_CORPO

    bonus_ataque: int = 0
    dano: str = ""
    dano_extra: Optional[str] = None
    dado_extra: Optional[str] = None
    margem_critico: int = 20
    multiplicador_critico: int = 2
    dano_critico: Optional[str] = None
    tipo_dano: str = ""
    pericia: PericiaAtaqueEnum = PericiaAtaqueEnum.LUTA
    mod_atributo_dano: Optional[str] = None
    alcance: Optional[str] = None
    descricao: Optional[str] = None

    critico_display: Optional[str] = None


class HabilidadeAmeaca(BaseModel):
    nome: str
    tipo_acao: TipoAcaoEnum = TipoAcaoEnum.PASSIVA
    custo_pm: Optional[int] = None
    recarga: Optional[str] = None
    duracao: Optional[str] = None
    descricao: str = ""
    rolls: List[str] = Field(default_factory=list)


class DefesasEspeciaisAmeaca(BaseModel):
    reducao_dano: List[str] = Field(default_factory=list)
    imunidades: List[str] = Field(default_factory=list)
    resistencias: List[str] = Field(default_factory=list)
    vulnerabilidades: List[str] = Field(default_factory=list)
    cura_acelerada: Optional[str] = None


class PericiaAmeaca(BaseModel):
    nome: str
    bonus: int
    observacao: Optional[str] = None


class Ameaca(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")

    nome: str
    nd: str = "1"
    tipo: str = "Monstro"
    subtipo: Optional[str] = None
    tamanho: TamanhoEnum = TamanhoEnum.MEDIO
    papel: PapelAmeacaEnum = PapelAmeacaEnum.SOLO

    iniciativa: int = 0
    percepcao: int = 0
    sentidos: List[str] = Field(default_factory=list)

    defesa: int = 10
    fortitude: int = 0
    reflexos: int = 0
    vontade: int = 0
    defesas_especiais: DefesasEspeciaisAmeaca = Field(default_factory=DefesasEspeciaisAmeaca)
    pontos_de_vida: int = 0
    pontos_de_mana: Optional[int] = None
    deslocamento: str = "9m (6q)"

    ataques: List[AtaqueAmeaca] = Field(default_factory=list)
    habilidades: List[HabilidadeAmeaca] = Field(default_factory=list)
    magias: List[Magia] = Field(default_factory=list)
    cd_magias: Optional[int] = None
    nivel_conjurador: Optional[str] = None

    atributos: Atributos = Field(default_factory=Atributos)
    pericias: List[PericiaAmeaca] = Field(default_factory=list)

    equipamento: Optional[str] = None
    tesouro: Optional[str] = None
    parceiro: Optional[str] = None
    reforcos: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)

    fonte: Optional[Dict[str, Any]] = None

    @field_validator('id', mode='before')
    @classmethod
    def converter_objectid(cls, v):
        if v is None:
            return None
        return str(v)

    model_config = ConfigDict(populate_by_name=True)
