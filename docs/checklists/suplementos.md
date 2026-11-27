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
- [x] **Cap. 1 (Novos Poderes, p. 54–95):** 288 novos poderes para as 14 classes básicas (+ 7 novos efeitos de *Golpe Pessoal*) e 155 novos poderes gerais (25 Combate, 13 Destino, 14 Magia, 6 Tormenta, 77 Raça, 20 Grupo) + categorias `Raça` e `Grupo` em `GET /poderes`
- [x] **Cap. 2 (Distinções, p. 104–211):** Catálogo completo das 36 Distinções, 36 Marcas e 185 Poderes exclusivos (`dados_distincoes_herois.py`), motor `regras/distincoes.py` e endpoint `GET /dados/distincoes`
- [x] **Cap. 3 (Equipamentos, Melhorias, Magias e Itens Mágicos):** 37 armas, 14 armaduras/escudos, 136 itens gerais/munições/aparatos/bebidas/veículos, 12 melhorias, 22 novas magias arcanas/universais e 95 itens mágicos específicos (`dados_equipamentos_herois.py`, `dados_magias_herois.py`)
- [ ] **Cap. 3 (Sistema de Bases):** Regras e painel de Bases de aventureiros (pendente)

## Fase 3 — *Deuses de Arton*
- [x] **Classe Frade (Cap. 1, p. 38–41):** Características (12/+3 PV, 6 PM/nv + Sab), 6 habilidades fixas, 29 poderes (incl. 8 Sacrários), progressão de magias 1º–5º círculo (`dados_frade_deuses.py`)
- [x] **3A:** Expansão dos 20 Deuses Maiores — 75 novos Poderes Concedidos (Cap. 1, p. 42–47, Tabela 1-2, `dados_poderes_concedidos_deuses.py`), **Linhagem Abençoada** de Feiticeiro (p. 33) + regras *Ser Devoto* (*Devoção Ampla* +2 PM/patamar, Druida de Aharadak/Tenebra/Arton)
- [x] **3C:** Equipamentos Religiosos (70 itens, Tabela 1-3), 5 Melhorias (Tabela 1-4), 35 Itens Litúrgicos (`dados_equipamentos_deuses.py`), 29 Novas Magias Divinas/Universais (`dados_magias_deuses.py`) e 23 Distinções Divinas com 112 poderes (`dados_distincoes_deuses.py`)

## Suplemento Separado — *Guia de Deuses Menores* & *Manual de Criação de Ameaças*
- [x] **Guia de Deuses Menores:** Catálogo dos 60 Deuses Menores e seus Poderes Concedidos (`dados_deuses_menores.py`, `GET /dados/deuses-menores`)
- [x] **Manual de Criação de Ameaças (*Ameaças de Arton*, Cap. 2):** Tabelas 2-3 A/B/C completas (`dados_criacao_ameacas.py`, `/ameacas/construtor/tabelas`, `/ameacas/construtor/gerar`) + **Construtor de Ameaças** interativo na tela do Bestiário (`ConstrutorAmeacaModal.tsx`)

## Fase 4 — *Atlas de Arton*
- [x] **4A:** 66 Origens Regionais (p. 470–479) com benefício único automático e escolhas interativas
- [ ] **4B:** Equipamentos & Regras Regionais

## Fase 5 — UX Dedicada & Polimento
- [x] **Helper passo a passo para criação de Duende** (`DuendeHelperModal.tsx` + botão *Sonhos Malucos*)
- [x] **Painel interativo do Melhor Amigo** (`MelhorAmigoPanel.tsx`) na Ficha do Treinador
- [x] **Painel de Regras Opcionais / Complicações / Papel no Grupo** (`RegrasOpcionaisPanel.tsx`) na Ficha
- [x] **Painel de Distinções** (`DistincoesPanel.tsx`) na Ficha
- [x] **Motor executável de habilidades ativáveis** (`regras/ativaveis.py`, `GET /personagens/{id}/ativaveis`, `POST /personagens/{id}/ativar`)
- [ ] **Atualizar exportações (PDF, ODT, ODG, Roll20)** com os novos campos de suplementos
