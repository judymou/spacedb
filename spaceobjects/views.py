# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import SpaceObject

def index(request):
    space_objects = SpaceObject.objects.all()[:30]
    return render(request, 'spaceobjects/index.html',
          {'space_objects': space_objects})

def detail(request, slug):
    try:
        space_object = SpaceObject.objects.get(slug__iexact=slug)
    except SpaceObject.DoesNotExist:
        return index(request)
    return render(request, 'spaceobjects/detail.html',
        {'object': space_object})

def search(request):
    search_str = request.GET.get('q')
    matches = SpaceObject.objects.filter(fullname__icontains=search_str)
    return JsonResponse({'results': [roid.to_search_result() for roid in matches[:10]]})

def random(request):
    obj = SpaceObject.objects.order_by('?').first()
    return redirect(obj)
