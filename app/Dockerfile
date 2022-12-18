FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8


WORKDIR /app

COPY requirements.txt ./requirements.txt


RUN pip install -r requirements.txt 
RUN pip install pyyaml


COPY ./ ./

ENV TIMEOUT=3600


COPY ./wait /wait
RUN chmod +x /wait