# -*- coding:utf-8 -*-
from django.conf.urls import include, url

__author__ = 'pavel.sh'

urlpatterns = [
    url(r'text/$', 'xchanger.views.getInText'),
    url(r'json/$', 'xchanger.views.getInJson'),
]
