# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0019_successorderitem_be_out'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowitem',
            name='without_check',
            field=models.BooleanField(default=False),
        ),
    ]
