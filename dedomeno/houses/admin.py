from django.contrib import admin
from .models import RealEstate, Date, Price, Property, House, Room, Office, Garage, Land, Commercial

'''
class SourceAdmin(admin.ModelAdmin):
    # fields = ['name', 'slug', 'url']
    list_display = ['source_name', 'slug', 'url']


class EquipmentAdmin(admin.ModelAdmin):
    search_fields = ['equipment_name']


class CountryAdmin(admin.ModelAdmin):
    search_fields = ['country_name']


class TerritorialEntityAdmin(admin.ModelAdmin):
    search_fields = ['territorial_entity_name']
    list_display = ['territorial_entity_name', 'depth_number', 'depth_name']
    list_filter = ['depth_number', 'depth_name']


class AgencyLocalizationInLineAdmin(admin.TabularInline):
    model = AgencyLocalization


class AgencyAdmin(admin.ModelAdmin):
    fields = ['agency_name', 'logo', 'url', 'is_completed']
    inlines = [
        AgencyLocalizationInLineAdmin,
    ]
    list_display = ('agency_name', 'url', 'is_completed')
    list_filter = ['is_completed']
    search_fields = ['agency_name']


class AgencyLocalizationAdmin(admin.ModelAdmin):
    search_fields = ['agency']
    list_display = ('agency', 'place', 'telephone')


class AgencyLocalizationSourceAdmin(admin.ModelAdmin):
    search_fields = ['agency_source_name']
    list_display = ('agency_source_name', 'agency_localization', 'source')


class TransactionAdmin(admin.ModelAdmin):
    search_fields = ['transaction_name']


class SourceTransactionAdmin(admin.ModelAdmin):
    search_fields = ['source_transaction_name']


class URLSourceTerritoryAdmin(admin.ModelAdmin):
    search_fields = ['url_source_territory_name']


# class ManagementAdmin(admin.ModelAdmin):
#    actions = [firstImportComunidadesAutonomasProvincias('Spain')]


admin.site.register(Source, SourceAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(TerritorialEntity, TerritorialEntityAdmin)
admin.site.register(Agency, AgencyAdmin)
admin.site.register(AgencyLocalization, AgencyLocalizationAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(SourceTransaction, SourceTransactionAdmin)
admin.site.register(URLSourceTerritory, URLSourceTerritoryAdmin)
admin.site.register(AgencyLocalizationSource, AgencyLocalizationSourceAdmin)
'''


class PriceInLineAdmin(admin.TabularInline):
    model = Price


class PriceAdmin(admin.ModelAdmin):
    list_display = ['property_price', 'value', 'date_start', 'date_end']


class DateInLineAdmin(admin.TabularInline):
    model = Date


class DateAdmin(admin.ModelAdmin):
    list_display = ['property_date', 'online', 'offline']


class PropertyInLineAdmin(admin.TabularInline):
    model = Property


class RealEstateAdmin(admin.ModelAdmin):
    search_fields = ['name', 'slug']
    list_display = ('name', 'slug', 'source', 'telephone', 'address')
    inlines = [
        PropertyInLineAdmin,
    ]


class HouseAdmin(admin.ModelAdmin):
    search_fields = ['title', 'slug']
    list_display = ('title', 'slug', 'transaction', 'house_type', 'rooms')
    list_filter = ['transaction', 'house_type']
    inlines = [
        PriceInLineAdmin, DateInLineAdmin,
    ]


class RoomAdmin(admin.ModelAdmin):
    search_fields = ['title', 'slug']
    list_display = ('title', 'slug', 'house_type', 'm2_total', 'price_raw')
    list_filter = ['house_type', 'people_max', 'smoking_allowed', 'pet_allowed', 'looking_for_male', 'looking_for_female', 'looking_for_student', 'looking_for_worker', 'gay_friendly']
    inlines = [
        PriceInLineAdmin, DateInLineAdmin,
    ]


class OfficeAdmin(admin.ModelAdmin):
    search_fields = ['title', 'slug']
    list_display = ('title', 'slug', 'distribution', 'transaction', 'm2_total', 'price_raw')
    list_filter = ['office_type', 'distribution']
    inlines = [
        PriceInLineAdmin, DateInLineAdmin,
    ]


class GarageAdmin(admin.ModelAdmin):
    search_fields = ['title', 'slug']
    list_display = ('title', 'slug', 'transaction', 'garage_type', 'automatic_door', 'price_raw', 'real_estate_raw')
    list_filter = ['transaction', 'garage_type', 'automatic_door', 'covered', 'elevator', 'security_cameras', 'alarm', 'security_guard']
    inlines = [
        PriceInLineAdmin, DateInLineAdmin,
    ]


class LandAdmin(admin.ModelAdmin):
    search_fields = ['title', 'slug']
    list_display = ('title', 'slug', 'transaction', 'm2_total', 'ground', 'price_raw')
    list_filter = ['ground', 'nearest_town', 'access', 'zoned']
    inlines = [
        PriceInLineAdmin, DateInLineAdmin,
    ]


class CommercialAdmin(admin.ModelAdmin):
    search_fields = ['title', 'slug']
    list_display = ('title', 'slug', 'transaction', 'm2_total', 'price_raw')
    # list_filter = ['ground', 'nearest_town', 'access', 'zoned']
    inlines = [
        PriceInLineAdmin, DateInLineAdmin,
    ]


admin.site.register(Date, DateAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(RealEstate, RealEstateAdmin)
admin.site.register(House, HouseAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Office, OfficeAdmin)
admin.site.register(Garage, GarageAdmin)
admin.site.register(Land, LandAdmin)
admin.site.register(Commercial, CommercialAdmin)
