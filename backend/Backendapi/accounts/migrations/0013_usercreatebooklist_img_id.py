# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20170902_2137'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercreatebooklist',
            name='img_id',
            field=models.CharField(default=b'--', max_length=300),
        ),
    ]
