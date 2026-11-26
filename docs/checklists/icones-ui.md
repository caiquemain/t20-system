# 🎨 Migração de Ícones — Unicode → Biblioteca SVG Moderna

**Status:** 📋 Planejada (Fase 2 do [`PLANO_DE_ACAO.md`](../PLANO_DE_ACAO.md))  
**Diagnóstico atual (2026-11-25):**
- **Frontend (`frontend/src/`):** 225 ocorrências de emojis Unicode em 37 arquivos
- **Backend (`app/src/regras/`):** 29 ocorrências em 7 arquivos (strings de `efeitos_ativos` e `fontes_bonus`)

---

## 🎯 Biblioteca Recomendada

| Camada | Biblioteca | Por quê |
|---|---|---|
| **Base de UI & RPG geral** | `lucide-react` | Leve, tree-shakeable, traço moderno e uniforme, TypeScript nativo, compatível com React 19 |
| **Ícones temáticos (opcional)** | `react-icons` (`react-icons/gi` — Game Icons) | Apenas onde o Lucide não tiver metáfora boa de fantasia (ex.: dragão, runa, chifres, asas, tridente) |

---

## 🏗️ Arquitetura da Migração

- [ ] Instalar `lucide-react` em `frontend/`
- [ ] Criar componente central `frontend/src/components/T20Icon.tsx` com mapa semântico tipado (`IconName`), tamanho padrão e herança de cor (`currentColor`)
- [ ] Definir paleta consistente por categoria (combate/vermelho, magia/roxo-azul, defesa/verde, sentido/ciano, alerta/âmbar, ouro/dourado)

## 📦 Frentes de Substituição (por ordem de impacto)

### 1. Core da Ficha (maior concentração)
- [ ] `frontend/src/pages/Ficha.tsx` (58 ocorrências — abas, cards de efeitos ativos, ações de header)
- [ ] `frontend/src/components/StatusBars.tsx` (21 ocorrências — PV, PM, Defesa, Deslocamento, formas)
- [ ] `frontend/src/components/EquipamentoCard.tsx` (21 ocorrências — armas, armaduras, itens, carga)
- [ ] `frontend/src/components/GrimorioModal.tsx` (16 ocorrências — escolas, círculos, ações)

### 2. Navegação, Wizard e Catálogos
- [ ] `frontend/src/pages/Wizard.tsx` (11 ocorrências) e `steps/*`
- [ ] `frontend/src/pages/Home.tsx` (7 ocorrências)
- [ ] `frontend/src/pages/Bestiario.tsx`, `MonsterCard.tsx` (5) e `AmeacaDetail.tsx`
- [ ] `frontend/src/pages/Grimorio.tsx`

### 3. Componentes Secundários
- [ ] `SkillList.tsx` (8), `AttackList.tsx` (5), `EntitySelectorModal.tsx` (5), `AbilityCard.tsx`, `RacialAbilityRow.tsx`, `DesejosButton.tsx`, `useFicha.ts` (8 em logs/mensagens)

### 4. Desacoplar Backend (`app/src/regras/`)
- [ ] Remover emojis fixos de `efeitos_ativos` em `habilidades.py` (11), `status.py` (7), `magias.py` (4), `pericias.py` (3), `__init__.py` (2), `poderes_arcanista.py` (1), `combate.py` (1)
- [ ] Padronizar categorias/tags de efeito para o frontend renderizar o `<T20Icon />` sem depender de regex de emoji
- [ ] Remover a regex de limpeza de emoji em `Ficha.tsx` após migração concluída
