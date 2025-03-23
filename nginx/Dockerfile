FROM alpine/openssl:latest AS certs

WORKDIR /certs/

RUN openssl ecparam -genkey -name secp384r1 -out key.pem
RUN openssl req -x509 -new -key key.pem -out cert.crt -days 365 -subj "/C=RU/ST=MOSCOW/CN=QRIGAMI"


FROM ghcr.io/astral-sh/uv:alpine AS static

ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1

WORKDIR /qrigami/

COPY ../.python-version ./
RUN uv python install

COPY ../pyproject.toml ./
RUN uv sync --upgrade --no-dev

COPY ../qrigami/ ./qrigami/
RUN uv run --no-dev ./qrigami/manage.py collectstatic --no-input


FROM nginx:stable-alpine-slim

COPY --from=certs /certs/key.pem /etc/nginx/certs/
COPY --from=certs /certs/cert.crt /etc/nginx/certs/
COPY --from=static /qrigami/qrigami/static/ /var/www/static/
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
