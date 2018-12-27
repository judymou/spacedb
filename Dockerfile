FROM python:2.7.15-alpine3.7

ENV PYTHONUNBUFFERED 1

WORKDIR /app

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
