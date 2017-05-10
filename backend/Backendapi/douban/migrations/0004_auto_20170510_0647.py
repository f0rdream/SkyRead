# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('douban', '0003_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='author',
            field=models.TextField(default=None),
        ),
        migrations.AddField(
            model_name='review',
            name='content',
            field=models.TextField(default=None),
        ),
        migrations.AddField(
            model_name='review',
            name='title',
            field=models.TextField(default=None),
        ),
    ]
