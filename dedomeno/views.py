from django.shortcuts import render

from houses.models import House, Agency, Transaction


def index(request):
    # template_name = 'houses/index.html'

    agencies_list = Agency.objects.order_by('agency_name')
    agencies_total = Agency.objects.count()
    houses_rent_total = House.objects.filter(transaction_type=Transaction.objects.filter(transaction_name='rent').first()).count()
    houses_buy_total = House.objects.filter(transaction_type=Transaction.objects.filter(transaction_name='sale').first()).count()
    houses_rent_total_active = House.objects.filter(
        transaction_type=Transaction.objects.filter(transaction_name='rent').first(), is_online=True).count()
    houses_buy_total_active = House.objects.filter(
        transaction_type=Transaction.objects.filter(transaction_name='sale').first(), is_online=True).count()

    context = {
        'agencies_total': agencies_total,
        'agencies_list': agencies_list,
        'houses_rent_total': houses_rent_total,
        'houses_buy_total': houses_buy_total,
        'houses_rent_total_active': houses_rent_total_active,
        'houses_buy_total_active': houses_buy_total_active,
    }
    return render(request, 'dedomeno/index.html', context)
