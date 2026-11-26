# 🗺️ Plano de Ação — Fechamento do Livro Básico (T20 JdA)

**Atualizado em:** 2026-11-26  
**Foco:** Consolidar 100% do **Livro Básico (Tormenta20 Jogo do Ano)** antes de expandir suplementos, mantendo motor de regras confiável, testes automatizados e identidade visual coesa.

---

## ✅ Fase 0 — Higiene, Bugs Pontuais e Base de Testes (Concluída)
- [x] Corrigida regex de emojis em `frontend/src/pages/Ficha.tsx` (`/^(?:✨|🛡️|👁️|📏)\s*/u`)
- [x] Removidos logs `[RACIAL-DEBUG]` em `useFicha.ts` e `Ficha.tsx`
- [x] Removido arquivo duplicado/sombreado `frontend/src/types/index.ts`
- [x] Migrado `app/src/routers/pdf.py` de `import fitz` (deprecado) para `import pymupdf` + sanitização de `Content-Disposition`
- [x] Criada suíte `app/tests/test_pdf.py` (429 testes passando)
- [x] Removidos arquivos residuais (`{`, `t20-roll20-bridge/*.bak`, `*.backup`)
- [x] Documentação e checklists sincronizadas com o estado real do projeto

---

## ✅ Fase 1 — Fechar Dívidas das Raças do Livro Básico (Concluída)
> Checklist detalhada: [`docs/checklists/racas-e2e.md`](./checklists/racas-e2e.md)

- [x] **Separar Livro Básico de suplementos no `/racas` e `/dados/racas`:** filtro padrão `fonte == "T20 JdA"` (18 entradas = 17 raças base), com parâmetros opcionais `?incluir_suplementos=true` e `?fonte=...`.
- [x] **Conectar efeitos raciais declarados mas ignorados pelo motor:**
  - `resistencia_veneno` (Medusa — *Natureza Venenosa*, +5 contra veneno) refletido em `efeitos_ativos` e tooltip situacional de `Fortitude`.
  - `deslocamento_escalada_igual` (Goblin — *Espelunqueiro*) refletido em `efeitos_ativos` com o deslocamento terrestre calculado.
- [x] **Reaprendizado de habilidades duplicadas:** regra genérica em `processar_acumulo_habilidades` + preservação de duplicatas raça/classe em `garantir_habilidades_iniciais` (Dahllan + Druida → `+2 Adestramento`; Kliren + Inventor → `Engenhosidade` cai de 2 PM para 1 PM), coberto por `app/tests/test_raca_fase1_dividas.py` (439 testes passando).

---

## ✅ Fase 2 — Migração de Ícones (Concluída)
> Checklist detalhada: [`docs/checklists/icones-ui.md`](./checklists/icones-ui.md)

- [x] **`lucide-react` instalado** + componente central [`T20Icon.tsx`](../frontend/src/components/T20Icon.tsx) com mapa semântico tipado (`IconName`) e `getEfeitoVisual`.
- [x] **100% do frontend migrado:** Ficha, StatusBars, EquipamentoCard, AttackList, SkillList, GrimorioModal, todos os 12 modais secundários, Home, Bestiário, Grimório e todo o fluxo do Wizard (`Wizard.tsx`, `WizardStepper`, `SelectionModal` e os 7 passos).
- [x] **Backend desacoplado:** emojis removidos de `efeitos_ativos` (`habilidades.py`) e `fontes_bonus` (`pericias.py`), eliminando a regex de emojis em `Ficha.tsx`.

---

## ✅ Fase 3 — Completar Todas as 14 Classes do Livro Básico (Concluída)
> Checklist detalhada: [`docs/checklists/classes-livro-basico.md`](./checklists/classes-livro-basico.md)

Todas as **14/14 classes do Livro Básico (T20 JdA)** estão 100% catalogadas em `dados_habilidades_classe.py`, integradas ao motor de regras (`app/src/regras/`) e cobertas por suítes dedicadas (`801 testes passando`):

- [x] **Base anterior:** Arcanista (24/24), Bárbaro (24/24)
- [x] **Lote 1 (Marciais):** Guerreiro (23/23), Lutador (29/29), Cavaleiro (26/26)
- [x] **Lote 2 (Especialistas):** Ladino (27/27), Caçador (28/28), Bucaneiro (26/26)
- [x] **Lote 3 (Divinos & Suporte):** Clérigo (21/21), Paladino (30/30), Druida (27/27)
- [x] **Lote 4 (Versáteis & Complexas):** Bardo (24/24), Nobre (26/26), Inventor (38/38)

---

