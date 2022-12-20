FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10


WORKDIR /app

COPY requirements.txt ./requirements.txt


RUN pip install -r requirements.txt 
RUN pip install pyyaml


COPY ./ ./

ENV TIMEOUT=3600