# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-05-16 22:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spaceobjects', '0031_auto_20190304_0448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shapemodel',
            name='jd',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shapemodel',
            name='period_hr',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shapemodel',
            name='spin_angle',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shapemodel',
            name='spin_latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shapemodel',
            name='spin_longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
