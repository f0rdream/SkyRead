# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20170618_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phoneuser',
            name='money',
            field=models.IntegerField(default=1000000),
        ),
    ]
