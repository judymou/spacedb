# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math
from datetime import datetime
from enum import Enum

from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from jsonfield import JSONField

from spaceobjects.description import get_diameter_comparison, composition, COMET_CLASSES

class ObjectType(Enum):
    ASTEROID = 'ASTEROID'
    COMET = 'COMET'

    @classmethod
    def from_class(self, classname):
        if classname in COMET_CLASSES:
            return self.COMET
        return self.ASTEROID

    def __str__(self):
        return self.value

class OrbitClass(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)
    abbrev = models.CharField(max_length=10)

    desc = models.CharField(max_length=500)
    orbit_sentence = models.CharField(max_length=500)

    def get_absolute_url(self):
        return reverse('category', args=[self.slug])

    def __str__(self):
        return self.abbrev

    class Meta:
        ordering = ['id']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['abbrev']),
        ]

class SpaceObject(models.Model):
    fullname = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)

    orbit_class = models.ForeignKey(OrbitClass, blank=True, null=True)
    object_type = models.CharField(max_length = 20,
            choices=[(tag.name, tag.value) for tag in ObjectType])

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
    spec_B = models.CharField(max_length=200, null=True, blank=True)
    spec_T = models.CharField(max_length=200, null=True, blank=True)
    H = models.FloatField(null=True, blank=True)

    # For now this is only SBDB diameter. See get_diameter_estimate below.
    diameter = models.FloatField(null=True, blank=True)

    # Automatically filled via get_diameter_estimate
    diameter_estimate = models.FloatField(null=True, blank=True)

    # sbdb blob
    sbdb_entry = JSONField()

    def get_absolute_url(self):
        if self.object_type == ObjectType.COMET.value:
            return reverse('detail_comet', args=[self.slug])
        return reverse('detail_asteroid', args=[self.slug])

    @cached_property
    def shorthand(self):
        if self.name.find('(') > -1:
            return self.name[self.name.find('(') + 1 : self.name.find(')')]
        return self.name

    @cached_property
    def has_shorthand(self):
        return self.shorthand() != self.name

    @cached_property
    def get_object_type(self):
        if self.fullname == '1 Ceres':
            return 'object'

        if self.is_comet:
            return 'comet'
        if self.is_asteroid:
            return 'asteroid'

        # This should never happen...
        return 'object'

    @cached_property
    def composition(self):
        return composition(self)

    @cached_property
    def perihelion(self):
        return self.a * (1 - self.e)

    @cached_property
    def aphelion(self):
        return self.a * (1 + self.e)

    @cached_property
    def moid(self):
        entry = self.sbdb_entry.get('moid')
        if not entry:
            return None
        return float(entry)

    @cached_property
    def firstobs_date(self):
        firstobs = self.sbdb_entry.get('first_obs')
        return datetime.strptime(firstobs, '%Y-%m-%d')

    @cached_property
    def lastobs_date(self):
        lastobs = self.sbdb_entry.get('last_obs')
        return datetime.strptime(lastobs, '%Y-%m-%d')

    @cached_property
    def size_adjective(self):
        diameter = self.get_diameter_estimate()
        if not diameter:
            return None

        if diameter < 0.5:
            return 'very small'
        if diameter < 1:
            return 'small'
        if diameter < 10:
            return 'mid-sized'
        if diameter < 100:
            return 'large'
        if diameter < 200:
            return 'large'
        if diameter < 300:
            return 'very large'
        if self.object_type == ObjectType.ASTEROID.value:
            return 'dwarf planet'
        return 'large'

    @cached_property
    def avg_orbital_speed(self):
        # in km/s
        if self.period_in_days > 0:
            return (2 * math.pi * self.a * 149597870.7) / (self.period_in_days * 86400)
        return None

    @cached_property
    def is_dwarf_planet(self):
        return self.size_adjective == 'dwarf planet'

    @cached_property
    def is_asteroid(self):
        return self.object_type == ObjectType.ASTEROID.value

    @cached_property
    def is_comet(self):
        return self.object_type == ObjectType.COMET.value

    @cached_property
    def has_size_info(self):
        diam = self.sbdb_entry.get('diameter')
        return diam != '' and diam is not None

    @cached_property
    def has_size_info_estimate(self):
        return self.get_diameter_estimate() is not None

    @cached_property
    def get_size_rough_comparison(self):
        diameter = self.get_diameter_estimate()
        if not diameter:
            return None
        if diameter > 900:
            return 'the largest asteroid/dwarf planet'
        if diameter > 300:
            return 'one of the largest objects'
        if diameter > 1:
            return 'larger than 99% of asteroids'
        if diameter > 0.5:
            return 'larger than ~97% of asteroids but small compared to large asteroids'
        if diameter > 0.3:
            return 'larger than 90% of asteroids but tiny compared to large asteroids'
        return 'a small to average asteroid'

    @cached_property
    def get_diameter_comparison(self):
        return get_diameter_comparison(self)

    @cached_property
    def get_similar_orbits(self, n=3):
        a_range = [self.a - 0.01, self.a + 0.01]
        similar = SpaceObject.objects.filter(a__range=a_range).exclude(pk=self.pk)
        return similar[:n]

    @cached_property
    def period_in_days(self):
        try:
            return float(self.sbdb_entry['per'])
        except:
            return None

    @cached_property
    def period_in_years(self):
        try:
            return float(self.sbdb_entry['per']) / 365.25
        except:
            return None

    @cached_property
    def ordered_close_approaches(self):
        return self.closeapproach_set.all().order_by('date')

    @cached_property
    def ordered_sentry_events(self):
        return self.sentryevent_set.all().order_by('-prob')

    @cached_property
    def ordered_shape_models(self):
        return self.shapemodel_set.all().order_by('-quality')


    def get_diameter_estimate_low(self):
        return self.get_diameter_estimate(method='LOW')

    def get_diameter_estimate_high(self):
        return self.get_diameter_estimate(method='HIGH')

    def get_diameter_estimate(self, method='MID'):
        '''Diameter estimate in km, using either SBDB-supplied estimate
        or estimate based on magnitude/albedo'''
        diameter = self.diameter
        if diameter:
            return diameter

        # NHATS also has a diameter estimate
        nhats_set = self.nhatsobject_set.all()
        if len(nhats_set):
            nhats = nhats_set[0]
            if method == 'MID':
                return (nhats.min_diameter + nhats.max_diameter) / 2.0 / 1000.
            elif method == 'HIGH':
                return nhats.max_diameter / 1000.
            else:
                # method == LOW
                return nhats.min_diameter / 1000.

        try:
            if 'H' in self.sbdb_entry:
                mag = float(self.sbdb_entry['H'])
                if method == 'MID':
                    albedo_default = 0.15
                elif method == 'HIGH':
                    albedo_default = 0.05
                else:
                    # method == LOW
                    albedo_default = 0.25
            elif 'M2' in self.sbdb_entry:
                # Comet nuclear magnitude
                mag = float(self.sbdb_entry['M2'])
                # Typical albedo for a comet
                # https://en.wikipedia.org/wiki/Comet_nucleus#Albedo
                albedo_default = 0.04

            albedo_known = self.sbdb_entry.get('albedo')
            albedo = float(albedo_known) if albedo_known else albedo_default

            # Estimate diameter in km
            # http://www.physics.sfasu.edu/astro/asteroids/sizemagnitude.html
            return 1329 / math.sqrt(albedo) * math.pow(10, -0.2 * mag)
        except ValueError:
            pass
        except KeyError:
            pass
        except TypeError:
            pass
        return None

    @cached_property
    def get_1wtc_pct(self):
        # Helper function used to get size ratio compared to 1 WTC in New York City.
        diam_km = self.get_diameter_estimate()
        return diam_km / 0.5413 * 100.0

    @cached_property
    def get_everest_pct(self):
        # Helper function used to get size ratio compared to Mt Everest prominence of photo.
        # Photo shows elevation from ~16417 ft to ~29032 ft = 3.845052 km * adjustment.
        diam_km = self.get_diameter_estimate()
        return diam_km / (3.845052 * 2.25) * 100.0

    def to_search_result(self):
        q = self.sbdb_entry.get('q', None)
        if q:
            q = float(q)
        tp = self.sbdb_entry.get('tp', None)
        if tp:
            tp = float(tp)
        n = self.sbdb_entry.get('n', None)
        if n:
            n = float(n)
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
                'q': q,
                'n': n,
                'tp': tp,
                'epoch': self.epoch,
            }
        }

    def to_orbit_obj(self):
        q = self.sbdb_entry.get('q', None)
        if q:
            q = float(q)
        tp = self.sbdb_entry.get('tp', None)
        if tp:
            tp = float(tp)
        return {
            'a': self.a,
            'e': self.e,
            'i': self.i,
            'om': self.om,
            'w': self.w,
            'ma': self.ma,
            'q': q,
            'tp': tp,
            'epoch': self.epoch,
        }

    def save(self):
        self.diameter_estimate = self.get_diameter_estimate()
        super(SpaceObject, self).save()

    def __str__(self):
        return self.fullname

    class Meta:
        ordering = ['id']
        indexes = [
            models.Index(fields=['fullname']),
            models.Index(fields=['slug']),
            models.Index(fields=['orbit_class']),
            models.Index(fields=['object_type']),
            models.Index(fields=['is_nea']),
            models.Index(fields=['is_pha']),
            models.Index(fields=['diameter']),
            models.Index(fields=['a']),
        ]

