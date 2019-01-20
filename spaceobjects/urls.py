from django.conf.urls import url

from .import views

urlpatterns = [
  url('^asteroid/random$', views.random, name='random'),
  url('^asteroid/(?P<slug>[^/]+)$', views.detail, name='detail'),
  url('^category/(?P<category>[^/]+)$', views.category, name='category'),
  url('^solar-system$', views.solar_system, name='solar_system'),
  url('^api/asteroids$', views.search, name='search'),
  url('^$', views.index, name='index'),
]
