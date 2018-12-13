# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
from jsonfield import JSONField

# https://pdssbn.astro.umd.edu/data_other/objclass.shtml
ORBIT_CLASS_MAPPING = {
    'COM': 'Comet',
    'CTc': 'Chiron-type Comet',
    'ETc': 'Encke-type Comet',
    'HTC': 'Halley-type Comet',
    'HYP': 'Hyperbolic Comet',
    'JFc': 'Jupiter-family Comet',
    'JFC': 'Jupiter-family Comet',
    'PAR': 'Parabolic Comet',

    'AMO': 'Amor-class Asteroid',
    'APO': 'Apollo-class Asteroid',
    'AST': 'Asteroid',
    'ATE': 'Aten-class Asteroid',
    'CEN': 'Centaur-class Asteroid',
    'HYA': 'Hyperbolic Asteroid',
    'IEO': 'Interior-Earth Asteroid',
    'IMB': 'Inner Main-belt Asteroid',
    'MBA': 'Main-belt Asteroid',
    'MCA': 'Mars-crossing Asteroid',
    'OMB': 'Outer Main-belt Asteroid',
    'PAA': 'Parabolic Asteroid',
    'TJN': 'Jupiter Trojan',
    'TNO': 'Trans-Neptunian Object',
}

class SpaceObject(models.Model):
  fullname = models.CharField(max_length=500)
  name = models.CharField(max_length=500)

  # Basic orbital elements
  a = models.FloatField()
  e = models.FloatField()
  i = models.FloatField()
  om = models.FloatField()
  w = models.FloatField()
  ma = models.FloatField()
  epoch = models.FloatField()

  # sbdb blob
  sbdb_entry = JSONField()

  def get_orbit_class(self):
      return ORBIT_CLASS_MAPPING.get(self.sbdb_entry['class'])

  def is_neo(self):
      entry = self.sbdb_entry.get('neo', False)
      if entry == 'N':
          return False
      return entry

  def is_pha(self):
      entry = self.sbdb_entry.get('pha', False)
      if entry == 'N':
          return False
      return entry

  def get_diameter_comparison(self):
      diameter_str = self.sbdb_entry.get('diameter', None)
      if not diameter_str:
          return None

      # Convert diameter to miles... sorry but that's the unit of my other data.
      diameter = float(diameter_str) * 0.621371

      # http://www.decisionsciencenews.com/2015/02/20/put-size-countries-perspective-comparing-us-states/
      # https://en.wikipedia.org/wiki/List_of_United_States_cities_by_area
      if diameter < 134:
          return 'Philadelphia'
      if diameter < 153:
          return 'Denver'
      if diameter < 302:
          return 'New York'
      if diameter < 340:
          return 'Dallas'
      if diameter < 361:
          return 'Indianapolis'
      if diameter < 600:
          return 'Houston'
      if diameter < 5000:
          return 'Rhode Island'
      if diameter < 14000:
          return 'Delaware'
      if diameter < 22000:
          return 'Connecticut'
      if diameter < 24000:
          return 'New Jersey'
      if diameter < 27000:
          return 'Vermont'
      if diameter < 32000:
          return 'Massachusetts'
      if diameter < 62000:
          return 'Maryland'
      if diameter < 82000:
          return 'West Virginia'
      if diameter < 91000:
          return 'South Carolina'
      if diameter < 94000:
          return 'Maine'
      if diameter < 104000:
          return 'Indiana'
      return 'big!!'


class CloseApproach(models.Model):
  space_object = models.ForeignKey(SpaceObject)
  dist_min = models.FloatField()

admin.site.register(SpaceObject)
