FROM node:22-alpine

WORKDIR /app

# Copia dependências
COPY package.json package-lock.json* ./

# Instala dependências
RUN npm install

# Copia o código fonte
COPY . .

# Expõe a porta do Vite
EXPOSE 5173

# O --host é essencial para o Docker expor a rede
CMD ["npm", "run", "dev", "--", "--host"]
