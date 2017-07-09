# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newadmin', '0009_picture_about_book'),
    ]

    operations = [
        migrations.RenameField(
            model_name='picture',
            old_name='isbn13_list',
            new_name='isbn13',
        ),
    ]
