# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_usercreatebooklist_img_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercreatebooklist',
            name='date',
            field=models.CharField(default=b'xxxx-xx-xx', max_length=300),
        ),
    ]
