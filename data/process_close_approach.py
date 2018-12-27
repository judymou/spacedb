#!/usr/bin/env python

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

from spaceobjects.models import SpaceObject, CloseApproach
from data.util import get_normalized_full_name

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process(fields, data):
    CloseApproach.objects.all().delete()
    newobjects = []
    for count, row in enumerate(data, 1):
        if count % 100 == 0:
            logger.info(count)
        ca_raw = dict(zip(fields, row))
        fullname = get_normalized_full_name(ca_raw['fullname'])

        date_str = ca_raw['cd']
        date = datetime.strptime(date_str, '%Y-%b-%d %H:%M')

        try:
            space_object = SpaceObject.objects.get(fullname=fullname)
            ca = CloseApproach(
                    space_object=space_object,
                    date=date,
                    dist_au=float(ca_raw['dist']),
                    dist_min_au=float(ca_raw['dist_min']),
                    v_rel=float(ca_raw['v_rel']),
                    # TODO(ian): Make hmag nullable
                    h_mag=float(ca_raw['h'] if ca_raw['h'] else -99),
                    )
            newobjects.append(ca)
        except SpaceObject.DoesNotExist:
            logger.error('Cannot find space object %s' % fullname)

    CloseApproach.objects.bulk_create(newobjects)


if __name__ == '__main__':
    logger.info('Processing close approach data')

    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.realpath(os.path.join(dir_path, 'rawdata/close_approach.json'))
    with open(data_path) as f:
        close_approach_file = json.load(f)
        process(close_approach_file["fields"],
                close_approach_file["data"])
