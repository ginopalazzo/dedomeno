from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from houses.models import House, Agency, Transaction


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

    context = {
        'agencies_total': agencies_total,
        'agencies_list': agencies_list,
        'houses_rent_total': houses_rent_total,
        'houses_buy_total': houses_buy_total,
        'houses_rent_total_active': houses_rent_total_active,
        'houses_buy_total_active': houses_buy_total_active,
    }
    return render(request, 'dedomeno/index.html', context)
