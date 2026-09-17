"""Penalidade de armadura em perícias (T20 JdA p.152-153)."""
from src.models import Personagem, Item
from src.regras import atualizar_ficha


def _ficha(proficiencias):
    p = Personagem()
    p.proficiencias = proficiencias
    p.status.proficiencias = proficiencias  # fonte real p/ sync de classe
    return p


def test_proficiente_sofre_so_pericias_de_agilidade():
    p = _ficha(['Armas Marciais', 'Armaduras Pesadas', 'Escudos'])
    p.inventario.equipamentos.append(Item(nome='Cota de malha', tipo='Armadura', equipado=True))
    atualizar_ficha(p)
    assert p.status.penalidade_armadura == 2
    assert p.pericias['Furtividade'].total == -2
    assert p.pericias['Acrobacia'].total == -2
    assert p.pericias['Ladinagem'].total == -2
    assert p.pericias['Luta'].total == 0        # FOR mas proficiente
    assert p.pericias['Percepção'].total == 0   # SAB


def test_nao_proficiente_penaliza_for_e_des():
    p = _ficha([])
    # Arcanista não tem proficiência de armadura (Guerreiro tem, e o
    # sync de proficiencias recalcula da classe por cima do [])
    if p.classes:
        p.classes[0].nome = 'Arcanista'
    p.inventario.equipamentos.append(Item(nome='Couro batido', tipo='Armadura', equipado=True))
    atualizar_ficha(p)
    assert p.status.penalidade_armadura == 1
    assert p.pericias['Furtividade'].total == -1
    assert p.pericias['Luta'].total == -1       # FOR (p.152)
    assert p.pericias['Reflexos'].total == -1   # DES (p.152)
    assert p.pericias['Diplomacia'].total == 0  # CAR intacta


def test_sem_armadura_sem_penalidade():
    p = _ficha([])
    atualizar_ficha(p)
    assert p.status.penalidade_armadura == 0
    assert p.pericias['Furtividade'].total == 0
    assert p.pericias['Luta'].total == 0


def test_penalidade_transparente_no_calculo():
    """O tooltip lê calculo.fontes[categoria=Penalidade] — precisa existir."""
    p = _ficha(['Armaduras Pesadas'])
    p.inventario.equipamentos.append(Item(nome='Cota de malha', tipo='Armadura', equipado=True))
    atualizar_ficha(p)
    pens = [f for f in p.pericias['Furtividade'].calculo.fontes if f.categoria == 'Penalidade']
    assert pens and pens[0].valor == -2
