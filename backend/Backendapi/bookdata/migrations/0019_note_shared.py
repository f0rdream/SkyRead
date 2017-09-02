# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookdata', '0018_auto_20170830_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='shared',
            field=models.BooleanField(default=False),
        ),
    ]
