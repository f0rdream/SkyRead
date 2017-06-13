# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0013_auto_20170613_1705'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='waitorderitem',
            name='find_id',
        ),
        migrations.RemoveField(
            model_name='waitorderitem',
            name='if_phone',
        ),
        migrations.RemoveField(
            model_name='waitorderitem',
            name='location',
        ),
        migrations.RemoveField(
            model_name='waitorderitem',
            name='status',
        ),
        migrations.AddField(
            model_name='waitorderitem',
            name='book_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='waitorderitem',
            name='may_return_time',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AddField(
            model_name='waitorderitem',
            name='title',
            field=models.TextField(default=None),
        ),
    ]
