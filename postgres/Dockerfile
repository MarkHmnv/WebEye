FROM postgres:16.1-alpine

ENV POSTGRES_USER=devuser
ENV POSTGRES_PASSWORD=changeme

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432