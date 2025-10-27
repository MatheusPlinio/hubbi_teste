# Projeto Django com Docker

Este guia ensina como configurar e rodar o projeto localmente usando Docker e Django.

---

## 1. Configuração do Ambiente

Copie o arquivo de exemplo `.env` e configure seu banco de dados:

```bash
cp .env.example .env
```

Edite o `.env` e defina:

* `DB_NAME` → Nome do banco de dados
* `DB_USER` → Usuário do banco
* `DB_PASSWORD` → Senha do banco

---

## 2. Inicializando o Docker

Suba os containers em segundo plano:

```bash
docker compose up -d
```

---

## 3. Rodando Migrações

Crie as tabelas do banco de dados:

```bash
python manage.py migrate
```

---

## 4. Iniciando o Servidor

Rode o servidor de desenvolvimento do Django em uma porta disponível:

```bash
python manage.py runserver [porta_disponivel]
```

Exemplo:

```bash
python manage.py runserver 8000
```

---

Pronto! O projeto deve estar funcionando localmente.
