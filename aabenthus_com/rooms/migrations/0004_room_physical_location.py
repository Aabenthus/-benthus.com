# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0003_room_glyphicon'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='physical_location',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
    ]
