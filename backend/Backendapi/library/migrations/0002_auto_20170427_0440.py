# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='borrowitem',
            options={'permissions': (('is_a_admin', 'can add book to bar'),)},
        ),
        migrations.AddField(
            model_name='returnitem',
            name='borrow_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='returnitem',
            name='library_name',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='returnitem',
            name='location',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='returnitem',
            name='qrcode',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='returnitem',
            name='return_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='borrowitem',
            name='borrow_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='borrowitem',
            name='return_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