## ✅ Fase 4 — Revisão das 35 Origens do Livro Básico (Concluída)
> Checklist detalhada: [`docs/checklists/origens-livro-basico.md`](./checklists/origens-livro-basico.md)

- [x] **Auditoria de dados (`dados_origens.py`):** todas as 35 origens conferidas contra T20 JdA p.85–95; corrigidos `pericias_fixas` indevidas (*Amigo dos Animais*, *Assistente de Laboratório*, *Minerador*), especificações de *Ofício*, capitalização de *Quebra-Galho* e regra especial de *Amnésico*.
- [x] **Poderes exclusivos (`dados_poderes_origem.py`):** `35/35` poderes com efeitos declarativos e descrições corrigidas; conectados ao motor *Coração Heroico* (`+3/+6/+9/+12 PM` por patamar), *Mochileiro* (`+5` carga máxima), *Escavador* (Picareta +1 dano), *Amigo Especial* (`+5 Adestramento` e `+2` parceiro), *Vida Rústica* (imunidade) e preservação de `memoria_escolhas` em poderes de origem.
- [x] **Testes dedicados:** criada suíte `app/tests/test_origens.py` (`819 testes passando`).

---

## ✅ Fase 5 — Revisão dos 20 Deuses do Panteão, Tooltips & Toques Finais (Concluída)
> Checklist detalhada: [`docs/checklists/deuses-panteao.md`](./checklists/deuses-panteao.md)

