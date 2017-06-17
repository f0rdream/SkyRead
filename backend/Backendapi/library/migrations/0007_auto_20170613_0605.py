# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_auto_20170516_0903'),
    ]

    operations = [
        migrations.RenameField(
            model_name='borrowitem',
            old_name='borrow_find_id',
            new_name='book_id',
        ),
        migrations.RemoveField(
            model_name='borrowitem',
            name='library_name',
        ),
        migrations.AddField(
            model_name='borrowitem',
            name='find_id',
            field=models.TextField(default=None),
        ),
    ]
