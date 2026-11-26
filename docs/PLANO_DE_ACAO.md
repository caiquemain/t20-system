# 🗺️ Plano de Ação — Fechamento do Livro Básico (T20 JdA)

**Atualizado em:** 2026-11-25  
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

## 🎨 Fase 2 — Migração de Ícones (Fim dos Emojis Unicode Genéricos)
> Checklist detalhada: [`docs/checklists/icones-ui.md`](./checklists/icones-ui.md)

Hoje existem **225 ocorrências de emojis Unicode em 37 arquivos do frontend** e **29 ocorrências em 7 arquivos do backend** (`app/src/regras/`). Emojis nativos variam entre Windows/Linux/macOS, não herdam cor/tema e misturam apresentação visual dentro de strings do motor de regras.

### Stack recomendada (moderna, leve e temática para RPG)
- **Principal — `lucide-react`:** ícones SVG modernos, traço uniforme, tree-shakeable, suporte nativo a React 19 + TypeScript, ótimo para UI geral (`Shield`, `Swords`, `Sparkles`, `Eye`, `Heart`, `Zap`, `ScrollText`, `BookOpen`, `Dices`, `Flame`, `Skull`, `Backpack`, `Coins`, `Compass`, `Download`, `Send`).
- **Complemento temático (opcional) — `react-icons/gi` (Game Icons):** quando precisar de silhuetas bem RPG/fantasia que o Lucide não tem (ex.: dragão, elmo, poção, runa, chifres, asas, tridente).
- **Componente central `<T20Icon name="..." />`:** encapsula o mapeamento semântico (`hp`, `pm`, `defesa`, `imunidade`, `sentido`, `magia`, `ataque`, etc.) para manter tamanho, `strokeWidth` e paleta consistentes em todo o app.
- **Desacoplar o backend:** `efeitos_ativos` e `fontes_bonus` deixam de prefixar strings com `🚫`, `🧬`, `💥`, `🎲` e passam a usar texto limpo ou metadado de tipo (`categoria`/`icone`), deixando o frontend renderizar o ícone SVG correspondente.

---

## ⚔️ Fase 3 — Completar as 12 Classes Restantes do Livro Básico
> Checklist detalhada: [`docs/checklists/classes-livro-basico.md`](./checklists/classes-livro-basico.md)

Hoje apenas **Arcanista (24/24)** e **Bárbaro (24/24)** estão 100% completos com poderes e suíte de testes.  
Sugestão de execução em **4 lotes de 3 classes** (do mais mecânico/frequente ao mais complexo):

- **Lote 1 (Marciais):** Guerreiro, Lutador, Cavaleiro
- **Lote 2 (Especialistas):** Ladino, Caçador, Bucaneiro
- **Lote 3 (Divinos & Suporte):** Clérigo, Paladino, Druida
- **Lote 4 (Versáteis & Complexas):** Bardo, Nobre, Inventor

**Critério de pronto por classe:**
1. Todas as habilidades fixas (níveis 1–20) e poderes de classe do Livro Básico cadastrados em `dados_habilidades_classe.py`.
2. Efeitos mecânicos declarativos conectados em `app/src/regras/`.
3. Suíte `app/tests/test_<classe>_*.py` cobrindo base, poderes passivos e poderes ativos.

---

## ✨ Fase 4 — Poderes Concedidos & Poderes Gerais
- **Poderes Concedidos (`dados_poderes_concedidos.py`):** modelar `efeitos` nos 20 poderes concedidos (hoje `0/20` têm efeitos mecânicos).
- **Poderes Gerais (`dados_habilidades.py`):** revisar os 68 poderes gerais (de 202) que ainda estão sem `efeitos` declarativos, priorizando os do Livro Básico (Combate, Destino, Magia, Tormenta).

---

## 🎲 Fase 5 — Rolagens, Polimento de PDF, Roll20 e Qualidade Frontend
- **Sistema de Rolagens** ([`rolagens.md`](./checklists/rolagens.md)): 1d20 + modificadores em perícias/ataques, histórico e consumo automático de *Engenhosidade*, *Desejos* e *Sorte Salvadora (Hynne)*.
- **Refinamentos do PDF** ([`pdf.md`](./checklists/pdf.md)): cache do template em memória, multiclasse no cabeçalho, loading no botão, campos pendentes (dinheiro, proficiências, armadura/escudo, CD de magia).
- **Ponte Roll20** ([`roll20-bridge.md`](./checklists/roll20-bridge.md)): modo "ficha nova" direto da ponte e consolidar envio de monstros/NPCs.
- **ESLint Frontend:** zerar os ~230 erros restantes (`@typescript-eslint/no-explicit-any` e `@ts-ignore` → `@ts-expect-error`) por módulo.
