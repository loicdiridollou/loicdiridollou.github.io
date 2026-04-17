FROM hugomods/hugo:exts-0.159.1 AS builder
WORKDIR /src
COPY . .
RUN hugo --gc --minify --baseURL /

FROM nginx:1.27-alpine
COPY --from=builder /src/public /usr/share/nginx/html
