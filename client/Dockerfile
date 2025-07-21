# 開発環境
FROM node:lts-alpine AS dev
WORKDIR /app
COPY package*.json ./
RUN npm install
CMD ["npm", "run", "dev"]


# ビルド環境
FROM node:lts-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build -- --mode production

# 本番環境
FROM nginx:stable-alpine AS prod

RUN apk add --no-cache tzdata \
    && cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime \
    && echo "Asia/Tokyo" > /etc/timezone

COPY --from=build /app/dist /usr/share/nginx/html

COPY nginx/conf/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
