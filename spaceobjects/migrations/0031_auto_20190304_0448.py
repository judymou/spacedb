# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-03-04 04:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spaceobjects', '0030_auto_20190226_0604'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='closeapproach',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='nhatsobject',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='sentryevent',
            options={'ordering': ['id']},
        ),
        migrations.AddIndex(
            model_name='closeapproach',
            index=models.Index(fields=['date'], name='spaceobject_date_e8c089_idx'),
        ),
        migrations.AddIndex(
            model_name='spaceobject',
            index=models.Index(fields=['diameter'], name='spaceobject_diamete_a2968b_idx'),
        ),
        migrations.AddIndex(
            model_name='sentryevent',
            index=models.Index(fields=['prob'], name='spaceobject_prob_b35e86_idx'),
        ),
        migrations.AddIndex(
            model_name='nhatsobject',
            index=models.Index(fields=['min_dv'], name='spaceobject_min_dv_014adf_idx'),
        ),
    ]