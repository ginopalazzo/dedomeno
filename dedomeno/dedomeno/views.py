from django.shortcuts import render

from houses.models import House, RealEstate, Garage, Office, Room, Commercial, Land, StoreRoom, Building


def index(request):
    # template_name = 'houses/index.html'

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

    context = {
        'real_estate_list': real_estate_list,
        'real_estates_total': real_estates_total,
        'houses_total_rent': houses_total_rent,
        'houses_total_sale': houses_total_sale,
        'garages_total_rent': garages_total_rent,
        'garages_total_sale': garages_total_sale,
        'offices_total_rent': offices_total_rent,
        'offices_total_sale': offices_total_sale,
        'rooms_total': rooms_total,
        'commercials_total_rent': commercials_total_rent,
        'commercials_total_sale': commercials_total_sale,
        'lands_total_rent': lands_total_rent,
        'lands_total_sale': lands_total_sale,
        'storeroom_total_rent': storeroom_total_rent,
        'storeroom_total_sale': storeroom_total_sale,
        'buildings_total_rent': buildings_total_rent,
        'buildings_total_sale': buildings_total_sale,
    }

    return render(request, 'dedomeno/index.html', context)
