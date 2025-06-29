FROM python:3.11-slim as base

ENV TZ=Asia/Tokyo

RUN apt update && \
    apt install -y tzdata && \
    ln -snf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    echo "Asia/Tokyo" > /etc/timezone && \
    apt clean

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


FROM base as dev

RUN chmod +x entrypoint_dev.sh
ENTRYPOINT ["/app/entrypoint_dev.sh"]


FROM base as prod

RUN chmod +x entrypoint_prod.sh
ENTRYPOINT ["/app/entrypoint_prod.sh"]
