# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import admin

class SpaceObject(models.Model):
  fullname = models.CharField(max_length=500)
  name = models.CharField(max_length=500)

class CloseApproach(models.Model):
  space_object = models.ForeignKey(SpaceObject)
  dist_min = models.FloatField()

admin.site.register(SpaceObject)
