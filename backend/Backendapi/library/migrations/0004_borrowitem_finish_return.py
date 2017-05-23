# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_auto_20170427_0845'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowitem',
            name='finish_return',
            field=models.BooleanField(default=False),
        ),
    ]
