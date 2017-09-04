# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0020_borrowitem_without_check'),
    ]

    operations = [
        migrations.RenameField(
            model_name='borrowitem',
            old_name='without_check',
            new_name='quick_return',
        ),
    ]
