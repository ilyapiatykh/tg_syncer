FROM python:3.11-slim

WORKDIR /

COPY app /app
COPY configs/prod.yaml configs/prod.yaml
COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt
RUN mkdir data

ENV PYTHONPATH="/"

ENTRYPOINT ["python", "/app/main.py"]
