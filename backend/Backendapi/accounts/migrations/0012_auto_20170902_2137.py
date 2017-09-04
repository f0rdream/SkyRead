# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_starbooklist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='starbooklist',
            old_name='star_book_list',
            new_name='book_list',
        ),
    ]
