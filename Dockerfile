FROM python:3.7.4-slim
ENV DEBIAN_FRONTEND noninteractive

RUN apt update && \
  apt install --yes --no-install-recommends \
  libpq-dev \
  build-essential && \
# package install cleanup
  apt-get autoclean && apt-get --purge --yes autoremove && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV PYTHONUNBUFFERED 1

RUN pip install pipenv

RUN mkdir -p /app
WORKDIR /app

COPY Pipfile.lock /app/
COPY Pipfile /app/

RUN pipenv install --system --deploy --ignore-pipfile

COPY . /app/
