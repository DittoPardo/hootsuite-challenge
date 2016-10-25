FROM python:3.5-slim

RUN mkdir -p /usr/src/app
COPY web /usr/src/app
WORKDIR /usr/src/app

RUN apt-get update && apt-get -y --no-install-recommends install curl vim telnet net-tools bash
RUN pip install -r requirements-dev.txt
