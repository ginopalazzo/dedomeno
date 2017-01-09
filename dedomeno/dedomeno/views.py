from django.shortcuts import render

from houses.models import House, RealEstate


def index(request):
    # template_name = 'houses/index.html'

    real_estate_list = RealEstate.objects.order_by('name')
    real_estate_total = RealEstate.objects.count()
    houses_rent_total = House.objects.filter(transaction='rent').count()
    houses_sale_total = House.objects.filter(transaction='sale').count()
    context = {
        'real_estate_total': real_estate_total,
        'real_estate_list': real_estate_list,
        'houses_rent_total': houses_rent_total,
        'houses_sale_total': houses_sale_total,
    }
    return render(request, 'dedomeno/index.html', context)
