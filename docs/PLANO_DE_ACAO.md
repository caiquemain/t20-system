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

## ✨ Fase 6 — Perícias, Poderes Concedidos & Poderes Gerais
- [x] **Perícias (`dados_pericias.py`, `frontend/src/data/pericias.ts`, `SkillUsesModal.tsx`):** revisadas todas as 29 perícias contra Tabela 2-1 (T20 JdA p.115), corrigido catálogo do frontend (que tinha entradas inválidas/incompletas) e criado modal interativo **Usos da Perícia** com todas as ações/CDs oficiais (p.115–123), bloqueio de usos *Apenas Treinado* e rolagem rápida `1d20 + total` (`app/tests/test_pericias_catalogo.py`, `833 testes passando`).
- **Poderes Concedidos (`dados_poderes_concedidos.py`):** modelar `efeitos` nos 20 poderes concedidos (hoje `0/20` têm efeitos mecânicos).
- **Poderes Gerais (`dados_habilidades.py`):** revisar os 68 poderes gerais (de 202) que ainda estão sem `efeitos` declarativos, priorizando os do Livro Básico (Combate, Destino, Magia, Tormenta).

---

## 🎲 Fase 7 — Rolagens, Polimento de PDF, Roll20 e Qualidade Frontend
- **Sistema de Rolagens** ([`rolagens.md`](./checklists/rolagens.md)): 1d20 + modificadores em perícias/ataques, histórico e consumo automático de *Engenhosidade*, *Desejos* e *Sorte Salvadora (Hynne)*.
- **Refinamentos do PDF** ([`pdf.md`](./checklists/pdf.md)): cache do template em memória, multiclasse no cabeçalho, loading no botão, campos pendentes (dinheiro, proficiências, armadura/escudo, CD de magia).
- **Ponte Roll20** ([`roll20-bridge.md`](./checklists/roll20-bridge.md)): modo "ficha nova" direto da ponte e consolidar envio de monstros/NPCs.
- **ESLint Frontend:** zerar os ~230 erros restantes (`@typescript-eslint/no-explicit-any` e `@ts-ignore` → `@ts-expect-error`) por módulo.
