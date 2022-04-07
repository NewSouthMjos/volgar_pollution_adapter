FROM python:3.10-slim-bullseye

WORKDIR /app

ENV PYTHONUNBUFFERED=1
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY requirements.txt .
RUN pip3 install -r requirements.txt

# RUN mkdir /tmp/prom_data
# ENV prometheus_multiproc_dir /tmp/prom_data

COPY ./api ./api
COPY ./commons ./commons
COPY main.py .
COPY __init__.py .
COPY entrypoint.sh .
# COPY gunicorn.conf.py .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]