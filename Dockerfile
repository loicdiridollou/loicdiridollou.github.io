FROM alpine:3.21 AS builder

ARG HUGO_VERSION=0.159.1

ARG DART_SASS_VERSION=1.86.3

RUN apk add --no-cache git libc6-compat libstdc++ && \
    wget -qO hugo.tar.gz "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz" && \
    tar -xzf hugo.tar.gz hugo && \
    mv hugo /usr/local/bin/ && \
    rm hugo.tar.gz && \
    wget -qO dart-sass.tar.gz "https://github.com/sass/dart-sass/releases/download/${DART_SASS_VERSION}/dart-sass-${DART_SASS_VERSION}-linux-x64.tar.gz" && \
    tar -xzf dart-sass.tar.gz -C /usr/local && \
    ln -s /usr/local/dart-sass/sass /usr/local/bin/sass && \
    rm dart-sass.tar.gz

WORKDIR /src
COPY . .
RUN hugo --gc --minify --baseURL /

FROM nginx:1.27-alpine
COPY --from=builder /src/public /usr/share/nginx/html
