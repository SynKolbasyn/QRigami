FROM alpine/openssl:latest AS certs

WORKDIR /certs/

RUN openssl ecparam -genkey -name secp384r1 -out key.pem
RUN openssl req -x509 -new -key key.pem -out cert.crt -days 365 -subj "/C=RU/ST=MOSCOW/CN=QRIGAMI"


FROM ghcr.io/astral-sh/uv:alpine AS static

ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1

RUN apk add --no-cache zstd
RUN apk add --no-cache brotli

WORKDIR /qrigami/

COPY ../.python-version ./
RUN uv python install

COPY ../pyproject.toml ./
RUN uv sync --upgrade --no-dev

COPY ../qrigami/ ./qrigami/
RUN DJANGO_DEBUG=True uv run --no-dev ./qrigami/manage.py collectstatic --no-input

RUN for file in $(find ./qrigami/static/ -type f); do \
    zstd -z --ultra -22 -o ${file}.zst $file && \
    brotli -q 11 -o ${file}.br $file && \
    gzip -9 -k $file; done


FROM debian:stable-slim

WORKDIR /tmp/nginx/

RUN apt update
RUN apt upgrade -y
RUN apt install -y git
RUN apt install -y gcc
RUN apt install -y make
RUN apt install -y libpcre3-dev
RUN apt install -y zlib1g-dev
RUN apt install -y libssl-dev
RUN apt install -y libzstd-dev
RUN apt install -y cmake
RUN git clone https://github.com/nginx/nginx.git ./
RUN git clone https://github.com/tokers/zstd-nginx-module.git /tmp/zstd-nginx-module/
RUN git clone --recurse-submodules https://github.com/google/ngx_brotli.git /tmp/ngx_brotli/
RUN cd /tmp/ngx_brotli/deps/brotli && \
    cmake -S ./ -B ./out/ \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS=OFF \
    -DCMAKE_C_FLAGS="-Ofast -m64 -march=native -mtune=native -flto -funroll-loops -ffunction-sections -fdata-sections -Wl,--gc-sections" \
    -DCMAKE_CXX_FLAGS="-Ofast -m64 -march=native -mtune=native -flto -funroll-loops -ffunction-sections -fdata-sections -Wl,--gc-sections" \
    -DCMAKE_INSTALL_PREFIX=./out/installed
RUN cd /tmp/ngx_brotli/deps/brotli && \
    cmake --build ./out/ --config Release --target brotlienc
RUN ./auto/configure \
    --with-compat \
    --prefix=/etc/nginx/ \
    --with-http_gzip_static_module \
    --with-http_ssl_module \
    --with-http_v2_module \
    --add-module=/tmp/zstd-nginx-module/ \
    --add-module=/tmp/ngx_brotli/
RUN make -j $(nproc) modules
RUN make install
RUN cp /tmp/nginx/conf/mime.types /etc/nginx/

COPY --from=certs /certs/key.pem /etc/nginx/certs/
COPY --from=certs /certs/cert.crt /etc/nginx/certs/
COPY --from=static /qrigami/qrigami/static/ /var/www/static/
COPY ./nginx/nginx.conf /etc/nginx/

CMD ["/etc/nginx/sbin/nginx", "-g", "daemon off;", "-c", "/etc/nginx/nginx.conf"]
