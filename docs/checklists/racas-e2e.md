# Checklist E2E — Raças (T20 JdA)

Estado da validação das raças do **livro base** em `2026-10-12`.

## Cobertura por teste

| Aspecto | Teste |
|---|---|
| Modificadores de atributo (17 raças) | `test_racas.py` |
| Humano/Versátil (2 perícias ou 1+1 poder) | `test_humano_versatil.py` |
| Anão — Duro como Pedra + Heredrimm | `test_raca_anao.py` |
| Sereia — Tridente + Canção dos Mares | `test_raca_sereia.py` |
| Furtividade por tamanho | `test_raca_tamanho_furtividade.py` |
| Bônus raciais em perícia e Defesa | `test_raca_pericias_bonus.py` |
| Escolhas do wizard consumidas pelo motor | `test_raca_escolhas_wizard.py` |
| Estrutura de habilidades ativáveis | `test_raca_habilidades_ativaveis.py` |

## Débitos conhecidos (não bloqueiam o livro base)

### Comportamentos em combate não modelados

- **Golem — Fonte Elemental**: regra "ao sofrer dano mágico do tipo escolhido,
  em vez disso cura PV = metade do dano" **não é aplicada** em combate.
  Exigiria hook no pipeline de dano.
- **Osteon — Natureza Esquelética**: "cura mágica de luz causa dano a você;
  dano de trevas recupera seus PV" **não é aplicada**. Mesma razão acima.
- **Golem — Criatura Artificial**: "Cura não funciona em você;
  Ofício (artesão) pode ser usada no lugar dela" não é enforçado.
- **Osteon — Preço da Não Vida**: efeitos vazios (`{}`). O sistema não
  modela "descanso sob estrelas ou sofre fome". Débito explícito.

### Habilidades de reaprendizado (duplicata)

Regra comum em várias raças: "caso receba esta habilidade novamente,
recebe +2 em X" — **não implementado genericamente**. Casos:
- **Dahllan — Empatia Selvagem**: se Druida + Dahllan → +2 Adestramento
- **Sílfide — Magia das Fadas**: reaprender magias reduz custo (parcialmente
  coberto por `reducao_custo_se_conhecida`, mas o "recebe novamente a
  habilidade" não soma bônus)
- **Kliren — Engenhosidade**: redução de custo já funciona via
  `nome_acumulo` + `reducao_se_acumular`, mas **não há teste cobrindo
  o cenário Inventor + Kliren**

### Raças de suplemento (fora do escopo do livro base)

O catálogo `DADOS_RACAS` contém **26 raças extras** (Heróis de Arton,
Ameaças de Arton, materiais antigos), misturadas com as 17 do livro:

- **Heróis de Arton**: Duende, Eiradaan, Galokk, Meio-Elfo, Sátiro
- **Ameaças/antigos**: Meio-Orc, Orc, Bugbear, Hobgoblin, Centauro, Gnoll,
  Kallyanach, Kaijin, Kappa, Nezumi, Tengu, Minauro, Ceratops, Pteros,
  Velocis, Voracis, Yidishan, Elfo-do-Mar, Nagah (M/F), Finntroll

**Problema**: aparecem no dropdown de criação sem distinção de fonte.
O endpoint `/racas` retorna todas. Ver débito no README.

- **Duende — 8 habilidades ativáveis sem `efeito`**: quebram o tooltip do
  card. Coberto por `test_todas_habilidades_ativaveis_do_livro_base_*`
  (escopo restrito). Fix pendente.

## Próximos passos sugeridos

1. Separar raças de suplemento em `DADOS_RACAS_SUPLEMENTOS` (ou filtrar
   `/racas` por `fonte == "T20 JdA"`)
2. Preencher `efeito` das 8 habilidades ativáveis do Duende
3. Modelar hooks de dano/cura para Golem e Osteon (projeto de combate)
4. Implementar reaprendizado genérico de habilidades raciais
