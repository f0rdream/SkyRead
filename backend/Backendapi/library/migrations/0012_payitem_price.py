# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0011_payitem_confirm'),
    ]

    operations = [
        migrations.AddField(
            model_name='payitem',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
