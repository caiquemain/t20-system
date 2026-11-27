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
| **Backend** | Python 3.11+ · FastAPI · Pydantic v2 · Motor (Mongo assíncrono) · PyMuPDF |
| **Banco** | MongoDB 7.0 |
| **Frontend** | React 19 · TypeScript 5.9 · Vite 7 · react-router-dom 7 · axios |
| **Infra** | Docker Compose (api + web + db) |
| **Testes** | pytest (82 arquivos, 1.040 testes do motor de regras, suplementos e exportações) |
| **Extras** | Extensão de browser `t20-roll20-bridge` (Manifest V3) |

---

## ✨ Funcionalidades

### Criação de Personagem (Wizard + Home + Ficha)
- **Wizard** (`/wizard`) de criação passo a passo + edição (`/wizard/:id`)
- **Home** (`/`) com listagem das fichas salvas e atalhos rápidos
- **Atributos** por pool de pontos (10 iniciais) com tabela de custo crescente
- **Modificadores raciais** fixos + escolhas (+1 em atributo à escolha)
- **Raças, Classes (14 base + Treinador + 14 Variantes + Frade), Origens (Básicas + 66 Regionais + 30 Especiais), Deuses** com filtros por livro e validações cruzadas
- Bloqueios de regra aplicados automaticamente (ex.: Golem não escolhe Origem; Meio-Elfo exclui Constituição; multiclasse bloqueada entre classe básica e variante)

### Suplementos Oficiais ([`docs/SUPLEMENTOS.md`](./docs/SUPLEMENTOS.md))
- **Ameaças de Arton:** 40 raças jogáveis (incl. 12 Moreau), regras adicionais (Armas Naturais, condições `Avariado`/`Destruído`), equipamentos, materiais especiais, recursos naturais, itens mágicos, artefatos e 7 magias.
- **Heróis de Arton:** 5 raças (Duende com criação completa + *Sonhos Malucos*, Eiradaan, Galokk, Meio-Elfo, Sátiro), classe **Treinador** com motor completo do **Melhor Amigo**, **14 Classes Variantes**, **30 Origens Especiais**, **288 novos poderes de classe** (+ 7 efeitos de *Golpe Pessoal*), **155 novos poderes gerais** (25 Combate, 13 Destino, 14 Magia, 6 Tormenta, 77 Raça, 20 Grupo) e **Regras Opcionais opt-in** (73 Complicações, 7 Idades Variadas, 9 Papéis no Grupo, 7 Objetivos Heroicos, Defesa Épica).
- **Atlas de Arton:** 66 Origens Regionais com benefício único automático e escolhas interativas (*Duplo Feérico*, *Aspirante a Herói*, *Futura Lenda*, *Cosmopolita*, etc.).
- **Deuses de Arton:** fundação pronta para os próximos lotes.

### Bestiário & Grimório Global
- **Bestiário** (`/bestiario` e `/bestiario/:id`): catálogo com **297 monstros/ameaças** importados, busca/filtros, ficha detalhada e botão de envio direto para o Roll20
- **Grimório Global** (`/grimorio`): consulta completa de magias fora da ficha com filtros por círculo, escola e tipo

### Motor de Regras (backend, `app/src/regras/`)
- **PV/PM** com fontes nomeadas por habilidade no tooltip
  (ex.: `Sangue Mágico (+1 PM/nível)` em vez de genérico)
- **Perícias**: treino, slots de classe/INT, atributo-chave selecionável,
  Ofícios customizados, penalidade de armadura, bônus condicionais
- **Defesa & Deslocamento**: pilha de bônus explicada, deslocamentos especiais
  (natação, voo) com toggle de forma
- **Combate**: BBA, ataques, bônus de dano por arma, proficiências, ficha automática do Melhor Amigo (`treinador_calc`)
- **Classes**: 14 classes do Livro Básico + Treinador + 14 Classes Variantes (ver `docs/checklists/classes-livro-basico.md` e `docs/SUPLEMENTOS.md`)
- **Magias**: grimório com 205+ magias (JdA + Ameaças), custo PM por círculo (Tabela 4-1),
  aprimoramentos, CD por atributo-chave, reduções condicionais de custo
