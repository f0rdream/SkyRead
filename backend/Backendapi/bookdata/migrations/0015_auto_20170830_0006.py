# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookdata', '0014_auto_20170829_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='readplan',
            name='last_date',
            field=models.CharField(default='xxxx-xx-xx', max_length=200),
        ),
        migrations.AddField(
            model_name='readplan',
            name='now_page',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='readplan',
            name='sum_page',
            field=models.IntegerField(default=0),
        ),
    ]
