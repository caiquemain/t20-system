from enum import Enum
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

# --- ENUMS ---


class TamanhoEnum(str, Enum):
    MINUSCULO = "Minúsculo"
    PEQUENO = "Pequeno"
    MEDIO = "Médio"
    GRANDE = "Grande"
    ENORME = "Enorme"
    COLOSSAL = "Colossal"

# --- SUB-MODELOS DE DETALHES (NOVO) ---


class DetalhesPV(BaseModel):
    inicial: int = 0
    nivel: int = 0
    con: int = 0
    outros: int = 0


class DetalhesPM(BaseModel):
    inicial: int = 0
    nivel: int = 0
    atributo: int = 0
    outros: int = 0


class DetalhesDeslocamento(BaseModel):
    base: float = 9.0
    armadura: float = 0.0
    outros: float = 0.0

# --- SUB-MODELOS EXISTENTES ---


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
    idade: Optional[str] = "20"
    altura: Optional[str] = None
    tamanho: TamanhoEnum = TamanhoEnum.MEDIO
    genero: Optional[str] = None
    idiomas: List[str] = []
    aparencia: Optional[str] = None
    historia: Optional[str] = None
    anotacoes: Optional[str] = None


class Atributos(BaseModel):
    forca: int = 0
    destreza: int = 0
    constituicao: int = 0
    inteligencia: int = 0
    sabedoria: int = 0
    carisma: int = 0


class StatusBarra(BaseModel):
    atual: int = 0
    maximo: int = 0
    temporario: int = 0
    # Detalhes adicionados aqui (Opcionais para compatibilidade)
    detalhes_pv: Optional[DetalhesPV] = None
    detalhes_pm: Optional[DetalhesPM] = None


class ModificadorDetalhes(BaseModel):
    base: int = 10
    des_mod: int = 0
    armadura: int = 0
    escudo: int = 0
    outros: int = 0


class RD(BaseModel):
    tipo: str
    valor: int
    fonte: Optional[str] = None


class Defesa(BaseModel):
    total: int = 10
    detalhes: ModificadorDetalhes = Field(default_factory=ModificadorDetalhes)


class Status(BaseModel):
    pv: StatusBarra = Field(default_factory=StatusBarra)
    pm: StatusBarra = Field(default_factory=StatusBarra)
    defesa: Defesa = Field(default_factory=Defesa)
    rd: List[RD] = []
    deslocamento: float = 9.0
    detalhes_deslocamento: DetalhesDeslocamento = Field(
        default_factory=DetalhesDeslocamento)


class PericiaInfo(BaseModel):
    total: int = 0
    treino: int = 0
    bonus_item: int = 0
    outros: int = 0
    atributo_chave: str = "int"


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
    bba: int = 0
    iniciativa: int = 0


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
    tipo: str
    descricao: Optional[str] = None
    fonte: Optional[str] = None
    escolhas_aplicadas: Dict[str, Any] = Field(default_factory=dict)


class Personagem(BaseModel):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    usuario_id: str = "admin"

    cabecalho: Cabecalho = Field(default_factory=Cabecalho)
    classes: List[ClasseInfo] = Field(default_factory=list)
    descricao: Descricao = Field(default_factory=Descricao)

    atributos_base: Atributos = Field(default_factory=Atributos)
    atributos: Atributos = Field(default_factory=Atributos)

    modificadores_raciais: Dict[str, int] = Field(default_factory=dict)
    modificadores_envelhecimento: Dict[str, int] = Field(default_factory=dict)
    modificadores_outros: Dict[str, int] = Field(default_factory=dict)
    escolhas_atributos_raciais: List[str] = Field(default_factory=list)

    escolhas_origem: List[str] = Field(default_factory=list)

    status: Status = Field(default_factory=Status)
    pericias: Dict[str, PericiaInfo] = Field(default_factory=dict)
    proficiencias: List[str] = Field(default_factory=list)
    combate: Combate = Field(default_factory=Combate)

    habilidades: List[Habilidade] = Field(default_factory=list)
    inventario: Inventario = Field(default_factory=Inventario)

    class Config:
        populate_by_name = True
