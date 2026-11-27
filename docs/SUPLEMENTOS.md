# 📚 Suplementos Oficiais de Tormenta20 — Arquitetura e Progresso

Este documento registra a arquitetura, o conteúdo já implementado e os próximos lotes planejados para a integração dos **4 suplementos oficiais** de Tormenta20 (JdA) no **T20 System**.

> **Princípios de engenharia adotados:**
> 1. **Fidelidade ao texto oficial:** nenhuma regra é inventada de memória; todos os catálogos e efeitos seguem os textos oficiais enviados em lotes.
> 2. **Regras opcionais 100% opt-in:** toda regra opcional de suplemento é ativada explicitamente por ficha (`regras_opcionais_ativas`, `complicacoes`, `papel_grupo`), com zero impacto em personagens padrão.
> 3. **Motor + UI unificados:** escolhas interativas são declaradas em uma fonte única de verdade (`app/src/dados_escolhas.py` → `GET /dados/escolhas`), processadas no backend (`app/src/regras/escolhas_suplementos.py`) e renderizadas pelo componente único `EscolhasDinamicasPanel.tsx` no Wizard e na Ficha.

---

## 1. Status Geral por Livro

| Livro | Status | O que está pronto | Pendente |
|---|---|---|---|
| **Fundação (Fase 0)** | ✅ Concluída | `dados_suplementos.py`, badges/filtros por livro, `suplementos_ativos`, `regras_opcionais_ativas`, `distincoes`, `complicacoes`, `papel_grupo`, `objetivo_heroico`, `melhores_amigos` | — |
| **Ameaças de Arton** | ✅ Fase 1 concluída | 40 raças jogáveis (incl. 12 Moreau), Regras Adicionais p. 374–375 + `Item.condicao` (`Avariado`/`Destruído`), Cap. 3 Equipamentos/Materiais/Recursos/Itens Mágicos/Artefatos, Cap. 3 Magias (7 novas + 4 aprimoramentos) | Origens/Parceiros adicionais (se desejado) |
| **Heróis de Arton** | 🟡 Em andamento | Cap. 1: 5 Novas Raças (auditoria completa do **Duende** + *Sonhos Malucos*), Classe **Treinador** + motor do **Melhor Amigo**, **14 Classes Variantes**, **30 Novas Origens Especiais**; Cap. 4: **Regras Opcionais** (73 Complicações, 7 Idades Variadas, 9 Papéis no Grupo, 7 Objetivos Heroicos, Defesa Épica, Culinária poderes, helpers) | Classe **Frade**, Novos Poderes de Classe/Gerais, Distinções, Equipamentos/Bases (Cap. 2–3), tabelas extensas opcionais (d100 Falhas Críticas / Pratos / Construções) |
| **Atlas de Arton** | 🟡 Fase 4A concluída | **66 Origens Regionais** (p. 470–479) com benefício único automático e escolhas interativas (*Duplo Feérico*, *Aspirante a Herói*, *Futura Lenda*, *Cosmopolita*, *Estandarte Vivo*, *Estudante da Academia*, *De Outro Mundo*, *Tamalu*) | Equipamentos & Regras Regionais (Fase 4B) |
| **Deuses de Arton** | ⏳ Aguardando lotes | Estrutura pronta em `dados_suplementos.py` | Expansão dos 20 Deuses Maiores, Deuses Menores, Magias Divinas, Itens Litúrgicos, Distinções Divinas |

---

## 2. Mapa de Arquivos (Backend & Frontend)

