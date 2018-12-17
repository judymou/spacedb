# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math
from datetime import datetime

from django.db import models
from django.contrib import admin
from jsonfield import JSONField

from .description import get_orbit_class, get_orbit_desc, \
        get_diameter_comparison, get_composition

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

    class Meta:
        indexes = [
            models.Index(fields=['fullname'])
        ]

    def get_absolute_url(self):
        return '/asteroid/%s' % self.slug

    def get_orbit_class(self):
        return get_orbit_class(self)

    def get_orbit_desc(self):
        return get_orbit_desc(self)

    def get_composition(self):
        return get_composition(self)

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

    def get_moid(self):
        entry = self.sbdb_entry.get('moid')
        if not entry:
            return None
        return float(entry)

    def get_diameter_estimate_low(self):
        return self.get_diameter_estimate(method='LOW')

    def get_diameter_estimate_high(self):
        return self.get_diameter_estimate(method='HIGH')

    def get_diameter_estimate(self, method='MID'):
        '''Diameter estimate in km, using either SBDB-supplied estimate
        or estimate based on magnitude/albedo'''
        diameter_str = self.sbdb_entry.get('diameter')
        if diameter_str:
            return float(diameter_str)
        try:
            mag = float(self.sbdb_entry.get('H'))
            # Assume default albedo of .2
            albedo_str = self.sbdb_entry.get('albedo')
            if albedo_str:
                albedo = float(albedo_str)
            elif method == 'MID':
                albedo = 0.15
            elif method == 'HIGH':
                albedo = 0.05
            else:
                albedo = 0.25
            # Estimate diameter in km
            # http://www.physics.sfasu.edu/astro/asteroids/sizemagnitude.html
            return 1329 / math.sqrt(albedo) * math.pow(10, -0.2 * mag)
        except ValueError:
            pass
        return None

    def get_discovery_date(self):
        firstobs = self.sbdb_entry.get('first_obs')
        return datetime.strptime(firstobs, '%Y-%m-%d')

    def get_lastobs_date(self):
        lastobs = self.sbdb_entry.get('last_obs')
        return datetime.strptime(lastobs, '%Y-%m-%d')

    def get_size_adjective(self):
        diameter = self.get_diameter_estimate()
        if not diameter:
            return None

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

    def has_size_info_estimate(self):
        return self.get_diameter_estimate() is not None

    def get_size_rough_comparison(self):
        diameter = self.get_diameter_estimate()
        if not diameter:
            return None
        if diameter > 900:
            return 'the largest asteroid/dwarf planet'
        if diameter > 300:
            return 'one of the largest asteroids'
        if diameter > 1:
            return 'larger than most asteroids'
        return 'a small to average asteroid'

    def get_diameter_comparison(self):
        return get_diameter_comparison(self)

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

class CloseApproach(models.Model):
    space_object = models.ForeignKey(SpaceObject)

    date = models.DateField()
    v_rel = models.FloatField()
    h_mag = models.FloatField()

    # Distances in AU
    dist = models.FloatField()
    dist_min = models.FloatField()

class SentryEvent(models.Model):
    space_object = models.ForeignKey(SpaceObject)

    date = models.DateField()
    energy_mt = models.FloatField()
    dist_km = models.FloatField()
    dist_err  = models.FloatField()  # 1-sigma semi-width of the uncertainty region
    palermo_scale = models.FloatField()
    torino_scale = models.FloatField()
    prob = models.FloatField()

    def get_prob_percentage(self):
        return self.prob * 100.0

    def get_energy_with_units(self):
        if self.energy_mt > 1:
            return '%s megatons' % (self.energy_mt)
        return '%s kilotons' % (self.energy_mt * 1000)

admin.site.register(SpaceObject)
