# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20170709_1835'),
    ]

    operations = [
        migrations.AddField(
            model_name='phoneuser',
            name='recommend_times',
            field=models.IntegerField(default=1),
        ),
    ]
