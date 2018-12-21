#!/usr/bin/env python

# TODO(ian): Process detail for each object, including orbital plot
# TODO(ian): Orbit condition codes (occ) https://minorplanetcenter.net/iau/info/UValue.html

import csv
import django
import json
import logging
import os
import sys
from datetime import datetime

from django.db import transaction

current_dir = os.path.dirname(__file__)
parent_dir = os.path.join(current_dir, '../')
sys.path.insert(0, os.path.realpath(parent_dir))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spacedb.settings')
django.setup()

from spaceobjects.models import NhatsObject, SpaceObject
from data.util import get_normalized_full_name

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process(entries):
    newobjects = []
    count = 0
    for entry in entries:
        count += 1
        if count % 500 == 0:
            logger.info(count)

        fullname = get_normalized_full_name(entry['fullname'])

        try:
            space_object = SpaceObject.objects.get(fullname=fullname)
            newobj = NhatsObject(
                    space_object=space_object,
                    min_dv=entry['min_dv']['dv'],
                    min_dv_duration=entry['min_dv']['dur'],
                    min_diameter=entry['min_size'],
                    max_diameter=entry['max_size'],
                    num_trajectories=entry['n_via_traj'],
                    )
            newobjects.append(newobj)
        except SpaceObject.DoesNotExist:
            logger.error('Cannot find space object %s' % fullname)

    logger.info('Inserting records...')
    NhatsObject.objects.all().delete()
    NhatsObject.objects.bulk_create(newobjects, batch_size=499)
    logger.info('%d records inserted' % len(newobjects))

if __name__ == '__main__':
    logger.info('Processing sentry data')

    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.realpath(os.path.join(dir_path, 'rawdata/nhats.json'))
    with open(data_path) as f:
        result = json.load(f)
        process(result['data'])
