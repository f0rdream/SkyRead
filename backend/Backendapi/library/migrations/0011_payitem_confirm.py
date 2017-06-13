# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0010_auto_20170613_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='payitem',
            name='confirm',
            field=models.BooleanField(default=False),
        ),
    ]
