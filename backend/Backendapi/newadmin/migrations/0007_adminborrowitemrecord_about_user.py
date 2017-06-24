# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newadmin', '0006_excelfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminborrowitemrecord',
            name='about_user',
            field=models.IntegerField(default=0),
        ),
    ]
