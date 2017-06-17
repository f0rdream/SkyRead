# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_auto_20170613_0605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowitem',
            name='borrow_time',
            field=models.DateTimeField(default=None, blank=True),
        ),
        migrations.AlterField(
            model_name='borrowitem',
            name='return_time',
            field=models.DateTimeField(default=None, blank=True),
        ),
    ]
