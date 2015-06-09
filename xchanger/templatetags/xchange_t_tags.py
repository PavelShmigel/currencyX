# -*- coding:utf-8 -*-
from django import template
from django.db.models import Max
from xchanger.models import UpdateInfo, Rates
from xchanger.tools.dbupdate import update_db

register = template.Library()

@register.inclusion_tag('results.html')
def show_results():
    success = 0
    base_currency = None
    upd_date = None
    currency_course = list()
    try:
        # если база пуста
        if UpdateInfo.objects.all().count() == 0:
            update_db()
        # получаем последнее обновление
        last_upd = UpdateInfo.objects.all().aggregate(Max('u_datatime'))
        upd_obj = UpdateInfo.objects.get(u_datatime=last_upd['u_datatime__max'])

        base_currency = upd_obj.base_code
        upd_date = upd_obj.u_datatime

        for course in Rates.objects.filter(upd=upd_obj.id):
            c_code = course.c_code.c_code
            c_name = course.c_code.c_name
            value = course.r_value
            currency_course.append((c_code, c_name, value))
        success = 1
    except:
        return {'success': success}

    return {'success': success,
            'base_currency': base_currency,
            'upd_date': upd_date,
            'currency_course': sorted(currency_course)}
