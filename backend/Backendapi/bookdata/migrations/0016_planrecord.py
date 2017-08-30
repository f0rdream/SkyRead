# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookdata', '0015_auto_20170830_0006'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('record_date', models.CharField(default='xxxx-xx-xx', max_length=200)),
                ('now_page', models.IntegerField(default=0)),
                ('plan_for', models.ForeignKey(to='bookdata.ReadPlan')),
            ],
        ),
    ]
