FROM python:3.5-slim

RUN mkdir -p /usr/src/app
COPY feeder-service /usr/src/app
WORKDIR /usr/src/app

RUN apt-get update && apt-get -y --no-install-recommends install cron vim telnet net-tools bash
COPY feeder-service/crontab /etc/cron.d/feeder-cron
RUN chmod +x /etc/cron.d/feeder-cron
RUN touch /var/log/read-command.log

RUN pip install -r requirements-dev.txt
