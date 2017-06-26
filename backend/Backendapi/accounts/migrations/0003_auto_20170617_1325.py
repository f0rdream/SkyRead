# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_phoneuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phoneuser',
            name='email',
            field=models.CharField(default=None, max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='phoneuser',
            name='real_name',
            field=models.CharField(default=None, max_length=200, null=True, blank=True),
        ),
    ]
