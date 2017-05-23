# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_auto_20170427_0440'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='returnitem',
            name='user',
        ),
        migrations.AddField(
            model_name='borrowitem',
            name='in_return_bar',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='ReturnItem',
        ),
    ]
