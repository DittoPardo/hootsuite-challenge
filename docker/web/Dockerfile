FROM python:3.5-slim

RUN apt-get update && apt-get -y --no-install-recommends install curl vim telnet net-tools bash sudo

#RUN useradd --user-group --create-home --shell /bin/false web
RUN adduser --disabled-password --gecos '' --shell /bin/false web
RUN adduser web sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
ENV HOME=/home/web

RUN mkdir -p $HOME/app
COPY web/requirements.txt web/requirements-dev.txt $HOME/app/

WORKDIR $HOME/app
# install globaly
RUN pip install -r requirements-dev.txt

USER web