- **Habilidades ativáveis**: custo PM, ação, duração, buffs com origem rastreada
- **Condições situacionais**: toggle no card da habilidade
  (Reptiliano, Conhecimento das Rochas) que alimenta `condicoes_ativas`
- **Histórico/level-up**: linha do tempo da ficha com level-up assistido
- **Inventário/equipamentos** com efeitos mecânicos e condições de item (`Avariado` / `Destruído`)

### UX de Escolhas
- **Painel unificado de escolhas dinâmicas** (`EscolhasDinamicasPanel.tsx` alimentado por `GET /dados/escolhas`) no Wizard e na Ficha
- **Modais de seleção** com busca, filtros por livro, blacklist e listas restritas
  (ex.: Canção dos Mares oferece só as 6 magias da regra, com match exato)
- **Slots flexíveis**: perícia OU poder OU racial (Versátil, Memória Póstuma,
  Deformidade) com abas e troca de modo
- **Chips de escolha** nos cards com rótulos legíveis (`Magia 1: Luz`)
- **Engenhosidade (Kliren)**: botão por perícia, gasta 2 PM, soma INT no teste
- **Desejos (Qareen)**: botão abre modal com as magias do grimório;
  a magia desejada custa −1 PM

### Persistência & Exportação
- Salvamento automático com debounce (PUT) + criação (POST) + exclusão (DELETE)
- Recálculo completo (`atualizar_ficha`) em todo GET/PUT — fonte única de verdade
- Descanso completo, buffs temporários, efeitos ativos por aba dedicada
- **Exportação da ficha em PDF** (`GET /personagens/{id}/pdf`, via **PyMuPDF**)
- **Exportação editável para LibreOffice** em **ODT** (`GET /personagens/{id}/odt`) e **ODG** (`GET /personagens/{id}/odg`)

### Ponte Roll20 (`t20-roll20-bridge/`)
- Extensão Manifest V3 que envia a ficha do T20 System (e ameaças do Bestiário) para a ficha oficial
  JdA do Roll20 (perícias treinadas, dinheiro, ataques, poderes, magias, equipamentos)
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
│   └── tests/                             # suíte pytest (82 arquivos, 1.040 testes)
├── frontend/                              # Frontend (imagem t20-system-web)
│   ├── Dockerfile                         # Node 22 + Vite dev server :5173
│   ├── public/fonts/Tormenta.ttf          # fonte oficial T20
│   └── src/
│       ├── pages/                         # Home.tsx, Wizard.tsx, Ficha.tsx
│       ├── components/                    # AbilityCard, SkillList, RacialAbilityRow,
│       │                                  #   EscolhasDinamicasPanel, StatusBars, modais...
│       ├── hooks/useFicha.ts              # estado global + autosave + catálogos
│       ├── services/api.ts                # cliente HTTP
│       └── types.ts                       # tipos do domínio
├── t20-roll20-bridge/                     # Extensão browser → ficha JdA Roll20
├── docs/
│   ├── SUPLEMENTOS.md                     # arquitetura e progresso dos suplementos oficiais
│   ├── roll20-field-mapping.md
│   └── checklists/                        # estado de features (suplementos, raças E2E...)
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
| 17 | Hynne | Arremessador, Pequeno e Rechonchudo, Sorte Salvadora (reroll na Fase de Rolagens) |

Estado detalhado por raça em `docs/checklists/racas-e2e.md`.

---

## 🏃 Como rodar do zero

### Opção A — Com Docker Compose (recomendado)

