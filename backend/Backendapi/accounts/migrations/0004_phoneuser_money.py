# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20170617_1325'),
    ]

    operations = [
        migrations.AddField(
            model_name='phoneuser',
            name='money',
            field=models.IntegerField(default=0),
        ),
    ]
