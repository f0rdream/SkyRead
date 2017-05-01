# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WeChatUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(default=b'', max_length=1000)),
                ('openid', models.CharField(default=b'', max_length=1000)),
                ('sex', models.IntegerField(default=1)),
                ('province', models.CharField(default=b'', max_length=1000)),
                ('city', models.CharField(default=b'', max_length=1000)),
                ('country', models.CharField(default=b'', max_length=1000)),
                ('headimgurl', models.CharField(default=b'', max_length=1000)),
            ],
        ),
    ]
