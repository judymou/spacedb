# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-17 05:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spaceobjects', '0009_sentryevent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='closeapproach',
            name='time_jd',
        ),
        migrations.AddField(
            model_name='closeapproach',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 12, 17, 5, 56, 9, 89760)),
            preserve_default=False,
        ),
    ]
