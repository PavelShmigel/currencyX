# -*- coding:utf-8 -*-
from decimal import Decimal
from functools import wraps
from django.db.models import Max
from django.core.cache import cache as _cache
from xchanger.models import UpdateInfo, Currency, Rates
from xchanger.tools.dbupdate import update_db

__author__ = 'pavel.sh'

calc_xchange_value = lambda amount, rate_1, rate_2: amount/rate_1*rate_2

class cache(object):

    def __init__(self, seconds=None):
        self.seconds = seconds

    def __call__(self, func):

        @wraps(func)
        def callable(*args, **kwargs):
            cache_key = [func, args, kwargs]
            result = _cache.get(cache_key)
            if result:
                return result
            result = func(*args, **kwargs)
            _cache.set(cache_key, result, timeout=self.seconds)
            return result

        return callable

@cache(seconds=60*30)
def getResult(amount, c_code_1, c_code_2):
    success = True
    result = dict()
    # если база пуста
    if UpdateInfo.objects.all().count() == 0:
        update_db()
    # получаем последнее обновление
    last_upd = UpdateInfo.objects.all().aggregate(Max('u_datatime'))
    upd_obj = UpdateInfo.objects.get(u_datatime=last_upd['u_datatime__max'])

    try:
        # получим id валют
        с_id_1 = Currency.objects.get(c_code=c_code_1.upper()).id
        с_id_2 = Currency.objects.get(c_code=c_code_2.upper()).id
    except:
        success = False
        error = 'Указан несуществующий код валюты'
        result.update({'success': success})
        result.update({'error': error})
        return result

    try:
        # достанем курсы валют относительно базовой валюты
        rate_1 = Rates.objects.get(c_code_id=с_id_1, upd_id=upd_obj.id).r_value
        rate_2 = Rates.objects.get(c_code_id=с_id_2, upd_id=upd_obj.id).r_value
    except:
        success = False
        error = 'Данные по курсу одной из валют отсутствуют'
        result.update({'success': success})
        result.update({'error': error})
        return result

    val = calc_xchange_value(Decimal(amount), rate_1, rate_2)
    result.update({'success': success})
    result.update({'result': float(val)})
    return result

def floatSmartRound(x):
    try:
        if x > 1000:
            result = round(x, 2)
        elif x > 100:
            result = round(x, 3)
        elif x > 1:
            result = round(x, 4)
        elif x > 0.00001:
            result = round(x, 6)
        elif x > 0.0000001:
            result = round(x, 8)
        else:
            # иначе все пичально
            result = x
    except:
        result = x
    finally:
        return result