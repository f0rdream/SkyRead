# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newadmin', '0007_adminborrowitemrecord_about_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('picture', models.ImageField(upload_to=b'./newadmin/picture')),
                ('isbn13_list', models.TextField()),
            ],
        ),
    ]
