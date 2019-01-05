# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-05 17:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spaceobjects', '0016_auto_20190105_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='spaceobject',
            name='is_neo',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spaceobject',
            name='is_pha',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
