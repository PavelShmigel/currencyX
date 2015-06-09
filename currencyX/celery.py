# -*- coding:utf-8 -*-
from __future__ import absolute_import

__author__ = 'pavel.sh'

import os
from celery import Celery
from django.conf import settings

# Indicate Celery to use the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'currencyX.settings')

app = Celery('currencyX')
app.config_from_object('django.conf:settings')
# This line will tell Celery to autodiscover all your tasks.py that are in your app folders
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)