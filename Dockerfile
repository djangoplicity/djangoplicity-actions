FROM python:2.7-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    gcc \
    git \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    python-dev

RUN mkdir /app
WORKDIR /app

COPY requirements/ requirements/
COPY requirements.txt .

RUN pip install -r requirements.txt


COPY djangoplicity/ djangoplicity/
COPY test_project/ test_project/
COPY test_app/ test_app/
COPY setup.py .
COPY manage.py .