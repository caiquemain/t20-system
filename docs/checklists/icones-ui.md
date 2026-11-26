# 🎨 Migração de Ícones — Unicode → Biblioteca SVG Moderna

**Status:** 🟡 Núcleo migrado (Core da Ficha + Home + Bestiário + Grimório + Backend desacoplado)  
**Biblioteca instalada:** `lucide-react` (`frontend/src/components/T20Icon.tsx`)  
**Atualizado em:** 2026-11-26

---

## 🏗️ Arquitetura da Migração

- [x] Instalado `lucide-react` em `frontend/`
- [x] Criado componente central `frontend/src/components/T20Icon.tsx` com mapa semântico tipado (`IconName`), tamanho padrão e herança de cor (`currentColor`)
- [x] Criado resolver `getEfeitoVisual(efeito)` em `T20Icon.tsx` com paleta por categoria (sem depender de regex de emoji)

## 📦 Frentes de Substituição

### 1. Core da Ficha & Navegação Principal (Concluído)
- [x] `frontend/src/pages/Ficha.tsx` (header, abas, botões, efeitos ativos via `getEfeitoVisual`, grimório e linha do tempo)
- [x] `frontend/src/components/StatusBars.tsx` (Defesa, Deslocamento/Voo/Natação, Descanso, RD elemental, Imunidades, Sentidos)
- [x] `frontend/src/components/EquipamentoCard.tsx` (header, moedas, categorias de itens, lixeira, modal de catálogo)
- [x] `frontend/src/components/AttackList.tsx` (header, Fluxo de Mana, Foco Vital, alertas/especiais)
- [x] `frontend/src/components/SkillList.tsx` (badges de treino/armadura/Engenhosidade, tooltip e banner)
- [x] `frontend/src/components/GrimorioModal.tsx` (header, cadeados, avisos, empty state e rodapé)
- [x] `frontend/src/pages/Home.tsx` (cards principais, lista de personagens e botão editar)
- [x] `frontend/src/pages/Bestiario.tsx`, `MonsterCard.tsx` e `AmeacaDetail.tsx`
- [x] `frontend/src/pages/Grimorio.tsx`

### 2. Desacoplamento do Backend (`app/src/regras/`) (Concluído)
- [x] Removidos emojis de `efeitos_ativos` em `app/src/regras/habilidades.py`
- [x] Removidos emojis de `fontes_bonus` / `StatCalculado` em `app/src/regras/pericias.py`
- [x] Removida regex de limpeza de emoji em `Ficha.tsx`

### 3. Modais & Componentes Secundários (Concluído)
- [x] `EntitySelectorModal.tsx`, `AbilityCard.tsx`, `AbilityConfigModal.tsx`, `CondicoesRaciais.tsx`, `DesejosButton.tsx`, `FullGrimorioModal.tsx`, `PowerListItem.tsx`, `PowerSelectorModal.tsx`, `RacialAbilityRow.tsx`, `RacialAttributeModal.tsx`, `SpellDetailsModal.tsx`, `SpellSummary.tsx`

### 4. Wizard (Opcional — baixa prioridade)
- [ ] `frontend/src/pages/Wizard.tsx` e `frontend/src/components/wizard/steps/*`
