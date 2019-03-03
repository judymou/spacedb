# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from datetime import date
from random import randint

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
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

    named_after = []
    named_after_slugs = ['2001-einstein-1973-eb', '7672-hawking-1995-uo2',
      '2709-sagan-1982-fh', '6469-armstrong-1982-pc', '6471-collins-1983-eb1']
    for named_after_slug in named_after_slugs:
      named_after.append(SpaceObject.objects.get(slug=named_after_slug))
    
    return render(request, 'spaceobjects/index.html',
          {
              'object_count': SpaceObject.objects.count(),
              'space_objects': space_objects,
              'object_sets': [
                {'name': 'Largest',
                 'data': SpaceObject.objects.all().order_by('-diameter')[:5],
                 'description': 'These are among the largest and earliest discovered asteroids in our solar system.'
                },
                {'name': 'Smallest',
                 'data': SpaceObject.objects.all().order_by('diameter')[:5],
                 'description': 'These are among the smallest asteroids in our solar system.'
                },
                {'name': 'In Honor Of...',
                 'data': named_after, 
                 'description': 'These objects are named after notable people.'
                },
              ],
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
        return HttpResponseNotFound('Could not find object "%s"' % slug)

    close_approaches = space_object.closeapproach_set.all().order_by('date')
    sentry_events = space_object.sentryevent_set.all().order_by('-prob')
    shape_models = space_object.shapemodel_set.all().order_by('-quality')

    return render(request, 'spaceobjects/detail.html', {
                'object': space_object,
                'close_approaches': close_approaches,
                'sentry_events': sentry_events,
                'shape_models': shape_models,
            })

def detail_shape(request, slug):
    try:
        space_object = SpaceObject.objects.get(slug=slug)
    except SpaceObject.DoesNotExist:
        return HttpResponseNotFound('Could not find object "%s"' % slug)

    shape_models = space_object.shapemodel_set.all().order_by('-quality')

    return render(request, 'spaceobjects/shape_model.html', {
                'object': space_object,
                'shape_models': shape_models,
            })

def get_category_info(category):
    '''Given a category string, return objects belonging to that category and
    other information.
    '''
    orbit_class = None
    page_name = None
    if category == 'asteroids':
        # All asteroids
        objects = SpaceObject.objects.filter(object_type=ObjectType.ASTEROID)
        page_name = 'Asteroids'
    elif category == 'comets':
        # All comets
        objects = SpaceObject.objects.filter(object_type=ObjectType.COMET)
        page_name = 'Comets'
    elif category == 'asteroid-shapes':
        objects = SpaceObject.objects.annotate(num_shapes=Count('shapemodel')).filter(num_shapes__gt=0)
        page_name = 'Asteroids with Known Shapes'
    elif category == 'near-earth-asteroids':
        objects = SpaceObject.objects.filter(is_nea=True)
        page_name = 'Near-Earth Asteroids'
    elif category == 'potentially-hazardous-asteroids':
        page_name = 'Potentially Hazardous Asteroids'
        objects = SpaceObject.objects.filter(is_pha=True)
    elif category.startswith('asteroid-type-'):
        page_name = 'Type ? Asteroids'
    else:
        # The default case: a category that maps directly to an orbit class.
        try:
            orbit_class = OrbitClass.objects.get(slug=category)
        except ObjectDoesNotExist:
            return HttpResponseNotFound('Unknown category "%s"' % category)

        objects = SpaceObject.objects.filter(orbit_class=orbit_class)
        page_name = '%ss' % orbit_class.name

    return {
        'objects': objects,
        'page_name': page_name,
        'orbit_class': orbit_class,
    }

def category(request, category):
    info = get_category_info(category)
    objects = info['objects']

    count = objects.count()
    total_count = SpaceObject.objects.all().count()
    population_pct = count / float(total_count) * 100.0
    return render(request, 'spaceobjects/category.html', {
                'category': category,
                'page_name': info['page_name'],
                'orbit_class': info['orbit_class'],
                'count': count,
                'total_count': total_count,
                'population_pct': population_pct,
                'objects': objects[:20],
            })

def api_category_objects(request, category):
    info = get_category_info(category)
    objects = info['objects']

    limit = request.GET.get('limit', 10)

    return JsonResponse({
        'success': True,
        'data': [obj.to_orbit_obj() for obj in objects[:limit]],
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
