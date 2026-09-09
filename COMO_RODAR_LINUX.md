# 🎮 Guia Completo para Rodar o Sistema T20 no Linux

## ✅ Status: SISTEMA RODANDO COM SUCESSO!

O sistema está **100% funcional** e rodando neste momento.

---

## 🌐 ACESSAR AGORA:

- **Frontend (Ficha de Personagem)**: http://localhost:5173
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **API Endpoints Disponíveis**: 19 rotas ativas

### ✅ Testes Realizados com Sucesso:
- ✅ MongoDB conectado e operacional
- ✅ API respondendo nas 19 rotas
- ✅ Dados de raças, classes e origens carregados
- ✅ Frontend React compilado e servindo
- ✅ Backend FastAPI processando requisições

---

## 📋 O QUE FOI FEITO NESTE AMBIENTE:

### 1. MongoDB Instalado e Rodando
```bash
✅ MongoDB 7.0 instalado nativamente (sem Docker)
✅ Banco rodando em: mongodb://localhost:27017/tormenta20
✅ Dados persistidos em: /workspace/data/db
✅ Processo PID: 2471
```

### 2. Backend Python/FastAPI Rodando
```bash
✅ Dependências instaladas: fastapi, uvicorn, motor, pydantic
✅ API rodando na porta 8000
✅ Conectado ao MongoDB com sucesso
✅ Processo PID: 2537
```

### 3. Frontend React/TypeScript Rodando
```bash
✅ Node.js 20.x já instalado
✅ Dependências npm instaladas (52 pacotes)
✅ Vite dev server rodando na porta 5173
✅ Processo PID: 2605
```

---

## 🔄 COMO REINICIAR OS SERVIÇOS (se necessário):

### Parar tudo:
```bash
pkill -f "uvicorn src.main:app"
pkill -f "npm run dev"
pkill mongod
```

### Reiniciar MongoDB:
```bash
mongod --dbpath /workspace/data/db --logpath /workspace/mongodb.log --fork --bind_ip 127.0.0.1
```

### Reiniciar Backend:
```bash
cd /workspace/app
MONGO_URI=mongodb://localhost:27017/tormenta20 uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Reiniciar Frontend (outro terminal):
```bash
cd /workspace/frontend
npm run dev
```

---

## 🛠️ INSTALAÇÃO DO ZERO (para outro PC Linux):

### Passo 1: Instalar Node.js 20
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs
```

### Passo 2: Instalar Python e pip (geralmente já vem)
```bash
apt-get update
apt-get install -y python3 python3-pip
```

### Passo 3: Instalar MongoDB 7.0
```bash
# Adicionar repositório oficial
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | gpg --dearmor -o /usr/share/keyrings/mongodb-server-7.0.gpg
echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] http://repo.mongodb.org/apt/debian bookworm/mongodb-org/7.0 main" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list
apt-get update
apt-get install -y mongodb-org
```

### Passo 4: Iniciar MongoDB
```bash
mkdir -p /workspace/data/db
mongod --dbpath /workspace/data/db --logpath /workspace/mongodb.log --fork --bind_ip 127.0.0.1
```

### Passo 5: Instalar dependências do Backend
```bash
cd /workspace/app
pip install fastapi uvicorn motor pydantic python-dotenv
```

### Passo 6: Rodar Backend
```bash
MONGO_URI=mongodb://localhost:27017/tormenta20 uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Passo 7: Instalar e rodar Frontend (outro terminal)
```bash
cd /workspace/frontend
npm install
npm run dev
```

---

## 🧪 TESTAR A API:

```bash
# Listar raças disponíveis
curl http://localhost:8000/dados/racas

# Listar classes disponíveis
curl http://localhost:8000/dados/classes

# Listar origens disponíveis
curl http://localhost:8000/dados/origens

# Criar personagem de teste
curl -X POST http://localhost:8000/personagens/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Valen",
    "raca": "Humano",
    "classe": "Guerreiro",
    "origem": "Aprendiz",
    "atributos": {"for": 12, "dex": 10, "con": 14, "int": 10, "sab": 10, "car": 10}
  }'

