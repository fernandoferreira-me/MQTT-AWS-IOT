FROM python:3.9-bullseye

ARG USER_UID=501

RUN apt-get update \
  && apt-get install -y python3-pip \
  && pip3 install awsiotsdk

RUN useradd -m -u $USER_UID -s /bin/bash -d /home/iotuser iotuser \
    && mkdir /app \
    && chown -R iotuser:iotuser /app

VOLUME /app
WORKDIR /app

USER iotuser