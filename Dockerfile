FROM ghcr.io/astral-sh/uv:alpine

LABEL org.opencontainers.image.source="https://github.com/SynKolbasyn/QRigami"
LABEL org.opencontainers.image.description="Django image"
LABEL org.opencontainers.image.licenses="AGPL-3.0-or-later"

ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1

WORKDIR /qrigami/

COPY ./.python-version ./
RUN uv python install

COPY ./pyproject.toml ./
RUN uv sync --upgrade --no-dev

COPY ./qrigami/ ./qrigami/

WORKDIR /qrigami/qrigami/

CMD ["sh", "-c", "uv run --no-dev manage.py migrate && uv run --no-dev gunicorn -w $(nproc) -b 0.0.0.0:80 -k uvicorn.workers.UvicornWorker qrigami.asgi:application"]
