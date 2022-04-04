from datetime import date
from pickle import GLOBAL

from fastapi import APIRouter, HTTPException, Response

from commons.settings import settings

from prometheus_client import (multiprocess, CollectorRegistry,
    generate_latest, Gauge)

registry = CollectorRegistry()
multiprocess.MultiProcessCollector(registry)

router = APIRouter()

CONTENT_TYPE_LATEST = 'text/plain; version=0.0.4; charset=utf-8'

class Jimbo():
    def __init__(self) -> None:
        self.gauge1 = Gauge('gauge1', 'Desc')

a = Jimbo()



@router.get('/pollutions')
def get_pollutions():
    # l1 = "# HELP PARAM1 Description\n"
    # l2 = "# TYPE PARAM1 gauge\n"
    # l3 = f"PARAM1 {a.gauge1}\n"
    # result = ''.join((l1, l2, l3)).replace('\n', r'\n').encode('utf-8')
    # headers = {'Content-Type': CONTENT_TYPE_LATEST}
    # return Response(content=result, headers=headers)

    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@router.get('/set_gauge1', status_code=200)
def get_version(number:int):
    a.gauge1.set(number)
    return {'success': True}

@router.get('/version', status_code=200)
def get_version():
    return {'version': settings.version}



