FROM python:2.7.15-alpine3.7

ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Postgres and python deps
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev curl bash

# Install python deps
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY spacedb/ .
COPY spaceobjects/ .
COPY static/ .
COPY templates/ .
COPY data/ .
COPY manage.py manage.py

EXPOSE 8000

CMD python /app/manage.py runserver 0.0.0.0:8000
