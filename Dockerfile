# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt && pip cache purge
RUN apt-get update && apt-get install -y \
    gettext \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .
