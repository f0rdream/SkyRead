# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookdata', '0013_imagefile_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='isbn13',
            field=models.CharField(default='-1', max_length=1000),
        ),
    ]