class CloseApproach(models.Model):
    space_object = models.ForeignKey(SpaceObject)

    date = models.DateField()
    v_rel = models.FloatField()
    h_mag = models.FloatField()

    # Distances in AU
    dist_au = models.FloatField()
    dist_min_au = models.FloatField()

    @cached_property
    def dist_km(self):
        return self.dist_au * 1.496e8

    class Meta:
        ordering = ['id']
        indexes = [
            models.Index(fields=['date']),
        ]

class SentryEvent(models.Model):
    space_object = models.ForeignKey(SpaceObject)

    date = models.DateField()
    energy_mt = models.FloatField()
    dist_km = models.FloatField()
    dist_err  = models.FloatField()  # 1-sigma semi-width of the uncertainty region
    palermo_scale = models.FloatField()
    torino_scale = models.FloatField()
    prob = models.FloatField()

    @cached_property
    def prob_percentage(self):
        return self.prob * 100.0

    @cached_property
    def energy_with_units(self):
        if self.energy_mt > 1:
            return '%s megatons' % (self.energy_mt)
        return '%s kilotons' % (self.energy_mt * 1000)

    class Meta:
        ordering = ['id']
        indexes = [
            models.Index(fields=['prob']),
        ]

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

    class Meta:
        ordering = ['id']
        indexes = [
            models.Index(fields=['min_dv']),
        ]

