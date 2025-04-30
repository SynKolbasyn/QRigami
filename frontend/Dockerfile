FROM debian:stable-slim AS static

WORKDIR /static/

RUN apt update
RUN apt upgrade -y
RUN apt install -y zstd
RUN apt install -y brotli

COPY ./html/ ./html/
COPY ./css/ ./css/
COPY ./js/ ./js/

RUN for file in $(find ./ -type f); do \
    zstd -z --ultra -22 -o ${file}.zst $file && \
    brotli -q 11 -o ${file}.br $file && \
    gzip -9 -k $file; done


FROM debian:stable-slim AS build

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

WORKDIR /tmp/ngx_brotli/deps/brotli/
RUN cmake -S ./ -B ./out/ \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS=OFF \
    -DCMAKE_C_FLAGS="-Ofast -m64 -march=native -mtune=native -flto -funroll-loops -ffunction-sections -fdata-sections -Wl,--gc-sections" \
    -DCMAKE_CXX_FLAGS="-Ofast -m64 -march=native -mtune=native -flto -funroll-loops -ffunction-sections -fdata-sections -Wl,--gc-sections" \
    -DCMAKE_INSTALL_PREFIX=./out/installed
RUN cmake --build ./out/ --config Release --target brotlienc

WORKDIR /tmp/nginx/
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


FROM debian:stable-slim

RUN apt update
RUN apt upgrade -y
RUN apt install -y libpcre3-dev

COPY --from=build /etc/nginx/ /etc/nginx/
COPY --from=static /static/ /var/www/static/
COPY ./nginx.conf /etc/nginx/

CMD ["/etc/nginx/sbin/nginx", "-g", "daemon off;", "-c", "/etc/nginx/nginx.conf"]
