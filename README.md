# Grimório T20 - Sistema de Gerenciamento de Fichas

Sistema web completo para criação, gerenciamento e automação de fichas de personagens para o sistema de RPG **Tormenta 20 (Jogo do Ano)**.

O projeto utiliza uma arquitetura moderna separando as Regras de Negócio (Backend) da Interface (Frontend), garantindo que cálculos complexos como PV, PM, Defesa e Perícias sejam sempre consistentes.

## 🚀 Tecnologias

### Backend (API de Regras)
* **Python 3.11+**
* **FastAPI**: Framework de alta performance para APIs.
* **MongoDB (Motor)**: Banco de dados NoSQL para armazenar as fichas flexíveis.
* **Pydantic**: Validação rigorosa de dados e modelos.

### Frontend (Interface)
* **React 18 + TypeScript**: Interface reativa e tipada.
* **Vite**: Build tool rápida.
* **CSS Modules**: Estilização modular.
* **Axios**: Comunicação com a API.

---

## ✨ Funcionalidades Implementadas

### 1. Criação de Personagem
* Seleção de **Raça**, **Classe** e **Origem** com carregamento dinâmico de dados.
* **Sistema de Pontos de Atributo**: Compra de atributos com validação de custo (-1 a 4) e aplicação automática de bônus raciais (fixos ou escolha).

### 2. Automação de Regras
* **Validação de Pré-requisitos**: O sistema bloqueia a seleção de poderes caso o personagem não cumpra requisitos de Atributo, Nível, Perícia ou outros Poderes.
* **Prevenção de Duplicatas**: Lógica inteligente que impede selecionar a mesma perícia ou poder duas vezes através de fontes diferentes (ex: Origem vs Raça).
* **Cálculo em Tempo Real**:
    * **PV e PM**: Detalhados por (Inicial + Nível + Con/Atributo + Outros).
    * **Defesa e Deslocamento**: Calculados automaticamente com base em atributos e equipamentos.
    * **Perícias**: Cálculo automático de bônus de nível (1/2), treino e atributos.

### 3. Grimório de Magias
* Banco de dados completo de magias (Arcanas, Divinas, Universais).
* Filtros por Círculo, Escola e Tipo.
* Adição rápida de magias à ficha do personagem.

### 4. Interface Rica
* **Tooltips**: Ao passar o mouse sobre qualquer status (Vida, Mana, Defesa), o sistema mostra a fórmula matemática exata usada para chegar naquele valor.
* **Modais de Seleção**: Interfaces de busca para Poderes e Perícias com filtros visuais (Tags coloridas).

---

## 📂 Estrutura do Projeto

```text
t20-system/
├── src/ (Backend)
│   ├── main.py             # Rotas da API
│   ├── regras.py           # Motor de Regras (Cálculos de T20)
│   ├── models.py           # Estrutura do Banco de Dados
│   └── dados_*.py          # Bancos de dados estáticos (Raças, Itens, Magias...)
│
├── frontend/src/ (Frontend)
│   ├── components/         # Componentes visuais (Modais, Cards)
│   ├── hooks/              # Lógica de Estado (useFicha)
│   ├── pages/              # Páginas (Home, Ficha)
│   ├── services/           # Comunicação com API
│   ├── utils/              # Validadores de Regras no Front
│   └── types/              # Tipagem TypeScript
│
└── docker-compose.yml      # Orquestração dos containers

🛠️ Como Rodar
O projeto é totalmente containerizado com Docker.

Pré-requisitos: Tenha o Docker e Docker Compose instalados.

Iniciar:

Bash

docker-compose up --build
Acessar:

Frontend: http://localhost:5173

API Docs (Swagger): http://localhost:8000/docs

🛡️ Status do Desenvolvimento
[x] Atributos e Status Base

[x] Perícias e Treinamentos

[x] Sistema de Raças (Bônus fixos e escolhas)

[x] Sistema de Origens (Benefícios e Itens)

[x] Habilidades de Classe e Poderes (Com validação de requisitos)

[x] Grimório de Magias

[ ] Inventário Avançado (Equipar itens altera status)

[ ] Ataques e Combate Automatizado

Projeto desenvolvido para facilitar a vida de jogadores de Tormenta 20.