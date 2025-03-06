FROM python:3.11-alpine

WORKDIR /usr/local/app/bot

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/local/app/bot