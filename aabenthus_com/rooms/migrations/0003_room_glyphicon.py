# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0002_room_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='glyphicon',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
    ]
