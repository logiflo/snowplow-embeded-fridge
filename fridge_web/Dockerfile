FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /fridge

WORKDIR /fridge

COPY requirements.txt /fridge/

RUN pip3 install -r requirements.txt

COPY . /fridge/
