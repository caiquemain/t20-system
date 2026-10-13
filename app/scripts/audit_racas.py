"""Auditoria estatica: cria 1 ficha por raca (Guerreiro nv 1) e imprime estado."""
from src.models import Personagem, Cabecalho, ClasseInfo
from src.regras import atualizar_ficha

RACAS = [
    "Humano", "Anão", "Dahllan", "Elfo", "Goblin", "Lefou", "Minotauro",
    "Qareen", "Golem", "Hynne", "Kliren", "Medusa", "Osteon",
    "Sereia/Tritão", "Sílfide", "Suraggel (Aggelus)", "Suraggel (Sulfure)", "Trog",
]

def _ficha(raca):
    f = Personagem()
    f.cabecalho = Cabecalho(nome=f"Teste {raca}", raca=raca, nivel_total=1)
    f.classes = [ClasseInfo(nome="Guerreiro", nivel=1, primaria=True)]
    return f

for raca in RACAS:
    print("=" * 70)
    print(f"RAÇA: {raca}")
    print("=" * 70)

    f = _ficha(raca)
    try:
        atualizar_ficha(f)
    except Exception as e:
        print(f"  ERRO ao processar: {type(e).__name__}: {e}")
        continue

    print(f"  Atributos:  FOR={f.atributos.forca} DES={f.atributos.destreza} "
          f"CON={f.atributos.constituicao} INT={f.atributos.inteligencia} "
          f"SAB={f.atributos.sabedoria} CAR={f.atributos.carisma}")
    print(f"  Tamanho:    {f.descricao.tamanho.value}")
    print(f"  Desloc:     {f.status.deslocamento}m")
    print(f"  PV max:     {f.status.pv.maximo}")
    print(f"  PM max:     {f.status.pm.maximo}")

    habs = [h.nome for h in f.habilidades if h.tipo == "Racial"]
    print(f"  Habilidades ({len(habs)}):")
    for h in habs:
        print(f"      - {h}")

    if f.status.efeitos_ativos:
        print(f"  Efeitos ativos:")
        for e in f.status.efeitos_ativos:
            print(f"      - {e}")

    if f.combate.magias:
        print(f"  Magias ({len(f.combate.magias)}):")
        for m in f.combate.magias:
            print(f"      - {m.nome} (fonte: {m.fonte or m.fonte_origem or '?'})")

    defesa_fontes = []
    if f.status.defesa_calc:
        defesa_fontes = [f"{fnt.fonte}={fnt.valor:+d}" for fnt in f.status.defesa_calc.fontes]
    print(f"  Defesa:     {f.status.defesa.total}  fontes={defesa_fontes}")

    if f.status.rd:
        print(f"  RD:         {f.status.rd}")
    if f.status.imunidades:
        print(f"  Imunidades: {f.status.imunidades}")
    if f.status.sentidos:
        print(f"  Sentidos:   {f.status.sentidos}")
    if f.status.vulnerabilidades:
        print(f"  Vulnerab.:  {f.status.vulnerabilidades}")
    if f.status.proficiencias:
        print(f"  Profic.:    {f.status.proficiencias}")
    if f.combate.bonus_ataque_arma:
        print(f"  Bonus atk armas: {f.combate.bonus_ataque_arma}")
    if f.combate.bonus_dano_arma:
        print(f"  Bonus dano armas: {f.combate.bonus_dano_arma}")

    print()
