FROM alpine/openssl:latest AS certs

WORKDIR /certs/

RUN openssl ecparam -genkey -name secp384r1 -out key.pem
RUN openssl req -x509 -new -key key.pem -out cert.crt -days 365 -subj "/C=RU/ST=MOSCOW/CN=QRIGAMI"


FROM nginx:stable-alpine-slim

COPY --from=certs /certs/key.pem /etc/nginx/certs/
COPY --from=certs /certs/cert.crt /etc/nginx/certs/
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
