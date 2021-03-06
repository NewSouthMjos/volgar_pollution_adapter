#!/bin/bash
# WORKERS_COUNT="${WORKERS_COUNT:=1}"
BIND_ADDRESS="${BIND_ADDRESS:=0.0.0.0:9999}"
LOG_LEVEL="${LOG_LEVEL:=info}"
exec gunicorn --bind $BIND_ADDRESS main:app -w 1 -k uvicorn.workers.UvicornWorker --log-level LOG_LEVEL