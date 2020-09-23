FROM python:3.8-slim

RUN apt-get update && \
    apt-get install -y netcat && \
    apt-get clean

EXPOSE 5000
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP="api.py"
RUN chmod a+x ./docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["python", "api.py"]
