from django.conf.urls import patterns, url

from tweets import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name="search"),
    url(r'^user/(?P<username>\w{0,50})/$', views.user, name="user"),
)
