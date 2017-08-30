# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookdata', '0017_planrecord_last_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='book_img_url',
            field=models.CharField(default=b'img_url', max_length=1000),
        ),
        migrations.AddField(
            model_name='note',
            name='comment',
            field=models.TextField(default=b'comment'),
        ),
    ]