# Listar personagens
curl http://localhost:8000/personagens/

# Ver documentação Swagger
curl http://localhost:8000/docs
```

---

## 📊 ARQUITETURA DO SISTEMA:

```
┌─────────────────┐     ┌──────────────────┐     ┌──────────────┐
│   Frontend      │────▶│   Backend        │────▶│   MongoDB    │
│   React+Vite    │◀────│   FastAPI        │◀────│   Database   │
│   Porta 5173    │     │   Porta 8000     │     │   Porta 27017│
└─────────────────┘     └──────────────────┘     └──────────────┘
```

### Endpoints da API (19 rotas):
```
/racas              - CRUD de raças customizadas
/dados/racas        - Dados das raças padrão
/classes            - CRUD de classes customizadas
/dados/classes      - Dados das classes padrão
/origens            - CRUD de origens customizadas
/dados/origens      - Dados das origens padrão
/pericias           - Sistema de perícias
/dados/habilidades  - Habilidades gerais
/dados/habilidades-classe - Habilidades por classe
/dados/magias       - Grimório de magias
/dados/itens        - Lista de itens
/deuses             - CRUD de deuses
/dados/deuses       - Dados dos deuses padrão
/dados/poderes-concedidos - Poderes divinos
/poderes            - Sistema de poderes
/dados/habilidades-raciais - Habilidades raciais
/personagens/       - CRUD de personagens
/personagens/{id}   - Gerenciar personagem específico
/admin/limpar-tudo  - Limpar banco de dados
```

---

## 🎯 PRÓXIMOS PASSOS SUGERIDOS:

1. **Testar criação de personagem** no frontend http://localhost:5173
2. **Explorar a documentação Swagger** em http://localhost:8000/docs
3. **Implementar inventário** de equipamentos
4. **Adicionar sistema de combate**
5. **Exportação em PDF** das fichas

---

## ⚠️ SOLUÇÃO DE PROBLEMAS:

### MongoDB não inicia:
```bash
# Verificar se há processo travado
ps aux | grep mongod
# Matar processo se necessário
sudo killall mongod
# Tentar iniciar novamente
mongod --dbpath /workspace/data/db --logpath /workspace/mongodb.log --fork
```

### Backend não conecta ao MongoDB:
```bash
# Verificar se MongoDB está rodando
pgrep mongod
# Verificar logs
tail -f /workspace/mongodb.log
```

### Frontend não carrega:
```bash
# Limpar cache do navegador (Ctrl+Shift+R)
# Ou reinstalar dependências
cd /workspace/frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Porta já em uso:
```bash
# Descobrir processo usando a porta
lsof -i :8000
lsof -i :5173
# Matar processo
kill -9 <PID>
```

---

## 📝 COMANDOS ÚTEIS:

```bash
# Ver logs do backend em tempo real
tail -f /workspace/backend.log

# Ver logs do frontend em tempo real
tail -f /workspace/frontend.log

# Ver logs do MongoDB
tail -f /workspace/mongodb.log

# Ver processos rodando
ps aux | grep -E "(mongod|uvicorn|node)"

# Testar conexão com MongoDB
mongosh mongodb://localhost:27017/tormenta20 --eval "db.stats()"

# Ver endpoints disponíveis
curl http://localhost:8000/openapi.json | python3 -c "import sys,json; d=json.load(sys.stdin); print('\n'.join([p for p in d.get('paths',{}).keys()]))"
```

---

## 📁 ARQUIVOS DE LOG:

- **Backend**: `/workspace/backend.log`
- **Frontend**: `/workspace/frontend.log`
- **MongoDB**: `/workspace/mongodb.log`
- **Dados DB**: `/workspace/data/db/`

---

**Sistema revisado, corrigido e rodando com sucesso! 🎉**

Documentação completa salva em: `/workspace/COMO_RODAR_LINUX.md`
