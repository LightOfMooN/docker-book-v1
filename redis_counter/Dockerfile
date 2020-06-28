ARG PYTHONVERSION=3
FROM python:$PYTHONVERSION-alpine

ENV REDIS_HOST=localhost REDIS_PORT=6379 DEBUG_MODE=True
EXPOSE 5000
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python"]

CMD ["main.py"]
