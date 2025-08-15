# -------------------------
# for base
# -------------------------

FROM python:3.11-slim as server-base

RUN apt update && \
    apt install -y tzdata && \
    ln -snf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    echo "Asia/Tokyo" > /etc/timezone && \
    apt clean

WORKDIR /app

COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server .



# -------------------------
# for development
# -------------------------

FROM node:lts-alpine AS client-dev
WORKDIR /app
COPY client/package*.json ./
RUN npm install
CMD ["npm", "run", "dev"]


FROM server-base as server-dev

RUN chmod +x entrypoint_dev.sh
ENTRYPOINT ["/app/entrypoint_dev.sh"]


# -------------------------
# for build
# -------------------------

FROM node:lts-alpine AS client-build
WORKDIR /app
COPY client/package*.json ./
RUN npm install
COPY client .
RUN npm run build -- --mode production


# -------------------------
# for production
# -------------------------

FROM nginx:stable-alpine AS client-prod

RUN apk add --no-cache tzdata \
    && cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime \
    && echo "Asia/Tokyo" > /etc/timezone

COPY --from=client-build /app/dist /usr/share/nginx/html

COPY client/nginx/conf/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]


FROM server-base as server-prod

RUN chmod +x entrypoint_prod.sh
ENTRYPOINT ["/app/entrypoint_prod.sh"]


FROM server-base as db-manager

COPY db-manager/entrypoint.sh .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
