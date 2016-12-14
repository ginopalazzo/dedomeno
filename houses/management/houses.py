# -*- coding: utf-8 -*-

from lxml import html
import requests
from houses.models import *
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def importAllhouses(source_name, country_name):
    """
    Will import all the houses for the last depth Territorial Entity
    """
    # https://www.idealista.com/venta-viviendas/castelldefels/el-poal/con-pisos/pagina-2.htm?ordenado-por=fecha-publicacion-desc
    # source + transaction.depth=0 + - + transaction.depth=1 + / + url_source_territory + / con- + transaction.depth=2 + /pagina- + page_num +.htm + ?ordenado-por=fecha-publicacion-desc
    logger.info("START Import all Houses in " + country_name + ' for ' + source_name + '. This will take a while...')
    country = Country.objects.get(country_name=country_name)
    source = Source.objects.get(source_name=source_name)
    # only implemented for Idealista & Spain
    if source.slug == 'id' and country_name == 'Spain':
        sale_transaction = Transaction.objects.get(transaction_name='sale', depth_number=0)
        house_transaction = Transaction.objects.get(transaction_name='house', father=sale_transaction)
        territorial_leaves_list = TerritorialEntity.objects.filter(depth_last=True, country=country)
        transaction_leaves_list = Transaction.objects.filter(depth_number=2)
        for territorial_leaf in territorial_leaves_list:
            for transaction_leaf in transaction_leaves_list:
                house_type_name = SourceTransaction.objects.get(source=source, transaction=transaction_leaf)
                property_name = SourceTransaction.objects.get(source=source, transaction=transaction_leaf)
                transaction_name = SourceTransaction.objects.get(source=source, transaction=transaction_leaf)
class SourceTransaction(models.Model):
    source_transaction_name = models.CharField(max_length=100, null=True, blank=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)


            url = source.url + SourceTransaction.objects.get(source=source, transaction=sale_transaction).source_transaction_name + source.separator_url + SourceTransaction.objects.get(source=source, transaction=house_transaction).source_transaction_name + '/' + URLSourceTerritory.objects.get(source=source, territory=territorial_leaf).url_source_territory_name_list + "/agencias-inmobiliarias-"
            collectHouses(source, url, territorial_leaf, 1)
        logger.info("END Import all Agencies in " + country_name + ' for ' + source_name + '.')
    else:
        logger.warning('Only Idealista - Spain is implemented')


def collectHouses(source, url_base, territorial_leaf, page_number):
    """
    For every page in the territorial_leafe agency page collect and compose the Agencies
    """
    url = url_base + str(page_number)
    try:
        # collect and compose a tree for a url page
        page = requests.get(url)
        tree = html.fromstring(page.content)
        agency_name = tree.xpath('//dl[@class="item"]//span[@class="comm-name"]/text()')
        agency_source_url = tree.xpath('//dl[@class="item"]/dd/a/@href')
        # if all list all same length
        if len(agency_name) == len(agency_source_url):
            list_agencies = zip(agency_name, agency_source_url)
            for agency_item in list_agencies:
                agency = Agency.objects.get_or_create(agency_name=agency_item[0])
                agency_localization = AgencyLocalization.objects.get_or_create(agency=agency[0], place=territorial_leaf)
                agency_localization_source = AgencyLocalizationSource.objects.get_or_create(source=source, agency_localization=agency_localization[0], agency_source_name=agency_item[1].split('/')[2], agency_source_url=agency_item[1])
            if len(agency_name) != 0:
                collectAgencies(source, url_base, territorial_leaf, page_number + 1)
        else:
            logger.error('Some agencies doesn´t have name or source_url in : ' + url + ".")
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        logger.error('requests.exceptions.Timeout : ' + url)
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        logger.error('requests.exceptions.TooManyRedirects: ' + url)
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        logger.error('requests.exceptions.RequestException: ' + url + ', ' + e)
        sys.exit(1)








# data of url
domain = 'https://www.idealista.com'
typology = 'alquiler-viviendas'
province = 'madrid-madrid'
area = 'zona-noroeste'
pagination = 'pagina-'
extension = ".htm"
query = "?ordenado-por=fecha-publicacion-desc"


#
# compose methods for house data
#
def compose_phone(phones):
    list_phone = []
    for phone in phones:
        list_phone.append(phone[4:])
    return list_phone


def compose_code(codes):
    list_code = []
    for code in codes:
        list_code.append(code[10:-1])
    return list_code


def compose_link(codes):
    list_links = []
    for code in codes:
        list_links.append(domain + "/inmueble/" + code)
    return list_code


def compose_house(house):
    pass


def compose_building(buiding):
    pass


def compose_address(address):
    pass


def compose_deposit(deposit):
    pass


#
def get_houses_page(page_number):
    # read html page
    url = domain + '/' + typology + '/' + province + '/' + pagination + str(page_number) + extension + query
    page = requests.get(url)
    tree = html.fromstring(page.content)
    # get
    code = compose_code(tree.xpath('//a[@class="item-link "]/@href'))
    link = compose_link(code)
    title = tree.xpath('//a[@class="item-link "]/text()')
    price = tree.xpath('//span[@class="item-price"]/text()')
    phone = compose_phone(tree.xpath('//a[@class="icon-phone phone-btn item-clickable-phone"]/@href'))
    # return houses


#
def get_houses():
    page = 1
    page_total = 1
    # while there is pages left
    while page <= page_total:
        # get-total-page-number
        get_houses_page(page)


# get other data from the house
def complete_house(code):
    # read html page
    url = domain+"/inmueble/"+code
    page = requests.get(url)
    tree = html.fromstring(page.content)
    # get
    desc = tree.xpath('//div[@class="adCommentsLanguage expandable"]/text()')[0]
    new_price_aux = tree.xpath('//p[@class="price"]/text()')[0]
    new_price = new_price_aux[:new_price_aux.index(" ")]
    deposit = tree.xpath('//span[@class="txt-deposit"]/span[1]/text()')[0]
    c_house = tree.xpath('//section[@id="details"]/div[3]/ul/li/text()')
    c_building = tree.xpath('//section[@id="details"]/div[4]/ul/li/text()')
    c_street = tree.xpath('//div[@id="addressPromo"]/ul/li/text()')
    c_owner_real_state = tree.xpath('//a[@class="about-advertiser-name"]/text()') #len=0 ->particular, len=1 ->real_state_name
    print deposit

def check_new_hosese() :
    pass


#complete_house('35143462')
#complete_house('31673112')
get_houses_page(1)
