FROM alpine

RUN apk add --update nginx \
    && rm -rf /var/cache/apk/* \
    && mkdir -p /tmp/nginx/ \
    && mkdir -p /run/nginx/ \
    && ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

CMD ["nginx", "-g", "daemon off;"]
