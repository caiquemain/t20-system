# ⚔️ T20 System — Ficha de Personagem Digital para Tormenta20

Sistema completo de criação e gerenciamento de fichas de personagem para o RPG
**Tormenta20 (T20 JdA)**, com motor de regras automatizado no backend e interface
rica no frontend. Toda a matemática do sistema (PV, PM, perícias, defesa, custo de
magias, bônus condicionais) é recalculada pelo backend a cada alteração — a ficha
nunca "mente".

> 🎨 Interface com a fonte oficial **Tormenta.ttf**, identidade visual do livro.

---

## 🚀 Stack Tecnológica

| Camada | Tecnologia |
|---|---|
| **Backend** | Python 3.11 · FastAPI · Pydantic v2 · Motor (Mongo assíncrono) · pypdf |
| **Banco** | MongoDB 7.0 |
| **Frontend** | React 19 · TypeScript 5.9 · Vite 7 · react-router-dom 7 · axios |
| **Infra** | Docker Compose (api + web + db) |
| **Testes** | pytest (16 arquivos, ~156 testes do motor de regras) |
| **Extras** | Extensão de browser `t20-roll20-bridge` (Manifest V3) |

---

## ✨ Funcionalidades

### Criação de Personagem (Wizard + Home + Ficha)
- **Wizard** (`/wizard`) de criação passo a passo + edição (`/wizard/:id`)
- **Home** (`/`) com listagem das fichas salvas
- **Atributos** por pool de pontos (10 iniciais) com tabela de custo crescente
- **Modificadores raciais** fixos + escolhas (+1 em atributo à escolha)
- **Raças, Classes (16), Origens, Deuses** com validações cruzadas
- Bloqueios de regra aplicados automaticamente (ex.: Golem não escolhe Origem)

### Motor de Regras (backend, `app/src/regras/`)
- **PV/PM** com fontes nomeadas por habilidade no tooltip
  (ex.: `Sangue Mágico (+1 PM/nível)` em vez de genérico)
- **Perícias**: treino, slots de classe/INT, atributo-chave selecionável,
  Ofícios customizados, penalidade de armadura, bônus condicionais
- **Defesa & Deslocamento**: pilha de bônus explicada, deslocamentos especiais
  (natação 🧜‍♀️, voo 🪽) com toggle de forma
- **Combate**: BBA, ataques, bônus de dano por arma, proficiências
- **Magias**: grimório com ~198 magias, custo PM por círculo (Tabela 4-1),
  aprimoramentos, CD por atributo-chave, reduções condicionais de custo
- **Habilidades ativáveis**: custo PM, ação, duração, buffs com origem rastreada
- **Condições situacionais**: toggle no card da habilidade
  (🦎 Reptiliano, ⛰️ Conhecimento das Rochas) que alimenta `condicoes_ativas`
- **Histórico/level-up**: linha do tempo da ficha com level-up assistido
- **Inventário/equipamentos** com efeitos mecânicos

### UX de Escolhas
- **Modais de seleção** com busca, blacklist e listas restritas
  (ex.: Canção dos Mares oferece só as 6 magias da regra, com match exato)
- **Slots flexíveis**: perícia OU poder OU racial (Versátil, Memória Póstuma,
  Deformidade) com abas e troca de modo
- **Chips de escolha** nos cards com rótulos legíveis (`✨ Magia 1: Luz`)
- **Engenhosidade (Kliren)**: botão ⚡ por perícia, gasta 2 PM, soma INT no teste
- **Desejos (Qareen)**: botão 🧞 abre modal com as magias do grimório;
  a magia desejada custa −1 PM

### Persistência & Exportação
- Salvamento automático com debounce (PUT) + criação (POST) + exclusão (DELETE)
- Recálculo completo (`atualizar_ficha`) em todo GET/PUT — fonte única de verdade
- Descanso completo, buffs temporários, efeitos ativos por aba dedicada
- **Exportação da ficha em PDF** (`GET /personagens/{id}/pdf`, via pypdf)

### Ponte Roll20 (`t20-roll20-bridge/`)
- Extensão Manifest V3 que envia a ficha do T20 System para a ficha oficial
  JdA do Roll20 (perícias treinadas, dinheiro, campos da ficha principal)