**Pré-requisitos:** [Git](https://git-scm.com/) e [Docker](https://docs.docker.com/get-docker/) com Docker Compose (`docker compose version`).

**1. Clone o repositório e entre na pasta:**
```bash
git clone https://github.com/caiquemain/t20-system.git
cd t20-system
```

**2. Construa e suba todos os serviços** (`MongoDB :27017` + `API FastAPI :8000` + `Frontend Vite :5173`):
```bash
docker compose up -d --build
```
> O `docker-compose.yml` já configura healthcheck no MongoDB (`t20_db`) e só inicia a API (`t20_api`) quando o banco estiver saudável, além de retry automático de conexão na inicialização.

**3. Verifique se os 3 containers estão de pé:**
```bash
docker compose ps
# Esperado: t20_db (healthy), t20_api (Up), t20_web (Up)
```

**4. Acesse no navegador:**
- **Aplicação Web:** http://localhost:5173
  - `/` Home · `/wizard` Criação de Personagem · `/ficha/:id` Ficha · `/bestiario` Bestiário · `/grimorio` Grimório Global
- **Documentação interativa da API (Swagger):** http://localhost:8000/docs

**Comandos úteis do Docker:**
```bash
docker compose logs -f api        # acompanhar logs do backend
docker compose logs -f web        # acompanhar logs do frontend
docker compose down               # parar e remover containers (mantém o banco)
docker compose down -v            # parar e APAGAR o volume do MongoDB (reset total)
```

> **Solução rápida de rede/DNS no Docker:** se a API exibir `Temporary failure in name resolution` ao tentar conectar em `db:27017` (comum quando uma rede antiga fica órfã no Docker Desktop), recrie os containers e a rede com:
> ```bash
> docker compose down --remove-orphans && docker network prune -f && docker compose up -d --force-recreate
> ```

---

### Opção B — Rodando localmente sem Docker (dev nativo)

**Pré-requisitos:** Python 3.11+, [Poetry](https://python-poetry.org/docs/#installation), Node.js 22+ (`npm`) e MongoDB 7.0 rodando na porta `27017`.

**1. Suba o MongoDB** (localmente ou apenas o container do banco):
```bash
docker compose up -d db
```

**2. Instale e inicie o Backend (FastAPI na porta `8000`):**
```bash
cd app
poetry install
MONGO_URI=mongodb://localhost:27017/tormenta20 poetry run uvicorn src.main:app --reload --port 8000
```

**3. Em outro terminal, instale e inicie o Frontend (Vite na porta `5173`):**
```bash
cd frontend
npm install
VITE_API_URL=http://localhost:8000 npm run dev
```

---

### Testes e Build

**Backend (82 arquivos · 1.040 testes):**
```bash
# Via Docker:
docker compose exec -T api python -m pytest tests/ -q

# Ou localmente via Poetry:
cd app && poetry run pytest -q
```

**Frontend (verificação TypeScript + build de produção + lint):**
```bash
cd frontend
npm run build
npm run lint
```

### Extensão Roll20 (`t20-roll20-bridge/`)
1. Abra `chrome://extensions` (Chrome, Edge ou Brave).
2. Ative o **Modo do desenvolvedor** no canto superior direito.
3. Clique em **Carregar sem compactação** e selecione a pasta `t20-roll20-bridge/`.

Guia detalhado para Linux: [`COMO_RODAR_LINUX.md`](./COMO_RODAR_LINUX.md).

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

## 🗺️ Roadmap & Plano de Ação
O plano detalhado e priorizado para fechar 100% do **Livro Básico (T20 JdA)** está em [**`docs/PLANO_DE_ACAO.md`**](./docs/PLANO_DE_ACAO.md):
- **Fase 1:** Fechar dívidas das raças base (filtro Livro Básico vs. suplementos, `resistencia_veneno`, `deslocamento_escalada_igual`, reaprendizado)
- **Fase 2:** Migrar emojis Unicode para biblioteca SVG moderna (`lucide-react` + componente `<T20Icon />`) — ver `docs/checklists/icones-ui.md`
- **Fase 3:** Completar as 12 classes restantes do Livro Básico (hoje 2/14 completas) — ver `docs/checklists/classes-livro-basico.md`
- **Fase 4:** Modelar efeitos nos Poderes Concedidos (20/20) e Poderes Gerais faltantes
- **Fase 5:** Sistema de rolagens (`docs/checklists/rolagens.md`), refinamentos de PDF (`docs/checklists/pdf.md`), Roll20 (`docs/checklists/roll20-bridge.md`) e ESLint

---

## 🤝 Convenções de commit
Padrão Conventional Commits em português:
`feat(raça): ...` · `fix(componente): ...` · `refactor(motor): ...` · `docs(...): ...`

---

## 📜 Licença & Créditos
Sistema de fichas não-oficial, feito por fãs, para uso pessoal.
Tormenta20 é propriedade de seus autores/editora (Jambô).
Este projeto não substitui a compra do Tormenta20 Jogando com Deuses Avançado (JdA).
