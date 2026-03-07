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
