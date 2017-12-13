FROM postgres:9.6.5

COPY ./ops/postgres/docker-healthcheck.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/docker-healthcheck.sh

HEALTHCHECK CMD ["docker-healthcheck.sh"]
