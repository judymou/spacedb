# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-02-23 19:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spaceobjects', '0025_auto_20190202_0328'),
    ]

    operations = [
        migrations.RenameField(
            model_name='spaceobject',
            old_name='is_neo',
            new_name='is_nea',
        ),
        migrations.AddIndex(
            model_name='spaceobject',
            index=models.Index(fields=['is_nea'], name='spaceobject_is_nea_27a9a3_idx'),
        ),
        migrations.AddIndex(
            model_name='spaceobject',
            index=models.Index(fields=['is_pha'], name='spaceobject_is_pha_3d9700_idx'),
        ),
    ]