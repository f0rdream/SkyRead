# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('douban', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reading',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('isbn13', models.CharField(default=None, max_length=200)),
                ('title', models.TextField(default=None)),
                ('note', models.TextField(default=None)),
            ],
        ),
    ]
