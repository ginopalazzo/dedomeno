from django.conf.urls import url

from . import views

app_name = 'houses'
urlpatterns = [
    # /houses
    url(r'^$', views.index, name='index'),
    # /houses/1
    url(r'^(?P<pk>[0-9]+)/$', views.DetailHouseView.as_view(), name='detail_house'),
    # /realestate/
    url(r'^realestate$', views.real_estate, name='real_estate'),
    # /houses/realstate/1
    url(r'^realestate/(?P<pk>[0-9]+)/$', views.DetailRealEstateView.as_view(), name='detail_real_estate'),
    # /map/
    url(r'^map$', views.province, name='province'),
]
