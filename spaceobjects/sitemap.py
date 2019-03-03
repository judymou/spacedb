from django.contrib.sitemaps import Sitemap

from spaceobjects.models import SpaceObject, OrbitClass

class SpaceObjectSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        return SpaceObject.objects.filter(is_pha=True) | SpaceObject.objects.filter(diameter__gt=100)

    def priority(self, obj):
        if obj.is_pha:
            return 0.25
        return 0.5

class OrbitClassSitemap(Sitemap):
    protocol = 'https'
    priority = 0.6

    def items(self):
        return OrbitClass.objects.all()
