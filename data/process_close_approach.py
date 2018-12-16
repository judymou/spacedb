#!/usr/bin/env python

import csv
import django
import json
import logging
import os
import sys

from django.db import transaction

current_dir = os.path.dirname(__file__)
parent_dir = os.path.join(current_dir, '../')
sys.path.insert(0, os.path.realpath(parent_dir))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spacedb.settings')
django.setup()

from spaceobjects.models import SpaceObject, CloseApproach
from data.util import get_normalized_full_name

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def processData(fields, data):
    CloseApproach.objects.all().delete()
    newobjects = []
    for count, row in enumerate(data, 1):
        if count % 100 == 0:
            logger.info(count)
        ca_raw = dict(zip(fields, row))
        fullname = get_normalized_full_name(ca_raw['fullname'])

        try:
            space_object = SpaceObject.objects.get(fullname=fullname)
            ca = CloseApproach(
                    space_object=space_object,
                    dist = float(ca_raw['dist']),
                    dist_min = float(ca_raw['dist_min']),
                    v_rel = float(ca_raw['v_rel']),
                    time_jd = float(ca_raw['jd']),
                    h_mag = float(ca_raw['h']),
                    )
            newobjects.append(ca)
        except SpaceObject.DoesNotExist:
            logger.error('Cannot find space object' + fullname)

    CloseApproach.objects.bulk_create(newobjects)


if __name__ == '__main__':
    logger.info('Processing close approach data')

    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.realpath(os.path.join(dir_path, 'rawdata/close_approach.json'))
    with open(data_path) as f:
        close_approach_file = json.load(f)
        processData(close_approach_file["fields"],
                close_approach_file["data"])
