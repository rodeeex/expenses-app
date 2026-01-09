# Expenses - приложение для ведения личных расходов

## Стек

- Фронтенд - React.js
- Бэкенд - FastAPI
- СУБД - SQLite
- Инфраструктура - Docker

## Разработчики

- Anton Pushkarev - DevOps, бэкенд
- Bogdan Nekrasov - фронтенд, бэкенд
- Daniil Zhelanov - БД, бэкенд

## Руководство по запуску

> Требование: запущенный Docker engine

1. Склонируйте репозиторий и перейдите в папку проекта

```bash
git clone https://github.com/rodeeex/expenses-app
cd expenses-app
```

2. Перейдите в папку infrastructure и запустите docker-compose

```bash
cd infrastructure
docker compose up --build # или же docker-compose, если он установлен как отдельный плагин
```

3. После этого приложение становится доступно по адресу `http://localhost:5173/`. Документация к API: `http://localhost:8000/docs`.

Для того, чтобы воспользоваться приложением, нужно создать аккаунт. В таком случае вход в него будет выполнен автоматически.
