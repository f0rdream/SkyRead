# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookdata', '0016_planrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='planrecord',
            name='last_page',
            field=models.IntegerField(default=0),
        ),
    ]
