FROM python:3.5-slim

RUN mkdir -p /usr/src/app
COPY feeder-service /usr/src/app
WORKDIR /usr/src/app

RUN apt-get update && apt-get -y --no-install-recommends install vim telnet net-tools bash
RUN pip install -r requirements-dev.txt
