# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookdata', '0012_book_author_for_index'),
        ('newadmin', '0008_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='about_book',
            field=models.ForeignKey(default=None, to='bookdata.Book'),
        ),
    ]
