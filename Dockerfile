FROM python:3-alpine

COPY . /app
WORKDIR /app

RUN pip install pipenv
RUN pipenv install --system --deploy
