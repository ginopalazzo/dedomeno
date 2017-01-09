"""
import scrapy
import logging
from houses.models import Country, Source, Transaction, SourceTransaction, TerritorialEntity, URLSourceTerritory

logger = logging.getLogger(__name__)
country = Country.objects.get(country_name='Spain')
source = Source.objects.get(source_name='Idealista')


class AgencySpider(scrapy.Spider):
    # name of the spider
    name = "agency"
    # start of the urls: it gets the url from the django db
    territory_leaf_list = TerritorialEntity.objects.filter(depth_last=True)
    sale_transaction = Transaction.objects.get(transaction_name='sale', depth_number=0)
    house_transaction = Transaction.objects.get(transaction_name='house', father=sale_transaction)
    territorial_leaves_list = TerritorialEntity.objects.filter(depth_last=True, country=country)
    start_urls = []
    for territorial_leaf in territorial_leaves_list:
        start_urls.append(source.url + "pro/" + SourceTransaction.objects.get(source=source, transaction=sale_transaction).source_transaction_name + source.separator_url + SourceTransaction.objects.get(source=source, transaction=house_transaction).source_transaction_name + '/' + URLSourceTerritory.objects.get(source=source, territory=territorial_leaf).url_source_territory_name_list + "/agencias-inmobiliarias-")

    def parse(self, response):
"""