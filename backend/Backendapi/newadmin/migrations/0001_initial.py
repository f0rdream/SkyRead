# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0017_returnitem'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminBorrowItemRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('record_type', models.IntegerField(default=0)),
                ('record_time', models.DateTimeField(auto_now_add=True)),
                ('PayItem', models.ForeignKey(blank=True, to='library.PayItem', null=True)),
                ('borrow_item', models.ForeignKey(blank=True, to='library.BorrowItem', null=True)),
                ('order_item', models.ForeignKey(blank=True, to='library.SuccessOrderItem', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
