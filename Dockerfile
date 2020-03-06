FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /redditapi

WORKDIR /redditapi

COPY requirements.txt /redditapi/

RUN pip install -r requirements.txt

COPY . /redditapi/