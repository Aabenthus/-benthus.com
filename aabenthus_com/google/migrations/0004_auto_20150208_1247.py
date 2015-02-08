# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('google', '0003_auto_20150208_1230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authorization',
            name='id',
        ),
        migrations.AlterField(
            model_name='authorization',
            name='email',
            field=models.EmailField(max_length=256, serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
