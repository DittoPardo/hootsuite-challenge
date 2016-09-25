FROM python:3.5-slim

RUN mkdir -p /usr/src/app
COPY web /usr/src/app
WORKDIR /usr/src/app

RUN pip install -r requirements-dev.txt
CMD python reddit_web_app.py
