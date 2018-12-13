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
    space_object = SpaceObject.objects.create(
        fullname = row['full_name'],
        name = row['name'],
        a = float(row['a']),
        e = float(row['e']),
        i = float(row['i']),
        om = float(row['om']),
        w = float(row['w']),
        ma = float(row['ma']),
        epoch = float(row['epoch']),
        sbdb_entry = row,
        )
    space_object.save()

if __name__ == '__main__':
  logger.info('Processing sbdb data')

  dir_path = os.path.dirname(os.path.realpath(__file__))
  data_path = os.path.realpath(os.path.join(dir_path, 'rawdata/sbdb.csv'))
  with open(data_path) as f:
    reader = csv.DictReader(f, delimiter=',')
    processData(reader)
