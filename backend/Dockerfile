FROM alpine/openssl:latest AS certs

WORKDIR /certs/

RUN openssl ecparam -genkey -name secp384r1 -out key.pem
RUN openssl req -x509 -new -key key.pem -out cert.pem -days 365 -subj "/C=RU/ST=Moscow/CN=QRigami"


FROM ghcr.io/astral-sh/uv:alpine

ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1

WORKDIR /qrigami/

COPY ./.python-version ./
RUN uv python install

COPY ./pyproject.toml ./
RUN uv sync

COPY ./src/ ./src/
COPY --from=certs /certs/ ./certs/

CMD ["sh", "-c", "uv run hypercorn --certfile certs/cert.pem --keyfile certs/key.pem -b 0.0.0.0:443 -w $(nproc) src.main:app"]
