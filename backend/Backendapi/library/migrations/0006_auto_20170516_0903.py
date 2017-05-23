# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_successorderitem_waitorderitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='borrowitem',
            options={'permissions': (('is_a_book_admin', 'can add book to bar'),)},
        ),
        migrations.AddField(
            model_name='borrowitem',
            name='borrow_find_id',
            field=models.TextField(default=None),
        ),
    ]
