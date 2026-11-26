# Checklist E2E — Raças (T20 JdA)

Estado da validação das **17 raças do livro base** (18 entradas com Suraggel Aggelus/Sulfure) em `2026-11-25`: **17/17 implementadas e testadas no motor de regras**.

## Cobertura por teste

| Aspecto | Teste |
|---|---|
| Modificadores de atributo e regras base (17 raças, incl. Hynne) | `test_racas.py` |
| Humano/Versátil (2 perícias ou 1+1 poder) | `test_humano_versatil.py` |
| Anão — Duro como Pedra + Heredrimm | `test_raca_anao.py` |
| Sereia — Tridente + Canção dos Mares | `test_raca_sereia.py` |
| Furtividade por tamanho | `test_raca_tamanho_furtividade.py` |
| Bônus raciais em perícia e Defesa | `test_raca_pericias_bonus.py` |
| Escolhas do wizard consumidas pelo motor | `test_raca_escolhas_wizard.py` |
| Estrutura de habilidades ativáveis | `test_raca_habilidades_ativaveis.py` |
| Filtro Livro Básico, efeitos Medusa/Goblin e reaprendizado | `test_raca_fase1_dividas.py` |

## ✅ Resolvido na Fase 1
- [x] Endpoints `/racas` e `/dados/racas` filtram por `fonte == "T20 JdA"` por padrão (`?incluir_suplementos=true` opcional).
- [x] **Medusa — Natureza Venenosa** (`resistencia_veneno`): +5 contra veneno em `efeitos_ativos` e tooltip situacional de `Fortitude`.
- [x] **Goblin — Espelunqueiro** (`deslocamento_escalada_igual`): deslocamento de escalada exibido em `efeitos_ativos`.
- [x] **Reaprendizado de habilidades duplicadas**: **Dahllan + Druida** (*Empatia Selvagem* → +2 Adestramento) e **Kliren + Inventor** (*Engenhosidade* → custo reduzido para 1 PM), com testes de regressão e idempotência.

## Débitos remanescentes (fora do escopo imediato do Livro Básico)

### Comportamentos em combate não modelados
- **Golem — Fonte Elemental**: curar metade do dano mágico elemental exige hook no pipeline de dano.
- **Osteon — Natureza Esquelética**: luz causa dano / trevas cura exige hook no pipeline de dano/cura.
- **Golem — Criatura Artificial**: restrição de cura / Ofício (artesão).
- **Osteon — Preço da Não Vida**: efeitos vazios (`{}` — descanso sob estrelas).
- **Hynne — Sorte Salvadora**: reroll depende do sistema de rolagens (`docs/checklists/rolagens.md`).

### Suplementos (quando retomar fora do Livro Básico)
- **Duende (Heróis de Arton)** — 8 habilidades ativáveis sem `efeito` (fora do filtro padrão `T20 JdA`).
