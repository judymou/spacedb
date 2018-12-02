# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import SpaceObject

def index(request):
  space_objects = SpaceObject.objects.all()
  return render(request, 'spaceobjects/index.html',
      {'space_objects': space_objects})
