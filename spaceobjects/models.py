# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import admin

class SpaceObject(models.Model):
  name = models.CharField(max_length=500)

admin.site.register(SpaceObject)
