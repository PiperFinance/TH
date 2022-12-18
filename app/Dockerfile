FROM tiangolo/uvicorn-gunicorn-fastapi:latest


WORKDIR /app

COPY requirements.txt ./requirements.txt


RUN pip install -r requirements.txt 
RUN pip install pyyaml


COPY ./ ./

ENV TIMEOUT=3600


# COPY ./wait /wait
# RUN chmod +x /wait