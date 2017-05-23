# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('isbn13', models.CharField(default=None, max_length=200)),
                ('author', models.CharField(default=None, max_length=200, null=True, blank=True)),
                ('time', models.CharField(default=None, max_length=200, null=True, blank=True)),
                ('star', models.IntegerField(default=None)),
                ('vote', models.CharField(default=None, max_length=200, null=True, blank=True)),
                ('content', models.TextField(default=None)),
            ],
        ),
    ]
