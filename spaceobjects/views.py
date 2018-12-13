# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import SpaceObject

def index(request):
  space_objects = SpaceObject.objects.all()
  return render(request, 'spaceobjects/index.html',
      {'space_objects': space_objects})

def detail(request, name):
  try:
    space_object = SpaceObject.objects.get(name__iexact=name)
  except SpaceObject.DoesNotExist:
    return index(request)
  return render(request, 'spaceobjects/detail.html',
      {'object': space_object})
