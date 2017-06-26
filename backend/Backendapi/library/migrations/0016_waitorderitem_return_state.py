# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0015_auto_20170613_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='waitorderitem',
            name='return_state',
            field=models.BooleanField(default=False),
        ),
    ]
