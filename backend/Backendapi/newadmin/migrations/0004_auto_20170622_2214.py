# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('newadmin', '0003_adminpermission'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin_Permission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('andriod_permisson', models.BooleanField(default=False)),
                ('admin_permisson', models.BooleanField(default=False)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='adminpermission',
            name='user',
        ),
        migrations.DeleteModel(
            name='AdminPermission',
        ),
    ]
