# ---- Dev ----
FROM node:20-alpine AS dev

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3030

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3030"]

# ---- Production build ----
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

ARG NUXT_PUBLIC_API_BASE=https://api-toi.daraedu.kz
ENV NUXT_PUBLIC_API_BASE=$NUXT_PUBLIC_API_BASE

RUN npm run build

# ---- Production SSR server ----
FROM node:20-alpine AS production

WORKDIR /app

ENV NODE_ENV=production
ENV HOST=0.0.0.0
ENV NITRO_HOST=0.0.0.0
ENV PORT=3030
ENV NUXT_PUBLIC_API_BASE=https://api-toi.daraedu.kz

COPY --from=builder /app/.output ./.output

EXPOSE 3030

CMD ["node", ".output/server/index.mjs"]
