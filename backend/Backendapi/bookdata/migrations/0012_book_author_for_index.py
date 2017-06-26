# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookdata', '0011_browsedbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='author_for_index',
            field=models.TextField(default=None),
        ),
    ]
