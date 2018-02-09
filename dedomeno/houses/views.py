from django.shortcuts import get_object_or_404, render
# from django.http import HttpResponseRedirect
# from django.urls import reverse

from django.views.generic.detail import DetailView
from django.db.models import Q
from django.db.models import Count
from django.db.models import Avg


from houses.models import Property, House, RealEstate, Garage, Office, Room, Commercial, Land, StoreRoom, Building
from idealista import settings

from django.conf.urls import *
from django.http import HttpResponse


def my_view(request):
    return HttpResponse("Hello!")


# TODO: https://docs.djangoproject.com/en/2.0/topics/db/queries/#caching-and-querysets
# TODO: https://github.com/wq/django-rest-pandas
def index(request):
    # template_name = 'houses/index.html'

    property_list = Property.objects.all().values('property_type').annotate(
                      rent=Count('address_province', filter=Q(transaction='rent')),
                      sale=Count('address_province', filter=Q(transaction='sale')),
                      total=Count('address_province')).order_by('-total')

    real_estate_list = Property.objects.all().values('real_estate', 'real_estate_raw').annotate(
                           total=Count('real_estate')).order_by('-total')[:len(property_list)]
    province_list = Property.objects.all().values('address_province', 'transaction').annotate(
                    rent=Count('address_province', filter=Q(transaction='rent')),
                    sale=Count('address_province', filter=Q(transaction='sale')),
                    total=Count('address_province')).order_by('-total')[:len(property_list)]

    context = {
        'property_list': property_list,
        'province_list': province_list,
        'real_estate_list': real_estate_list,
    }
    return render(request, 'houses/index.html', context)


def real_estate(request):
    context = {}
    return render(request, 'houses/real_estate/index.html', context)


def province(request):
    province_ine = settings.IDEALISTA_URL_SCHEME['provinces_ine']
    for key, value in province_ine.items():
        name_dedomeno = province_ine[key]['name_dedomeno']
        query = Property.objects.filter(address_province=name_dedomeno).values('address_province', 'transaction', 'property_type').annotate(
                rent=Avg('price_raw', filter=Q(transaction='rent')),
                sale=Avg('price_raw', filter=Q(transaction='sale')))

        province_ine[key]['property_type'] = {i[0]: {'sale':0,'rent':0} for i in Property._meta.get_field('property_type').choices}
        for item in query:
            province_ine[key]['property_type'][item['property_type']][item['transaction']] = item[item['transaction']]

    context = {
        'provinces_ine': province_ine
    }
    return render(request, 'houses/province/index.html', context)


class DetailRealEstateView(DetailView):
    model = RealEstate
    context_object_name = 'real_estate'
    template_name = 'houses/real_estate/detail_real_estate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = Property.objects.filter(real_estate=context['object'])
        context['total'] = q.count()
        context['property_type_list'] = [i[0] for i in Property._meta.get_field('property_type').choices]
        context['transaction_list'] = [i[0] for i in Property._meta.get_field('transaction').choices]
        context['donut_chart'] = []
        for transaction in context['transaction_list']:
            array = []
            total = 0
            for property_type in context['property_type_list']:
                val = q.filter(property_type=property_type, transaction=transaction).count()
                array.append({
                    'cat': property_type,
                    'val': val,
                 })
                total += val
            context['donut_chart'].append({
                'type': transaction,
                'unit': ' property',
                'data': array,
                'total': total,
            })
        """
        for transaction in context['transaction_list']:
            dic = {}
            for property_type in context['property_type_list']:
                dic[property_type] = q.filter(property_type=property_type, transaction=transaction).count()
            context[transaction] = dic
        """
        return context


class DetailHouseView(DetailView):
    model = House
    template_name = 'houses/detail_house.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context