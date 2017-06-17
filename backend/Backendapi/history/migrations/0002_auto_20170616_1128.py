# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderhistory',
            name='user',
        ),
        migrations.DeleteModel(
            name='OrderHistory',
        ),
    ]
