# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-17 02:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spaceobjects', '0008_auto_20181216_2135'),
    ]

    operations = [
        migrations.CreateModel(
            name='SentryEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('energy_mt', models.FloatField()),
                ('dist_km', models.FloatField()),
                ('dist_err', models.FloatField()),
                ('palermo_scale', models.FloatField()),
                ('torino_scale', models.FloatField()),
                ('prob', models.FloatField()),
                ('space_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spaceobjects.SpaceObject')),
            ],
        ),
    ]
