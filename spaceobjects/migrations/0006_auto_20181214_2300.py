# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-14 23:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spaceobjects', '0005_spaceobject_sbdb_entry'),
    ]

    operations = [
        migrations.AddField(
            model_name='spaceobject',
            name='slug',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='spaceobject',
            name='fullname',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='spaceobject',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
