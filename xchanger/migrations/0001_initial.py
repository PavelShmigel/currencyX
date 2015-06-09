# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('c_code', models.CharField(max_length=3)),
                ('c_name', models.CharField(max_length=140)),
            ],
        ),
        migrations.CreateModel(
            name='Rates',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('r_value', models.DecimalField(decimal_places=10, max_digits=19)),
                ('c_code', models.ForeignKey(to='xchanger.Currency')),
            ],
        ),
        migrations.CreateModel(
            name='UpdateInfo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('u_datatime', models.DateTimeField()),
                ('base_code', models.ForeignKey(to='xchanger.Currency')),
            ],
        ),
        migrations.AddField(
            model_name='rates',
            name='upd',
            field=models.ForeignKey(to='xchanger.UpdateInfo'),
        ),
    ]
