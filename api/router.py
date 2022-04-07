from datetime import date

from fastapi import APIRouter, HTTPException, Response

from commons.settings import settings
from commons.metrics_core import metrics
from api.services import pogoda_handler

router = APIRouter()

CONTENT_TYPE_LATEST = 'text/plain; version=0.0.4; charset=utf-8'

@router.get('/pollutions')
def get_pollutions():
    # l1 = "# HELP PARAM1 Description\n"
    # l2 = "# TYPE PARAM1 gauge\n"
    # l3 = f"PARAM1 {a.gauge1}\n"
    # result = ''.join((l1, l2, l3)).replace('\n', r'\n').encode('utf-8')
    # headers = {'Content-Type': CONTENT_TYPE_LATEST}
    # return Response(content=result, headers=headers)
    imp_dict = pogoda_handler.get_impurities_data()
    for key, impurity in imp_dict.items():
        metrics.meters.g1().labels(key, 'calc').set(float(impurity['value']))
        metrics.meters.g1().labels(key, 'pogoda_sv_rounded').set(float(impurity['factor']))

    return Response(content=metrics.generate_latest(), media_type=CONTENT_TYPE_LATEST)

# @router.get('/set_gauge1', status_code=200)
# def set_gauge1(number:int):
#     metrics.meters.c1().set(number)
#     # metrics.meters.c1.set(number)
#     return {'success': True}

@router.get('/version', status_code=200)
def get_version():
    return {'version': settings.version}