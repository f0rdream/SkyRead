# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0012_payitem_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='successorderitem',
            old_name='if_phone',
            new_name='book_id',
        ),
        migrations.RemoveField(
            model_name='successorderitem',
            name='find_id',
        ),
        migrations.RemoveField(
            model_name='successorderitem',
            name='location',
        ),
        migrations.RemoveField(
            model_name='successorderitem',
            name='status',
        ),
        migrations.AddField(
            model_name='successorderitem',
            name='qrcode',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='successorderitem',
            name='title',
            field=models.TextField(default=None),
        ),
    ]
