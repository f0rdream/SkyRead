# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookdata', '0003_auto_20170518_1053'),
    ]

    operations = [
        migrations.CreateModel(
            name='Refer',
            fields=[
                ('isbn13', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('refer_id', models.TextField(default=None)),
            ],
        ),
    ]
