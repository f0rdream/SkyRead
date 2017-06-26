# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookdata', '0009_readplan'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='title_for_index',
            field=models.TextField(default=None),
        ),
    ]
