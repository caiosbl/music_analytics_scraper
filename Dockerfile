FROM python:3-alpine

RUN apk update && \
    apk add --no-cache \
        chromium \
        chromium-chromedriver \
        && rm -rf /var/cache/apk/*

COPY . /app
WORKDIR /app
ENV PATH="/usr/lib/chromium/:${PATH}"

RUN pip install pipenv
RUN pipenv install --system --deploy
