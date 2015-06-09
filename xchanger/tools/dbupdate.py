# -*- coding:utf-8 -*-
from datetime import datetime
from threading import RLock
from requests import Session
import sys
import json
from currencyX.private_settings import APP_ID
from xchanger.models import Currency, UpdateInfo, Rates

__author__ = 'pavel.sh'

BASE_URL = 'https://openexchangerates.org/api/'
CURRENCIES = 'currencies.json'
LATEST_RATES = 'latest.json'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0',
           'Accept-Encoding': 'gzip, deflate',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

def getCurrencys():
    result = None
    s = Session()
    try:
        resp = s.get(BASE_URL+CURRENCIES, params={'app_id': APP_ID})
        currencys = json.loads(resp.text)

        result = currencys

    except Exception as e:
        result = None
    finally:
        s.close()
        return result

def getRates():
    result = None
    s = Session()
    try:
        resp = s.get(BASE_URL+LATEST_RATES, params={'app_id': APP_ID})

        raw_rates_json = json.loads(resp.text)
        result = raw_rates_json

    except Exception as e:
        result = None
    finally:
        s.close()
        return result

lock = RLock()
def update_db():
    with lock:
        currency_codes = None
        raw_upd_rates_json = None

        # Загрузим описания валют
        currencys = getCurrencys()
        # Если получилось, добавим новые коды в базу
        if currencys:
            c_codes = Currency.objects.values_list('c_code', flat=True)
            c_codes_dif = [cc for cc in currencys.keys() if cc not in c_codes]
            if len(c_codes_dif) > 0:
                for c_code in c_codes_dif:
                    Currency.objects.create(c_code=c_code, c_name=currencys[c_code])

        # Получим latest.json с курсом валют, базовой валютой и временем обновления
        raw_upd_rates_json = getRates()
        if raw_upd_rates_json:
            # Переобразуем пришедший tmestamp в datetime
            d_t = datetime.fromtimestamp(raw_upd_rates_json['timestamp'])

            # Если такого обновления небыло
            if UpdateInfo.objects.filter(u_datatime=d_t).count() == 0:

                # Код базовой валюты
                base_c_code = raw_upd_rates_json['base']
                # Курсы валют
                rates = raw_upd_rates_json['rates']
                # Объект базовой валюты
                base_c_code_obj = Currency.objects.get(c_code=base_c_code)

                # Запишем время изменения и базовую валюту
                upd_obj = UpdateInfo.objects.create(u_datatime=d_t,
                                                    base_code_id=base_c_code_obj.id)

                # запишем новые курсы валют
                for c_code, value in rates.items():
                    currency_obj = Currency.objects.get(c_code=c_code)
                    Rates.objects.create(c_code_id=currency_obj.id,
                                         r_value=value,
                                         upd_id=upd_obj.id)
