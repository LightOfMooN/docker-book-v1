FROM alpine
COPY --from=nginx:alpine /usr/share/nginx/html/index.html /index.txt
CMD ["cat", "index.txt"]
