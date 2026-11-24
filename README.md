# PirataFlix 🎬

Aplicação web de catálogo de filmes desenvolvida com React, Flask e PostgreSQL, utilizando Docker para executar o frontend, backend e banco de dados em containers independentes.

## Tecnologias

- React
- Python / Flask
- PostgreSQL
- Nginx
- Docker

## Estrutura

```text
pirataflix/
├── Backend/
│   ├── Dockerfile.node
│   └── .dockerignore
└── Frontend/
    ├── Dockerfile.node
    ├── .dockerignore
    └── nginx.conf
```

## Como executar

**Pré-requisito:** Docker instalado e em execução.

### 1. Baixar o projeto

```bash
git clone LINK_DO_REPOSITORIO
cd NOME_DA_PASTA
```

### 2. Criar o banco de dados

```bash
docker run --name pirataflix-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=dbPirataFlix \
  -p 5435:5432 \
  -d postgres:18.6-alpine3.24
```

### 3. Construir e executar o backend

```bash
docker build -t pirataflix-backend:1.0.0 -f Backend/Dockerfile.node Backend
```

```bash
docker run -d \
  --name pirataflix-backend \
  --add-host=host.docker.internal:host-gateway \
  -e DB_NAME=dbPirataFlix \
  -e DB_USER=postgres \
  -e DB_PASSWORD=postgres \
  -e DB_HOST=host.docker.internal \
  -e DB_PORT=5435 \
  -p 5000:5000 \
  pirataflix-backend:1.0.0
```

### 4. Construir e executar o frontend

```bash
docker build -t pirataflix-frontend:1.0.0 -f Frontend/Dockerfile.node Frontend
```

```bash
docker run -d \
  --name pirataflix-frontend \
  --add-host=host.docker.internal:host-gateway \
  -p 8080:80 \
  pirataflix-frontend:1.0.0
```

### 5. Acessar a aplicação

Abra no navegador:

```text
http://localhost:8080
```

## Verificar containers

```bash
docker ps
```

| Serviço | Porta |
|---|---:|
| Frontend (Nginx) | 8080 |
| Backend (Flask) | 5000 |
| PostgreSQL | 5435 |

## Contas de demonstração

| Tipo | E-mail | Senha |
|---|---|---|
| Administrador | admin@gmail.com | senha123 |
| Usuário | usuario@gmail.com | senha123 |

O banco cadastra automaticamente 10 filmes e as duas contas na inicialização, caso ainda não existam.

## Encerrar os containers

```bash
docker stop pirataflix-frontend pirataflix-backend pirataflix-db
```

Para iniciar novamente:

```bash
docker start pirataflix-db pirataflix-backend pirataflix-frontend
```

Visualizar o banco de dados

O PostgreSQL é executado em um container Docker. Para acessar o banco pelo terminal:

docker exec -it pirataflix-db psql -U postgres -d dbPirataFlix

Comandos úteis

Listar as tabelas:

\dt

Visualizar a estrutura de uma tabela:

\d filme

Consultar os filmes cadastrados:

SELECT * FROM filme;

Consultar os usuários:

SELECT id, nome, email FROM usuario;

Consultar os administradores:

SELECT id, nome, email FROM adm;

Consultar os gêneros:

SELECT * FROM filme_genero;

Para sair do PostgreSQL:

\q