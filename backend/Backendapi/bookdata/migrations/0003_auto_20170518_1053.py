# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookdata', '0002_bookcomment_bookreview'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BookComment',
        ),
        migrations.DeleteModel(
            name='BookReview',
        ),
    ]
