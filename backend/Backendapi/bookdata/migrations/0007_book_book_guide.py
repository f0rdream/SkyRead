# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookdata', '0006_starbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_guide',
            field=models.IntegerField(default=0),
        ),
    ]
