# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('isbn13', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('numraters', models.CharField(default=b'', max_length=100)),
                ('average', models.CharField(default=b'', max_length=100)),
                ('subtitle', models.CharField(default=b'', max_length=500)),
                ('author', models.CharField(default=b'', max_length=1000)),
                ('pubdate', models.CharField(default=b'', max_length=100)),
                ('origin_title', models.CharField(default=b'', max_length=500)),
                ('img_id', models.CharField(default=b'', max_length=100)),
                ('bingding', models.CharField(default=b'', max_length=100)),
                ('tags', models.TextField(default=b'')),
                ('catalog', models.TextField(default=b'')),
                ('pages', models.CharField(default=b'', max_length=100)),
                ('d_id', models.CharField(default=b'', max_length=100)),
                ('publisher', models.CharField(default=b'', max_length=500)),
                ('title', models.CharField(default=b'', max_length=500)),
                ('summary', models.TextField(default=b'')),
                ('author_intro', models.TextField(default=b'')),
                ('price', models.CharField(default=b'', max_length=100)),
            ],
        ),
    ]
