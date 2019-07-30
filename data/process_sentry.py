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

from spaceobjects.models import SentryEvent, SpaceObject
from data.util import get_normalized_full_name

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process(events):
    newobjects = []
    count = 0
    invalid_count = 0
    for event in events:
        count += 1
        if count % 2000 == 0:
            logger.info(count)

        if 'dist' not in event:
            continue

        fullname = get_normalized_full_name(event['fullname'])

        date_str = event['date']
        try:
            date = datetime.strptime(date_str[:date_str.find('.')], '%Y-%m-%d')
        except:
            invalid_count += 1
            continue

        try:
            space_object = SpaceObject.objects.get(fullname=fullname)
            se = SentryEvent(
                    space_object=space_object,
                    date=date,
                    energy_mt=float(event['energy']),
                    dist_km=float(event['dist']) * 6420,
                    dist_err=float(event['width']) * 6420,
                    prob=float(event['ip']),
                    torino_scale=float(event['ts']) if event['ts'] else -1,
                    palermo_scale=float(event['ps']),
                    )
            newobjects.append(se)
        except SpaceObject.DoesNotExist:
            logger.error('Cannot find space object %s' % fullname)

    logger.warn('%d invalid dates' % invalid_count)
    logger.info('Inserting records...')
    SentryEvent.objects.all().delete()
    SentryEvent.objects.bulk_create(newobjects, batch_size=499)
    logger.info('%d records inserted' % len(newobjects))

if __name__ == '__main__':
    logger.info('Processing sentry data')

    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.realpath(os.path.join(dir_path, 'rawdata/sentry.json'))
    with open(data_path) as f:
        result = json.load(f)
        process(result['data'])
