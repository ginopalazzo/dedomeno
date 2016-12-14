from django.contrib import admin
from .models import *


class SourceAdmin(admin.ModelAdmin):
    # fields = ['name', 'slug', 'url']
    list_display = ['source_name', 'slug', 'url']


class HouseAdmin(admin.ModelAdmin):
    # fieldsets = [
    #    (None, {'fields': ['title', 'price']}),
    #    ('House Data', {'fields': ['house_type', 'm2_total', 'rooms', 'bathrooms', 'desc']}),
    #    ('Internal Data', {'fields': ['is_completed', 'is_online', 'online_date', 'offline_date']}),
    #    ('Owner Data', {'fields': ['is_owner_real_state', 'owner_phone', 'agency']}),
    # ]
    list_display = ('title', 'is_completed', 'is_online')
    list_filter = [
        'price', 'm2_total', 'rooms', 'bathrooms',
        'is_completed', 'is_online', 'online_date', 'offline_date'
    ]
    search_fields = ['title']


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
    fields = ['agency_name', 'logo', 'url']
    inlines = (AgencyLocalizationInLineAdmin,)
    list_display = ('agency_name', 'url')
    # list_filter = ['']
    search_fields = ['agency_name']


class AgencyLocalizationAdmin(admin.ModelAdmin):
    search_fields = ['agency']
    list_display = ('agency', 'place', 'telephone')


class AgencyLocalizationSourceAdmin(admin.ModelAdmin):
    search_fields = ['agency']


class TransactionAdmin(admin.ModelAdmin):
    search_fields = ['transaction_name']


class SourceTransactionAdmin(admin.ModelAdmin):
    search_fields = ['source_transaction_name']


class URLSourceTerritoryAdmin(admin.ModelAdmin):
    search_fields = ['url_source_territory_name']



# class ManagementAdmin(admin.ModelAdmin):
#    actions = [firstImportComunidadesAutonomasProvincias('Spain')]


admin.site.register(Source, SourceAdmin)
admin.site.register(House, HouseAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(TerritorialEntity, TerritorialEntityAdmin)
admin.site.register(Agency, AgencyAdmin)
admin.site.register(AgencyLocalization, AgencyLocalizationAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(SourceTransaction, SourceTransactionAdmin)
admin.site.register(URLSourceTerritory, URLSourceTerritoryAdmin)
admin.site.register(AgencyLocalizationSource, AgencyLocalizationSourceAdmin)
