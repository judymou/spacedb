# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math
from datetime import datetime
from enum import Enum

from django.db import models
from django.contrib import admin
from django.urls import reverse
from jsonfield import JSONField

from spaceobjects.description import get_diameter_comparison, get_composition, COMET_CLASSES

class ObjectType(Enum):
    ASTEROID = 'ASTEROID'
    COMET = 'COMET'

    @classmethod
    def from_class(self, classname):
        if classname in COMET_CLASSES:
            return self.COMET
        return self.ASTEROID

class OrbitClass(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)
    abbrev = models.CharField(max_length=10)

    desc = models.CharField(max_length=500)
    orbit_sentence = models.CharField(max_length=500)

    def __str__(self):
        return self.abbrev

    class Meta:
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['abbrev']),
        ]

class SpaceObject(models.Model):
    # The index at which the object appears in the Small Body Database
    sbdb_order_id = models.IntegerField()

    fullname = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)

    orbit_class = models.ForeignKey(OrbitClass)
    object_type = models.CharField(max_length = 20,
            choices=[(tag, tag.value) for tag in ObjectType])

    # Basic orbital elements
    a = models.FloatField()
    e = models.FloatField()
    i = models.FloatField()
    om = models.FloatField()
    w = models.FloatField()
    ma = models.FloatField()
    epoch = models.FloatField()

    is_nea = models.BooleanField()
    is_pha = models.BooleanField()
    spec_B = models.CharField(max_length=200)
    spec_T = models.CharField(max_length=200)
    H = models.FloatField()

    # For now this is only SBDB diameter. See get_diameter_estimate below.
    diameter = models.FloatField(null=True, blank=True)

    # sbdb blob
    sbdb_entry = JSONField()

    def get_absolute_url(self):
        return reverse('detail', args=[self.slug])

    def get_shorthand(self):
        if self.name.find('(') > -1:
            return self.name[self.name.find('(') + 1 : self.name.find(')')]
        return self.name

    def has_shorthand(self):
        return self.get_shorthand() != self.name

    def get_object_type(self):
        orbclass = self.orbit_class.name
        if orbclass.find('Comet') > -1:
            return 'comet'
        if self.fullname == '1 Ceres':
            return 'object'
        return 'asteroid'

    def get_composition(self):
        return get_composition(self)

    def get_perihelion(self):
        return self.a * (1 - self.e)

    def get_aphelion(self):
        return self.a * (1 + self.e)

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
        diameter_str = self.diameter
        if diameter_str:
            return float(diameter_str)

        # NHATS also has a diameter estimate
        nhats_set = self.nhatsobject_set.all()
        if len(nhats_set):
            nhats = nhats_set[0]
            if method == 'MID':
                return (nhats.min_diameter + nhats.max_diameter) / 2.0 / 100.
            elif method == 'HIGH':
                return nhats.max_diameter / 100.
            else:
                return nhats.min_diameter / 100.

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

    def get_firstobs_date(self):
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
          'ephem': {
            'a': self.a,
            'e': self.e,
            'i': self.i,
            'om': self.om,
            'w': self.w,
            'ma': self.ma,
            'epoch': self.epoch,
          }
        }

    def __str__(self):
        return self.fullname

    class Meta:
        indexes = [
            models.Index(fields=['sbdb_order_id']),
            models.Index(fields=['fullname']),
            models.Index(fields=['slug']),
            models.Index(fields=['orbit_class']),
            models.Index(fields=['object_type']),
            models.Index(fields=['is_nea']),
            models.Index(fields=['is_pha']),
        ]

class CloseApproach(models.Model):
    space_object = models.ForeignKey(SpaceObject)

    date = models.DateField()
    v_rel = models.FloatField()
    h_mag = models.FloatField()

    # Distances in AU
    dist_au = models.FloatField()
    dist_min_au = models.FloatField()

    def get_dist_km(self):
        return self.dist_au * 1.496e8

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

class NhatsObject(models.Model):
    space_object = models.ForeignKey(SpaceObject)

    num_trajectories = models.IntegerField()

    min_dv = models.FloatField()
    min_dv_duration = models.FloatField()

    # Diameter in meters
    min_diameter = models.FloatField()
    max_diameter = models.FloatField()

    def __str__(self):
        return self.space_object.fullname

class ShapeModel(models.Model):
    space_object = models.ForeignKey(SpaceObject)

    # Path to shapefile
    shape_path = models.CharField(max_length=200)

    # Path to image
    render_path = models.CharField(max_length=200)

    # Ecliptic lat/lng of the spin axis direction (beta and lambda
    # respectively).
    spin_latitude = models.FloatField()
    spin_longitude = models.FloatField()
    # Initial rotation angle (phi)
    spin_angle = models.FloatField()

    # Period in hours
    period_hr = models.FloatField()

    # Initial julian date
    jd = models.FloatField()

    # Linear change in the rotation rate (dω / dt) caused by the
    # Yarkovsky-O'Keefe-Radzievskii-Paddack effect (rad / day2)
    yorp = models.FloatField(null=True, blank=True)

    # References string
    # reference = models.CharField(max_length=1000)

    # Equivalent diameter - diameter of sphere that has the same volume as
    # model.
    equiv_diameter_km = models.FloatField(null=True, blank=True)

    # Quality level
    quality = models.FloatField()

admin.site.register(SpaceObject)
admin.site.register(CloseApproach)
admin.site.register(SentryEvent)
admin.site.register(NhatsObject)
admin.site.register(OrbitClass)
admin.site.register(ShapeModel)