### Catálogos de Dados (`app/src/`)
- [`dados_suplementos.py`](../app/src/dados_suplementos.py) — Catálogo oficial dos 5 livros (`T20 JdA`, `Ameaças de Arton`, `Heróis de Arton`, `Deuses de Arton`, `Atlas de Arton`) e inferência de `fonte`.
- [`dados_habilidades_raciais_ameacas.py`](../app/src/dados_habilidades_raciais_ameacas.py) — 40 raças jogáveis do *Ameaças de Arton* (mesclado em `dados_racas.py` e `dados_habilidades_raciais.py`).
- [`dados_equipamentos_ameacas.py`](../app/src/dados_equipamentos_ameacas.py) — 16 armas, 4 armaduras/escudos, 41 itens gerais, 2 melhorias, 8 materiais especiais, Recursos Naturais, 6 itens mágicos, 2 artefatos.
- [`dados_magias_ameacas.py`](../app/src/dados_magias_ameacas.py) — 7 novas magias com metadados `rolagem` + 4 aprimoramentos de *Conjurar Mortos-Vivos*.
- [`dados_origens_atlas.py`](../app/src/dados_origens_atlas.py) — 66 Origens Regionais do *Atlas de Arton*.
- [`dados_regras_opcionais_herois.py`](../app/src/dados_regras_opcionais_herois.py) — Cap. 4 de *Heróis de Arton* (27 regras opcionais, 3 Estilos de Jogo, 6 métodos de atributos, 73 Complicações, 7 Idades Variadas, 9 Papéis no Grupo, 7 Objetivos Heroicos, poderes *Ás da Cozinha* e *Bom de Garfo*).
- [`dados_treinador_herois.py`](../app/src/dados_treinador_herois.py) — Classe *Treinador* (6 habilidades fixas, 21 poderes, 8 mascotes, 5 tipos de Melhor Amigo, 22 truques).
- [`dados_variantes_herois.py`](../app/src/dados_variantes_herois.py) — 14 Classes Variantes (Tabelas 1-2 a 1-16, incluindo *Ritual do Lich* do Necromante e validação de multiclasse).
- [`dados_origens_herois.py`](../app/src/dados_origens_herois.py) — 30 Novas Origens Especiais de *Heróis de Arton* (p. 46–53).
- [`dados_escolhas.py`](../app/src/dados_escolhas.py) — Fonte única de verdade de escolhas interativas (Livro Básico + Ameaças + Atlas + Heróis).

### Motores de Regras (`app/src/regras/`)
- [`ameacas.py`](../app/src/regras/ameacas.py) — Tabela 2-1 Armas Naturais, escala de tamanho, atributo-chave de CD, Ameaças e Morte, condições de item (`Avariado`/`Destruído`).
- [`escolhas_suplementos.py`](../app/src/regras/escolhas_suplementos.py) — Processador unificado de escolhas interativas (Ameaças, Atlas e Heróis).
- [`regras_opcionais_herois.py`](../app/src/regras/regras_opcionais_herois.py) — Motor opt-in (Complicações + poder bônus com regra de ≥50% dos níveis na classe, Idades Variadas, Papéis no Grupo, helpers de mesa).
- [`duende.py`](../app/src/regras/duende.py) — Gerador aleatório oficial *Sonhos Malucos* (`1d3`, `1d4`, `2d6`, `3d12` + 2 PM + 22 exemplos de Tabu).
- [`treinador.py`](../app/src/regras/treinador.py) — Cálculo completo do *Treinador* (`combate.treinador_calc`) e da ficha derivada de cada *Melhor Amigo*.

### Novos Endpoints da API (`app/src/routers/`)
- `GET /dados/suplementos` — Catálogo de livros suportados.
- `GET /dados/escolhas` — Esquema unificado de escolhas interativas.
- `GET /dados/regras-opcionais` — Catálogo estruturado de Regras Opcionais (*Heróis de Arton* Cap. 4).
- `GET /dados/duende/sonhos-malucos` — Rolagem aleatória oficial de Duende (+2 PM).
- `GET /dados/treinador` — Catálogo de habilidades, mascotes, tipos e truques do Melhor Amigo.
- `GET /personagens/{id}/odt` — Exportação editável para LibreOffice Writer (`.odt`).
- `GET /personagens/{id}/odg` — Exportação para LibreOffice Draw (`.odg`).

### Frontend (`frontend/src/`)
- [`EscolhasDinamicasPanel.tsx`](../frontend/src/components/EscolhasDinamicasPanel.tsx) — Painel reutilizável de escolhas dinâmicas plugado no `AbilityConfigModal.tsx` (Ficha) e no `StepPoderes.tsx` (Wizard).
- Badges e filtros de livro integrados em `EntitySelectorModal.tsx`, `SelectionModal.tsx`, `EntityDetailPanel.tsx` e `StepConceito.tsx`.

---

## 3. Backlog Futuro (UX & Polimento — Fase 5)

- **Helper / Assistente Guiado de Criação de Duende:** fluxo passo a passo dedicado no Wizard (1. Natureza → 2. Tamanho → 3. Dons → 4. 3 Presentes → 5. Limitações/Tabu + botão *Sonhos Malucos* consumindo `GET /dados/duende/sonhos-malucos`).
- **Painel de Melhor Amigo (Treinador):** card interativo na Ficha para configurar tipo, tamanho, nome e truques dos Melhores Amigos e visualizar PV/Defesa/Ataques calculados em `combate.treinador_calc`.
- **Painel de Regras Opcionais & Complicações na Ficha:** toggles opt-in por estilo de jogo (`Tática`, `Épica`, `Velha Guarda`), seletor de Complicação + poder geral bônus e seletor de Papel no Grupo.
- **Exportação ODT/PDF/Roll20:** exibir Complicações, Distinções, Melhor Amigo e Origens Especiais/Regionais nas exportações.
