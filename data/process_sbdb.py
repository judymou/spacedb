#!/usr/bin/env python

import csv
import gzip
import json
import logging
import os
import sys

import django
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils.text import slugify

current_dir = os.path.dirname(__file__)
parent_dir = os.path.join(current_dir, '../')
sys.path.insert(0, os.path.realpath(parent_dir))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spacedb.settings_pipeline')
django.setup()

from spaceobjects.models import SpaceObject, OrbitClass, ObjectType
from data.util import get_normalized_full_name, queryset_iterator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@transaction.atomic
def insert_all(newobjects, delete=False):
    if delete:
        SpaceObject.objects.all().only('pk').delete()
    SpaceObject.objects.bulk_create(newobjects, batch_size=499)

def process(reader):
    newobjects = []
    inserted_once = False
    failures_ma = 0
    for count, row in enumerate(reader, 1):
        if count % 10000 == 0:
            logger.info(count)

        if count % 30000 == 0:
            # Subdivide insertions - slower, but needed for low memory
            # environments like production machine
            logger.info('Inserting...')
            insert_all(newobjects, delete=(not inserted_once))
            inserted_once = True
            newobjects = []

        if not row['ma']:
            logger.warn('Missing mean anom: Failed to parse row %d (%s): %s' % \
                            (count, row.get('full_name', '?'), json.dumps(row)))
            failures_ma += 1
            continue
        fullname = get_normalized_full_name(row['full_name'])

        try:
            orbit_class = OrbitClass.objects.get(abbrev__iexact=row['class'])
        except ObjectDoesNotExist:
            orbit_class = None

        object_type = ObjectType.from_class(row['class'])
        if row['name'] and object_type != ObjectType.COMET:
            shortname = row['name'].strip()
        else:
            shortname = fullname

        magnitude = float(row['H']) if row['H'] else None
        if not magnitude:
            # Comet total magnitude
            magnitude = float(row['M1']) if row['M1'] else None

        space_object = SpaceObject(
            fullname = fullname,
            name = shortname,
            slug = slugify(fullname.replace('/',' ')),
            a = float(row['a']),
            e = float(row['e']),
            i = float(row['i']),
            om = float(row['om']),
            w = float(row['w']),
            ma = float(row['ma']),
            epoch = float(row['epoch']),
            is_nea = True if row['neo'] == 'Y' else False,
            is_pha = True if row['pha'] == 'Y' else False,
            orbit_class = orbit_class,
            object_type = object_type,
            diameter = float(row['diameter'].decode('utf-8')) if row['diameter'] else None,
            spec_B = row['spec_B'],
            spec_T = row['spec_T'],
            H = magnitude,
            sbdb_entry = row,
            )

        newobjects.append(space_object)

    logger.info('Inserting final records...')
    insert_all(newobjects, delete=(not inserted_once))

    logger.warning('%d blank mean anomalies' % failures_ma)

    logger.info('Done.')

if __name__ == '__main__':
    logger.info('Processing sbdb data')

    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.realpath(os.path.join(dir_path, 'rawdata/sbdb.csv.gz'))
    with gzip.open(data_path) as f:
        reader = csv.DictReader(f, delimiter=',')
        process(reader)
