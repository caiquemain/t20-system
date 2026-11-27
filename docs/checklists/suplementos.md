# 📚 Checklist — Suplementos Oficiais (T20 JdA)

Rastreamento por fase e lote. Documentação arquitetural completa em [`docs/SUPLEMENTOS.md`](../SUPLEMENTOS.md).

## Fase 0 — Fundação
- [x] Catálogo de suplementos e inferência de `fonte` (`dados_suplementos.py`, `GET /dados/suplementos`)
- [x] Modelos Pydantic: `suplementos_ativos`, `regras_opcionais_ativas`, `distincoes`, `complicacoes`, `papel_grupo`, `objetivo_heroico`, `melhores_amigos`
- [x] Badges e filtros por livro no frontend (`EntitySelectorModal`, `SelectionModal`, `EntityDetailPanel`, `StepConceito`)
- [x] Motor e UI unificada de escolhas interativas (`dados_escolhas.py`, `escolhas_suplementos.py`, `EscolhasDinamicasPanel.tsx`)

## Fase 1 — *Ameaças de Arton*
- [x] **1A:** 40 Raças Jogáveis + 12 heranças Moreau (`dados_habilidades_raciais_ameacas.py`)
- [x] **1A+:** Regras Adicionais p. 374–375 + `Item.condicao` (`Avariado`/`Destruído`) (`regras/ameacas.py`)
- [x] **1B:** Cap. 3 Equipamentos (16 armas, 4 armaduras/escudos, 41 itens gerais, 2 melhorias, 8 materiais especiais, Recursos Naturais, 6 itens mágicos, 2 artefatos)
- [x] **1C:** Cap. 3 Magias (7 novas magias + 4 aprimoramentos de *Conjurar Mortos-Vivos*)

## Fase 2 — *Heróis de Arton*
- [x] **Cap. 4 (Regras Opcionais — opt-in):** 27 regras, 3 Estilos de Jogo, 6 métodos de atributos, 73 Complicações, 7 Idades Variadas, 9 Papéis no Grupo, 7 Objetivos Heroicos, Defesa Épica, poderes *Ás da Cozinha* e *Bom de Garfo* (`GET /dados/regras-opcionais`)
- [x] **Cap. 1 (5 Novas Raças, p. 8–15):** Duende (auditoria completa + *Sonhos Malucos* em `GET /dados/duende/sonhos-malucos`), Eiradaan, Galokk, Meio-Elfo (`exceto Con`), Sátiro
- [x] **Cap. 1 (Classe Treinador, p. 16–21):** 6 habilidades fixas, 21 poderes, 8 mascotes, 5 tipos e 22 truques do Melhor Amigo + motor `treinador_calc` (`GET /dados/treinador`)
- [x] **Cap. 1 (14 Classes Variantes, p. 22–45):** Alquimista, Atleta, Burguês, Duelista, Ermitão, Inovador, Machado de Pedra, Magimarcialista, Necromante (+ *Ritual do Lich*), Santo, Seteiro, Usurpador, Vassalo, Ventanista
- [x] **Cap. 1 (30 Novas Origens Especiais, p. 46–53):** Todas as 30 origens com efeitos mecânicos e escolhas interativas
- [ ] **Cap. 1 (Classe Frade):** Características, habilidades fixas, poderes de Frade e progressão de magias
- [ ] **Cap. 1/2 (Novos Poderes):** Novos poderes de classe e poderes gerais de *Heróis de Arton*
- [ ] **Cap. 2 (Distinções):** Catálogo de Distinções, marcas, admissão e poderes exclusivos
- [ ] **Cap. 3 (Equipamentos, Itens e Bases):** Novos equipamentos, melhorias, itens alquímicos e sistema de Bases

## Fase 3 — *Deuses de Arton*
- [ ] **3A:** Expansão dos 20 Deuses Maiores (novos poderes concedidos e regras de devoção)
- [ ] **3B:** Deuses Menores (catálogo, seletor na ficha/wizard e poderes concedidos)
- [ ] **3C:** Novas Magias Divinas, Itens Litúrgicos/Mágicos e Distinções Divinas

## Fase 4 — *Atlas de Arton*
- [x] **4A:** 66 Origens Regionais (p. 470–479) com benefício único automático e escolhas interativas
- [ ] **4B:** Equipamentos & Regras Regionais

## Fase 5 — UX Dedicada & Polimento
- [ ] **Helper passo a passo para criação de Duende** (5 passos + botão *Sonhos Malucos*)
- [ ] **Painel interativo do Melhor Amigo** na Ficha do Treinador
- [ ] **Painel de Regras Opcionais / Complicações / Papel no Grupo** na Ficha e Wizard
- [ ] **Painel de Distinções** na Ficha
- [ ] **Atualizar exportações (PDF, ODT, ODG, Roll20)** com os novos campos de suplementos
