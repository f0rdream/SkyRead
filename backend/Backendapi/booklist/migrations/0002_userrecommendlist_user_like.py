# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booklist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrecommendlist',
            name='user_like',
            field=models.TextField(default=None),
        ),
    ]
