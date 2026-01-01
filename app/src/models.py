from typing import List, Dict, Optional, Any, Union
from enum import Enum
from pydantic import BaseModel, Field, model_validator, field_validator, root_validator

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

# --- SUB-MODELOS DE DETALHES (Cálculos) ---

# ADICIONADO: Classe unificada que o regras.py está pedindo


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
    forca: int = 0
    destreza: int = 0
    constituicao: int = 0
    inteligencia: int = 0
    sabedoria: int = 0
    carisma: int = 0


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
    # ATUALIZADO: Agora usa a classe unificada DetalhesCalculo
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
    detalhes_deslocamento: Optional[DetalhesDeslocamento] = None
    buffs: List[Buff] = []
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

class Ataque(BaseModel):
    nome: str = ""
    bonus_ataque: str = "+0"
    dano: str = "1d4"
    critico: str = "x2"
    tipo: str = "Corte"
    alcance: str = "Curto"


class Aprimoramento(BaseModel):
    custo: str
    descricao: str
    efeitos: Dict[str, Any] = {}

# Atualize a class Magia para incluir a lista


class Magia(BaseModel):
    nome: str
    circulo: int
    escola: str = ""
    tipo: str = "Universal"
    execucao: str = ""
    alcance: str = ""
    alvo: str = ""
    duracao: str = ""
    resistencia: str = ""
    custo_pm: int = 0
    descricao: str = ""

    # --- CAMPOS ADICIONADOS PARA COMPATIBILIDADE ---
    atributo_chave: str = ""   # Ex: "Car" para Bardo/Sereia
    fonte: str = ""            # Ex: "Racial: Sereia"
    efeito: str = ""           # Texto mecânico curto (comum nos JSONs)
    # -----------------------------------------------

    aprimoramentos: List[Aprimoramento] = []

    @model_validator(mode='before')
    @classmethod
    def mapear_alvo_area(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if 'alvo_area' in data and not data.get('alvo'):
                data['alvo'] = data['alvo_area']
        return data

    class Config:
        populate_by_name = True


class Combate(BaseModel):
    ataques: List[Ataque] = []
    magias: List[Magia] = []
    cd_magias: int = 10
    bba: int = 0
    iniciativa: int = 0

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

    modificadores_raciais: Dict[str, int] = {}
    modificadores_envelhecimento: Dict[str, int] = {}
    modificadores_outros: Dict[str, int] = {}

    escolhas_atributos_raciais: List[str] = []
    escolhas_origem: List[str] = []

    descricao: Descricao = Field(default_factory=Descricao)
    status: Status = Field(default_factory=Status)

    pericias: Dict[str, PericiaInfo] = {}
    proficiencias: List[str] = []

    combate: Combate = Field(default_factory=Combate)
    habilidades: List[Habilidade] = []
    inventario: Inventario = Field(default_factory=Inventario)

    @field_validator('id', mode='before')
    @classmethod
    def converter_objectid(cls, v):
        if v is None:
            return None
        return str(v)

    class Config:
        populate_by_name = True
