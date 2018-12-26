# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from spaceobjects.models import SpaceObject, SentryEvent, CloseApproach, NhatsObject

def index(request):
    space_objects = SpaceObject.objects.all()[:5]

    potential_impactors = []
    seen_impactors = set()
    for event in SentryEvent.objects.order_by('-prob'):
        if event.space_object.fullname in seen_impactors:
            continue
        potential_impactors.append(event)
        seen_impactors.add(event.space_object.fullname)
        if len(potential_impactors) >= 5:
            break

    close_approaches = []
    seen_approaches = set()
    for event in CloseApproach.objects.order_by('date'):
        if event.space_object.fullname in seen_approaches:
            continue
        close_approaches.append(event)
        seen_approaches.add(event.space_object.fullname)
        if len(close_approaches) >= 5:
            break

    return render(request, 'spaceobjects/index.html',
          {
              'space_objects': space_objects,
              'potential_impactors': potential_impactors,
              'close_approaches': close_approaches,
              'nhats_objects': NhatsObject.objects.all()[:5],
              'hide_top_nav': True,
          })

def detail(request, slug):
    try:
        space_object = SpaceObject.objects.get(slug__iexact=slug)
    except SpaceObject.DoesNotExist:
        return index(request)

    sentry_events = space_object.sentryevent_set.all().order_by('-prob')

    return render(request, 'spaceobjects/detail.html', {
                'object': space_object,
                'sentry_events': sentry_events,
            })

def search(request):
    search_str = request.GET.get('q')
    matches = SpaceObject.objects.filter(fullname__icontains=search_str)
    return JsonResponse({'results': [roid.to_search_result() for roid in matches[:10]]})

def random(request):
    obj = SpaceObject.objects.order_by('?').first()
    return redirect(obj)
