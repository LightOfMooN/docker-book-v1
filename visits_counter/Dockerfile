FROM python:3-alpine
EXPOSE 5000
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY main.py .
CMD ["python", "main.py"]