- Detalhes do mapeamento em `docs/roll20-field-mapping.md`

---

## 🏗️ Arquitetura

```text
t20-system/
├── app/                                   # Backend (imagem t20-system-api)
│   ├── Dockerfile                         # Python 3.11-slim + Poetry
│   ├── pyproject.toml
│   ├── diagnostico.py
│   ├── src/
│   │   ├── main.py                        # App FastAPI + CORS + lifespan
│   │   ├── models.py                      # Modelos Pydantic (Personagem, Buff, StatCalculado...)
│   │   ├── dependencies.py                # Injeção do banco
│   │   ├── dados_*.py                     # Catálogos oficiais (raças, classes,
│   │   │                                  #   magias ×198, origens, deuses, perícias,
│   │   │                                  #   equipamentos, poderes, familiares...)
│   │   ├── routers/
│   │   │   ├── personagens.py             # CRUD de personagens
│   │   │   ├── dados.py                   # Catálogos (raças, magias, poderes...)
│   │   │   ├── historico.py               # Linha do tempo / level-up
│   │   │   ├── pdf.py                     # Exportação em PDF
│   │   │   └── admin.py
│   │   └── regras/                        # 🧮 MOTOR DE REGRAS
│   │       ├── __init__.py                # orquestrador atualizar_ficha()
│   │       ├── status.py                  # PV, PM, defesa, deslocamento
│   │       ├── atributos.py               # pool de pontos + modificadores
│   │       ├── pericias.py                # cálculo de perícias + condicionais
│   │       ├── combate.py                 # ataques, BBA, bônus de dano
│   │       ├── custo_magia.py             # custo PM, reduções, limites
│   │       ├── magias.py                  # grimório, círculos, aprimoramentos
│   │       ├── habilidades.py             # montagem de habilidades + escolhas
│   │       ├── poderes_arcanista.py       # familiares, linhagens, focos
│   │       ├── inventario.py              # equipamentos
│   │       ├── historico.py               # level-up assistido
│   │       └── utils.py
│   └── tests/                             # suíte pytest (16 arquivos, ~156 testes)
├── frontend/                              # Frontend (imagem t20-system-web)
│   ├── Dockerfile                         # Node 22 + Vite dev server :5173
│   ├── public/fonts/Tormenta.ttf          # fonte oficial T20
│   └── src/
│       ├── pages/                         # Home.tsx, Wizard.tsx, Ficha.tsx
│       ├── components/                    # AbilityCard, SkillList, RacialAbilityRow,
│       │                                  #   DesejosButton, StatusBars, modais...
│       ├── hooks/useFicha.ts              # estado global + autosave + catálogos
│       ├── services/api.ts                # cliente HTTP
│       └── types.ts                       # tipos do domínio
├── t20-roll20-bridge/                     # Extensão browser → ficha JdA Roll20
├── docs/
│   ├── roll20-field-mapping.md
│   └── checklists/                        # estado de features (rolagens, raças E2E...)
├── data/db/                               # volume do MongoDB
├── docker-compose.yml                     # db (:27017) + api (:8000) + web (:5173)
├── COMO_RODAR_LINUX.md / GUIA_COMPLETO_LINUX.md
└── README.md
```

### Fluxo de dados

```text
UI (React) ──updateFicha──▶ PUT /personagens/{id}
                                    │
                                    ▼
                        atualizar_ficha() ← recalcula TUDO (regras/)
                                    │
                                    ▼
                        MongoDB ──▶ resposta com campos calculados
                                    │
                                    ▼
                        ficha renderizada (tooltips com fontes)
```

---

## 🧬 Raças: status de validação

Catálogo ampliado em `dados_racas.py` (raças do JdA + monstros jogáveis como
Bugbear, Hobgoblin, Centauro, Gnoll, Kallyanach + variantes como
Suraggel Aggelus/Sulfure e Nagah). Núcleo validado por testes E2E:

