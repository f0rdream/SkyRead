# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0004_borrowitem_finish_return'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuccessOrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('isbn13', models.CharField(default=b'', max_length=100)),
                ('order_time', models.DateTimeField(default=None, null=True, blank=True)),
                ('location', models.CharField(default=None, max_length=1000)),
                ('find_id', models.CharField(default=None, max_length=1000)),
                ('if_phone', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WaitOrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('isbn13', models.CharField(default=b'', max_length=100)),
                ('location', models.CharField(default=None, max_length=1000)),
                ('find_id', models.CharField(default=None, max_length=1000)),
                ('if_phone', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=1)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
