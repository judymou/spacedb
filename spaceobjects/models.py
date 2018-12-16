# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.contrib import admin
from jsonfield import JSONField

from .description import get_orbit_class, get_orbit_desc

class SpaceObject(models.Model):
  fullname = models.CharField(max_length=200)
  name = models.CharField(max_length=200)
  slug = models.CharField(max_length=200)

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

  def get_absolute_url(self):
      return '/asteroid/%s' % self.slug

  def get_orbit_class(self):
      return get_orbit_class(self)

  def get_orbit_desc(self):
      return get_orbit_desc(self)

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

  def get_discovery_date(self):
      firstobs = self.sbdb_entry.get('first_obs')
      return datetime.strptime(firstobs, '%Y-%m-%d')

  def get_size_adjective(self):
      diameter_str = self.sbdb_entry.get('diameter')
      if not diameter_str:
          return None

      diameter = float(diameter_str)
      if diameter < 1:
          return 'very small'
      if diameter < 10:
          return 'small'
      if diameter < 100:
          return 'relatively small'
      if diameter < 200:
          return 'average-sized'
      if diameter < 300:
          return 'large'
      if diameter < 600:
          return 'very large'
      return 'dwarf planet'

  def has_size_info(self):
      diam = self.sbdb_entry.get('diameter')
      return diam != '' and diam is not None

  def get_size_rough_comparison(self):
      diameter_str = self.sbdb_entry.get('diameter')
      if not diameter_str:
          return None

      diameter = float(diameter_str)
      if diameter > 900:
          return 'the largest asteroid/dwarf planet'
      if diameter > 300:
          return 'one of the largest asteroids'
      if diameter > 1:
          return 'larger than most asteroids'
      return 'a small to average asteroid'

  def get_diameter_comparison(self):
      diameter_str = self.sbdb_entry.get('diameter')
      if not diameter_str:
          return None

      diameter = float(diameter_str) ** 2

      # http://www.decisionsciencenews.com/2015/02/20/put-size-countries-perspective-comparing-us-states/
      # https://en.wikipedia.org/wiki/List_of_United_States_cities_by_area
      if diameter < 370:
          return 'the city of Philadelphia'
      if diameter < 400:
          return 'the city of Denver'
      if diameter < 953:
          return 'the city of Indianapolis'
      if diameter < 999:
          return 'the city of Dallas'
      if diameter < 1213:
          return 'the city of New York'
      if diameter < 1302:
          return 'the city of Los Angeles'
      if diameter < 1625:
          return 'the city of Houston'
      if diameter < 5000:
          return 'the U.S. state of Rhode Island'
      if diameter < 14000:
          return 'the U.S. state of Delaware'
      if diameter < 22000:
          return 'the U.S. state of Connecticut'
      if diameter < 24000:
          return 'the U.S. state of New Jersey'
      if diameter < 27000:
          return 'the U.S. state of Vermont'
      if diameter < 32000:
          return 'the U.S. state of Massachusetts'
      if diameter < 62000:
          return 'the U.S. state of Maryland'
      if diameter < 82000:
          return 'the U.S. state of West Virginia'
      if diameter < 91000:
          return 'the U.S. state of South Carolina'
      if diameter < 94000:
          return 'Portugal'
      if diameter < 104000:
          return 'South Korea'
      if diameter < 109000:
          return 'Iceland'
      if diameter < 119000:
          return 'the U.S. state of Virginia'
      if diameter < 125000:
          return 'the U.S. state of Pennsylvania'
      if diameter < 134000:
          return 'the U.S. state of Mississippi'
      if diameter < 170000:
          return 'the U.S. state of Iowa'
      if diameter < 200000:
          return 'the U.S. state of South Dakota'
      if diameter < 300000:
          return 'the U.K.'
      if diameter < 400000:
          return 'Japan'
      if diameter < 500000:
          return 'France'
      if diameter < 700000:
          return 'the U.S. state of Texas'
      return 'the U.S. state of Alaska'

  def get_similar_orbits(self, n=3):
      a_range = [self.a - 0.01, self.a + 0.01]
      similar = SpaceObject.objects.filter(a__range=a_range).exclude(pk=self.pk)
      return similar[:n]

  def to_search_result(self):
      return {
        'fullname': self.fullname,
        'name': self.name,
        'slug': self.slug,
      }

admin.site.register(SpaceObject)
