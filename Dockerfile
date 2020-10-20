FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN mkdir /blog_project

WORKDIR /blog_project

COPY requirements.txt /blog_project/

RUN pip install -r requirements.txt

COPY . /blog_project/


