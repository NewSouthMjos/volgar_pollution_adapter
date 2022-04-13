from datetime import date

from fastapi import APIRouter, HTTPException, Response

from commons.settings import settings
from commons.metrics_core import metrics
from api.services import pogoda_handler

router = APIRouter()

CONTENT_TYPE_LATEST = 'text/plain; version=0.0.4; charset=utf-8'


@router.get('/pollutions')
def get_pollutions():
    imp_dict = pogoda_handler.get_impurities_data()
    for key, impurity in imp_dict.items():
        metrics.meters.g1().labels(key, 'calc').set(float(impurity['value']))
        metrics.meters.g1().labels(key, 'pogoda_sv_rounded').set(float(impurity['factor']))

    return Response(content=metrics.generate_latest(), media_type=CONTENT_TYPE_LATEST)


@router.get('/version', status_code=200)
def get_version():
    return {'version': settings.version}