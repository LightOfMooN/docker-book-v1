FROM alpine
RUN addgroup -g 3333 app \
    && adduser -D -u 3333 -G app app
USER app
CMD ["id"]

FROM debian
RUN useradd --uid 3333 app
USER app
CMD ["id"]
