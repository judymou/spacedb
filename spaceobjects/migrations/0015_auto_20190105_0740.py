# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-05 07:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spaceobjects', '0014_auto_20181227_1730'),
    ]

    operations = [
        migrations.AddField(
            model_name='spaceobject',
            name='H',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spaceobject',
            name='diameter',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='spaceobject',
            name='neo',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spaceobject',
            name='orbit_class',
            field=models.CharField(default='A', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spaceobject',
            name='pha',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spaceobject',
            name='spec_B',
            field=models.CharField(default='C', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spaceobject',
            name='spec_T',
            field=models.CharField(default='C', max_length=200),
            preserve_default=False,
        ),
    ]
