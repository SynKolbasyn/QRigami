FROM ghcr.io/astral-sh/uv:alpine

ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1

WORKDIR /qrigami/

COPY ./.python-version ./
RUN uv python install

COPY ./pyproject.toml ./
RUN uv sync --upgrade --no-dev

COPY ./qrigami/ ./qrigami/

WORKDIR /qrigami/qrigami/

ENTRYPOINT ["sh", "-c", "uv run --no-dev gunicorn -w $(nproc) -b 0.0.0.0:80 -k uvicorn.workers.UvicornWorker qrigami.asgi:application"]
