# Shaqyru Frontend (Nuxt 3, SSR)

Сайт збирається з **Nuxt 3** у режимі **SSR** (server-side rendering), щоб пошукові системи (Google тощо) бачили повний HTML.

## Розробка

```bash
npm install
npm run dev
```

## Production (SSR)

Після `npm run build` запускайте Node-сервер:

```bash
node .output/server/index.mjs
```

На сервері має бути встановлена змінна **NUXT_PUBLIC_API_BASE** (URL бекенду), щоб SSR міг підвантажувати дані з API при рендері сторінок.

## Docker (SSR)

```bash
docker compose up --build -d
```

- Сайт: **http://localhost:3030**
- Після зміни `nuxt.config.ts` або переходу на SSR обовʼязково перезберіть образ без кешу:
  ```bash
  docker compose build --no-cache && docker compose up -d
  ```
- Щоб у HTML був контент (а не лише `<title>`), бекенд має бути доступний **із контейнера**. Якщо API на хості (наприклад `localhost:8000`), у `docker-compose` задайте:
  `NUXT_PUBLIC_API_BASE=http://host.docker.internal:8000` (Mac/Windows) або IP хоста замість `localhost`.
