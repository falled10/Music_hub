FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /music_hub
WORKDIR /music_hub
COPY ./music_hub /music_hub

RUN adduser -D user
USER user