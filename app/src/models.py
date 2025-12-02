from enum import Enum
from typing import List, Optional, Dict
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

# --- ENUMS (Opções Fixas) ---


class TamanhoEnum(str, Enum):
    MINUSCULO = "Minúsculo"
    PEQUENO = "Pequeno"
    MEDIO = "Médio"
    GRANDE = "Grande"
    ENORME = "Enorme"
    COLOSSAL = "Colossal"

# --- SUB-MODELOS (Peças da Ficha) ---


class XP(BaseModel):
    atual: int = 0
    proximo_nivel: int = 1000


class Cabecalho(BaseModel):
    nome: str
    jogador: str
    raca: str
    origem: str
    divindade: Optional[str] = None
    nivel_total: int = 1
    xp: XP = Field(default_factory=XP)


class ClasseInfo(BaseModel):
    nome: str
    nivel: int
    subclasse: Optional[str] = None
    primaria: bool = False


class Descricao(BaseModel):
    idade: Optional[str] = None
    altura: Optional[str] = None
    tamanho: TamanhoEnum = TamanhoEnum.MEDIO
    genero: Optional[str] = None
    idiomas: List[str] = []
    aparencia: Optional[str] = None
    historia: Optional[str] = None
    anotacoes: Optional[str] = None


class Atributos(BaseModel):
    forca: int = 10
    destreza: int = 10
    constituicao: int = 10
    inteligencia: int = 10
    sabedoria: int = 10
    carisma: int = 10


class StatusBarra(BaseModel):
    atual: int
    maximo: int
    temporario: int = 0


class DefesaDetalhe(BaseModel):
    base: int = 10
    des_mod: int = 0
    armadura: int = 0
    escudo: int = 0
    outros: int = 0


class Defesa(BaseModel):
    total: int = 10
    detalhes: DefesaDetalhe = Field(default_factory=DefesaDetalhe)


class RD(BaseModel):
    tipo: str  # Ex: Fogo, Corte, Geral
    valor: int
    fonte: Optional[str] = None


class Status(BaseModel):
    pv: StatusBarra
    pm: StatusBarra
    defesa: Defesa = Field(default_factory=Defesa)
    rd: List[RD] = []


class PericiaInfo(BaseModel):
    total: int = 0  # <--- CAMPO NOVO (Calculado pelo Backend)
    treino: int = 0  # 0=Destr, 1=Treinado, 2=Vet, 3=Expert
    bonus_item: int = 0
    outros: int = 0
    atributo_chave: str = "for"


class Ataque(BaseModel):
    nome: str
    bonus_ataque: int
    dano: str
    critico: str
    tipo: str
    alcance: str


class Magia(BaseModel):
    nome: str
    circulo: int
    escola: str
    custo_pm: int
    execucao: str
    alcance: str
    duracao: str
    resistencia: Optional[str] = None
    descricao: Optional[str] = None


class Combate(BaseModel):
    ataques: List[Ataque] = []
    magias: List[Magia] = []
    cd_magias: int = 10


class Item(BaseModel):
    nome: str
    qtd: int = 1
    espaco: float = 0
    equipado: bool = False
    local: str = "Mochila"


class Dinheiro(BaseModel):
    tl: int = 0
    tp: int = 0
    to: int = 0


class Inventario(BaseModel):
    dinheiro: Dinheiro = Field(default_factory=Dinheiro)
    equipamentos: List[Item] = []
    carga_total: float = 0.0
    carga_maxima: float = 0.0


class Habilidade(BaseModel):
    nome: str
    tipo: str  # Racial, Classe, Poder Geral
    descricao: Optional[str] = None

# --- MODELO PRINCIPAL (A Ficha Completa) ---


class Personagem(BaseModel):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    usuario_id: str = "admin"

    cabecalho: Cabecalho
    classes: List[ClasseInfo]
    descricao: Descricao = Field(default_factory=Descricao)
    atributos: Atributos
    status: Status

    # Dict onde a chave é o nome da perícia (Ex: "Luta": {...})
    pericias: Dict[str, PericiaInfo] = {}

    proficiencias: List[str] = []
    combate: Combate = Field(default_factory=Combate)
    habilidades: List[Habilidade] = []
    inventario: Inventario = Field(default_factory=Inventario)

    class Config:
        populate_by_name = True
