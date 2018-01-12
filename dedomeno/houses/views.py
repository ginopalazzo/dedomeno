from django.shortcuts import get_object_or_404, render
# from django.http import HttpResponseRedirect
# from django.urls import reverse

from django.views import generic
from django.contrib import admin

from houses.models import House, RealEstate, Garage, Office, Room, Commercial, Land, StoreRoom, Building

from .management.localizations import *
from .management.sources import *
from .management.agencies import *
from .management.houses import *

from django.conf.urls import *
from django.http import HttpResponse


def my_view(request):
    return HttpResponse("Hello!")


def get_admin_urls(urls):
    def get_urls():
        my_urls = [
            url(r'^houses/management/$', admin.site.admin_view(management)),
        ]

        return my_urls + urls
    return get_urls


admin_urls = get_admin_urls(admin.site.get_urls())
admin.site.get_urls = admin_urls


def index(request):
    # template_name = 'houses/index.html'
    real_estate_list = RealEstate.objects.order_by('name')[:10]
    real_estates_total = RealEstate.objects.count()
    houses_total = House.objects.all().count()
    garages_total = Garage.objects.count()
    offices_total = Office.objects.count()
    rooms_total = Room.objects.count()
    commercials_total = Commercial.objects.count()
    lands_total = Land.objects.count()
    storeroom_total = StoreRoom.objects.count()
    buildings_total = Buildings.objects.count()

    context = {
        'real_estate_list': real_estate_list,
        'real_estates_total': real_estates_total,
        'houses_total': houses_total,
        'garages_total': garages_total,
        'offices_total': offices_total,
        'rooms_total': rooms_total,
        'commercials_total': commercials_total,
        'lands_total': lands_total,
        'storeroom_total': storeroom_total,
        'buildings_total': buildings_total,
    }
    return render(request, 'houses/index.html', context)


class DetailRealEstateView(generic.DetailView):
    model = RealEstate
    template_name = 'houses/detail_real_estate.html'


class DetailHouseView(generic.DetailView):
    model = House
    template_name = 'houses/detail_house.html'


def management(request):
    real_estates_total = RealEstate.objects.count()
    houses_total = House.objects.count()
    garages_total = Garage.objects.count()
    offices_total = Office.objects.count()
    rooms_total = Room.objects.count()
    commercials_total = Commercial.objects.count()
    lands_total = Land.objects.count()

    context = {
        'real_estates_total': real_estates_total,
        'houses_total': houses_total,
        'garages_total': garages_total,
        'offices_total': offices_total,
        'rooms_total': rooms_total,
        'commercials_total': commercials_total,
        'lands_total': lands_total
    }
    # HOUSES
    if(request.GET.get('btn-import-houses-all')):
        startPropertySpider()#'sale', 'garage', 'almeria')
        #importAllhouses(request.GET.get('house-option-source'), request.GET.get('house-option-country'))
    #   Import children territorial entities for provinces (Map resuorce)
    elif(request.GET.get('btn-import-houses-provinces')):
        source = Source.objects.get(source_name=request.GET.get('house-option-source'))
        for province in request.GET.getlist('house-option-provinces'):
            territorial_entity = TerritorialEntity.objects.get(territorial_entity_name=province, depth_number=0)
            url_source_territory = URLSourceTerritory.objects.get(source=source, territory=territorial_entity)
            collectEntities(territorial_entity.country, source, territorial_entity, url_source_territory, territorial_entity.depth_number)
    # AGENCIES
    elif(request.GET.get('btn-import-all-agency')):
        importAllAgencies(request.GET.get('agency-option-source'), request.GET.get('agency-option-country'))
    elif(request.GET.get('btn-complete-all-agencies')):
        completeAllAgencies(request.GET.get('agency-option-source'))
    return render(request, 'houses/management.html', context)
    