| # | Raça | Habilidades validadas |
|---|---|---|
| 1 | Humano | Versátil |
| 2 | Elfo | Sangue Mágico, Graça de Glórienn, Sentidos Élficos |
| 3 | Anão | Conhecimento das Rochas ⛰️ |
| 4 | Goblin | Engenhoso, Espelunqueiro, Peste Esguia, Rato das Ruas |
| 5 | Kliren | Engenhosidade ⚡, Híbrido, Vanguardista |
| 6 | Qareen | Desejos 🧞, Resistência Elemental, Tatuagem Mística |
| 7 | Golem | Chassi, Criatura Artificial, Fonte Elemental, Propósito de Criação |
| 8 | Osteon | Memória Póstuma |
| 9 | Sereia/Tritão | Canção dos Mares, Transformação Anfíbia 🧜‍♀️ |
| 10 | Sílfide | Asas de Borboleta 🪽, Espírito da Natureza, Magia das Fadas |
| 11 | Suraggel | Herança Celestial + Abissal |
| 12 | Trog | Mau Cheiro, Mordida, Sangue Frio, Reptiliano 🦎 |
| 13 | Medusa | Olhar Atordoante 🐍, Sangue Serpente |
| 14 | Minotauro | Chifres, Couro Rígido, Faro |
| 15 | Dahllan | Amiga das Plantas, Armadura de Allihanna, Empatia Selvagem |
| 16 | Lefou | Cria da Tormenta, Deformidade |
| 17 | Hynne | (em validação — ver `docs/checklists/`) |

Estado detalhado por raça em `docs/checklists/racas-e2e.md`.

---

## 🏃 Como rodar

```bash
# Subir tudo (API :8000 + Web :5173 + Mongo :27017)
docker compose up -d --build
```

- App: http://localhost:5173 (`/` home · `/wizard` criação · `/ficha/:id` ficha)
- Docs interativas da API: http://localhost:8000/docs

### Testes

```bash
docker compose exec -T api python -m pytest tests/ -q
# 16 arquivos, ~156 testes do motor de regras
```

> ⚠️ Os testes rodam **dentro do container** (`docker compose exec api`).
> Fora do Docker não há `pytest` instalado — `python3 -m pytest` falha localmente.

### Diagnóstico rápido

```bash
docker compose ps          # 3 serviços esperados: t20_db, t20_api, t20_web
```

Guia passo a passo para Linux: `COMO_RODAR_LINUX.md`.

---

## 🧮 Convenções do motor de regras
- **StatCalculado**: todo valor exibido carrega `fontes[]` (fonte, categoria,
  valor) — é isso que alimenta os tooltips da UI.
- **Efeitos declarativos**: habilidades são dados (`dados_habilidades_raciais.py`)
  com chaves de efeito padronizadas (`bonus_pericia_condicional`,
  `magia_adicional_escolha`, `habilidade_ativavel`, `reducao_pm_condicional`...).
  Nova regra = nova chave de efeito + tratador em `regras/`.
- **Escolhas**: `escolhas_aplicadas` por habilidade; gatilhos numéricos vs. valores
  string são distinguidos para renderizar chips corretamente.
- **Mínimos e limites**: custo de magia mínimo 1 PM; limite de PM por magia = nível.

---

## 🗺️ Roadmap
- Hynne (Sorte/reroll) — validação E2E restante (`docs/checklists/racas-e2e.md`)
- Inventário de armas (destrava E2E de Mestre do Tridente e bônus de dano)
- Sistema de rolagens (consome Engenhosidade/Desejos automaticamente —
  ver `docs/checklists/rolagens.md`)
- R6: Símbolo Sagrado ativável, condicionais situacionais ampliados,
  stepper de aprimoramentos de magia
- Ponte Roll20: condições e dinheiro seguem manuais na mesa
  (ver `docs/checklists/roll20-bridge.md`)

---

## 🤝 Convenções de commit
Padrão Conventional Commits em português:
`feat(raça): ...` · `fix(componente): ...` · `refactor(motor): ...` · `docs(...): ...`

---

## 📜 Licença & Créditos
Sistema de fichas não-oficial, feito por fãs, para uso pessoal.
Tormenta20 é propriedade de seus autores/editora (Jambô).
Este projeto não substitui a compra do Tormenta20 Jogando com Deuses Avançado (JdA).
