FROM python:3.10
LABEL maintainer="Dmitrii Tregubov"

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app/

COPY Pipfile Pipfile.lock /app/
COPY ./app /app
WORKDIR /app
EXPOSE 8001


RUN pip install --upgrade pip setuptools wheel \
    && pip install pipenv \
    && pipenv install --system -d \
    && rm -rf /root/.cache/pip \
    && addgroup --system appgroup  \
    && adduser --system appuser --ingroup appgroup \
    && chown -R appuser:appgroup /app

USER appuser
