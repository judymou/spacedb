from django.contrib.sitemaps.views import sitemap
from django.conf.urls import url

import spaceobjects.views as views
from spaceobjects.sitemap import SpaceObjectSitemap

sitemaps = {
    'spaceobjects': SpaceObjectSitemap,
}

urlpatterns = [
    url('^asteroid/random$', views.random, name='random'),
    url('^asteroid/(?P<slug>[^/]+)$', views.detail, name='detail'),
    url('^asteroid/(?P<slug>[^/]+)/shape$', views.detail_shape, name='detail_shape'),
    url('^category/(?P<category>[^/]+)$', views.category, name='category'),
    url('^solar-system$', views.solar_system, name='solar_system'),
    url('^api/asteroids$', views.search, name='search'),
    url('^api/get-objects$', views.get_objects, name='get_objects'),
    url('^$', views.index, name='index'),

    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
            name='django.contrib.sitemaps.views.sitemap')
]
