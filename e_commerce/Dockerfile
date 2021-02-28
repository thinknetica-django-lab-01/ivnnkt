FROM python:3.8.2

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./rec.txt .
RUN pip install -r rec.txt
# copy project
COPY . .