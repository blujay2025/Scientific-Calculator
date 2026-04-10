FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM node:20-alpine

WORKDIR /app

RUN npm install -g serve

COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh
COPY --from=build /app/dist /app/dist

EXPOSE 4173

CMD ["sh", "-c", "/app/docker-entrypoint.sh && serve -s /app/dist -l 4173"]
