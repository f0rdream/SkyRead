# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_usercreatebooklist_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercreatebooklist',
            name='star',
            field=models.IntegerField(default=0),
        ),
    ]
