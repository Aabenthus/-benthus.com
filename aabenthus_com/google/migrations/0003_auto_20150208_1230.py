# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import oauth2client.django_orm


class Migration(migrations.Migration):

    dependencies = [
        ('google', '0002_auto_20150207_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorization',
            name='credentials',
            field=oauth2client.django_orm.CredentialsField(null=True),
            preserve_default=True,
        ),
    ]
