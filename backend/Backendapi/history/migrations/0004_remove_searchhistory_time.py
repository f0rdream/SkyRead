# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0003_auto_20170619_1220'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='searchhistory',
            name='time',
        ),
    ]
