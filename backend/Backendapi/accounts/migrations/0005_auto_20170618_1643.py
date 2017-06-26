# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_phoneuser_money'),
    ]

    operations = [
        migrations.AddField(
            model_name='phoneuser',
            name='order_message',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='phoneuser',
            name='return_message',
            field=models.BooleanField(default=True),
        ),
    ]
