# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0014_auto_20170613_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='successorderitem',
            name='order_time',
            field=models.DateTimeField(default=None),
        ),
    ]
