# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0017_returnitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='payitem',
            name='borrow_id',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
    ]
