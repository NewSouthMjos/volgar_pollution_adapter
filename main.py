import logging

from fastapi import FastAPI
from fastapi.logger import logger as fastapi_logger

from api import router


gunicorn_error_logger = logging.getLogger("gunicorn.error")
gunicorn_logger = logging.getLogger("gunicorn")
uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.handlers = gunicorn_error_logger.handlers

fastapi_logger.handlers = gunicorn_error_logger.handlers
fastapi_logger.setLevel(logging.ERROR)

app = FastAPI()

app.include_router(router.router)