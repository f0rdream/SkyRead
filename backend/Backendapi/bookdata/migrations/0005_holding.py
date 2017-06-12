# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookdata', '0004_refer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Holding',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('isbn13', models.CharField(max_length=100)),
                ('state', models.BooleanField(default=True)),
                ('back_time', models.CharField(default=None, max_length=300)),
                ('location', models.CharField(max_length=300)),
                ('find_id', models.CharField(max_length=300)),
                ('order_number', models.IntegerField(default=0)),
                ('book', models.ForeignKey(to='bookdata.Book')),
            ],
        ),
    ]
