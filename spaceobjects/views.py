# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from datetime import date
from random import randint

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Max
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from spaceobjects.models import SpaceObject, SentryEvent, CloseApproach, NhatsObject, OrbitClass, ObjectType

HOMEPAGE_NUM_ITEMS_PER_LIST = 5

def index(request):
    potential_impactors = []
    seen_impactors = set()
    for event in SentryEvent.objects.order_by('-prob')[:HOMEPAGE_NUM_ITEMS_PER_LIST*5]:
        if event.space_object.fullname in seen_impactors:
            continue
        potential_impactors.append(event.space_object)
        seen_impactors.add(event.space_object.fullname)
        if len(potential_impactors) >= HOMEPAGE_NUM_ITEMS_PER_LIST:
            break

    close_approaches = []
    seen_approaches = set()
    for event in CloseApproach.objects.filter(date__gte=date.today()) \
                                      .order_by('date')[:HOMEPAGE_NUM_ITEMS_PER_LIST*5]:
        if event.space_object.fullname in seen_approaches:
            continue
        close_approaches.append(event.space_object)
        seen_approaches.add(event.space_object.fullname)
        if len(close_approaches) >= HOMEPAGE_NUM_ITEMS_PER_LIST:
            break

    named_after = []
    named_after_slugs = ['2001-einstein-1973-eb', '7672-hawking-1995-uo2',
      '2709-sagan-1982-fh', '6469-armstrong-1982-pc', '6471-collins-1983-eb1']
    for named_after_slug in named_after_slugs:
        named_after.append(SpaceObject.objects.get(slug=named_after_slug))

    return render(request, 'spaceobjects/index.html',
          {
              'object_count': SpaceObject.objects.count(),
              'orbit_classes': OrbitClass.objects.all(),
              'hide_top_nav': True,
              'object_sets': [
                {
                    'name': 'Largest',
                    'data': SpaceObject.objects.all().order_by('-diameter').exclude(diameter__isnull=True)[:HOMEPAGE_NUM_ITEMS_PER_LIST],
                    'description': 'These are among the largest and earliest discovered asteroids in our solar system.',
                },
                {
                    'name': 'Upcoming Approaches',
                    'data': close_approaches,
                    'description': 'These objects have upcoming fly-bys of Earth.',

                    # Always show close approaches if possible.
                    'hide_impact_probability': True,
                },
                {
                    'name': 'Potential Impactors',
                    'data': potential_impactors,
                    'description': 'These objects have the potential to impact Earth (listed by probability of impact).',
                },
                {
                    'name': 'Potential for Exploration',
                    'data': [x.space_object for x in NhatsObject.objects.all().order_by('min_dv')[:HOMEPAGE_NUM_ITEMS_PER_LIST]],
                    'description': 'It is relatively inexpensive to send a spacecraft to these objects in terms of propulsive cost (listed by delta-v).',
                },
                {
                    'name': 'In Honor Of...',
                    'data': named_after,
                    'description': 'These objects are named after notable people.',
                },
              ],
          })

def detail_asteroid(request, slug):
    try:
        space_object = SpaceObject.objects.get(slug=slug)
    except SpaceObject.DoesNotExist:
        return HttpResponseNotFound('Could not find object "%s"' % slug)

    if space_object.is_comet:
        return redirect('/comet/%s' % slug)
    return detail(request, slug)

def detail_comet(request, slug):
    try:
        space_object = SpaceObject.objects.get(slug=slug)
    except SpaceObject.DoesNotExist:
        return HttpResponseNotFound('Could not find object "%s"' % slug)

    if not space_object.is_comet:
        return redirect('/asteroid/%s' % slug)
    return detail(request, slug)

def detail(request, slug):
    try:
        space_object = SpaceObject.objects.get(slug=slug)
    except SpaceObject.DoesNotExist:
        return HttpResponseNotFound('Could not find object "%s"' % slug)

    return render(request, 'spaceobjects/detail.html', {
                'object': space_object,
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
    elif category == 'kuiper-belt':
        objects = SpaceObject.objects.filter(a__gt=35)
        page_name = 'Kuiper Belt Objects'
    elif category == 'near-earth-asteroids':
        objects = SpaceObject.objects.filter(is_nea=True)
        page_name = 'Near-Earth Asteroids'
    elif category == 'potentially-hazardous-asteroids':
        page_name = 'Potentially Hazardous Asteroids'
        objects = SpaceObject.objects.filter(is_pha=True)
    elif category == 'dwarf-planets':
        page_name = 'Dwarf Planets'
        # FIXME(ian): Need to do this with estimated size.
        objects = SpaceObject.objects.filter(diameter__gt=600)
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
                'category_slug': category,
                'page_name': info['page_name'],
                'orbit_class': info['orbit_class'],
                'count': count,
                'total_count': total_count,
                'population_pct': population_pct,
                'objects': objects[:20],
            })

def api_category_orbits(request, category):
    info = get_category_info(category)
    objects = info['objects']

    limit = request.GET.get('limit', 10)

    return JsonResponse({
        'success': True,
        'data': [obj.to_orbit_obj() for obj in objects[:limit]],
    })

def api_category_objects(request, category):
    info = get_category_info(category)
    objects = info['objects']

    limit = request.GET.get('limit', 10)

    return JsonResponse({
        'success': True,
        'data': [obj.to_search_result() for obj in objects[:limit]],
    })

def solar_system(request):
    return render(request, 'spaceobjects/solar_system.html', {})

def api_objects_search(request):
    search_str = request.GET.get('q')
    matches = SpaceObject.objects.filter(fullname__icontains=search_str)
    return JsonResponse({'results': [roid.to_search_result() for roid in matches[:10]]})

def api_objects(request):
    search_term = request.GET.get('slugs').split(',');

    results = [];
    for search_str in search_term:
      space_object = SpaceObject.objects.get(slug=search_str);
      results.append(space_object.to_search_result());
    return JsonResponse({'results': results})

def random(request):
    max_id = SpaceObject.objects.all().aggregate(max_id=Max('id'))['max_id']
    count = 0
    while True:
        pk = randint(1, max_id)
        try:
            obj = SpaceObject.objects.get(pk=pk)
        except SpaceObject.DoesNotExist:
            count += 1
            if count > 500:
                redirect('/asteroid/1-ceres')
                return
            continue
        break

    return redirect(obj)
