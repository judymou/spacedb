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

def process_references(f_in):
    reader = csv.DictReader(codecs.EncodedFile(f_in, 'utf8', 'utf-8-sig'), delimiter=',')
    ret = {}
    for row in reader:
        cite = '%s. %s. %s. %s:%s' % (row['Author'], row['Year'], row['Title'], row['Publication'], row['Page'])
        ret[row['Reference ID']] = {
            'cite': cite,
            'url': row['URI'],
        }
    return ret

def process_shapes(f_in, refs):
    reader = csv.DictReader(codecs.EncodedFile(f_in, 'utf8', 'utf-8-sig'), delimiter=',')

    # Map from fullname to SpaceObject
    spaceobject_lookup = {}

    matched = 0
    count = 0
    newobjects = []
    for row in reader:
        count += 1

        reconstructed_desig = '%s %s' % (row['asteroid number'], row['asteroid name'])
        desig_with_parens = '(%s)' % row['asteroid designation']
        fullname = reconstructed_desig if row['asteroid name'] else desig_with_parens

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
        ast_id = row['asteroid id']
        model_id = row['model id']
        filename = 'A%s.M%s' % (ast_id, model_id)
        shape_path = '/data/shapefiles/damit/%s.shape.txt' % filename
        render_path = '/data/shapefiles/damit/%s.shape.png' % filename
        yorp = float(row['yorp']) if row['yorp'] else None
        quality = float(row['quality flag']) if row['quality flag'] else -1
        diam = float(row['equivalent diameter']) if row['equivalent diameter'] else None
        #reference = refs[row['reference id']]
        newobjects.append(ShapeModel(space_object=space_object,
                            shape_path=shape_path,
                            render_path=render_path,
                            spin_latitude=float(row['beta']),
                            spin_longitude=float(row['beta']),
                            spin_angle=float(row['phi0']),
                            period_hr=float(row['period']),
                            jd=float(row['jd0']),
                            yorp=yorp,
                            equiv_diameter_km=diam,
                            quality=quality,
                            #reference=reference,
                            ))
    logger.info('%d/%d objects matched' % (matched, count))

    logger.info('Creating...')
    ShapeModel.objects.bulk_create(newobjects)
    logger.info('Done.')

if __name__ == '__main__':
    with open('rawdata/shapes/damit_flush_extended.csv', 'r') as f_main, \
         open('rawdata/shapes/damit_flush_refs.csv', 'r') as f_refs:
        #refs = process_references(f_refs)
        refs = {}
        process_shapes(f_main, refs)
