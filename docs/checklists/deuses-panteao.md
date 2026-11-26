# 👑 Deuses do Panteão (T20 JdA p.96–105) — Revisão & Tooltips

**Status:** ✅ 20/20 deuses revisados + tooltips na seleção de divindade (100% Concluída!)  
**Fontes de dados:** `app/src/dados_deuses.py`  
**UI:** `frontend/src/utils/deusTooltip.ts`, `EntitySelectorModal.tsx`, `SelectionModal.tsx`, `Ficha.tsx`, `StepConceito.tsx`  
**Testes:** `app/tests/test_deuses.py` (`822 testes passando`)  
**Atualizado em:** 2026-11-26

---

## 📋 Checklist dos 20 Deuses do Panteão

- [x] **Aharadak** (*Deus da Tormenta* — Negativa, Corrente de espinhos, Todos)
- [x] **Allihanna** (*Deusa da Natureza* — Positiva, Bordão)
- [x] **Arsenal** (*Deus da Guerra* — Qualquer, Martelo de guerra)
- [x] **Azgher** (*Deus-Sol* — Positiva, Cimitarra)
- [x] **Hyninn** (*Deus da Trapaça* — Qualquer, Adaga)
- [x] **Kallyadranoch** (*Deus dos Dragões* — Negativa, Lança)
- [x] **Khalmyr** (*Deus da Justiça* — Positiva, Espada longa)
- [x] **Lena** (*Deusa da Vida* — Positiva, Sem arma preferida)
- [x] **Lin-Wu** (*Deus da Honra* — Qualquer, Katana)
- [x] **Marah** (*Deusa da Paz* — Positiva, Sem arma preferida)
- [x] **Megalokk** (*Deus dos Monstros* — Negativa, Maça)
- [x] **Nimb** (*Deus do Caos* — Qualquer, Qualquer arma; O&R `–5` em perícias de Carisma conectada em `pericias.py`)
- [x] **Oceano** (*Deus dos Mares* — Qualquer, Tridente)
- [x] **Sszzaas** (*Deus da Traição* — Negativa, Adaga)
- [x] **Tanna-Toh** (*Deusa do Conhecimento* — Qualquer, Bordão)
- [x] **Tenebra** (*Deusa das Trevas* — Negativa, Adaga)
- [x] **Thwor** (*Deus dos Goblinoides* — Qualquer, Machado de guerra, Duyshidakk)
- [x] **Thyatis** (*Deus da Ressurreição e Profecia* — Positiva, Espada longa)
- [x] **Valkaria** (*Deusa da Ambição* — Positiva, Mangual, Todos)
- [x] **Wynna** (*Deusa da Magia* — Qualquer, Adaga)

## ✅ Critério de Pronto (atendido)
1. Todos os 20 deuses com `titulo`, `crencas`, `simbolo`, `energia`, `arma`, `devotos`, `poderes` (4 cada), `obrigacoes` e `restricoes_mecanicas` fiéis ao T20 JdA p.96–105.
2. Penalidade mecânica de Nimb (`–5` em perícias baseadas em Carisma) conectada ao motor (`pericias.py`).
3. Tooltips ricos e painel de detalhes no hover tanto no modal da Ficha (`EntitySelectorModal`) quanto no Wizard (`SelectionModal` / `StepConceito`), exibindo Título, Energia, Arma Preferida, Símbolo Sagrado, Poderes Concedidos, Crenças e Obrigações & Restrições.
