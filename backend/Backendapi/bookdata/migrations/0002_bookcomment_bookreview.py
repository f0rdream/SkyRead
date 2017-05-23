# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookdata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('isbn13', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=1000, null=True, blank=True)),
                ('time', models.CharField(max_length=200, null=True, blank=True)),
                ('star', models.CharField(max_length=200, null=True, blank=True)),
                ('vote', models.CharField(max_length=200, null=True, blank=True)),
                ('content', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='BookReview',
            fields=[
                ('review_id', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('isbn13', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=1000, null=True, blank=True)),
                ('title', models.CharField(max_length=1000, null=True, blank=True)),
                ('content', models.TextField(max_length=1000, null=True, blank=True)),
                ('is_link', models.BooleanField(default=False)),
            ],
        ),
    ]
