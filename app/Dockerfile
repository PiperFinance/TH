FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10


WORKDIR /app

COPY requirements.txt ./requirements.txt


RUN pip install -r requirements.txt 


COPY ./ ./

ENV TIMEOUT=36000
# ENV TIMEOUT_KEEP_ALIVE=72000
ENV WORKERS_PER_CORE=2