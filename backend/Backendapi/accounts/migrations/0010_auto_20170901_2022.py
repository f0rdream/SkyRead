# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('bookdata', '0018_auto_20170830_1617'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0009_starlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookInList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('book', models.ForeignKey(to='bookdata.Book')),
            ],
        ),
        migrations.CreateModel(
            name='UserCreateBookList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=1000)),
                ('comment', models.TextField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='bookinlist',
            name='book_list',
            field=models.ForeignKey(to='accounts.UserCreateBookList'),
        ),
    ]
