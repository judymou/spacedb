#!/usr/bin/env python

import gzip
import json
import logging
import os
import time

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

URL_BASE = 'https://ssd-api.jpl.nasa.gov/mdesign.api?des='

def read_existing():
    seen_pdes = set()
    bad_count = 0
    with gzip.open('rawdata/mission_design15.json.gz', 'r') as f:
        for line in f.readlines():
            try:
                obj = json.loads(line)
            except ValueError:
                bad_count += 1
                continue
            seen_pdes.add(obj['pdes'])
    print '%d bad lines' % (bad_count)
    return seen_pdes

def process(reader, seen_pdes):
    with gzip.open('rawdata/mission_design16.json.gz', 'wb') as f:
        for count, row in enumerate(reader, 1):
            if count % 1000 == 0:
                logger.info(count)
                f.flush()

            pdes = row['pdes']
            if pdes in seen_pdes:
                continue

            obj = requests.get(URL_BASE + pdes).json()
            time.sleep(0.2)

            if 'object' not in obj:
                continue

            line = {
                'pdes': pdes,
                'fullname': obj['object']['fullname'],
            }

            found_something = False
            if 'dv_lowthrust' in obj:
                line['dv_lowthrust'] = obj['dv_lowthrust']
                found_something = True
            if 'selectedMissions' in obj and 'fields' in obj:
                line['fields'] = obj['fields']
                line['selectedMissions'] = obj['selectedMissions']
                found_something = True

            if found_something:
                logger.info('Writing row for %s', line['fullname'])
                f.write('%s\n' % json.dumps(line))

def generate_rows(fields, data):
    for row in data:
        yield dict(zip(fields, row))

if __name__ == '__main__':
    logger.info('Reading sbdb data for mission design...')

    seen_pdes = read_existing()

    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.realpath(os.path.join(dir_path, 'rawdata/sbdb.json.gz'))
    with gzip.open(data_path) as f:
        obj = json.load(f)
        fields = obj['fields']
        data = obj['data']
        rows = generate_rows(fields, data)
        process(rows, seen_pdes)
