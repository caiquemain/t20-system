# 🚀 Guia Completo: Como Rodar o Sistema T20 no Linux

Este guia assume que você tem **apenas o VS Code instalado** em uma distribuição Linux (Ubuntu, Debian, Fedora, etc).

---

## 📋 PRÉ-REQUISITOS

### 1. Instalar Node.js e npm (Frontend)

```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verificar instalação
node --version  # Deve mostrar v20.x.x
npm --version   # Deve mostrar 10.x.x ou superior
```

### 2. Instalar Python 3.11+ (Backend)

```bash
# Ubuntu/Debian (geralmente já vem instalado)
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

# Verificar instalação
python3 --version  # Deve mostrar Python 3.11 ou superior
pip3 --version
```

### 3. Instalar MongoDB (Banco de Dados)

**Opção A: Usando Docker (Recomendado)**
```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Reiniciar o terminal ou fazer logout/login para aplicar as mudanças no grupo
# Verificar instalação
docker --version
```

**Opção B: Instalação Nativa (Sem Docker)**
```bash
# Ubuntu/Debian
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt update
sudo apt install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

---

## 🔧 CONFIGURAÇÃO DO PROJETO

### Passo 1: Abrir o Projeto no VS Code

```bash
# Navegue até a pasta do projeto
cd /caminho/para/seu/projeto/t20-system

# Abrir no VS Code
code .
```

### Passo 2: Corrigir Arquivos do Frontend

O projeto já está corrigido, mas se precisar criar o arquivo de perícias manualmente:

```bash
# Criar diretório de dados
mkdir -p frontend/src/data

# Criar arquivo pericias.ts
cat > frontend/src/data/pericias.ts << 'EOF'
/**
 * Dados básicos de perícias para exibição no frontend
 */

export interface DadoPericia {
  atributo: string;
  treino_apenas?: boolean;
  penalidade_armadura?: boolean;
}

export const DADOS_PERICIAS_FRONTEND: Record<string, DadoPericia> = {
  'Acrobacia': { atributo: 'des', penalidade_armadura: true },
  'Atletismo': { atributo: 'for', penalidade_armadura: true },
  'Cavalgar': { atributo: 'des', penalidade_armadura: true },
  'Conhecimento (Arcano)': { atributo: 'int' },
  'Conhecimento (História)': { atributo: 'int' },
  'Conhecimento (Mundo)': { atributo: 'int' },
  'Conhecimento (Natureza)': { atributo: 'int' },
  'Conhecimento (Religião)': { atributo: 'int' },
  'Cura': { atributo: 'sab' },
  'Diplomacia': { atributo: 'car' },
  'Enganação': { atributo: 'car' },
  'Furtividade': { atributo: 'des', penalidade_armadura: true },
  'Guerra': { atributo: 'int' },
  'Iniciativa': { atributo: 'des' },
  'Intimidação': { atributo: 'car' },
  'Intuição': { atributo: 'sab' },
  'Investigação': { atributo: 'int' },
  'Luta': { atributo: 'for' },
  'Notação': { atributo: 'sab' },
  'Ofício': { atributo: 'int' },
  'Percepção': { atributo: 'sab' },
  'Pontaria': { atributo: 'des' },
  'Reflexos': { atributo: 'des', penalidade_armadura: true },
  'Reconhecimento': { atributo: 'sab' },
  'Relacionamento': { atributo: 'car' },
  'Sobrevivência': { atributo: 'sab' },
  'Vontade': { atributo: 'sab' },
};

export default DADOS_PERICIAS_FRONTEND;
EOF
```

---

## 🎯 OPÇÃO 1: RODAR COM DOCKER (RECOMENDADO)

Esta é a maneira mais fácil e isolada de rodar todo o sistema.

### Passo 1: Iniciar Todos os Serviços

```bash
# No diretório raiz do projeto (/workspace ou onde estiver o docker-compose.yml)
docker-compose up --build
```

### Passo 2: Acessar o Sistema

- **Frontend**: http://localhost:5173
- **API Docs (Swagger)**: http://localhost:8000/docs
- **MongoDB**: localhost:27017

### Comandos Úteis Docker

```bash
# Ver logs em tempo real
docker-compose logs -f

# Parar todos os serviços
docker-compose down

# Reiniciar serviços
docker-compose restart

# Ver status dos containers
docker-compose ps

# Limpar tudo e reconstruir
docker-compose down -v && docker-compose up --build
```

---

## 🎯 OPÇÃO 2: RODAR LOCALMENTE (SEM DOCKER)

Use esta opção se não quiser usar Docker ou se for fazer desenvolvimento mais detalhado.

### Passo 1: Iniciar o MongoDB

**Se usou Docker para MongoDB:**
```bash
docker run -d -p 27017:27017 --name t20_db mongo:latest
```

**Se instalou MongoDB nativamente:**
```bash
# O MongoDB já deve estar rodando como serviço
sudo systemctl status mongod
```

### Passo 2: Configurar e Rodar o Backend

```bash
# Navegar até o backend
cd /caminho/para/projeto/app

# Criar ambiente virtual (opcional mas recomendado)
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install fastapi uvicorn motor pydantic python-dotenv

# Rodar o servidor (em um terminal)
# Se MongoDB estiver no Docker:
MONGO_URI=mongodb://localhost:27017/tormenta20 uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Se MongoDB for nativo:
MONGO_URI=mongodb://127.0.0.1:27017/tormenta20 uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

