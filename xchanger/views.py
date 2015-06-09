import json
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from xchanger.tools.calc import getResult

# Create your views here.

@cache_page(60*30)
def getInText(request, **kwargs):
    result = getResult(**kwargs)
    resp = str(result['result']) if result['success'] else result['error']
    return HttpResponse(resp)

@cache_page(60*30)
def getInJson(request, **kwargs):
    result = getResult(**kwargs)
    resp = json.dumps(result)
    return HttpResponse(resp, content_type="application/json")



def test404(request, **kwargs):
    if request.POST:
        return HttpResponse('{}'.format(request.POST))
    return HttpResponse('404: указан несуществующий путь {}\n')
