#!/usr/bin/env python

import csv
import django
import logging
import os
import sys

from django.db import transaction

current_dir = os.path.dirname(__file__)
parent_dir = os.path.join(current_dir, '../')
sys.path.insert(0, os.path.realpath(parent_dir))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spacedb.settings')
django.setup()

from spaceobjects.models import SpaceObject 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@transaction.atomic
def processData(reader):
  SpaceObject.objects.all().delete()
  for count, row in enumerate(reader, 1):
    if count % 10000 == 0:
      logger.info(count)
      break
    space_object = SpaceObject.objects.create()
    space_object.fullname = row['full_name']
    space_object.name = row['name']
    space_object.save()

if __name__ == '__main__':
  logger.info('Processing sbdb data')
  with open('data/rawdata/sbdb.csv') as f:
    reader = csv.DictReader(f, delimiter=',')
    processData(reader)
