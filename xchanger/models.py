from django.db import models

# Таблица с кодами валют
class Currency(models.Model):
    c_code = models.CharField(max_length=3)
    c_name = models.CharField(max_length=140)

    def __str__(self):
        return '{}, {}'.format(self.c_code, self.c_name)

# Таблица с временем обновления и базовой валютой
class UpdateInfo(models.Model):
    u_datatime = models.DateTimeField()
    # на случай изменения базовой валюты, сохраним для дальнейших рассчетов
    base_code = models.ForeignKey(Currency)

    def __str__(self):
        return '{}, {}'.format(self.u_datatime, self.base_code.c_code)

# Таблица с соответствиями курса валюты и времени обновления
class Rates(models.Model):
    c_code = models.ForeignKey(Currency)
    # курс валюты относительно базового на время обновления
    r_value = models.DecimalField(max_digits=19, decimal_places=10)
    # ид обновления
    upd = models.ForeignKey(UpdateInfo)

    def __str__(self):
        return '{}, {}, {}'.format(self.c_code.c_code,
                                   self.r_value,
                                   self.upd.u_datatime)
