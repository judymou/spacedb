#!/usr/bin/env python

import codecs
import csv
import logging
import os
import sys

import django

current_dir = os.path.dirname(__file__)
parent_dir = os.path.join(current_dir, '../')
sys.path.insert(0, os.path.realpath(parent_dir))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spacedb.settings')
django.setup()

from spaceobjects.models import SpaceObject, ShapeModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SHAPES = [
    {
        'name': '486958 Arrokoth (2014 MU69)',
        'shape_path': '2014_mu69.obj',
        'render_path': '2014_mu69.png',
        # https://science.sciencemag.org/content/364/6441/eaaw9771?intcmp=trendmd-sci
        'source': 'S. A. Stern et al., Science, 2019',
    },
    {
        'name': '101955 Bennu (1999 RQ36)',
        'shape_path': 'bennu.obj',
        'render_path': 'bennu.gif',
        # https://www.asteroidmission.org/updated-bennu-shape-model-3d-files/
        'source': 'NASA/Goddard/University of Arizona',
    },
    # http://observations.lam.fr/astero/
    {
        'name': '2 Pallas',
        'shape_path': 'Pallas_ADAM.obj',
        'render_path': 'pallas.png',
        # https://www.nature.com/articles/s41550-019-1007-5
        'source': 'Marsset et al., Nature Astronomy, 2020',
    },
]

def process_shapes():
    # Map from fullname to SpaceObject
    spaceobject_lookup = {}

    newobjects = []
    matched = 0
    for count, shape in enumerate(SHAPES):
        fullname = shape['name']

        logger.info('%d: %s' % (count, fullname))

        # Locate SpaceObject match
        space_object = spaceobject_lookup.get(fullname)
        if space_object:
            matched += 1
        else:
            try:
                space_object = SpaceObject.objects.get(fullname=fullname)
                matched += 1
            except SpaceObject.DoesNotExist:
                try:
                    space_object = SpaceObject.objects.get(fullname__contains=fullname)
                    matched += 1
                except SpaceObject.DoesNotExist:
                    logger.error('Cannot find space object %s' % fullname)
                    continue
            spaceobject_lookup[fullname] = space_object

        # Create ShapeModel object
        shape_path = '/data/shapefiles/manual/%s' % shape['shape_path']
        render_path = '/data/shapefiles/manual/%s' % shape['render_path']

        newobjects.append(ShapeModel(space_object=space_object,
                            shape_path=shape_path,
                            render_path=render_path,
                            source=shape['source'],
                            ))
    logger.info('%d/%d objects matched' % (matched, count))

    logger.info('Creating...')
    #ShapeModel.objects.all().delete()
    ShapeModel.objects.bulk_create(newobjects)
    logger.info('Done.')

if __name__ == '__main__':
    process_shapes()
