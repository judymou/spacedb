from django.conf.urls import url

from .import views

urlpatterns = [
  url('^asteroid/random$', views.random, name='random'),
  url('^asteroid/(?P<slug>[^/]+)$', views.detail, name='detail'),
  url('^category/(?P<category>[^/]+)$', views.detail, name='orbit_classes'),
  url('^api/asteroids$', views.search, name='search'),
  url('^$', views.index, name='index'),
]