O backend estará disponível em: http://localhost:8000
Documentação da API: http://localhost:8000/docs

### Passo 3: Configurar e Rodar o Frontend

```bash
# Abrir NOVO terminal e navegar até o frontend
cd /caminho/para/projeto/frontend

# Instalar dependências
npm install

# Rodar em modo desenvolvimento
npm run dev
```

O frontend estará disponível em: http://localhost:5173

---

## ✅ VERIFICAÇÃO DE FUNCIONAMENTO

### Testar Backend

```bash
# Em um novo terminal
curl http://localhost:8000/api/racas
# Deve retornar uma lista de raças em JSON
```

### Testar Frontend

1. Abra o navegador em http://localhost:5173
2. Você deve ver a tela "Grimório T20"
3. Clique em "+ Novo Personagem"
4. Preencha os dados básicos e teste o sistema

### Testar API Completa

```bash
# Criar personagem de teste
curl -X POST http://localhost:8000/api/personagens \
  -H "Content-Type: application/json" \
  -d '{
    "cabecalho": {"nome": "Teste", "raca": "Humano", "origem": "Acólito", "nivel_total": 1},
    "classes": [{"nome": "Guerreiro", "nivel": 1}],
    "atributos_base": {"forca": 2, "destreza": 0, "constituicao": 0, "inteligencia": 0, "sabedoria": 0, "carisma": 0}
  }'
```

---

## 🐛 SOLUÇÃO DE PROBLEMAS

### Problema: Erro de conexão com MongoDB

**Solução:**
```bash
# Verificar se MongoDB está rodando
docker ps | grep mongo
# OU
sudo systemctl status mongod

# Se estiver usando Docker, reiniciar container
docker restart t20_db

# Verificar URI de conexão no main.py
# Deve ser: mongodb://localhost:27017/tormenta20 (local)
# Ou: mongodb://db:27017/tormenta20 (Docker Compose)
```

### Problema: Frontend não carrega

**Solução:**
```bash
# Limpar cache e reinstalar
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Problema: Erro de porta já em uso

**Solução:**
```bash
# Matar processos nas portas
sudo lsof -ti:8000 | xargs kill -9
sudo lsof -ti:5173 | xargs kill -9
sudo lsof -ti:27017 | xargs kill -9
```

### Problema: TypeScript errors no build

**Solução:**
Os arquivos já foram corrigidos, mas se aparecerem novos erros:
```bash
cd frontend
# Verificar erros específicos
npm run build

# Se faltar o arquivo pericias.ts, criar conforme passo 2 acima
```

---

## 📁 ESTRUTURA DE ARQUIVOS

```
/workspace/
├── app/                    # Backend Python/FastAPI
│   ├── src/
│   │   ├── main.py        # Ponto de entrada da API
│   │   ├── models.py      # Modelos de dados
│   │   ├── regras/        # Regras de negócio T20
│   │   └── dados_*.py     # Dados estáticos (raças, classes, etc)
│   └── requirements.txt
│
├── frontend/              # Frontend React/TypeScript
│   ├── src/
│   │   ├── components/    # Componentes React
│   │   ├── hooks/         # Hooks personalizados
│   │   ├── pages/         # Páginas (Home, Ficha)
│   │   ├── services/      # API calls
│   │   ├── data/          # Dados estáticos frontend
│   │   └── types.ts       # Tipagem TypeScript
│   └── package.json
│
├── docker-compose.yml     # Orquestração Docker
└── README.md
```

---

## 🎮 FLUXO DE TRABALHO RECOMENDADO

### Para Desenvolvimento Diário

**Terminal 1 - Backend:**
```bash
cd /workspace/app
source venv/bin/activate  # se usar venv
MONGO_URI=mongodb://localhost:27017/tormenta20 uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd /workspace/frontend
npm run dev
```

**Terminal 3 - MongoDB (se usar Docker):**
```bash
docker run -d -p 27017:27017 --name t20_db mongo:latest
# OU, se já estiver rodando:
docker logs -f t20_db
```

### Para Produção/Testes

```bash
cd /workspace
docker-compose up --build -d  # -d roda em background
```

---

## 📚 PRÓXIMOS PASSOS

Depois de rodar o sistema:

1. **Crie seu primeiro personagem** em http://localhost:5173
2. **Explore a API** em http://localhost:8000/docs
3. **Teste as funcionalidades**:
   - Selecionar raça, classe e origem
   - Distribuir pontos de atributo
   - Escolher perícias treinadas
   - Selecionar poderes de classe
   - Adicionar magias ao grimório

---

## 🔗 LINKS ÚTEIS

- **Documentação FastAPI**: https://fastapi.tiangolo.com/
- **React Docs**: https://react.dev/
- **MongoDB Docs**: https://www.mongodb.com/docs/
- **Tormenta 20**: https://jambow.com.br/tormenta20/

---

## ✨ STATUS DO PROJETO

✅ **Funcionalidades Implementadas:**
- Criação completa de personagens
- Sistema de atributos com pontos
- Perícias com cálculos automáticos
- Habilidades de classe, raciais e origens
- Grimório de magias
- Validação de pré-requisitos
- Interface responsiva com tooltips

🚧 **Em Desenvolvimento:**
- Inventário avançado com equipamentos
- Sistema de combate automatizado
- Exportação de fichas em PDF
- Autenticação de usuários

---

**Desenvolvido com ❤️ para a comunidade de Tormenta 20**
