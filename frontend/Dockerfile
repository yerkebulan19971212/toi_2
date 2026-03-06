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
FROM nginx:alpine AS prod

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.prod.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
