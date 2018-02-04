from django.shortcuts import render

from houses.models import Property, House, RealEstate, Garage, Office, Room, Commercial, Land, StoreRoom, Building
from idealista import settings

def index(request):
    # template_name = 'houses/index.html'
    # TODO: https://docs.djangoproject.com/en/2.0/topics/db/queries/#caching-and-querysets
    real_estate_list = RealEstate.objects.order_by('name')[:10]
    real_estates_total = RealEstate.objects.count()
    houses_total_rent = House.objects.filter(transaction='rent').count()
    houses_total_sale = House.objects.filter(transaction='sale').count()
    garages_total_rent = Garage.objects.filter(transaction='rent').count()
    garages_total_sale = Garage.objects.filter(transaction='sale').count()
    offices_total_rent = Office.objects.filter(transaction='rent').count()
    offices_total_sale = Office.objects.filter(transaction='sale').count()
    rooms_total = Room.objects.count()
    commercials_total_rent = Commercial.objects.filter(transaction='rent').count()
    commercials_total_sale = Commercial.objects.filter(transaction='sale').count()
    lands_total_rent = Land.objects.filter(transaction='rent').count()
    lands_total_sale = Land.objects.filter(transaction='sale').count()
    storeroom_total_rent = StoreRoom.objects.filter(transaction='rent').count()
    storeroom_total_sale = StoreRoom.objects.filter(transaction='sale').count()
    buildings_total_rent = Building.objects.filter(transaction='rent').count()
    buildings_total_sale = Building.objects.filter(transaction='sale').count()
    idealista_dict = settings.IDEALISTA_URL_SCHEME
    transaction_list = ['sale', 'rent']
    property_sale_list = list(idealista_dict['sale_transaction'].keys())
    property_rent_list = list(idealista_dict['rent_transaction'].keys())
    province_list = sorted(list(idealista_dict['provinces'].keys()))
    '''
    province_list = [i['address_province'] for i in
                     Property.objects.all().values('address_province').annotate(
                         Count('address_province')).order_by('address_province').values('address_province')]
    '''
    context = {
        'real_estate_list': real_estate_list,
        'real_estates_total': real_estates_total,
        'houses_total_rent': houses_total_rent,
        'houses_total_sale': houses_total_sale,
        'houses_total': houses_total_sale + houses_total_rent,
        'garages_total_rent': garages_total_rent,
        'garages_total_sale': garages_total_sale,
        'garages_total': garages_total_sale + garages_total_rent,
        'offices_total_rent': offices_total_rent,
        'offices_total_sale': offices_total_sale,
        'offices_total': offices_total_sale + offices_total_rent,
        'rooms_total': rooms_total,
        'commercials_total_rent': commercials_total_rent,
        'commercials_total_sale': commercials_total_sale,
        'commercials_total': commercials_total_sale + commercials_total_rent,
        'lands_total_rent': lands_total_rent,
        'lands_total_sale': lands_total_sale,
        'lands_total': lands_total_sale + lands_total_rent,
        'storeroom_total_rent': storeroom_total_rent,
        'storeroom_total_sale': storeroom_total_sale,
        'storeroom_total': storeroom_total_sale + storeroom_total_rent,
        'buildings_total_rent': buildings_total_rent,
        'buildings_total_sale': buildings_total_sale,
        'buildings_total': buildings_total_sale + buildings_total_rent,
        'transaction_list': transaction_list,
        'property_sale_list': property_sale_list,
        'property_rent_list': property_rent_list,
        'province_list': province_list,
    }

    return render(request, 'dedomeno/index.html', context)
