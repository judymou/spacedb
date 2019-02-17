# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from datetime import date
from random import randint

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from spaceobjects.models import SpaceObject, SentryEvent, CloseApproach, NhatsObject, OrbitClass, ObjectType

def index(request):
    # TODO(ian): order by pdes
    space_objects = SpaceObject.objects.all()[:5]

    potential_impactors = []
    seen_impactors = set()
    for event in SentryEvent.objects.order_by('-prob')[:25]:
        if event.space_object.fullname in seen_impactors:
            continue
        potential_impactors.append(event)
        seen_impactors.add(event.space_object.fullname)
        if len(potential_impactors) >= 5:
            break

    close_approaches = []
    seen_approaches = set()
    for event in CloseApproach.objects.filter(date__gte=date.today()) \
                                      .order_by('date')[:25]:
        if event.space_object.fullname in seen_approaches:
            continue
        close_approaches.append(event)
        seen_approaches.add(event.space_object.fullname)
        if len(close_approaches) >= 5:
            break

    return render(request, 'spaceobjects/index.html',
          {
              'object_count': SpaceObject.objects.count(),
              'space_objects': space_objects,
              'potential_impactors': potential_impactors,
              'close_approaches': close_approaches,
              'nhats_objects': NhatsObject.objects.all().order_by('min_dv')[:5],
              'orbit_classes': OrbitClass.objects.all(),
              'hide_top_nav': True,
          })

def detail(request, slug):
    try:
        space_object = SpaceObject.objects.get(slug=slug)
    except SpaceObject.DoesNotExist:
        return index(request)

    sentry_events = space_object.sentryevent_set.all().order_by('-prob')
    shape_models = space_object.shapemodel_set.all().order_by('-quality')

    return render(request, 'spaceobjects/detail.html', {
                'object': space_object,
                'sentry_events': sentry_events,
                'shape_models': shape_models,
            })

def detail_shape(request, slug):
    try:
        space_object = SpaceObject.objects.get(slug=slug)
    except SpaceObject.DoesNotExist:
        return index(request)

    shape_models = space_object.shapemodel_set.all().order_by('-quality')

    return render(request, 'spaceobjects/shape_model.html', {
                'object': space_object,
                'shape_models': shape_models,
            })

def category(request, category):
    orbit_class = None
    if category == 'asteroids':
        # All asteroids
        objects = SpaceObject.objects.filter(object_type=ObjectType.ASTEROID)
    elif category == 'comets':
        # All comets
        objects = SpaceObject.objects.filter(object_type=ObjectType.COMET)
    elif category == 'asteroid-shapes':
        objects = SpaceObject.objects.annotate(num_shapes=Count('shapemodel')).filter(num_shapes__gt=0)
    elif category == 'near-earth-asteroids':
        objects = SpaceObject.objects.filter(is_neo=True)
    elif category == 'potentially-hazardous-asteroids':
        objects = SpaceObject.objects.filter(is_pha=True)
    elif category.startswith('asteroid-type-'):
        pass
    else:
        try:
            orbit_class = OrbitClass.objects.get(slug=category)
        except ObjectDoesNotExist:
            return HttpResponse('unknown category')

        objects = SpaceObject.objects.filter(orbit_class=orbit_class)

    count = objects.count()
    total_count = SpaceObject.objects.all().count()
    population_pct = count / float(total_count) * 100.0
    return render(request, 'spaceobjects/category.html', {
                'orbit_class': orbit_class,
                'count': count,
                'total_count': total_count,
                'population_pct': population_pct,
                'objects': objects[:20],
            })

def solar_system(request):
    return render(request, 'spaceobjects/solar_system.html', {})

def search(request):
    search_str = request.GET.get('q')
    matches = SpaceObject.objects.filter(fullname__icontains=search_str)
    return JsonResponse({'results': [roid.to_search_result() for roid in matches[:10]]})

def get_objects(request):
    search_term = request.GET.get('q').split(',');

    results = [];
    for search_str in search_term:
      space_object = SpaceObject.objects.get(slug=search_str);
      results.append(space_object.to_search_result());
    return JsonResponse({'results': results})

def random(request):
    count = SpaceObject.objects.all().count()
    random_index = randint(0, count - 1)
    obj = SpaceObject.objects.all()[random_index]
    return redirect(obj)
