import json
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from xchanger.tools.calc import getResult,floatSmartRound
from django.template import RequestContext
from xchanger.forms import ConverterForm
from xchanger.models import Currency

# Create your views here.


def getInText(request, **kwargs):
    result = getResult(**kwargs)
    resp = str(result['result']) if result['success'] else result['error']
    return HttpResponse(resp)


def getInJson(request, **kwargs):
    result = getResult(**kwargs)
    resp = json.dumps(result)
    return HttpResponse(resp, content_type="application/json")


def getInHtml(request, **kwargs):
    if request.POST:
        form = ConverterForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            c_code_1 = form.cleaned_data['c_code_1']
            c_code_2 = form.cleaned_data['c_code_2']
            return redirect('xchanger.views.getInHtml', amount=str(amount), c_code_1=c_code_1, c_code_2=c_code_2)
        else:
            return render_to_response(template_name='xchange_form.html',
                                      context={'form': form, 'is_valid': False},
                                      context_instance=RequestContext(request))
    default = dict()
    if len(kwargs) != 0:
        for k, v in kwargs.items():
            default[k] = v.upper()
    else:
        default.update({'c_code_1': 'USD', 'c_code_2': 'USD'})
    form = ConverterForm(default)
    if form.is_valid():
        result = getResult(**kwargs)
        amount = form.cleaned_data['amount']
        c_code_1 = form.cleaned_data['c_code_1']
        c_code_2 = form.cleaned_data['c_code_2']
        currency_1 = Currency.objects.get(c_code=c_code_1).c_name
        currency_2 = Currency.objects.get(c_code=c_code_2).c_name
        return render_to_response(template_name='answer.html',
                                  context={'form': form,
                                           'amount': float(amount),
                                           'currency_1': currency_1,
                                           'currency_2': currency_2,
                                           'value': floatSmartRound(result)},
                                  context_instance=RequestContext(request))

    return render_to_response(template_name='xchange_form.html',
                              context={'form': form},
                              context_instance=RequestContext(request))

def test404(request, **kwargs):
    if request.POST:
        return HttpResponse('{}'.format(request.POST))
    return HttpResponse('404: указан несуществующий путь {}\n')
