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
| **Backend** | Python 3.11+ · FastAPI · Pydantic v2 |
| **Banco** | MongoDB (driver assíncrono) |
| **Frontend** | React 18 · TypeScript · Vite |
| **Infra** | Docker Compose (api + web + db) |
| **Testes** | pytest (100+ testes de regras) |

---

## ✨ Funcionalidades

### Criação de Personagem
- **Atributos** por pool de pontos (10 iniciais) com tabela de custo crescente
- **Modificadores raciais** fixos + escolhas (+1 em atributo à escolha)
- **Raças** (17 cadastradas), **Classes**, **Origens**, **Deuses** com validações cruzadas
- Bloqueios de regra aplicados automaticamente (ex.: Golem não escolhe Origem)

### Motor de Regras (backend)
- **PV/PM** com fontes nomeadas por habilidade no tooltip
  (ex.: `Sangue Mágico (+1 PM/nível)` em vez de genérico)
- **Perícias**: treino, slots de classe/INT, atributo-chave selecionável,
  Ofícios customizados, penalidade de armadura, bônus condicionais
- **Defesa & Deslocamento**: pilha de bônus explicada, deslocamentos especiais
  (natação 🧜‍♀️, voo 🪽) com toggle de forma
- **Combate**: BBA, ataques, bônus de dano por arma, proficiências
- **Magias**: grimório, custo PM por círculo (Tabela 4-1), aprimoramentos,
  CD por atributo-chave, reduções condicionais de custo
- **Habilidades ativáveis**: custo PM, ação, duração, buffs com origem rastreada
- **Condições situacionais**: toggle no card da habilidade
  (🦎 Reptiliano, ⛰️ Conhecimento das Rochas) que alimenta `condicoes_ativas`

### UX de Escolhas
- **Modais de seleção** com busca, blacklist e listas restritas
  (ex.: Canção dos Mares oferece só as 6 magias da regra, com match exato)
- **Slots flexíveis**: perícia OU poder OU racial (Versátil, Memória Póstuma,
  Deformidade) com abas e troca de modo
- **Chips de escolha** nos cards com rótulos legíveis (`✨ Magia 1: Luz`)
- **Engenhosidade (Kliren)**: botão ⚡ por perícia, gasta 2 PM, soma INT no teste
- **Desejos (Qareen)**: botão 🧞 abre modal com as magias do grimório;
  a magia desejada custa −1 PM

### Persistência
- Salvamento automático com debounce (PUT) + criação (POST) + exclusão (DELETE)
- Recálculo completo (`atualizar_ficha`) em todo GET/PUT — fonte única de verdade
- Descanso completo, buffs temporários, efeitos ativos por aba dedicada

---

## 🏗️ Arquitetura

```text
t20-system/
├── app/
│   └── src/
│       ├── main.py                        # App FastAPI + CORS + lifespan
│       ├── models.py                      # Modelos Pydantic (Personagem, Buff, StatCalculado...)
│       ├── dependencies.py                # Injeção do banco
│       ├── dados_classes.py               # Dados oficiais: classes
│       ├── dados_pericias.py              # Dados oficiais: perícias
│       ├── dados_habilidades_raciais.py   # Efeitos estruturados por raça
│       ├── routers/
│       │   ├── personagens.py             # CRUD de personagens
│       │   ├── dados.py                   # Catálogos (raças, magias, poderes...)
│       │   └── admin.py
│       └── regras/                        # 🧮 MOTOR DE REGRAS
│           ├── __init__.py                # orquestrador atualizar_ficha()
│           ├── status.py                  # PV, PM, defesa, deslocamento
│           ├── pericias.py                # cálculo de perícias + condicionais
│           ├── combate.py                 # ataques, BBA, bônus de dano
│           ├── custo_magia.py             # custo PM, reduções, limites
│           ├── habilidades.py             # montagem de habilidades + escolhas
│           └── poderes_arcanista.py       # familiares, linhagens, focos
├── frontend/
│   ├── public/fonts/Tormenta.ttf          # fonte oficial T20
│   └── src/
│       ├── components/                    # AbilityCard, SkillList, RacialAbilityRow,
│       │                                  #   DesejosButton, StatusBars, modais...
│       ├── pages/Ficha.tsx                # página principal da ficha
│       ├── hooks/useFicha.ts              # estado global + autosave + catálogos
│       ├── services/api.ts                # cliente HTTP
│       └── types.ts                       # tipos do domínio
├── tests/                                 # suíte pytest do motor de regras
└── docker-compose.yml
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

| # | Raça | Habilidades validadas |
|---|---|---|
| 1 | Humano | Versátil |
| 2 | Elfo | Sangue Mágico, Graça de Glórienn, Sentidos Élficos |
| 3 | Anão | Conhecimento das Rochas ⛰️ |
| 4 | Goblin | — |
| 5 | Kliren | Engenhosidade ⚡, Híbrido, Vanguardista |
| 6 | Qareen | Desejos 🧞, Resistência Elemental, Tatuagem Mística |
| 7 | Golem | Chassi, Criatura Artificial, Fonte Elemental, Propósito de Criação |
| 8 | Osteon | Memória Póstuma |
| 9 | Sereia | Canção dos Mares, Transformação Anfíbia 🧜‍♀️ |
| 10 | Sílfide | Asas de Borboleta 🪽, Espírito da Natureza, Magia das Fadas |
| 11 | Suraggel | Herança Celestial + Abissal |
| 12 | Trog | Mau Cheiro, Mordida, Sangue Frio, Reptiliano 🦎 |
| 13 | Medusa | Olhar Atordoante 🐍, Sangue Serpente |

**Em fila:** Minotauro · Dahllan · Lefou · Hynne

---

## 🏃 Como rodar

```bash
# Subir tudo (API :8000 + Web :5173 + Mongo)
docker compose up -d --build
```

- Frontend: http://localhost:5173
- Docs interativas da API: http://localhost:8000/docs

### Testes

```bash
docker compose exec -T api python -m pytest tests/ -q
```

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
- Minotauro / Dahllan / Lefou / Hynne (validação E2E)
- Inventário de armas (destrava E2E de Mestre do Tridente e bônus de dano)
- Sistema de rolagens (consome Engenhosidade/Desejos automaticamente)
- R6: Símbolo Sagrado ativável, condicionais situacionais ampliados,
  stepper de aprimoramentos de magia
- Sorte (Hynne): motor de reroll integrado às rolagens
- Exportação da ficha em PDF

---

## 🤝 Convenções de commit
Padrão Conventional Commits em português:
`feat(raça): ...` · `fix(componente): ...` · `refactor(motor): ...`

---

## 📜 Licença & Créditos
Sistema de fichas não-oficial, feito por fãs, para uso pessoal.
Tormenta20 é propriedade de seus autores/editora (Jambô).
Este projeto não substitui a compra do Tormenta20 Jogando com Deuses Avançado (JdA).
