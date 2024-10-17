FROM python:3.6-alpine

RUN apk add --no-cache \
    ca-certificates \
    curl \
    openssl \
    docker

RUN pip install requests

COPY . /app
WORKDIR /app