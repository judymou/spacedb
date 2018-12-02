from django.conf.urls import url

from .import views

urlpatterns = [
  url('(?P<name>[^/]+)$', views.detail, name='detail'),
  url('', views.index, name='index'),
]
