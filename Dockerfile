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

RUN pip install -r requirements.txt --find-links https://www.djangoplicity.org/repository/packages/
# Create app required directories
RUN mkdir -p tmp

COPY scripts/ scripts/
RUN chmod +x scripts/command-dev.sh
COPY djangoplicity/ djangoplicity/
COPY test_project/ test_project/
COPY setup.py .
COPY tox.ini .
COPY .coveragerc .
COPY manage.py .