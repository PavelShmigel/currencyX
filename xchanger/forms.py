# -*- coding:utf-8 -*-
from django import forms
from xchanger.models import Currency

__author__ = 'pavel.sh'

class ConverterForm(forms.Form):
    cc = [(c, c) for c in sorted(Currency.objects.values_list('c_code', flat=True))]
    amount = forms.DecimalField(widget=forms.TextInput(attrs={'class': "form-control",
                                                              'placeholder': "amount"}),
                                required=True,
                                label="")
    c_code_1 = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-control"}),
                                 choices=cc,
                                 initial='USD',
                                 label="")
    c_code_2 = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-control"}),
                                 choices=cc,
                                 initial='USD',
                                 label="")
