from django.conf.urls import url

from . import views

app_name = 'houses'
urlpatterns = [
    # /houses
    url(r'^$', views.index, name='index'),
    # /houses/realstate/1
    url(r'^realstate/(?P<pk>[0-9]+)/$', views.DetailAgencyView.as_view(), name='detail_agency'),
    # /houses/1
    url(r'^(?P<pk>[0-9]+)/$', views.DetailHouseView.as_view(), name='detail_house'),
    # /houses/
    url(r'^$', views.index, name='index'),
]
