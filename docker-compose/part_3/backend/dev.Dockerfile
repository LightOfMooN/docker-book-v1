FROM python:3.8-slim
EXPOSE 5000
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . .
ARG version=1
RUN echo version is: \"$version\"
CMD ["python", "api.py"]
