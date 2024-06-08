FROM python:3.11-alpine
LABEL maintainer="MarkHmnv"

ENV PYTHONUNBUFFERED 1

COPY . /api
WORKDIR /api
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r requirements.txt && \
    apk add --no-cache supervisor chromium chromium-chromedriver && \
    adduser \
        --disabled-password \
        --no-create-home \
        fastapi-user && \
    mkdir -p /home/fastapi-user/.cache/selenium && \
    chown -R fastapi-user:fastapi-user /home/fastapi-user/.cache/selenium

ENV PATH="/py/bin:$PATH"
ENV PYTHONPATH "${PYTHONPATH}:/"

USER fastapi-user