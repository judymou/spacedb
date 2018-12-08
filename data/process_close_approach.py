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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@transaction.atomic
def processData(fields, data):
  for count, row in enumerate(data, 1):
    if count % 100 == 0:
      logger.info(count)
      break
    ca_raw = dict(zip(fields, row))
  
    try:
      space_object = SpaceObject.objects.get(fullname=ca_raw['fullname'])
      ca = CloseApproach.objects.create(space_object=space_object,
          dist_min = float(ca_raw['dist_min']))
      ca.save()
      logger.info(ca_raw['fullname'] + 'saved')
    except SpaceObject.DoesNotExist:
      logger.error('Cannot find space object' + ca_raw['fullname'])


if __name__ == '__main__':
  logger.info('Processing close approach data')
  with open('data/rawdata/close_approach.json') as f:
    close_approach_file = json.load(f)
    processData(close_approach_file["fields"],
        close_approach_file["data"])
