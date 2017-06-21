# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newadmin', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminborrowitemrecord',
            name='PayItem',
        ),
        migrations.AddField(
            model_name='adminborrowitemrecord',
            name='pay_id',
            field=models.IntegerField(default=0),
        ),
    ]
