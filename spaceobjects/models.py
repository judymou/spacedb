# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import admin

class SpaceObject(models.Model):
  fullname = models.CharField(max_length=500)
  name = models.CharField(max_length=500)

  # Basic orbital elements
  a = models.FloatField()
  e = models.FloatField()
  i = models.FloatField()
  om = models.FloatField()
  w = models.FloatField()
  ma = models.FloatField()
  epoch = models.FloatField()

class CloseApproach(models.Model):
  space_object = models.ForeignKey(SpaceObject)
  dist_min = models.FloatField()

admin.site.register(SpaceObject)
