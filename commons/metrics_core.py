from time import time
from math import log10 , floor
import functools
from os import getenv 

from prometheus_client import (CollectorRegistry,
    generate_latest, Counter, Histogram, Gauge)


registry = CollectorRegistry()

METRICS_COUNTER_PASSAGES_LIMITS_LOWER = float(getenv('METRICS_COUNTER_PASSAGES_LIMITS_LOWER', 0.25))
METRICS_COUNTER_PASSAGES_LIMITS_UPPER = float(getenv('METRICS_COUNTER_PASSAGES_LIMITS_UPPER', 64))
METRICS_COUNTER_PASSAGES_INTERVALS_COUNT = int(getenv('METRICS_COUNTER_PASSAGES_INTERVALS_COUNT', 9))

def round_it(x, sig):
    """Округляет до первых sig значащих цифр
    Пример: round_it(0.12399, 3) > 0.124
    round_it(42365.2323, 3) > 42400.0
    """
    return round(x, sig-int(floor(log10(abs(x))))-1)


class MetricsCore:
    class __Meters:
        def __init__(self) -> None:
            self._g1 = Gauge(
                "pollutions",
                "Все загрязнения и погода",
                ['id', 'data_source'],
                registry=registry
            )

        def g1(self) -> Gauge:
            return self._g1

        # @staticmethod
        # def calculate_buckets_intervals(
        #         lower_limit: float, upper_limit: float, intervals_count: int = 10):
        #     """
        #     Строит интервалы для пропорциональной шкалы.
        #     Пропорциональная - каждое следующее значение
        #     на шкале больше предыдущего в k раз.
        #     Пример: calculate_buckets_intervals(1, 32, 6)
        #     >(1.0, 2.0, 4.0, 8.0, 16.0, 32.0, inf)
        #     """
        #     k = (upper_limit/lower_limit) ** (1 / (intervals_count-1))
        #     result = (lower_limit * k**i for i in range(intervals_count))
        #     return tuple(round_it(number, 3) for number in result) + tuple([float('inf')])


    def __init__(self) -> None:
        # self.check_envs()
        self.meters = self.__Meters()

    def generate_latest(self):
        return generate_latest(registry)

    # def catch_metrics(self, func):
    #     @functools.wraps(func)
    #     def wrapper(*args, **kwargs):
    #         start = time()
    #         return_value = func(*args, **kwargs)
    #         end = time()
    #         r_time = end-start
    #         f_name = func.__name__
    #         self.counters._h.labels(f_name).observe(r_time)
    #         return return_value
    #     return wrapper

    # @staticmethod
    # def check_envs():
    #     if METRICS_COUNTER_PASSAGES_LIMITS_LOWER <= 0:
    #         msg = 'METRICS_COUNTER_PASSAGES_LIMITS_LOWER должна быть больше 0'
    #         raise EnvironmentError(msg)
    #     if METRICS_COUNTER_PASSAGES_INTERVALS_COUNT < 2:
    #         msg = ('METRICS_COUNTER_PASSAGES_INTERVALS_COUNT - количество'
    #                ' интервалов должно быть больше или равно 2')
    #         raise EnvironmentError(msg)
    
    def save_data_to_regisry(self, d: dict) -> None:
        """
        Сохраняет из пришедшего словаря данные в свой
        регеестр информации
        """
        for key, value in d.items():
            self.meters.g1().labels('')


metrics = MetricsCore()
