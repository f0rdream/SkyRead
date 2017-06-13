# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0009_payitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowitem',
            name='borrow_time',
            field=models.CharField(default=None, max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='borrowitem',
            name='return_time',
            field=models.CharField(default=None, max_length=200, blank=True),
        ),
    ]
