FROM python:3.6.3-slim

RUN apt-get update && \
    apt-get install -y \
        python-psycopg2 \
        curl

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app
COPY ./ops/web/infrastructure.py /app/config_layers/infrastructure.py

EXPOSE 8014

HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f "http://localhost:8014/graphql?query=\{ping\}" || exit 1

CMD inv dev.runserver --host='0.0.0.0' --port=8014
