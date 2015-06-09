from django.contrib import admin
from xchanger.models import Currency, Rates, UpdateInfo


class CurrencyAdmin(admin.ModelAdmin):
    pass

class UpdAdmin(admin.ModelAdmin):
    pass


class RatesAdmin(admin.ModelAdmin):
    list_filter = ['c_code_id', 'upd_id']

admin.site.register(Currency, CurrencyAdmin)
admin.site.register(UpdateInfo, UpdAdmin)
admin.site.register(Rates, RatesAdmin)
