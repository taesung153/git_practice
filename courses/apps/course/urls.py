from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^courses$', views.Courses, name = 'Courses'),
    url(r'^confirm/(?P<id>\d+)$', views.confirm, name='confirm'),
    url(r'^courses/remove/(?P<id>\d+)$', views.remove, name='remove'),
    url(r'^back$', views.index, name = 'index'),

]