class ShapeModel(models.Model):
    space_object = models.ForeignKey(SpaceObject)

    source = models.CharField(max_length=512)

    # Path to shapefile
    shape_path = models.CharField(max_length=200)

    # Path to image
    render_path = models.CharField(max_length=200)

    # Ecliptic lat/lng of the spin axis direction (beta and lambda
    # respectively).
    spin_latitude = models.FloatField(null=True, blank=True)
    spin_longitude = models.FloatField(null=True, blank=True)
    # Initial rotation angle (phi)
    spin_angle = models.FloatField(null=True, blank=True)

    # Period in hours
    period_hr = models.FloatField(null=True, blank=True)

    # Initial julian date
    jd = models.FloatField(null=True, blank=True)

    # Linear change in the rotation rate (dω / dt) caused by the
    # Yarkovsky-O'Keefe-Radzievskii-Paddack effect (rad / day2)
    yorp = models.FloatField(null=True, blank=True)

    # References string
    # reference = models.CharField(max_length=1000)

    # Equivalent diameter - diameter of sphere that has the same volume as
    # model.
    equiv_diameter_km = models.FloatField(null=True, blank=True)

    # Quality level
    quality = models.FloatField(null=True, blank=True)

admin.site.register(SpaceObject)
admin.site.register(CloseApproach)
admin.site.register(SentryEvent)
admin.site.register(NhatsObject)
admin.site.register(OrbitClass)
admin.site.register(ShapeModel)
