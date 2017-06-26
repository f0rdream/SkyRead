# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0018_payitem_borrow_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='successorderitem',
            name='be_out',
            field=models.BooleanField(default=False),
        ),
    ]
