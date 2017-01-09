from django.shortcuts import get_object_or_404, render
# from django.http import HttpResponseRedirect
# from django.urls import reverse

from django.views import generic
from django.contrib import admin

from .models import House, RealEstate

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
    real_estate_total = RealEstate.objects.count()
    houses_rent_total = House.objects.filter(transaction='rent').count()
    houses_sale_total = House.objects.filter(transaction='sale').count()

    context = {
        'real_estate_total': real_estate_total,
        'real_estate_list': real_estate_list,
        'houses_rent_total': houses_rent_total,
        'houses_sale_total': houses_sale_total,
    }
    return render(request, 'houses/index.html', context)


class DetailRealEstateView(generic.DetailView):
    model = RealEstate
    template_name = 'houses/detail_real_state.html'


class DetailHouseView(generic.DetailView):
    model = House
    template_name = 'houses/detail_house.html'


def management(request):
    real_estate_count = RealEstate.objects.count()
    houses_rent_total = House.objects.count()
    houses_buy_total = House.objects.count()
    context = {
        'real_estate_count': real_state_count,
        'houses_rent_total': houses_rent_total_active,
        'houses_buy_total': houses_buy_total_active,
    }
    # HOUSES
    """
    if(request.GET.get('btn-import-houses-all')):
        importAllhouses(request.GET.get('house-option-source'), request.GET.get('house-option-country'))
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
    """
