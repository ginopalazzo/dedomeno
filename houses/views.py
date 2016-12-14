from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib import admin

from .models import House, Agency, Country, Source, Transaction, TerritorialEntity

from .management.localizations import *
from .management.sources import *
from .management.agencies import *

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

    agencies_list = Agency.objects.order_by('agency_name')
    agencies_total = Agency.objects.count()
    houses_rent_total = House.objects.filter(transaction_type=Transaction.objects.get(transaction_name='rent')).count()
    houses_buy_total = House.objects.filter(transaction_type=Transaction.objects.get(transaction_name='sale')).count()
    houses_rent_total_active = House.objects.filter(
        transaction_type=Transaction.objects.get(transaction_name='rent'), is_online=True).count()
    houses_buy_total_active = House.objects.filter(
        transaction_type=Transaction.objects.get(transaction_name='sale'), is_online=True).count()
    territorial_entities_total = TerritorialEntity.objects.filter().count()
    countries_list = Country.objects.order_by('pk')
    countries_total = Country.objects.filter().count()

    # houses_idealista_total
    # houses_idealista_total_active
    # houses_fotocasa_total

    context = {
        'agencies_total': agencies_total,
        'agencies_list': agencies_list,
        'houses_rent_total': houses_rent_total,
        'houses_buy_total': houses_buy_total,
        'houses_rent_total_active': houses_rent_total_active,
        'houses_buy_total_active': houses_buy_total_active,
        'territorial_entities_total': territorial_entities_total,
        'countries_total': countries_total,
        'countries_list': countries_list,
    }
    return render(request, 'houses/index.html', context)


class DetailAgencyView(generic.DetailView):
    model = Agency
    template_name = 'houses/detail_agency.html'


class DetailHouseView(generic.DetailView):
    model = House
    template_name = 'houses/detail_house.html'


def management(request):
    country_list = Country.objects.order_by('pk')
    country_count = country_list.count()
    source_list = Source.objects.order_by('pk')
    source_count = source_list.count()
    province_list = TerritorialEntity.objects.filter(depth_number=0).order_by('pk')
    territorial_count = TerritorialEntity.objects.count()
    agency_count = Agency.objects.count()
    context = {
        'country_list': country_list,
        'source_list': source_list,
        'province_list': province_list,
        'source_count': source_count,
        'country_count': country_count,
        'territorial_count': territorial_count,
        'agency_count': agency_count,
    }
    # SORUCE
    if(request.GET.get('btn-import-source')):
        importAllSources(request.GET.get('source-option-source'))
    # TERRITORIAL ENTITIES
    #   Import all territorial entities (Map resuorce)
    elif(request.GET.get('btn-import-territorial-entities')):
        importAllTerritorialEntities(request.GET.get('localization-option-source'), request.GET.get('localization-option-country'))
    #   Import children territorial entities for provinces (Map resuorce)
    elif(request.GET.get('btn-import-provinces')):
        source = Source.objects.get(source_name=request.GET.get('localization-option-source'))
        for province in request.GET.getlist('localization-option-provinces'):
            territorial_entity = TerritorialEntity.objects.get(territorial_entity_name=province, depth_number=0)
            url_source_territory = URLSourceTerritory.objects.get(source=source, territory=territorial_entity)
            collectEntities(territorial_entity.country, source, territorial_entity, url_source_territory, territorial_entity.depth_number)
    elif(request.GET.get('btn-import-municipios')):
        source = Source.objects.get(source_name=request.GET.get('localization-option-source'))
        for province in request.GET.getlist('localization-option-provinces'):
            territorial_entity = TerritorialEntity.objects.get(territorial_entity_name=province, depth_number=0)
            url_source_territory = URLSourceTerritory.objects.get(source=source, territory=territorial_entity)
            CollectMunicipios(territorial_entity.country, source, territorial_entity, url_source_territory)
    # HOUSES
    # AGENCIES
    elif(request.GET.get('btn-import-all-agency')):
        importAllAgencies(request.GET.get('agency-option-source'), request.GET.get('agency-option-country'))
    elif(request.GET.get('btn-complete-all-agencies')):
        completeAllAgencies(request.GET.get('agency-option-source'))
    return render(request, 'houses/management.html', context)
