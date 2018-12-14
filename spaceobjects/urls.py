from django.conf.urls import url

from .import views

urlpatterns = [
  url('^asteroid/(?P<slug>[^/]+)$', views.detail, name='detail'),
  url('', views.index, name='index'),
]
