# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AmazonComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('isbn13', models.CharField(default=None, max_length=200)),
                ('author', models.TextField(default=None)),
                ('content', models.TextField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='AmazonInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(default=None)),
                ('isbn13', models.CharField(default=None, max_length=200)),
                ('average', models.CharField(default=None, max_length=200)),
                ('erecommand', models.TextField(default=None)),
                ('frecommand', models.TextField(default=None)),
                ('mrecommand', models.TextField(default=None)),
            ],
        ),
    ]