- [x] **Auditoria de dados (`dados_deuses.py`):** todos os 20 deuses do T20 JdA p.96–105 atualizados com `titulo`, `crencas` completas, `simbolo`, `energia`, `arma` (incluindo Nimb `"Qualquer"` e Lena/Marah `None`), `devotos`, `poderes` (4 por deus) e `obrigacoes` (Obrigações & Restrições completas).
- [x] **Motor de regras (`pericias.py`):** penalidade de `–5` em perícias baseadas em Carisma para devotos de *Nimb* (T20 JdA p.102) conectada e testada (`app/tests/test_deuses.py`).
- [x] **Tooltips na seleção de divindade (Frontend):** criados `deusTooltip.ts` e painel de detalhes/tooltip no hover em `EntitySelectorModal` (Ficha) e `SelectionModal` (Wizard `StepConceito`), exibindo Título, Energia, Arma Preferida, Símbolo Sagrado, Poderes Concedidos, Crenças e Obrigações & Restrições.
- [x] **Toques Finais (T20 JdA p.106–111):** envelhecimento (*Maduro*/*Velho* + raças longevas ×2/×5) conectado em `atributos.py`, condições de descanso (*Ruim/Normal/Confortável/Luxuosa* + *Estoico*/*Mordomo*/*Vida Rústica* + zerar PV/PM temp.) em `status.py` e `StatusBars.tsx`, tooltip da Tabela 1-21 no badge `TAM`, e aba `DESCRIÇÃO` (`ToquesFinaisTab.tsx`) com Idade, Faixa Etária, os 9 Alinhamentos, Aparência, Personalidade, História e Anotações (`app/tests/test_toques_finais.py`, `826 testes passando`).

---

## ✅ Fase 6 — Perícias, Poderes Gerais, Concedidos & Tormenta (Concluída)
- [x] **Perícias (`dados_pericias.py`, `frontend/src/data/pericias.ts`, `SkillUsesModal.tsx`):** revisadas todas as 29 perícias contra Tabela 2-1 (T20 JdA p.115), corrigido catálogo do frontend e criado modal interativo **Usos da Perícia** com ações/CDs oficiais (p.115–123), bloqueio de usos *Apenas Treinado* e rolagem rápida `1d20 + total` (`app/tests/test_pericias_catalogo.py`).
- [x] **Poderes Concedidos (`dados_poderes_concedidos.py`):** catalogados todos os **72/72** poderes concedidos oficiais (T20 JdA p.131–136) com `efeitos` declarativos; conectados *Dom da Esperança* (Sab em vez de Con nos PV + imunidades), *Bênção do Mana*, *Descanso Natural*, *Escamas Dracônicas*, *Coragem Total*, *Habitante do Deserto*, *Fulgor Solar* e *Afinidade com a Tormenta*.
- [x] **Poderes da Tormenta (`dados_poderes_tormenta.py`):** catalogados todos os **22/22** poderes da Tormenta (p.136–137); corrigida a fórmula oficial de perda de Carisma (`–(qtd_efetiva+1)//2`, respeitando *Afinidade com a Tormenta*) e a escala oficial `+1 / +2 RD` a cada **dois outros** poderes em *Carapaça*, *Antenas*, *Articulações Flexíveis*, *Mãos Membranosas*, *Olhos Vermelhos* e *Pele Corrompida*.
- [x] **Poderes Gerais (`dados_habilidades.py`):** `68/68` poderes de Combate (40), Destino (20) e Magia (8) com `efeitos` declarativos; conectados *Vontade de Ferro* (`+1 PM` a cada 2 níveis) e *Inventário Organizado* (`+Int` carga máxima), cobertos por `app/tests/test_poderes_gerais_concedidos_tormenta.py` (`843 testes passando`).

---

## ✅ Fase 6.5 — Capítulo 3: Equipamento (Armas, Armaduras, Itens Gerais, Melhorias & Materiais) (Concluída)
- [x] **Armas, Riqueza & Carga (`dados_equipamentos.py`, `inventario.py`, `combate.py`):** revisadas Tabelas 3-1, 3-2 e 3-3 (T20 JdA p.140–151), corrigido `alcance: "Curto"` em Adaga/Lança/Machadinha/Tridente, adicionados `DINHEIRO_INICIAL_POR_NIVEL` e `ajustar_passo_dano`, conectadas moedas (1.000 = 1 espaço), *Mochila de aventureiro* (`+2` espaços) e *Inventário Organizado* (`0,5 → 0,25`).
- [x] **Armaduras, Escudos & Itens Gerais (`dados_equipamentos.py`, `pericias.py`, `inventario.py`, `status.py`):** conferidas Tabelas 3-5 (12 armaduras/escudos) e 3-6 (117 itens gerais + serviços), corrigidos typos em *Beladona* e *Bruma sonolenta*, e conectados bônus passivos de *Armadura acolchoada* (`+2 Fortitude`), *Símbolo sagrado* (`+1` resistências para devotos), 12 itens de *Vestuário* (respeitando limite de 4 itens ou 5 com *Costas Largas*), *Chapéu arcano* (`+1 PM` para Arcanista) e *Casaco longo* (penalidade de armadura 2).
- [x] **Itens Superiores & Materiais Especiais (`dados_equipamentos.py`):** catalogadas Tabelas 3-7 (`PRECO_MELHORIAS`), 3-8 (`DADOS_MELHORIAS`, 29 melhorias) e 3-9 (`DADOS_MATERIAIS_ESPECIAIS`, 6 materiais especiais), cobertos por `app/tests/test_equipamentos_armas.py` (`860 testes passando`).

---

## ✅ Fase 6.6 — Capítulo 4: Regras Gerais de Magia (p.170–172) (Concluída)
- [x] **Atributo-chave & CD de Magias (`custo_magia.py`, `regras/__init__.py`):** `calcular_cd_magias_ficha` conectado para **todas** as classes conjuradoras (Mago/Bruxo → INT, Clérigo/Druida → SAB, Bardo/Feiticeiro → CAR), com fórmula oficial `10 + metade do nível + atributo-chave + bônus`.
- [x] **Regras de Conjuração (`custo_magia.py`, `magias.py`):** Tabela 4-1 (`1/3/6/10/15 PM`), 8 escolas de magia (`ESCOLAS_MAGIA`, efeitos *mental* e *trevas*), Concentração (`calcular_cd_concentracao`: dano / `15 + PM` / `20 + PM`), Armaduras e Magia Arcana (`verificar_armadura_magia_arcana`: Misticismo CD `20 + PM`, isenções para raça/poder/item e Bardo com armadura leve), pré-requisitos de círculo em aprimoramentos (`pode_usar_aprimoramento`), correção do delta de limite de PM e Contramágica (`pode_anular_magia`), cobertos por `app/tests/test_regras_magia_cap4.py`.
- [x] **Adaptação das 198 magias atuais & Rolagens (`dados_magias.py`, `poderes_arcanista.py`, `SpellDetailsModal.tsx`, `AttackList.tsx`, `diceRoller.ts`):** corrigidos os custos em PM das 144 magias fora da Tabela 4-1 (`1/3/6/10/15 PM`), adicionados metadados `rolagem` às 46 magias de dano/cura/PV temporários, sincronizadas automaticamente as magias de dano em `combate.ataques` (com CD/Auto e bônus de dano mágico) e habilitadas rolagens interativas tanto na lista de Ataques quanto no modal da Magia (com seleção de aprimoramentos e cálculo de PM).
- [ ] **Posterior — Revisão textual do catálogo de magias (Cap. 4):** enviar e auditar o texto oficial completo de cada magia do Livro Básico em etapa futura.

---

## ✅ Fase 6.7 — Capítulo 8: Recompensas, XP & Itens Mágicos (p.326–348) (Concluída)
- [x] **Catálogo (`dados_recompensas.py`):** Tabelas 8-6 (*Tesouro Médio por Cena*), 8-7 (*Preço de Encantos*), 8-8 (28 encantos de armas), 8-9 (18 armas específicas), 8-10 (25 encantos de armaduras/escudos), 8-11 (13 armaduras/escudos específicos), 8-12 (38 poções/óleos/granadas), 8-13/8-14/8-15 (65 acessórios mágicos), 4 *Artefatos* (*A Espada-Deus*, *A Joia da Alma*, *O Baralho do Caos* com 22 cartas, *O Olho de Sszzaas*).
- [x] **Motor de Regras (`recompensas.py`, `atributos.py`, `status.py`, `pericias.py`, `inventario.py`):** cálculo de XP por desafio (ND × 1.000 / nº personagens, desafios irrelevantes e XP parcial), fabricação de consumíveis e itens permanentes (melhorias + encantos + sacrifício de PM), estatísticas de destruição de itens mágicos e bônus passivos de acessórios equipados (*Mochila de carga*, acessórios de atributo sem acúmulo, *Anel da vitalidade/energia*, *Braceletes de bronze/ouro*, *Anel da proteção*, *Colar guardião*, *Robe do arquimago*, *Manto da resistência*, *Símbolo abençoado*, *Botas velozes*, *Manto élfico/morcego*), cobertos por `app/tests/test_recompensas_cap8.py`.

---

## ✅ Fase 6.8 — Capítulo 5: Jogando, Testes, Dano & Combate (p.220–239) (Concluída)
- [x] **Regras Centrais & Tabelas (`regras/jogando.py`, `regras/__init__.py`):** catalogadas Tabelas 5-1 (*Dificuldades*), 5-2 (*Testes Estendidos*), 5-3 (*Situações Especiais*) e 5-4 (*Estatísticas de Objetos*), alcances padrão, 18 tipos de efeito, 11 tipos de dano e 5 manobras de combate.
- [x] **Motor de Cálculo (`jogando.py`):** avaliação de testes (20/1 natural), *Ajudar* (CD 10 `+1` por 10 acima), *Escolher 0*, CD de habilidades (`10 + metade do nível + atributo`), ordem oficial de operações de dano (resistência → divisões/vulnerabilidade ×1,5 → RD; *Perda de Vida* ignora RD), multiplicadores combinados (`x2 + x2 = x3`), teto de chance de falha (`75%`), limiar de morte (`min(-10, -PV/2)`) e PV de objetos por tamanho, cobertos por `app/tests/test_jogando_cap5.py`.

---

## ✅ Fase 6.9 — Apêndice: Lista de Condições (p.394–395) (Concluída)
- [x] **Catálogo (`dados_condicoes.py`):** todas as 35 condições oficiais do Apêndice com tipo de efeito, sub-condições implícitas, escalonamento ao repetir e modificadores mecânicos.
- [x] **Motor de Condições (`condicoes.py`, `status.py`, `pericias.py`, `custo_magia.py`):** expansão recursiva (*Petrificado → Inconsciente → Indefeso → Desprevenido*), escalonamento (*Abalado → Apavorado*, *Fatigado → Exausto*, *Fraco → Debilitado*, *Frustrado → Esmorecido*, *Exausto/Debilitado → Inconsciente*), não-acúmulo de efeitos iguais (aplicando o mais severo, exceto *Caído* cumulativo), arredondamento de *Lento* em incrementos de `1,5m` e aplicação direta na ficha (`Defesa`, `Perícias`, `Alquebrado +1 PM`), cobertos por `app/tests/test_condicoes_apendice.py`.

---

## 🎲 Fase 7 — Rolagens, Polimento de PDF, Roll20 e Qualidade Frontend
- [x] **Refinamentos do PDF** ([`pdf.md`](./checklists/pdf.md)): cache do template em memória, multiclasse no cabeçalho, loading no botão, todos os campos calculados preenchidos (`ModFor..ModCar`, colunas de perícias + Ofícios, defesa/armadura/escudo, dinheiro, proficiências, tamanho, CD de magia, Página 2 Descrição/Anotações sem sobrescrever `Observação`).
- [ ] **Sistema de Rolagens** ([`rolagens.md`](./checklists/rolagens.md)): 1d20 + modificadores em perícias/ataques, histórico e consumo automático de *Engenhosidade*, *Desejos* e *Sorte Salvadora (Hynne)*.
- [ ] **Ponte Roll20** ([`roll20-bridge.md`](./checklists/roll20-bridge.md)): modo "ficha nova" direto da ponte e consolidar envio de monstros/NPCs.
- [ ] **ESLint Frontend:** zerar os ~230 erros restantes (`@typescript-eslint/no-explicit-any` e `@ts-ignore` → `@ts-expect-error`) por módulo.
