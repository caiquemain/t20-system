# 🐧 Como Rodar o Sistema T20 no Linux

Guia único e atualizado para subir o sistema. O caminho canônico é via
**Docker Compose**; há também a opção de rodar localmente para desenvolvimento.

---

## ✅ OPÇÃO 1: Docker Compose (recomendado)

### Pré-requisitos
- Docker + plugin Compose (`docker compose version`)
- Portas livres: `5173` (web), `8000` (api), `27017` (db)

### Subir tudo

```bash
# Na raiz do projeto (onde está o docker-compose.yml)
docker compose up -d --build
```

| Serviço | Container | Acesso |
|---|---|---|
| Frontend (React + Vite) | `t20_web` | http://localhost:5173 |
| Backend (FastAPI + Swagger) | `t20_api` | http://localhost:8000/docs |
| MongoDB 7.0 | `t20_db` | `mongodb://localhost:27017/tormenta20` |

Rotas do app: `/` home · `/wizard` criação · `/ficha/:id` ficha.

### Comandos úteis

```bash
docker compose ps                  # status dos 3 serviços
docker compose logs -f [api|web]   # logs em tempo real
docker compose restart             # reiniciar
docker compose down                # parar (mantém dados em ./data/db)
docker compose exec -T api python -m pytest tests/ -q   # rodar testes
```

> ⚠️ `docker compose down -v` **apaga o banco**. Sem `-v`, os dados persistem
> no volume `./data/db`.

---

## 🔧 OPÇÃO 2: Rodar localmente (desenvolvimento)

Útil para debug com reload direto no código. Você precisa do MongoDB
acessível — via container Docker ou instalação nativa.

### 1. MongoDB

```bash
# Via Docker (só o banco):
docker run -d -p 27017:27017 --name t20_db mongo:7.0

# OU nativo (Ubuntu/Debian):
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc \
  | sudo gpg --dearmor -o /usr/share/keyrings/mongodb-server-7.0.gpg
echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] \
  https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/7.0 multiverse" \
  | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt update && sudo apt install -y mongodb-org
sudo systemctl start mongod
```

### 2. Backend (terminal 1)

```bash
cd app

# Com Poetry (dependências do pyproject.toml):
poetry install
MONGO_URI=mongodb://localhost:27017/tormenta20 poetry run uvicorn src.main:app --reload --port 8000

# OU com pip (sem Poetry):
pip install fastapi uvicorn motor pydantic pypdf
MONGO_URI=mongodb://localhost:27017/tormenta20 uvicorn src.main:app --reload --port 8000
```

> ⚠️ Localmente a URI usa `localhost`; dentro do Compose a API usa
> `mongodb://db:27017/tormenta20` (nome do serviço). Esse é o erro mais comum
> de "backend não conecta no banco".

### 3. Frontend (terminal 2)

```bash
cd frontend
npm install
npm run dev        # Vite em http://localhost:5173
```

O frontend espera a API em `http://localhost:8000` (`VITE_API_URL`).

---

## ✔️ Verificação de funcionamento

```bash
# Catálogos
curl http://localhost:8000/dados/racas   | head -c 200
curl http://localhost:8000/dados/classes | head -c 200
curl http://localhost:8000/dados/magias  | head -c 200

# Listar personagens (vazio no início: [])
curl http://localhost:8000/personagens/

# Rotas disponíveis (JSON):
curl -s http://localhost:8000/openapi.json \
  | python3 -c "import sys,json; print('\n'.join(sorted(json.load(sys.stdin)['paths']))))"
```

No navegador: crie um personagem em http://localhost:5173/wizard e abra a
documentação interativa em http://localhost:8000/docs para testar os endpoints.

---

## 🐛 Solução de problemas

### Backend não conecta ao MongoDB
```bash
# Mongo está rodando?
docker ps | grep t20_db          # via Docker
sudo systemctl status mongod     # nativo

# Confira a URI: 'localhost' fora do Compose, 'db' dentro do Compose.
```

### Porta já em uso
```bash
lsof -i :8000
lsof -i :5173
kill -9 <PID>
```

### Frontend não carrega / tela branca
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
# + hard refresh no navegador (Ctrl+Shift+R)
```

### Testes falham fora do Docker
Os testes só rodam **dentro do container** (`pytest` não é instalado localmente):
```bash
docker compose exec -T api python -m pytest tests/ -q
```

### Resetar tudo (⚠️ apaga fichas)
```bash
docker compose down -v && docker compose up -d --build
# OU só limpar o banco via API:
curl -X DELETE http://localhost:8000/admin/limpar-tudo
```

---

## 📚 Links úteis
- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/
- MongoDB: https://www.mongodb.com/docs/
- Arquitetura e roadmap do projeto: ver `README.md`
