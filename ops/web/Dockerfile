FROM python:3.6.3-slim

RUN mkdir /app

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
        python-psycopg2 \
        curl \
        nginx \
        supervisor \
        && \
    pip install gunicorn && \
    service supervisor stop && \
    service nginx stop

RUN pip install -r /app/requirements.txt

COPY . /app
COPY ./ops/web/infrastructure.py /app/config_layers/infrastructure.py

EXPOSE 80

HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f "http://localhost:80/graphql?query=\{ping\}" || exit 1

CMD supervisord -c /app/ops/web/supervisord.conf -n
