FROM node:20-alpine AS dev

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3030

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3030"]

# ---- Production build stage ----
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

ARG NUXT_PUBLIC_API_BASE=http://localhost:8081
ENV NUXT_PUBLIC_API_BASE=$NUXT_PUBLIC_API_BASE

RUN npm run generate

# ---- Production static serving ----
FROM node:20-alpine

WORKDIR /app

RUN npm install -g serve

COPY --from=builder /app/dist ./public

EXPOSE 3030

CMD ["serve", "-s", "public", "-l", "3030"]
