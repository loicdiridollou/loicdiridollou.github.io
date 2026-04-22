FROM alpine:3.21 AS builder

ARG HUGO_VERSION=0.159.1
ARG BASE_URL=http://localhost/

RUN apk add --no-cache git libc6-compat libstdc++ && \
    wget -qO hugo.tar.gz "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz" && \
    tar -xzf hugo.tar.gz hugo && \
    mv hugo /usr/local/bin/ && \
    rm hugo.tar.gz

WORKDIR /src
COPY . .
RUN hugo --gc --minify --baseURL "${BASE_URL}"

FROM nginx:1.27-alpine
COPY --from=builder /src/public /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
