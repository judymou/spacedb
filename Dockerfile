FROM python:3-alpine3.7

ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Postgres and python deps
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev curl bash

# Install python deps
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY spacedb spacedb
COPY spaceobjects spaceobjects
COPY static static
COPY templates templates
COPY data data
COPY manage.py manage.py

EXPOSE 8000

CMD python /app/manage.py runserver 0.0.0.0:8000
