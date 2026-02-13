# syntax=docker/dockerfile:1

FROM python:3.13-slim-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt
COPY main.py main.py

RUN pip3 install -r requirements.txt

CMD ["python3", "bot.py"]