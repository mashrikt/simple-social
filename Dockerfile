FROM python:3.10-slim
RUN pip install --upgrade pip
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app
