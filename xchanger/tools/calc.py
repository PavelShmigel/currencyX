# -*- coding:utf-8 -*-
from decimal import Decimal
from django.db.models import Max
from xchanger.models import UpdateInfo, Currency, Rates
from xchanger.tools.dbupdate import update_db

__author__ = 'pavel.sh'

calc_xchange_value = lambda amount, rate_1, rate_2: amount/rate_1*rate_2

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
